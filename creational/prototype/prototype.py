import copy
from abc import ABC, abstractmethod

class Prototype(ABC):
    """Base prototype interface"""
    @abstractmethod
    def clone(self):
        pass

class Shape(Prototype):
    def __init__(self, id=None, type=None):
        self.id = id
        self.type = type
    
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"{self.type} with ID: {self.id}"

class Circle(Shape):
    def __init__(self, id=None, radius=0):
        super().__init__(id, "Circle")
        self.radius = radius
    
    def __str__(self):
        return f"{super().__str__()}, radius: {self.radius}"

class Rectangle(Shape):
    def __init__(self, id=None, width=0, height=0):
        super().__init__(id, "Rectangle")
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"{super().__str__()}, width: {self.width}, height: {self.height}"

class ShapeCache:
    """Prototype registry"""
    _cache = {}
    
    @staticmethod
    def get_shape(id):
        shape = ShapeCache._cache.get(id)
        return shape.clone() if shape else None
    
    @staticmethod
    def load():
        circle = Circle("circle-1", 10)
        rectangle = Rectangle("rectangle-1", 20, 30)
        
        ShapeCache._cache[circle.id] = circle
        ShapeCache._cache[rectangle.id] = rectangle

if __name__ == "__main__":
    # Load predefined shapes to the cache
    ShapeCache.load()
    
    # Clone the circle
    cloned_circle = ShapeCache.get_shape("circle-1")
    print(f"Original: {ShapeCache._cache['circle-1']}")
    print(f"Cloned: {cloned_circle}")
    
    # Change the cloned object - this won't affect the original
    cloned_circle.radius = 15
    print(f"Modified clone: {cloned_circle}")
    print(f"Original is unaffected: {ShapeCache._cache['circle-1']}")
    
    # Clone and modify a rectangle
    cloned_rectangle = ShapeCache.get_shape("rectangle-1")
    cloned_rectangle.width = 50
    print(f"Original rectangle: {ShapeCache._cache['rectangle-1']}")
    print(f"Modified rectangle clone: {cloned_rectangle}")