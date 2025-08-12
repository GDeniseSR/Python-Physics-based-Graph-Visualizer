from Vector2 import Vector2

class Node[T]:
    def __init__(self, value:T, x, y) -> None:
        self.__value = value
        self.x = x
        self.y = y
    
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x):
        self.__x = x
    
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, y):
        self.__y = y
    
    @property
    def value(self) -> T:
        return self.__value
    @value.setter
    def value(self, val:T):
        self.__value = val
    
    @property
    def pos(self):
        return Vector2(self.x, self.y)
    @pos.setter
    def pos(self, pos : Vector2):
        self.x = pos.x
        self.y = pos.y
    
    def __eq__(self, other: object) -> bool:
        if type(other) is Node:
            return self.value == other.value
        else:
            return self.value == other
        
    def __hash__(self) -> int:
        return hash((self.value))
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"{self.value}"