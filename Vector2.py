from math import sqrt, cos, sin, degrees, radians, atan2
import numbers

class Vector2:
    def __init__(self, x:float=0, y:float=0) -> None:        
        self.__x = x
        self.__y = y
    
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
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)
    def dot(self, other:'Vector2') -> 'Vector2':
        return self.x * other.x + self.y * other.y
    def rotated(self, angle:float):
        angle = radians(angle)
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        return Vector2(x, y)
    
    def rotate(self, angle):
        self = Vector2(*self.rotated(angle))

    @property
    def angle(self) -> float:
        return degrees(atan2(self.x, self.y))
    

    @property
    def right(self):
        return Vector2(-self.y, self.x)
    @property
    def left(self):
        return Vector2(self.y, -self.x)
    @property
    def up(self):
        return Vector2(self.x, self.y)
    @property
    def down(self):
        return Vector2(-self.x, -self.y)
    
    def clamp_magnitude(self, n_max) -> 'Vector2':
        n = self.magnitude
        if n > 0:
            f = min(1, n_max / n)
            self *= f
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def __add__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise(TypeError("unsupported operand type(s)"))
    def __iadd__(self, other) -> 'Vector2':
        return self.__add__(other)
    
    def __mul__(self, other) -> 'Vector2':
        if isinstance(other, numbers.Number):
            return Vector2(self.x * other, self.y * other)
        else:
            raise(TypeError("unsupported operand type(s)"))
    def __rmul__(self, other) -> 'Vector2':
        return self.__mul__(other)
    def __imul__(self, other) -> 'Vector2':
        return self.__mul__(other)

    def __truediv__(self, other) -> 'Vector2':
        if isinstance(other, numbers.Number):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError("unsupported operand type(s)")

    def __itruediv__(self, other) -> 'Vector2':
        return self.__truediv__(other)
    
    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)
    def __pos__(self) -> 'Vector2':
        return Vector2(self.x, self.y)
    
    def __sub__(self, other) -> 'Vector2':
        return self.__add__(-other)
    def __isub__(self, other):
        return self.__sub__(other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.magnitude > other.magnitude
    def __ge__(self, other):
        return self.magnitude >= other.magnitude
    
    def __lt__(self, other):
        return self.magnitude < other.magnitude
    def __le__(self, other):
        return self.magnitude <= other.magnitude
    
    def __iter__(self):
        return iter((self.x, self.y))

Vector2.ONE = Vector2(1, 1)
Vector2.ZERO = Vector2(0, 0)
Vector2.RIGHT = Vector2(1, 0)
Vector2.LEFT = Vector2(-1, 0)
Vector2.UP = Vector2(0, 1)
Vector2.DOWN = Vector2(0, -1)