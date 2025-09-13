import sys
import os
import shutil

from gencontent import generate_pages_recursive, copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    print(f"=====Executing__MAIN__=====")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    basepath = "/"
    if sys.argv[1] is not None:
     basepath = sys.argv[1]
    print(f"basepath: {basepath}")

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)
    
            
if __name__ == "__main__":
    main()
