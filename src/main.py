import os
import sys
from shutil import rmtree, copy
from textnode import TextNode, TextType
from copystatic import get_file_list, copy_files
from generate_page import generate_pages_recursive

def overwrite_dir(source="static", dest="docs"):
    if os.path.isdir(dest):
        rmtree(dest)
    os.makedirs(dest)
    file_list = get_file_list(source)
    copy_files(file_list, source, dest)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    overwrite_dir()
    generate_pages_recursive(get_file_list("content"), "content", "docs", basepath)

if __name__ == "__main__":
    main()
