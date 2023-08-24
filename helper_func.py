from pathlib import Path
import os
from typing import List, Tuple
from PathProperties import PathProperties, PathType, PathUnit
from tqdm import tqdm
from CustomError import InvalidPathException
import sys

# --------------------------------------------------
CONFIG_PATH = "config.txt"

# --------------------------------------------------


def set_pathinfo(path: Path, depth: int, unit:PathUnit ) -> None:
    allfilepath = list(path.glob("*"))
    for path in tqdm(allfilepath):
        fileprop = __get_path_properties(path, 0, depth)
        __add_pathinfo(fileprop,unit)


def __get_directory_data(path: Path, pos: int, depth: int) -> Tuple[List[PathProperties], float]:
    directory_size = 0.0
    path_properties_list: List[PathProperties] = []
    allfilepath = list(path.glob("*"))
    for path in tqdm(allfilepath):
        pathprop = __get_path_properties(path, pos, depth)
        path_properties_list.extend(pathprop)
        directory_size += pathprop[0].get_uncalculated_size()
    return (path_properties_list, directory_size)


def __get_directory_size_depth_reach(path: Path) -> float:
    global error_count
    size = 0.0
    for pathfile, dirs, files in os.walk(path):
        for file in files:
            joined_path = os.path.join(pathfile, file)
            try:
                size += os.path.getsize(joined_path)
            except FileNotFoundError:
                # print("[ERROR]: Can't reach to the File or Directory")
                error_count +=1
    return size


def __add_pathinfo(path_properties_list: List[PathProperties], unit: PathUnit ) -> None:
    global pathinfo
    for path_object in path_properties_list:
        pathinfo += path_object(unit)


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
    file_title = PathProperties(path, size, PathType.TITLE)
    global pathinfo
    pathinfo = file_title(PathUnit.UNSIGNED) + pathinfo


def write_log(pathstring: str) -> None:
    with open(pathstring, 'w', encoding="utf-8") as f:
        f.write(pathinfo)


def check_valid_path(path: str) -> bool:
    if os.path.exists(path):
        return True
    raise InvalidPathException("[ERROR]: File or Directory not found at path: " + path)
    


def get_data_from_config(path: str = CONFIG_PATH) -> Tuple[List[Tuple[str,PathUnit]], int]:
    with open(path, 'r') as config:
        path_list: List[Tuple[str,PathUnit]] = []
        depth = 1000
        datas = config.read().splitlines()
        if not len(datas):
            raise InvalidPathException("[ERROR]: Please specify the path for scanning")
        if datas[-1].isdigit():
            depth = int(datas[-1])
            datas = datas[:-1]
        for data in datas:
            unit = PathUnit.UNSIGNED
            if(data[0] == "!"):
                unit = get_pathunit(data.split()[0][1:])
                data = data[3:].strip()
            check_valid_path(data)
            path_list.append((data,unit))
    return (path_list, depth)

def get_pathunit(unit:str)->PathUnit :
    unit = unit.lower()
    if unit == "b":
        return PathUnit.BYTE
    elif unit == "kb":
        return PathUnit.KILO
    elif unit == "mb":
        return PathUnit.MEGA
    elif unit == "gb":
        return PathUnit.GIGA
    else:
        raise InvalidPathException("[ERROR]: Please type one of these unit: \"b\", \"kb\", \"mb\", \"gb\"")
        

def check_path_log(path: str) -> bool:
    if os.path.isfile(path):
        return True
    return False


def edit_path_log(path: str) -> str:
    if platform_is_window():
        suffix_num = int(path.split("\\")[-1].split(".")[0][-1]) + 1 if path.split(
            "\\")[-1].split('.')[0][-1].isdigit() else 0
    else:
        suffix_num = int(path.split("/")[-1].split(".")[0][-1]) + 1 if path.split(
            "/")[-1].split('.')[0][-1].isdigit() else 0
    while (check_path_log(path[:-4] + str(suffix_num) + path[-4:])):
        suffix_num += 1
    return path[:-4] + str(suffix_num) + path[-4:]


def norm_path(path: str) -> str:
    return path.replace("/", "\\")


def platform_is_window() -> bool:
    return sys.platform == "win32"


def get_path_log(path: str) -> str:
    if platform_is_window():
        return ".\\log\\log_" + path.split("\\")[-1] + ".txt"
    return "./log/log_" + path.split("\\")[-1] + ".txt"



def run() -> None:
    global size, pathinfo, error_count
    
    
    try:
        path_list, depth = get_data_from_config()
        depth = int(depth)
        for path,condition_unit in path_list:
            size = 0
            pathinfo = """"""
            error_count = 0
            log_path = get_path_log(norm_path(path))
            if check_path_log(log_path):
                while True:
                    answer = input()
                    if answer not in {"y", "n"}:
                        break
                # while ((ans := input("Do you want to replace the file that already exist? (Y/n): ").lower()) not in ['y', 'n']):
                #     pass
                if answer == "n":
                    log_path = edit_path_log(log_path)
            path = Path(path)
            PathProperties.set_smallestindex(path)
            set_pathinfo(path, depth,condition_unit)
            set_title(path, size)
            write_log(log_path)
            print(f"[INFO]: Error count for path: {str(path)}: {error_count} error(s)")
    except FileExistsError as e:
        print(e)
        
