from abc import ABC, abstractmethod


# Visitor interface
class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: "Circle") -> None:
        pass

    @abstractmethod
    def visit_rectangle(self, rectangle: "Rectangle") -> None:
        pass

    @abstractmethod
    def visit_triangle(self, triangle: "Triangle") -> None:
        pass


# Element interface
class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> None:
        pass


# Concrete Elements
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_circle(self)


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_rectangle(self)


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base   = base
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_triangle(self)


# Concrete Visitors
class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> None:
        print(f"Circle area        : {3.14159 * circle.radius ** 2:.2f}")

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        print(f"Rectangle area     : {rectangle.width * rectangle.height:.2f}")

    def visit_triangle(self, triangle: Triangle) -> None:
        print(f"Triangle area      : {0.5 * triangle.base * triangle.height:.2f}")


class PerimeterCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> None:
        print(f"Circle perimeter   : {2 * 3.14159 * circle.radius:.2f}")

    def visit_rectangle(self, rectangle: Rectangle) -> None:
        print(f"Rectangle perimeter: {2 * (rectangle.width + rectangle.height):.2f}")

    def visit_triangle(self, triangle: Triangle) -> None:
        print(f"Triangle perimeter : requires all 3 sides")


# Example usage
if __name__ == "__main__":
    shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

    print("-- Area --")
    area_calc = AreaCalculator()
    for shape in shapes:
        shape.accept(area_calc)

    print("\n-- Perimeter --")
    perimeter_calc = PerimeterCalculator()
    for shape in shapes:
        shape.accept(perimeter_calc)

