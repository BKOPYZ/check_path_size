from pathlib import Path
import os
from typing import List, Tuple, Dict
from PathProperties import PathProperties,PathType, PathUnit
from tqdm import tqdm
from timeit import Timer
from CustomError import InvalidUrlException

# --------------------------------------------------
BYTE_TO_MEGABYTE = 1.0/(1024 * 1024)
BYTE_TO_KILOBYTE = 1.0/1024
BYTE_TO_GEGABYTE = 1.0/(1024 ** 3)
CONFIG_PATH = "config.txt"

#TODO delete pos in set_pathinfo __add_pathinfo
# --------------------------------------------------
def set_pathinfo(path: Path, depth: int, ) -> None:
    pathfile = Path(path)
    # Check if the path valid (is file or directory)
    if not pathfile.exists():
        raise OSError(
            "file or directory not exist. Please check the path again")

    allfilepath = list(pathfile.glob("*"))
    for pathfile in tqdm(allfilepath):
        fileprop = __get_path_properties(pathfile, 0, depth)
        __add_pathinfo(fileprop)

def __get_directory_data(pathfile: Path, pos: int, depth: int) -> Tuple[List[PathProperties],int]:
    size = 0.0
    pathfile = Path(pathfile)
    path_properties_list:List[PathProperties] = []
    allfilepath = list(pathfile.glob("*"))
    for pathfile in tqdm(allfilepath):
        pathprop = __get_path_properties(pathfile,pos,depth)
        path_properties_list.extend(pathprop)
        size += pathprop[0].get_size() * BYTE_TO_MEGABYTE
    return (path_properties_list,size)

def __get_directory_size_depth_reach(pathfile: str)->float:
    size = 0.0
    pathfile = Path(pathfile)
    for path, dirs, files in os.walk(pathfile):
        for file in files:
            size += os.path.getsize(path/file) * BYTE_TO_MEGABYTE
    return size
        
def __add_pathinfo(pathPropertieslist: List[PathProperties])-> None:
    global pathinfo
    for path_object in pathPropertieslist:
        pathinfo += path_object()


def __get_path_properties(pathfile: Path, pos: int, depth: int) -> List[PathProperties]:
    """
    """
    global size
    if Path(pathfile).is_file():
        size_of_file = os.path.getsize(pathfile) * BYTE_TO_MEGABYTE
        size += size_of_file
        return [PathProperties(pathfile, size_of_file, PathUnit.MEGA, PathType.FILE)]
    elif pos < depth:
        path_properties_list, directory_size = __get_directory_data(pathfile,pos+1,depth)
        size += directory_size
        pathprop = [PathProperties(pathfile,directory_size, PathUnit.MEGA,PathType.DIRECTORY)]
        pathprop.extend(path_properties_list)
        return pathprop
    else:
        directory_size = __get_directory_size_depth_reach(pathfile)
        size += directory_size
        return [PathProperties(pathfile,directory_size, PathUnit.MEGA, PathType.DIRECTORY)]
        
def set_title(pathfile: str, size: float) -> None:
    fileTitle = PathProperties(pathfile, size,PathUnit.KILO,PathType.DIRECTORY)
    global pathinfo
    pathinfo = fileTitle() + pathinfo

def write_log() -> None:
    with open("log.txt", 'w', encoding="utf-8") as f:
        f.write(pathinfo)


def check_valid_path(path: str)-> bool:
    if os.path.exists(path):
        return True
    return False

def get_data_from_config(path: str = CONFIG_PATH) -> Tuple[str,int]:
    depth = 1000
    with open(CONFIG_PATH, 'r') as config:
        datas = config.read().splitlines()
        if not len(datas):
            raise ValueError("[ERROR]: Please specify the path for scanning")
        elif len(datas) == 1:
            if not check_valid_path:
                raise FileNotFoundError("[ERROR]: File or Directory not found")
            path_to_check = datas[0]
        else:     
            depth = datas[1]
    return (path_to_check, depth)        
    
    


def run() -> None:
    global size, pathinfo
    size = 0
    pathinfo = """"""
    try:
        path_to_check, depth = get_data_from_config()
        depth = int(depth)
        PathProperties.set_smallestindex(path_to_check)
        set_pathinfo(path_to_check,depth)
        set_title(path_to_check, size)
        write_log()
    except Exception as e:
        print(e)
        print(e.with_traceback())
        
    
    
    
