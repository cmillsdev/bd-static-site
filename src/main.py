import os
from shutil import rmtree, copy
from textnode import TextNode, TextType
from copystatic import get_file_list, copy_files
from generate_page import process_public_files

def overwrite_dir(source="static", dest="public"):
    rmtree(dest)
    os.mkdir(dest)
    file_list = get_file_list(source)
    copy_files(file_list, source, dest)

def main():
    overwrite_dir()
    process_public_files(get_file_list("content"), "content", "public")

if __name__ == "__main__":
    main()
