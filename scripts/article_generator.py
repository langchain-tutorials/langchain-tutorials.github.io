"""Generate blog articles using Gemini AI"""
from google import genai
from config import TEXT_MODEL, GEMINI_API_KEY
import re

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_article(title, focus_kw, permalink, semantic_kw, affiliate_links):
    """Generate SEO-optimized blog article"""
    # List of recent valid 2026 posts for internal linking context
    recent_posts = """
    - 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools.md
    - 2026-04-05-langgraph-stategraph-multi-step-ai-agent.md
    - 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag.md
    - 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning.md
    - 2026-03-31-langchain-custom-output-parser-tutorial.md
    - 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked.md
    - 2026-02-05-build-rag-applications-langchain-vector-store-2026.md
    """

    prompt = f"""
write an SEO-optimised blog on the title {title}. using the Focus keyword {focus_kw} and using LSI Keywords {semantic_kw}
use the following

Rules:
- Simple English, a 10 year old can understand
- Don't write more than 3 sentences per paragraph, changes paragraph after 3 sentences
- Use "you" to address the reader
- if need link websites to refer to information
- do not highlight keywords
- Include practical examples related to {focus_kw}
- IMPORTANT: Internal Linking:
    - Use Jekyll format: [Link Text]({{% post_url yyyy-mm-dd-slug %}})
    - Current Year is 2026. DO NOT use years before 2026 for links.
    - Here are some valid recent posts you can link to if relevant:
    {recent_posts}
    - CRITICAL: DO NOT include the '.md' extension in the post_url tag.
- IMPORTANT: Liquid Syntax & Code Blocks:
    - If a code block contains double curly braces (e.g., {{{{ ... }}}}) or Liquid tags (e.g., {{% ... %}}), wrap the ENTIRE block in {{% raw %}} and {{% endraw %}} tags.
    - Example: {{% raw %}} ```python \n print("{{{{var}}}}") \n ``` {{% endraw %}}
- Use H2 and H3, h4, h5, h6 headings, no H1
- Use lists, tables, snippets, and other data formats
- Write more than 2000 words
- Write in Jekyll markdown format  artile filename extension .md only
- Naturally include focused & semantic keywords
- do not add any front matter or meta data
"""
    
    print("🤖 Generating article with Gemini...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    
    # Remove any front matter that AI might have added
    content = remove_front_matter(response.text)
    
    # Sanitize content for common Liquid/Jekyll errors
    content = sanitize_liquid_syntax(content)
    
    # Add custom front matter
    article = create_custom_front_matter(title, focus_kw, permalink) + "\n\n" + content
    
    return article

def sanitize_liquid_syntax(content):
    """
    Sanitize generated content for common Liquid syntax errors:
    1. Wrap code blocks containing {{ or {% in {% raw %} tags.
    2. Fix malformed Liquid tags (e.g., {% - endif %}).
    """
    import re
    
    # 1. Wrap code blocks containing {{ or {% in {% raw %} if not already wrapped
    # Match fenced code blocks
    code_block_regex = r'```(.*?)\n(.*?)```'
    
    def wrap_raw(match):
        lang = match.group(1)
        code = match.group(2)
        # Check if code contains suspicious Liquid-like syntax
        if ('{{' in code or '{%' in code) and '{% raw %}' not in code:
            return f'{{% raw %}}\n``` {lang}\n{code}```\n{{% endraw %}}'
        return match.group(0)
    
    # Apply to all code blocks
    content = re.sub(code_block_regex, wrap_raw, content, flags=re.DOTALL)
    
    # 2. Fix common malformed tags (e.g. spaces in the wrong places)
    content = content.replace('{% -', '{%-').replace('- %}', '-%}')
    content = content.replace('{%  endif %}', '{% endif %}')
    content = content.replace('{% - endif %}', '{% endif %}')
    
    # 3. Fix broken post_url tags (remove .md extension)
    content = re.sub(r'\{% post_url (.*?).md %\}', r'{% post_url \1 %}', content)
    
    return content

def remove_front_matter(content):
    """Remove any existing front matter from AI-generated content"""
    # Remove front matter between --- delimiters
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Remove any stray YAML-like lines at the beginning
    lines = content.split('\n')
    clean_lines = []
    skip_yaml = True
    
    for line in lines:
        # Stop skipping once we hit actual content (heading or paragraph)
        if line.strip().startswith('#') or (line.strip() and not ':' in line):
            skip_yaml = False
        
        if not skip_yaml:
            clean_lines.append(line)
        elif skip_yaml and line.strip() and ':' not in line:
            # This is actual content, not YAML
            skip_yaml = False
            clean_lines.append(line)
    
    return '\n'.join(clean_lines).strip()


def create_custom_front_matter(title, focus_kw, permalink):
    """Create properly formatted Jekyll front matter"""
    # Escape quotes in title
    escaped_title = title.replace('"', '\\"')
    
    # Generate description (you can make this dynamic)
    description = generate_description(title, focus_kw)
    
    # Create front matter - NO LEADING SPACES!
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
tags: [{focus_kw}]
featured: false
image: '/assets/images/{permalink}.webp'
---"""
       
    return front_matter

def generate_description(title, focus_kw):
    """Generate SEO-optimized meta description (160 characters)"""
    prompt = f"""
Generate a compelling meta description for this blog post.

Title: {title}
Focus Keyword: {focus_kw}

Requirements:
- EXACTLY 150-160 characters (this is critical)
- Include the focus keyword naturally
- Action-oriented and engaging
- Make readers want to click
- No quotes or special characters
- Complete sentence

Return ONLY the description text, nothing else.
"""
    
    print("📝 Generating meta description...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    
    description = response.text.strip()
    
    # Ensure it's under 160 characters
    if len(description) > 160:
        description = description[:157] + "..."
    
    print(f"✅ Description generated: {description} ({len(description)} chars)")
    
    return description



def generate_image_prompt(title):
    """Generate image prompt for Freepik AI"""
    prompt = f"""
Create a photorealistic featured image prompt for this blog post:
Title: {title}

Requirements:
- Professional, high-quality
- NO text or words in the image
- Suitable as a blog featured image
- 16:9 aspect ratio
- Relevant to the topic

Return ONLY the image prompt, nothing else.
"""
    
    print("🎨 Generating image prompt...")
    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt
    )
    return response.text.strip()
