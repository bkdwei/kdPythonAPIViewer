# coding: utf-8
import os

config_file = os.path.join(os.path.expanduser('~') , ".config/kdPythonAPIViewer/dict.txt")
cur_dir = os.path.dirname(os.path.realpath(__file__))
def get_file_realpath(file):
    return os.path.join(cur_dir,file)
def check_and_create(absolute_file_path):
    slash_last_index = absolute_file_path.rindex("/")
    path = absolute_file_path[:slash_last_index]
    file = absolute_file_path[slash_last_index + 1:]
    # 检查目录
    if os.path.exists(path) is not True:
        os.makedirs(path)
    elif os.path.isdir(path) is not True:
        print(path, "is no a dir,delete and create a dir")
        os.remove(path)
        os.makedirs(path)
    # 检查文件
    if os.path.exists(absolute_file_path) is not True:
        with open(absolute_file_path, "w+") as f:
            pass
    elif os.path.isfile(absolute_file_path) is not True:
        os.removedirs(absolute_file_path)
        with open(absolute_file_path, "w+") as f:
            pass


def check_and_create_dir(absolute_dir_path):
    if os.path.exists(absolute_dir_path) is not True:
        os.makedirs(absolute_dir_path)
    elif os.path.isdir(absolute_dir_path) is not True:
        print(absolute_dir_path, "is no a dir,delete and create a dir")
        os.remove(absolute_dir_path)
        os.makedirs(absolute_dir_path)
