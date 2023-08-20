from pathlib import Path
import os
from typing import List,Tuple, Dict

def get_all_file_path(path: Path) -> List:
    """
    Check if the path has child files/folder. Glob it and (append it to the list).
    Repeat until no more child.

    Param path: path of the file or folder

    Return list of string that contains all the path inside
    """
    all_file_path_list = []
    filepath = Path(path)
    
    # Check if the path valid (is file or directory)
    if not filepath.exists():
        raise OSError("file or directory not exist. Please check the path again")
    
    return all_file_path_list


def get_file_size(path: Path) -> Tuple:
    """
    """
    if os.path.isdir(path):
        return (path, "⇩");
    return (path,str(os.stat(path)))




    
        
