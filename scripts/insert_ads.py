import os
import re
import argparse

AD_CODE = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""

def insert_ads_into_content(content):
    # Split content into front matter and body
    parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    if len(parts) < 3:
        return content  # Not a standard Jekyll post with front matter

    front_matter = parts[1]
    body = parts[2:]
    body_text = "---".join(body)

    # Check if ad code already exists to avoid duplication
    if 'data-ad-slot="7340313511"' in body_text:
        return content

    # Split body into paragraphs/sections
    paragraphs = re.split(r'\n\s*\n', body_text)
    
    if len(paragraphs) < 5:
        # Too short for multiple ads, maybe just one in the middle
        if len(paragraphs) > 2:
            paragraphs.insert(len(paragraphs) // 2, AD_CODE)
    else:
        # Insert 2-3 ads
        # Insert first ad after ~1/4 of content
        pos1 = len(paragraphs) // 4
        paragraphs.insert(pos1, AD_CODE)
        
        # Insert second ad after ~2/4 of content (updated index)
        pos2 = (len(paragraphs) * 2) // 4 + 1
        paragraphs.insert(pos2, AD_CODE)
        
        # Insert third ad after ~3/4 of content (updated index)
        if len(paragraphs) > 10:
             pos3 = (len(paragraphs) * 3) // 4 + 2
             paragraphs.insert(pos3, AD_CODE)

    new_body = "\n\n".join(paragraphs)
    return f"---{front_matter}---{new_body}"

def process_file(file_path, dry_run=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = insert_ads_into_content(content)

    if content == new_content:
        print(f"No changes for {file_path} (Already has ads or too short)")
        return

    if dry_run:
        print(f"DRY RUN: Would update {file_path}")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Insert AdSense code into Jekyll posts.")
    parser.add_argument("--file", help="Specific file to process")
    parser.add_argument("--dir", default="_posts", help="Directory containing posts")
    parser.add_argument("--dry-run", action="store_true", help="Don't save changes")

    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file):
            process_file(args.file, args.dry_run)
        else:
            print(f"File not found: {args.file}")
    else:
        if not os.path.isdir(args.dir):
            print(f"Directory not found: {args.dir}")
            return

        for filename in os.listdir(args.dir):
            if filename.endswith(".md") or filename.endswith(".markdown"):
                file_path = os.path.join(args.dir, filename)
                process_file(file_path, args.dry_run)


if __name__ == "__main__":
    main()

