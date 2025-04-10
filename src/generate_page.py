import os
from md_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

def open_file(filepath):
    with open(filepath, "r") as f:
        md = f.read()
    return md

def generate_pages_recursive(file_list, source, dest, basepath):
    if not len(file_list):
        return True
    file_dest = file_list[0].replace(source,dest).replace(".md", ".html")
    dir_path = "/".join(file_dest.split("/")[:-1])
    print(f"process_public_files: {file_list[0]} -> {file_dest}")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    generate_page(file_list[0], "template.html", file_dest, basepath)
    generate_pages_recursive(file_list[1:], source, dest, basepath)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        if (block_to_block_type(b)) == BlockType.HEADING:
            return b.strip("#").strip()

def generate_page(source_path, template_path, dest_path, basepath):
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")
    source_md = open_file(source_path)
    template_html = open_file(template_path)

    title = extract_title(source_md)
    conv_html = markdown_to_html_node(source_md)

    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", conv_html.to_html())
    template_html = template_html.replace('href="/', f'href="{basepath}')
    template_html = template_html.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w") as f:
        f.write(template_html)