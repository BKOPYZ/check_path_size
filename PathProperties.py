from enum import Enum

class PathUnit(Enum):
    KILO = 0
    MEGA = 1
    GIGA = 2

class PathType(Enum):
    FILE =0
    DIRECTORY = 1 
    UNKNOWN =2

class PathProperties:

    smallestindex = None;
    # next time will do the file and folder count the check the similarity next time
    def __init__(self, path: str, size , pathunit: PathUnit, pathtype: PathType = PathType.UNKNOWN ):
        self.__path = path
        self.__name = self.__set_name(path)
        self.__size = size
        self.parent = False # change later
        self.child = False # change later
        self.has_child = False # change later
        self.pos = self.__get_pos()
        self.type = pathtype
        self.unit = pathunit
        
    def __call__(self) -> str:
        spacebet = 95
        spacefront = "\t" * self.pos + "|-"
 
        return  f"{spacefront}{self.get_name():<{spacebet}} {self.get_size():.2f} MB\n"

    def get_name(self) -> str:
        return self.__name
    
    def get_size(self) -> float:
        return self.__size
    
    def get_path(self) -> str:
        return self.__path
    
    def __set_name(self, path:str) -> str:
        splited_file = str(path).split("\\")
        name = splited_file[-1] if not splited_file[-1].isspace() else splited_file[-2]
        return name
    
    def __get_pos(self) -> int:
        return len(str(self.get_path()).split("\\")) - self.smallestindex
    
    @classmethod
    def set_smallestindex(cls,path: str):
        cls.smallestindex = len(path.split('\\'))
       
    
    
    
    

        
