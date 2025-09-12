import os
import shutil
import re

from htmlnode import HTMLNode
from block_markdown import markdown_to_html_node


# input: <string>
# output: <string>
def extract_title(markdown):
    title = ""
    h1_pattern = r"^#{1}(?P<title>.*)"
    title = re.search(h1_pattern, markdown).group('title').strip()
    return title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page... from {from_path} to {dest_path} using {template_path}")

    md = ""
    template = ""
    html = ""
    # read and store (from_path)
    try:
        with open(from_path, "r") as f:
            md = f.read()
    except Exception as e:
        return f"Error reading file at '{from_path}': {e}"
    # read and store (template_path)
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except Exception as e:
        return f"Error reading file at '{template_path}': {e}"

    # use markdown_to_html_node and .to_html() to convert md file to html string
    html = markdown_to_html_node(md).to_html()

    # extract title
    title = extract_title(md)

    # replace placeholders in template with HTML and title
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # write full HTML page to dest_path.
    try:
        with open(dest_path, "w") as f:
            f.write(new_page)
    except Exception as e:
        return f"Error writing file at '{dest_path}': {e}"

def copy_contents_to_public(src, dest):
    abs_src_path = os.path.abspath(src)
    abs_dest_path = os.path.abspath(dest)
    abs_public_dir = os.path.abspath(os.path.join(os.getcwd(), "public"))

    # check if source exists
    if not os.path.exists(abs_src_path):
        raise FileNotFoundError(f"Source ({src}) does not exist")
    # check if destination is within the 'public' directory
    if not abs_dest_path.startswith(abs_public_dir):
        raise ValueError(f"Path Error: Destination ({dest}) must be within the 'public' directory")

    # delete previous public directory
    if abs_dest_path == abs_public_dir:
        print(f"deleting... {abs_public_dir}")
        shutil.rmtree(abs_public_dir)
        print(f"remaking... {abs_public_dir}")
        os.mkdir(abs_public_dir)
        
    src_contents = os.listdir(abs_src_path)
    print(f"\t{abs_src_path}:\n\t\t{src_contents}")
    for content in src_contents:
        if content.startswith("_"):
            continue
        content_path = os.path.join(abs_src_path, content)
        new_dest_path = os.path.join(abs_dest_path, content)
        if os.path.isdir(content_path):
            os.mkdir(new_dest_path)
            print(f"making new dir... {content} @ {new_dest_path}")
            copy_contents_to_public(content_path, new_dest_path)
        if os.path.isfile(content_path):
            print(f"copying... {content} -> {new_dest_path}")
            shutil.copy(content_path, new_dest_path)

def main():
    print(f"=====Executing__MAIN__=====")
    copy_contents_to_public('static', 'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')

if __name__ == "__main__":
    main()
