import os
import shutil
from generate_html import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def delete_content_from_dir(path_to_dir):
    items_in_dir = os.listdir(path_to_dir)
    for item in items_in_dir:
        path_to_item = os.path.join(path_to_dir, item)
        if os.path.isdir(path_to_item):
            delete_content_from_dir(path_to_item)
            os.rmdir(path_to_item)
        else:
            os.remove(path_to_item)

def copy_files_to_dest(path_to_src, path_to_dest):
    items_in_src = os.listdir(path_to_src)
    for item in items_in_src:
        path_to_item = os.path.join(path_to_src, item)
        if os.path.isfile(path_to_item):
            shutil.copy(path_to_item, path_to_dest)
        else:
            new_dest_path = os.path.join(path_to_dest, item)
            if not os.path.exists(new_dest_path):
                os.mkdir(new_dest_path)
            copy_files_to_dest(path_to_item, new_dest_path)
            

def generate_public(src, dest="public"):
    if not os.path.exists(dest):
        os.mkdir(dest)
    dest_path = os.path.abspath(dest)
    src_path = os.path.abspath(src)
    delete_content_from_dir(dest_path)
    copy_files_to_dest(src_path, dest_path)

if __name__ == "__main__":
    print("Cleaning public, and copying static files")
    generate_public(dir_path_static, dir_path_public)
    print("Generating page...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)