# This is a tiny tool to scan a directory and find all the duplicated files, then create a link to save disk space.


import os
import hashlib
import argparse


config = {
    "path": "",
    "hash": "md5",
    "link": "soft"
}


parser = argparse.ArgumentParser(description='Find duplicated files and create links to save disk space.')
parser.add_argument("dir", help="The path to scan")
parser.add_argument("--hash", help="The algorithm to use, default is md5", choices=["md5", "sha1", "sha256", "sha512"])
parser.add_argument("-t", "--type", help="The type of link to create, default is soft", choices=["soft", "hard"])

config["path"] = parser.parse_args().dir
if parser.parse_args().hash:
    config["hash"] = parser.parse_args().hash
if parser.parse_args().type:
    config["link"] = parser.parse_args().type


def get_file_hash(file_path):
    hash_method = hashlib.new(config["hash"])
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_method.update(chunk)
    return hash_method.hexdigest()


def file_size_beautify(file_size):
    if file_size < 1024:
        return "%sB" % file_size
    elif file_size < 1024 * 1024:
        return "%sKB" % (file_size / 1024)
    elif file_size < 1024 * 1024 * 1024:
        return "%sMB" % (file_size / 1024 / 1024)
    else:
        return "%sGB" % (file_size / 1024 / 1024 / 1024)


def scan_file(dir):
    """
    :param dir:
    :return: all the paths
    """
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_list.append(os.path.join(root, file))
    file_list.sort()
    return file_list


def make_link(src, dst):
    if config["link"] == "hard":
        os.link(src, dst)
    elif config["link"] == "soft":
        src = os.path.relpath(src, os.path.dirname(dst))
        os.symlink(src, dst, target_is_directory=False)


def remove_file(path):
    os.remove(path)


def remove_duplicated(file_list):
    """
    :param file_list:
    :return:
    """
    file_info = dict()
    total_file_size_saved = 0
    for file in file_list:
        file_hash = get_file_hash(file)
        if file_hash not in file_info:
            file_info[file_hash] = file
        else:
            file_size = os.path.getsize(file)
            print(f"{file} ==> {file_info[file_hash]} ({file_size_beautify(file_size)})")
            remove_file(file)
            make_link(file_info[file_hash], file)
            total_file_size_saved += file_size

    print("Finished. Total file size saved: %s" % file_size_beautify(total_file_size_saved))


if __name__ == "__main__":
    file_list = scan_file(config["path"])
    remove_duplicated(file_list)
