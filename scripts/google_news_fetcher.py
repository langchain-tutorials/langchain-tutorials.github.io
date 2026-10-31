"""Fetch trending LangChain, LangGraph, and AI Agent topics from Google News and prevent duplicate coverage"""
import os
import sys
import re
import json
import time
import random
import glob
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Ensure scripts dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import TEXT_MODEL, GEMINI_API_KEY
from google import genai

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def get_genai_client():
    global client
    if client is None:
        if not GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY environment variable is not set")
        client = genai.Client(api_key=GEMINI_API_KEY)
    return client


class GoogleNewsFetcher:
    """Fetch and process trending news and developer tutorials about LangChain, LangGraph, and AI Agents"""

    def __init__(self, used_topics_file="_data/used_topics.json", posts_dir="_posts"):
        self.base_url = "https://news.google.com/rss/search"
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }

        # Resolve paths whether executed from repo root or scripts/ directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists(posts_dir) and os.path.exists(os.path.join(project_root, "_posts")):
            posts_dir = os.path.join(project_root, "_posts")
        if not os.path.exists(os.path.dirname(used_topics_file) or '.') and os.path.exists(os.path.join(project_root, "_data")):
            used_topics_file = os.path.join(project_root, "_data", "used_topics.json")

        self.used_topics_file = used_topics_file
        self.posts_dir = posts_dir
        self.used_topics = self._load_used_topics()
        self.existing_posts = self._index_existing_posts()

    def _index_existing_posts(self):
        """Index titles and permalinks from all existing markdown posts in _posts/"""
        indexed = {}
        if not os.path.exists(self.posts_dir):
            return indexed

        post_files = glob.glob(os.path.join(self.posts_dir, "*.md")) + glob.glob(os.path.join(self.posts_dir, "*.markdown"))
        print(f"📚 Indexing {len(post_files)} existing blog posts from {self.posts_dir}/...")

        for file_path in post_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(2048)  # Read header / front matter

                # Extract title from front matter
                title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else ""

                # Extract permalink / filename slug
                filename = os.path.basename(file_path)
                slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename).replace('.md', '').replace('.markdown', '')

                if title:
                    indexed[title.lower().strip()] = {
                        'title': title,
                        'slug': slug,
                        'file': filename
                    }
                if slug:
                    indexed[slug.lower().strip()] = {
                        'title': title or slug,
                        'slug': slug,
                        'file': filename
                    }
            except Exception:
                continue

        print(f"✅ Indexed {len(indexed)} unique titles/slugs from existing posts")
        return indexed

    def _load_used_topics(self):
        """Load previously used topics from JSON file"""
        if os.path.exists(self.used_topics_file):
            try:
                with open(self.used_topics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cutoff_date = (datetime.now() - timedelta(days=45)).isoformat()
                    data = {k: v for k, v in data.items() if v.get('date', '') > cutoff_date}
                    print(f"📋 Loaded {len(data)} previously tracked topics from {self.used_topics_file}")
                    return data
            except Exception as e:
                print(f"⚠️ Error loading used topics: {e}")
                return {}
        return {}

    def _save_used_topics(self):
        """Save used topics to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.used_topics_file) or '.', exist_ok=True)
            with open(self.used_topics_file, 'w', encoding='utf-8') as f:
                json.dump(self.used_topics, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved used topics list ({len(self.used_topics)} topics)")
        except Exception as e:
            print(f"⚠️ Error saving used topics: {e}")

    def _calculate_similarity(self, str1, str2):
        """Calculate word-level similarity ratio between two strings"""
        stopwords = {
            'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'how', 'what', 'why', 'is', 'are', 'your', 'guide', 'tutorial', 'build',
            'building', 'using', 'step', 'complete', 'intro', 'introduction'
        }
        words1 = set(re.findall(r'\w+', str1.lower())) - stopwords
        words2 = set(re.findall(r'\w+', str2.lower())) - stopwords

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _is_topic_used(self, title):
        """Check if topic has been used in existing posts or recent runs"""
        normalized = title.lower().strip()

        # Check exact matches in used_topics
        if normalized in self.used_topics:
            return True

        # Check exact matches in existing_posts
        if normalized in self.existing_posts:
            return True

        # Check similarity against used_topics (>70%)
        for used_title in self.used_topics.keys():
            if self._calculate_similarity(normalized, used_title) > 0.70:
                print(f"⚠️ Topic too similar to recent run: {used_title[:60]}...")
                return True

        # Check similarity against existing_posts (>70%)
        for existing_title in self.existing_posts.keys():
            if self._calculate_similarity(normalized, existing_title) > 0.70:
                print(f"⚠️ Topic too similar to existing post: {existing_title[:60]}...")
                return True

        return False

    def _mark_topic_used(self, title, permalink):
        """Mark topic as used"""
        normalized = title.lower().strip()
        self.used_topics[normalized] = {
            'title': title,
            'permalink': permalink,
            'date': datetime.now().isoformat()
        }
        self.existing_posts[permalink.lower().strip()] = {
            'title': title,
            'slug': permalink
        }
        self._save_used_topics()

    def fetch_trending_topics(self, max_results=25):
        """
        Fetch trending news and developer articles about LangChain and AI Agents from Google News RSS
        """
        print("📰 Fetching trending LangChain & AI agent news from Google News...")

        queries = [
            "LangChain AI tutorial",
            "LangGraph AI agents python",
            "AI agents framework python",
            "Retrieval Augmented Generation RAG tutorial",
            "multi agent systems AI python",
            "tool calling function calling AI agents",
            "vector database RAG langchain",
            "LangSmith LLM evaluation observability",
            "autonomous AI agents python code",
            "OpenAI Gemini Anthropic agent development",
            "LlamaIndex LangChain AI",
            "MCP Model Context Protocol AI agents"
        ]

        # Shuffle queries to vary topics across runs
        random.shuffle(queries)
        all_news = []

        for query in queries:
            try:
                url = f"{self.base_url}?q={requests.utils.quote(query)}&hl=en-US&gl=US&ceid=US:en"
                print(f"🔍 Searching: {query}")

                response = requests.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')

                added_for_query = 0
                for item in items:
                    try:
                        title_el = item.find('title')
                        link_el = item.find('link')
                        pub_date_el = item.find('pubDate')
                        desc_el = item.find('description')

                        title = title_el.text if title_el else None
                        link = link_el.text if link_el else None
                        pub_date = pub_date_el.text if pub_date_el else None
                        description = desc_el.text if desc_el else ""

                        if title and link:
                            # Clean up news source suffix (e.g. "... - Medium" -> "...")
                            cleaned_title = re.sub(r'\s*-\s*[^-]+$', '', title).strip()

                            if self._is_topic_used(cleaned_title):
                                continue

                            if not any(news['title'] == cleaned_title for news in all_news):
                                all_news.append({
                                    'title': cleaned_title,
                                    'raw_title': title,
                                    'description': description,
                                    'link': link,
                                    'pub_date': pub_date,
                                    'source_query': query
                                })
                                added_for_query += 1

                    except Exception:
                        continue

                print(f"   ↳ Added {added_for_query} new candidate headlines")
                time.sleep(random.uniform(0.5, 1.2))

                if len(all_news) >= max_results * 2:
                    break

            except Exception as e:
                print(f"❌ Error querying '{query}': {e}")
                continue

        print(f"✅ Total unique NEW candidate news items: {len(all_news)}")
        return all_news[:max_results]

    def filter_suitable_topics(self, news_items):
        """
        Use Gemini AI to filter and pick the 5 best actionable topics for LangChain Tutorials
        """
        if not news_items:
            return []

        print("🤖 Using Gemini AI to curate the best AI Agent & LangChain blog topics...")

        news_list = []
        for i, item in enumerate(news_items[:20]):
            news_list.append(f"{i}. {item['title']}")

        news_text = '\n'.join(news_list)

        prompt = f"""
You are the Chief Developer Advocate and Technical Editor for LangChain Tutorials (https://langchain-tutorials.github.io), a leading technical blog for software developers building AI agents, LangGraph systems, RAG applications, and LLM orchestration tools.

Here are recent trending news headlines and developer articles:
{news_text}

Task: Select the 5 BEST headlines for writing in-depth, hands-on, actionable Python tutorials and developer guides.

Selection criteria:
- High search intent and practical utility for AI developers, Python programmers, and software engineers
- Directly connects to modern frameworks (LangChain, LangGraph, AI Agents, Tool Calling, Vector DBs, RAG, LangSmith, Multi-Agent systems)
- Has enough technical depth for a 2,000+ word comprehensive code-heavy tutorial
- Actionable and educational (avoid generic corporate press releases, superficial gossip, or stock market buzz)
- Strong SEO and technical reference value

Return ONLY the numbers (0-{len(news_items)-1}) of the 5 best headlines, separated by commas.
Example: 0,3,7,12,15

Your response:
"""

        try:
            from article_generator import generate_text_with_retry_and_fallback
            response = generate_text_with_retry_and_fallback(prompt)

            selected = response.text.strip()
            indices = [int(x.strip()) for x in re.findall(r'\d+', selected)]
            indices = [i for i in indices if i < len(news_items)][:5]

            if not indices:
                indices = list(range(min(5, len(news_items))))

            filtered_news = [news_items[i] for i in indices]

            print(f"✅ Selected {len(filtered_news)} curated tutorial topics:")
            for i, news in enumerate(filtered_news, 1):
                print(f"   {i}. {news['title']}")

            return filtered_news

        except Exception as e:
            print(f"⚠️ AI filtering fallback: {e}")
            return news_items[:5]

    def generate_blog_metadata_from_news(self, news_item):
        """
        Generate complete SEO metadata for an AI tutorial blog post using Gemini
        """
        print(f"🤖 Generating blog metadata for: '{news_item['title']}'...")

        prompt = f"""
You are creating an SEO-optimized developer tutorial for LangChain Tutorials (https://langchain-tutorials.github.io).

News/Trend Headline: {news_item['title']}
Description: {news_item.get('description', 'N/A')}
Source: {news_item.get('link', 'N/A')}

Generate complete SEO metadata for a hands-on, comprehensive Python and AI developer tutorial inspired by this trend.

Requirements:
1. Title: Engaging, clear, click-worthy developer tutorial title (55-70 characters, clear technical outcome)
2. Focus Keyword: Primary SEO keyword (2-4 words, e.g. "LangGraph Multi-Agent Workflows", "LangChain Vector Store RAG")
3. URL Permalink: Lowercase, hyphens only, concise URL slug without dates
4. Semantic Keywords: 6-8 LSI / related technical keywords, comma-separated
5. Hook Keyword: Catchy developer hook phrase (3-6 words)
6. Search Intent Keywords: 4-6 queries developers search on Google, comma-separated
7. Tags: 3-5 relevant tags (e.g. LangChain, LangGraph, Python, AI Agents, RAG), comma-separated

Format your response EXACTLY as follows (one per line):
TITLE: [Your Title Here]
FOCUS_KW: [focus keyword]
PERMALINK: [url-slug-here]
SEMANTIC_KW: [kw1, kw2, kw3, kw4, kw5, kw6]
HOOK_KW: [Catchy Hook Phrase]
SEARCH_KW: [query 1, query 2, query 3]
TAGS: [Tag1, Tag2, Tag3]

Return ONLY these 7 lines.
"""

        try:
            from article_generator import generate_text_with_retry_and_fallback
            response = generate_text_with_retry_and_fallback(prompt)

            lines = response.text.strip().split('\n')
            metadata = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace('_', '')
                    value = value.strip()

                    if key == 'title':
                        metadata['title'] = value
                    elif key == 'focuskw':
                        metadata['focus_kw'] = value
                    elif key == 'permalink':
                        metadata['permalink'] = self._clean_permalink(value)
                    elif key == 'semantickw':
                        metadata['semantic_kw'] = value
                    elif key == 'hookkw':
                        metadata['hook_kw'] = value
                    elif key == 'searchkw':
                        metadata['search_kw'] = value
                    elif key == 'tags':
                        metadata['tags'] = value

            # Validate required fields
            required = ['title', 'focus_kw', 'permalink', 'semantic_kw']
            if not all(k in metadata for k in required):
                raise ValueError(f"Missing required fields in AI metadata: {list(metadata.keys())}")

            metadata['affiliate_links'] = ""
            metadata['source_link'] = news_item.get('link', '')

            print(f"✅ Generated Metadata:")
            print(f"   📌 Title: {metadata['title']}")
            print(f"   🎯 Focus KW: {metadata['focus_kw']}")
            print(f"   🔗 Permalink: {metadata['permalink']}")

            return metadata

        except Exception as e:
            print(f"❌ Metadata generation failed: {e}")
            return None

    def _clean_permalink(self, permalink):
        """Clean permalink to ensure safe URL slug"""
        permalink = permalink.lower()
        permalink = re.sub(r'https?://[^\s]+', '', permalink)
        permalink = re.sub(r'[^a-z0-9\-]', '-', permalink)
        permalink = re.sub(r'-+', '-', permalink)
        return permalink.strip('-')

    def get_trending_topic_for_blog(self):
        """
        Main method: Fetch trending AI/LangChain news and return one ready-to-write blog topic
        """
        print("=" * 60)
        print("🔥 DISCOVERING TRENDING LANGCHAIN / AI AGENTS TOPIC")
        print("=" * 60)

        news_items = self.fetch_trending_topics(max_results=20)
        if not news_items:
            print("❌ No new candidate news items found")
            return None

        suitable_topics = self.filter_suitable_topics(news_items)
        if not suitable_topics:
            print("❌ No suitable topics passed AI filter")
            return None

        for i, selected_news in enumerate(suitable_topics, 1):
            print(f"\n🔄 Evaluating candidate topic {i}/{len(suitable_topics)}: '{selected_news['title']}'")
            metadata = self.generate_blog_metadata_from_news(selected_news)

            if metadata:
                # Check if generated permalink or title matches existing
                if self._is_topic_used(metadata['title']) or self._is_topic_used(metadata['permalink']):
                    print(f"⚠️ Generated metadata matches existing post, trying next candidate...")
                    continue

                self._mark_topic_used(metadata['title'], metadata['permalink'])
                return metadata

        print("❌ All suitable candidate topics failed validation")
        return None


if __name__ == "__main__":
    fetcher = GoogleNewsFetcher()
    topic = fetcher.get_trending_topic_for_blog()
    if topic:
        print("\n🎉 Topic ready:")
        for k, v in topic.items():
            print(f"  {k}: {v}")
    else:
        print("Failed to fetch trending topic.")

