import os
import shutil
import re
from pathlib import Path
from block_markdown import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    contents = os.listdir(dir_path_content)
    for content in contents:
        content_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(content_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(content_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(content_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
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
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    # write directory up to dest_path
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    # write full HTML page to dest_path.
    try:
        with open(dest_path, "w") as f:
            f.write(new_page)
    except Exception as e:
        return f"Error writing file at '{dest_path}': {e}"


def extract_title(markdown):
    title = ""
    h1_pattern = r"^#{1}(?P<title>.*)"
    title = re.search(h1_pattern, markdown).group('title').strip()
    return title


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
            
