"""Generate blog articles using Gemini AI with fallback models and retry handling"""
import os
import sys
import re
import glob

# Ensure scripts dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google import genai
from config import TEXT_MODEL, GEMINI_API_KEY, POSTS_DIR

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


def generate_text_with_retry_and_fallback(contents, preferred_model=TEXT_MODEL):
    """Generate content with automatic fallback across Gemini flash models and retry on rate limits"""
    import time
    ai_client = get_genai_client()
    models_to_try = [preferred_model]
    for m in ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"]:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = ai_client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                return response
            except Exception as e:
                last_error = e
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print(f"ℹ️ Model {model_name} quota hit / rate-limited. Trying fallback model...")
                    time.sleep(2)
                    break
                else:
                    time.sleep(1)
    raise last_error


def get_recent_posts_context(limit=8):
    """Dynamically get recent posts for contextual internal linking"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_path = os.path.join(project_root, POSTS_DIR)
    if not os.path.exists(posts_path):
        posts_path = POSTS_DIR

    if not os.path.exists(posts_path):
        return "- 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools\n- 2026-04-05-langgraph-stategraph-multi-step-ai-agent"

    post_files = sorted(glob.glob(os.path.join(posts_path, "*.md")), reverse=True)
    recent_slugs = []
    for pf in post_files[:limit]:
        basename = os.path.basename(pf).replace('.md', '').replace('.markdown', '')
        recent_slugs.append(f"- {basename}")

    return "\n".join(recent_slugs)


def generate_article(title, focus_kw, permalink, semantic_kw, affiliate_links="", hook_kw="", search_kw="", tags=""):
    """Generate SEO-optimized blog article"""
    recent_posts = get_recent_posts_context()

    prompt = f"""
Write an in-depth, authoritative, SEO-optimised technical tutorial and developer guide on the title "{title}".
Focus Keyword: {focus_kw}
LSI / Semantic Keywords: {semantic_kw}
Search Intent Queries: {search_kw}

Rules & Guidelines:
- Simple, clear, and practical English that any software developer can understand and implement immediately.
- Don't write more than 3 sentences per paragraph; change paragraph after 3 sentences.
- Hook: {hook_kw or "Master building production-ready AI agents and workflows with step-by-step guidance."}
- Use "you" to address the reader directly.
- Include complete, realistic, and runnable Python code snippets using modern LangChain (or LangGraph / AI frameworks).
- Include architecture explanations, diagrams in text or markdown tables, and configuration options.
- IMPORTANT Internal Linking:
    - Use Jekyll format: [Link Text]({{% post_url yyyy-mm-dd-slug %}})
    - Here are some valid recent posts in this blog you can link to where relevant:
{recent_posts}
    - CRITICAL: DO NOT include the '.md' extension in the post_url tag.
- IMPORTANT Liquid Syntax & Code Blocks:
    - If a code block contains double curly braces (e.g., {{{{ ... }}}}) or Liquid tags (e.g., {{% ... %}}), wrap the ENTIRE block in {{% raw %}} and {{% endraw %}} tags.
- Do NOT use H1 in the markdown body. Use H2, H3, H4 headings with a clean logical structure.
- Use bullet points, comparison tables, step-by-step code frameworks, and data callouts.
- Write a comprehensive article of more than 2,000 words.
- Include a dedicated "Frequently Asked Questions (FAQs)" section at the end.
- Format cleanly in Jekyll Markdown.
- Naturally weave in the focus keyword and semantic keywords.
- Do NOT output any front matter, YAML, or metadata blocks in your response.
"""

    print("🤖 Generating comprehensive technical tutorial with Gemini...")
    response = generate_text_with_retry_and_fallback(prompt)

    # Remove any front matter that AI might have added
    content = remove_front_matter(response.text)

    # Sanitize content for common Liquid/Jekyll errors
    content = sanitize_liquid_syntax(content)

    # Add custom front matter
    article = create_custom_front_matter(title, focus_kw, permalink, tags=tags) + "\n\n" + content

    return article


def sanitize_liquid_syntax(content):
    """
    Sanitize generated content for common Liquid syntax errors:
    1. Wrap code blocks containing {{ or {% in {% raw %} tags.
    2. Fix malformed Liquid tags (e.g., {% - endif %}).
    3. Remove .md from post_url tags.
    """
    code_block_regex = r'```(.*?)\n(.*?)```'

    def wrap_raw(match):
        lang = match.group(1)
        code = match.group(2)
        if ('{{' in code or '{%' in code) and '{% raw %}' not in code:
            return f'{{% raw %}}\n```{lang}\n{code}```\n{{% endraw %}}'
        return match.group(0)

    content = re.sub(code_block_regex, wrap_raw, content, flags=re.DOTALL)
    content = content.replace('{% -', '{%-').replace('- %}', '-%}')
    content = content.replace('{%  endif %}', '{% endif %}')
    content = content.replace('{% - endif %}', '{% endif %}')
    content = re.sub(r'\{% post_url (.*?).md %\}', r'{% post_url \1 %}', content)

    return content


def remove_front_matter(content):
    """Remove any existing front matter from AI-generated content"""
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    lines = content.split('\n')
    clean_lines = []
    skip_yaml = True

    for line in lines:
        if line.strip().startswith('#') or (line.strip() and ':' not in line):
            skip_yaml = False

        if not skip_yaml:
            clean_lines.append(line)
        elif skip_yaml and line.strip() and ':' not in line:
            skip_yaml = False
            clean_lines.append(line)

    return '\n'.join(clean_lines).strip()


def create_custom_front_matter(title, focus_kw, permalink, tags=""):
    """Create properly formatted Jekyll front matter"""
    escaped_title = title.replace('"', '\\"')

    # Generate meta description
    description = generate_description(title, focus_kw)

    # Format tags
    if tags:
        if isinstance(tags, str):
            tag_list = [t.strip().strip('"').strip("'") for t in tags.split(',') if t.strip()]
        else:
            tag_list = [str(t).strip() for t in tags if str(t).strip()]
    else:
        tag_list = [focus_kw.title(), "LangChain", "AI Agents", "Python", "Tutorial"]

    # Ensure uniqueness while preserving order
    seen = set()
    unique_tags = []
    for t in tag_list:
        if t.lower() not in seen:
            seen.add(t.lower())
            unique_tags.append(t)

    formatted_tags = ", ".join(f'"{t}"' for t in unique_tags[:6])

    front_matter = f"""---
title: "{escaped_title}"
description: "{description}"
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [{formatted_tags}]
featured: false
image: '/assets/images/{permalink}.webp'
---"""

    return front_matter


def generate_description(title, focus_kw):
    """Generate SEO-optimized meta description (150-160 characters)"""
    prompt = f"""
Generate a compelling meta description for this AI development tutorial.

Title: {title}
Focus Keyword: {focus_kw}

Requirements:
- EXACTLY 150-160 characters (critical)
- Include the focus keyword naturally
- Action-oriented and engaging for Python and AI developers
- No quotes or special characters
- Complete sentence

Return ONLY the description text, nothing else.
"""

    print("📝 Generating meta description...")
    response = generate_text_with_retry_and_fallback(prompt)

    description = response.text.strip().replace('"', '').replace("'", "")

    if len(description) > 160:
        description = description[:157].rsplit(' ', 1)[0] + "..."

    print(f"✅ Description generated: {description} ({len(description)} chars)")
    return description


def generate_stock_photo_keywords(title, focus_kw=""):
    """Generate clean, highly relevant stock photo search queries for Pexels and Unsplash"""
    prompt = f"""
Given this AI tutorial title: "{title}" and focus keyword: "{focus_kw}"
Generate 3 distinct, clean search queries (1-3 words each) suitable for finding authentic, high-quality developer or tech stock photos on Pexels or Unsplash.

Examples of good queries:
- For "LangGraph Multi-Agent Architecture": "developer programming, neural network, modern server room"
- For "LangChain Function Calling": "python code screen, software engineer desk, cloud computing"
- For "RAG Hybrid Search Tutorial": "big data analysis, cyber security code, modern tech workspace"

Return ONLY a comma-separated list of 3 queries. No quotes, no markdown, no explanations.
"""
    try:
        print("🔍 Generating stock photo search queries...")
        response = generate_text_with_retry_and_fallback(prompt)
        queries = [q.strip().strip('"').strip("'") for q in response.text.strip().split(',') if q.strip()]
        return queries if queries else [focus_kw, "software code", "artificial intelligence"]
    except Exception as e:
        print(f"⚠️ Stock query generation fallback: {e}")
        return [focus_kw, "developer computer", "artificial intelligence"]


def generate_image_prompt(title, focus_kw=""):
    """Generate an ultra-relevant featured image prompt tailored for technical AI blogs"""
    prompt = f"""
You are an expert art director creating an ultra-realistic, modern featured image prompt for an AI developer publication (LangChain Tutorials).

Article Title: "{title}"
Focus Keyword: "{focus_kw}"

CRITICAL RULES:
1. MUST BE A CONCRETE MODERN TECH/DEVELOPER SCENE:
   - Depict tangible, authentic elements: modern developer desk with mechanical keyboard, curved monitor with sleek syntax highlighted code terminal, subtle blue/violet ambient LED lighting, minimalist hardware chips, high-tech server racks, or conceptual clean glass neural nodes.
   - STRICTLY FORBIDDEN: NO fantasy magical spells, NO glowing wizard hands, NO cartoon robots, NO childish sci-fi illustrations.
   - AVOID CLICHÉS: Do NOT generate cheesy blue globe holograms or robotic handshakes.
2. HIGH RELEVANCE: The aesthetic should immediately resonate with software engineers, AI developers, and tech builders.
3. ABSOLUTE ZERO TEXT: NO text, NO letters, NO words, NO numbers, NO watermarks, NO brand logos anywhere.
4. STYLE: Commercial editorial photography, 8K resolution, realistic natural & neon ambient lighting, cinematic shallow depth of field, 16:9 widescreen composition.

Output ONLY the final image generation prompt (1-2 vivid sentences describing the setting, objects, lighting, and camera angle).
"""

    print("🎨 Generating contextual AI image prompt...")
    response = generate_text_with_retry_and_fallback(prompt)
    return response.text.strip()
