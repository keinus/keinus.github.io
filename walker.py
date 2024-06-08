import os

def add_text_to_md_files(directory):
    """
    Add text to all .md files in the given directory and its subdirectories.
    
    :param directory: The root directory to start searching for .md files.
    :param text: The text to add to the .md files.
    :param position: 'start' to add at the beginning, 'end' to add at the end of the file.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Read the original content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title = file[:-3]
                last_slash_index = root.rfind("/")  # 마지막 슬래시의 인덱스 찾기
                parent = root[last_slash_index + 1:]  # 슬래시 다음부터 끝까지 추출
                text_to_add = f"""---
layout: default
title: {title}
nav_order: 1
parent: {parent}
---
                """
                # Add the text at the specified position
                new_content = text_to_add + '\n\n' + content
                
                # Write the new content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"Added text to {file_path}")

# Example usage
root_directory = './docs'  # Current directory
add_text_to_md_files(root_directory)
