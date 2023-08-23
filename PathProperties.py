from enum import Enum
from math import floor

#TODO: fix the bug that happen from assigning the pathunit and convert the size before calculate the size of the directory

class PathUnit(Enum):
    BYTE = 3
    KILO = 2
    MEGA = 1
    GIGA = 0
    

class PathType(Enum):
    FILE =0
    DIRECTORY = 1 
    TITLE =2

class PathProperties:
    BYTE_TO_KILOBYTE = 1.0/1024
    BYTE_TO_MEGABYTE = 1.0/(1024 ** 2)
    BYTE_TO_GIGABYTE = 1.0/(1024 ** 3)
    smallestindex = None;
    # next time will do the file and folder count the check the similarity next time
    def __init__(self, path: str, size: float, pathtype: PathType = PathType.TITLE):
        self.unit = PathUnit.BYTE
        self.type = pathtype
        self.pos = self.__set_pos(path)
        self.__path = path
        self.__uncalculated_size = size
        self.__name = self.__set_name(path)
        self.__size = self.__set_size(size)
        
        
    def __call__(self) -> str:
        spacebet = 95 + 3-len(str(floor(self.get_size())))
        spacefront = "\t" * self.pos + ("┗╸" if self.type == PathType.TITLE else "┣╸" )
        suffix = self.suffix_ended()
        return  f"{spacefront}{self.get_name():<{spacebet}} {self.get_size():.2f} {suffix}\n"

    def suffix_ended(self)->str:
        match self.unit:
            case PathUnit.KILO:
                return "KB"
            case PathUnit.MEGA:
                return "MB"
            case PathUnit.GIGA:
                return "GB"
            case PathUnit.BYTE:
                return "B"

    def get_name(self) -> str:
        return self.__name
    
    def get_size(self) -> float:
        return self.__size
    
    def get_uncalculated_size(self)->float:
        return self.__uncalculated_size
    
    def get_path(self) -> str:
        return self.__path
    
    def __set_name(self, path:str) -> str:
        splited_file = str(path).split("\\")
        name = splited_file[-1] if not splited_file[-1].isspace() else splited_file[-2]
        if len(name) >= 20:
            name = name[:20] + "..."
        return name
    
    def __set_size(self, size: float) -> float:
        if size > 1000000000 : 
            self.unit = PathUnit.GIGA
            return size * PathProperties.BYTE_TO_GIGABYTE
        elif size > 1000000:
            self.unit = PathUnit.MEGA
            return size * PathProperties.BYTE_TO_MEGABYTE
        elif size > 1000:
            self.unit = PathUnit.KILO
            return size * PathProperties.BYTE_TO_KILOBYTE
        else:
            return size 
        
    def __set_pos(self, path: str) -> int:
        return len(str(path).split("\\")) - self.smallestindex
     
    @classmethod
    def set_smallestindex(cls,path: str):
        cls.smallestindex = len(path.split('\\'))
       
    
    
    
    

        
