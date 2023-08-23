from pathlib import Path
import os
from typing import List, Tuple, Dict
from PathProperties import PathProperties, PathType, PathUnit
from tqdm import tqdm
from timeit import Timer
from CustomError import InvalidPathException
import math
import sys

# --------------------------------------------------
CONFIG_PATH = "config.txt"

# --------------------------------------------------


def set_pathinfo(path: Path, depth: int, ) -> None:
    allfilepath = list(path.glob("*"))
    for path in tqdm(allfilepath):
        fileprop = __get_path_properties(path, 0, depth)
        __add_pathinfo(fileprop)


def __get_directory_data(path: Path, pos: int, depth: int) -> Tuple[List[PathProperties], int]:
    directory_size = 0.0
    path_properties_list: List[PathProperties] = []
    allfilepath = list(path.glob("*"))
    for path in tqdm(allfilepath):
        pathprop = __get_path_properties(path, pos, depth)
        path_properties_list.extend(pathprop)
        directory_size += pathprop[0].get_uncalculated_size()
    return (path_properties_list, directory_size)


def __get_directory_size_depth_reach(path: Path) -> float:
    size = 0.0
    for path, dirs, files in os.walk(path):
        for file in files:
            joined_path = os.path.join(path, file)
            size += os.path.getsize(joined_path)
    return size


def __add_pathinfo(pathPropertieslist: List[PathProperties]) -> None:
    global pathinfo
    for path_object in pathPropertieslist:
        pathinfo += path_object()


def __get_path_properties(path: Path, pos: int, depth: int) -> List[PathProperties]:
    """
    """
    global size
    if path.is_file():
        size_of_file = os.path.getsize(path)
        size += size_of_file
        return [PathProperties(path, size_of_file, PathType.FILE)]
    elif pos < depth:
        path_properties_list, directory_size = __get_directory_data(
            path, pos+1, depth)
        pathprop = [PathProperties(
            path, directory_size, PathType.DIRECTORY)]
        pathprop.extend(path_properties_list)
        return pathprop
    else:
        directory_size = __get_directory_size_depth_reach(path)
        size += directory_size
        return [PathProperties(path, directory_size, PathType.DIRECTORY)]


def set_title(path: Path, size: float) -> None:
    fileTitle = PathProperties(path, size, PathType.TITLE)
    global pathinfo
    pathinfo = fileTitle() + pathinfo


def write_log(pathstring: str) -> None:
    with open(pathstring, 'w', encoding="utf-8") as f:
        f.write(pathinfo)


def check_valid_path(path: str) -> bool:
    if os.path.exists(path):
        return True
    return False


def get_data_from_config(path: str = CONFIG_PATH) -> Tuple[str, int]:
    depth = 1000
    with open(CONFIG_PATH, 'r') as config:
        datas = config.read().splitlines()
        if not len(datas):
            raise InvalidPathException("[ERROR]: Please specify the path for scanning")
        elif len(datas) == 1:
            if not check_valid_path(path):
                raise FileNotFoundError("[ERROR]: File or Directory not found")
        else:
            depth = datas[1]
        path_to_check = datas[0]
    return (path_to_check, depth)


def check_path_log(path: str) -> bool:
    if os.path.isfile(path):
        return True
    return False


def edit_path_log(path: str) -> str:
    if platform_is_window():
        suffix_num = 0 if path.split(
            "\\")[-1].split('.')[0][-1].isalpha() else int(path.split("\\")[-1].split(".")[0][-1]) + 1
    else:
        suffix_num = 0 if path.split(
            "/")[-1].split('.')[0][-1].isalpha() else int(path.split("/")[-1].split(".")[0][-1]) + 1
    while (check_path_log(path[:-4] + str(suffix_num) + path[-4:])):
        suffix_num += 1
    return path[:-4] + str(suffix_num) + path[-4:]


def norm_path(path: str) -> str:
    return path.replace("/", "\\")


def platform_is_window() -> bool:
    return sys.platform == "win32"


def get_path_log(path: str) -> str:
    if platform_is_window():
        return ".\log\log_" + path.split("\\")[-1] + ".txt"
    return "./log/log_" + path.split("\\")[-1] + ".txt"


def run() -> None:
    global size, pathinfo
    size = 0
    pathinfo = """"""
    try:
        path_to_check, depth = get_data_from_config()
        depth = int(depth)
        path = get_path_log(norm_path(path_to_check))
        if check_path_log(path):
            while ((ans := input("Do you want to replace the file that already exist? (Y/n): ").lower()) not in ['y', 'n']):
                pass
            if ans == "n":
                path = edit_path_log(path)
        PathProperties.set_smallestindex(path_to_check)
        path_to_check = Path(path_to_check)
        set_pathinfo(path_to_check, depth)
        set_title(path_to_check, size)
        write_log(path)
    except Exception as e:
        print(e)
        print(e.with_traceback())
