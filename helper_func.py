from pathlib import Path
import os
from typing import List,Tuple, Dict
from FileProperties import FileProperties
from tqdm import tqdm
from timeit import Timer

#--------------------------------------------------
BYTE_TO_MEGABYTE = 1.0/(1024 * 1024)
CONFIG_PATH = "config.txt"



#--------------------------------------------------
def set_pathinfo(paths: Path) -> None:
    filepath = Path(paths)
    # Check if the path valid (is file or directory)
    if not filepath.exists():
        raise OSError("file or directory not exist. Please check the path again")
    
    allfilepath = list(filepath.glob("*"))
    for pathfile in tqdm(allfilepath):
        if add_pathinfo(pathfile=pathfile):
            continue
        set_pathinfo(pathfile)



def add_pathinfo(pathfile:str) -> bool:
    fileprop = get_file(path=pathfile)
    global pathinfo
    pathinfo += fileprop()
    if os.path.isdir(pathfile):
        return False
    return True

def add_title(pathfile: str, size: float) -> None:
    fileTitle = FileProperties(pathfile,size)
    global pathinfo
    pathinfo = fileTitle() + pathinfo
    


def get_file(path: Path) -> FileProperties:
    """
    """
    if Path(path).is_dir():
        return FileProperties(path, 0)
    size_of_file = os.path.getsize(path) * BYTE_TO_MEGABYTE
    global size
    size += size_of_file
    return FileProperties(path, size_of_file)



def write_log() -> None:
    with open("log.txt" , 'w' , encoding="utf-8") as f:
        f.write(pathinfo)



def run() -> None:
    
    with open(CONFIG_PATH, 'r') as config:
        lines = config.read().splitlines()
        if not len(lines):
            raise ValueError("ERROR")
        path_to_check = lines[0]
    global size
    size = 0
    FileProperties.set_smallestindex(path_to_check)
    global pathinfo
    pathinfo = """"""
    set_pathinfo(path_to_check)
    add_title(path_to_check,size)
    write_log()
    
    





    
        
