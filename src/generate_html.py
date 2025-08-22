from md_to_textnode import markdown_to_html_node
import os

def extract_title(md):
    title = md.split("\n")[0]
    if title[:2] != "# ":
        raise ValueError("markdown text does not contain a title")
    return title.lstrip("# ")


def read_text_from_file(file_path):
    f = open(file_path)
    contents = f.read()
    f.close()
    return contents


def write_html_file(html_page, dest_path):
    f = open(dest_path, "x")
    f.write(html_page)
    f.close()
    

def generate_page_from_template(markdown_text, template_text, basepath):
    contents = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(markdown_text)
    return template_text.replace("{{ Title }}", title).replace("{{ Content }}", contents).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating pages from {from_path} to {dest_path} using {template_path}\n")
    markdown_text = read_text_from_file(from_path)
    template_text = read_text_from_file(template_path)
    html_page = generate_page_from_template(markdown_text, template_text, basepath)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    write_html_file(html_page, dest_path)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    items_in_content_dir = os.listdir(dir_path_content)

    for item in items_in_content_dir:
        path_to_item = os.path.join(dir_path_content, item)
        if os.path.isdir(path_to_item):
            generate_pages_recursive(path_to_item, template_path, os.path.join(dest_dir_path, item), basepath)
        else:
            generate_page(path_to_item, template_path, os.path.join(dest_dir_path, item).replace(".md", ".html"), basepath)





if __name__ == "__main__":
    print(extract_title("# Hello World"))
