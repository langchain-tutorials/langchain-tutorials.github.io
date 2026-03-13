import os

def get_post_titles(posts_dir):
    """
    Extracts the 'title' from the YAML frontmatter of markdown files in the given directory.
    """
    titles = []
    
    if not os.path.exists(posts_dir):
        print(f"Error: Directory '{posts_dir}' not found.")
        return titles

    for filename in sorted(os.listdir(posts_dir)):
        if filename.endswith(".md") or filename.endswith(".markdown"):
            filepath = os.path.join(posts_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    in_frontmatter = False
                    for line in f:
                        line = line.strip()
                        if line == '---':
                            if not in_frontmatter:
                                in_frontmatter = True
                            else:
                                # Reached the end of frontmatter without finding title
                                break
                        elif in_frontmatter and line.startswith('title:'):
                            # Extract the title and remove the 'title:' prefix
                            title = line[6:].strip()
                            
                            # Remove surrounding quotes if present
                            if (title.startswith('"') and title.endswith('"')) or (title.startswith("'") and title.endswith("'")):
                                title = title[1:-1]
                            
                            titles.append(title)
                            break
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                        
    return titles

if __name__ == "__main__":
    # Assuming the script will be in the 'scripts' directory or the project root.
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if we are in the 'scripts' folder, if so, the project root is one level up
    if os.path.basename(script_dir) == 'scripts':
        project_root = os.path.dirname(script_dir)
    else:
        project_root = script_dir
        
    posts_directory = os.path.join(project_root, "_posts")
    
    # Fallback to current working directory if _posts is not found
    if not os.path.exists(posts_directory):
        posts_directory = os.path.join(os.getcwd(), "_posts")
         
    print(f"Scanning directory: {posts_directory} \n")
    titles = get_post_titles(posts_directory)
    
    print(f"Found {len(titles)} post titles:")
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
