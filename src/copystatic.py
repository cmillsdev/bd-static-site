import os
from shutil import copy
def get_file_list(path):
    file_list = []
    for p in os.listdir(path):
        full_path = os.path.join(path, p)
        if os.path.isfile(full_path):
            print(f"Found: {full_path}")
            file_list.append(full_path)
        elif os.path.isdir(full_path):
            file_list.extend(get_file_list(full_path))
    return file_list
        
def copy_files(file_list, source, dest):
    if not len(file_list):
        return True
    file_dest = file_list[0].replace(source,dest)
    dir_path = "/".join(file_dest.split("/")[:-1])
    print(f"copy_files: {file_list[0]} -> {file_dest}")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    copy(file_list[0],file_dest)
    copy_files(file_list[1:], source, dest)