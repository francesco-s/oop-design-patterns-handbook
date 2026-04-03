from abc import ABC, abstractmethod


# Implementor interface
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, radius: float) -> None:
        pass

    @abstractmethod
    def render_square(self, side: float) -> None:
        pass


# Concrete Implementors
class VectorRenderer(Renderer):
    def render_circle(self, radius: float) -> None:
        print(f"Drawing circle with radius {radius} as vector")

    def render_square(self, side: float) -> None:
        print(f"Drawing square with side {side} as vector")


class RasterRenderer(Renderer):
    def render_circle(self, radius: float) -> None:
        print(f"Drawing circle with radius {radius} as raster (pixels)")

    def render_square(self, side: float) -> None:
        print(f"Drawing square with side {side} as raster (pixels)")


# Abstraction
class Shape(ABC):
    def __init_Circle_(self, renderer: Renderer):
        self._renderer = renderer

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def resize(self, factor: float) -> None:
        pass


# Refined Abstractions
class Circle(Shape):
    def __init__(self, renderer: Renderer, radius: float):
        super().__init__(renderer)
        self._radius = radius

    def draw(self) -> None:
        self._renderer.render_circle(self._radius)

    def resize(self, factor: float) -> None:
        self._radius *= factor


class Square(Shape):
    def __init__(self, renderer: Renderer, side: float):
        super().__init__(renderer)
        self._side = side

    def draw(self) -> None:
        self._renderer.render_square(self._side)

    def resize(self, factor: float) -> None:
        self._side *= factor


# Example usage
if __name__ == "__main__":
    vector = VectorRenderer()
    raster = RasterRenderer()

    print("-- Vector rendering --")
    Circle(vector, 5).draw()
    Square(vector, 4).draw()

    print("\n-- Raster rendering --")
    Circle(raster, 5).draw()
    Square(raster, 4).draw()

    print("\n-- Resize then draw --")
    c = Circle(vector, 5)
    c.draw()
    c.resize(2)
    c.draw()
