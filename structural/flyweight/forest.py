from dataclasses import dataclass
from typing import Dict, List, Tuple


# Flyweight — stores shared (intrinsic) state
@dataclass(frozen=True)
class TreeType:
    name: str
    color: str
    texture: str

    def draw(self, x: int, y: int) -> None:
        print(f"Drawing '{self.name}' tree [{self.color}, {self.texture}] at ({x}, {y})")


# Flyweight Factory — caches and reuses TreeType instances
class TreeTypeFactory:
    _cache: Dict[Tuple, TreeType] = {}

    @classmethod
    def get(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._cache:
            cls._cache[key] = TreeType(name, color, texture)
            print(f"  [Factory] Created new TreeType: '{name}'")
        return cls._cache[key]

    @classmethod
    def count(cls) -> int:
        return len(cls._cache)


# Context — stores unique (extrinsic) state + reference to flyweight
@dataclass
class Tree:
    x: int
    y: int
    tree_type: TreeType

    def draw(self) -> None:
        self.tree_type.draw(self.x, self.y)


# Client
class Forest:
    def __init__(self):
        self._trees: List[Tree] = []

    def plant(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        tree_type = TreeTypeFactory.get(name, color, texture)
        self._trees.append(Tree(x, y, tree_type))

    def draw(self) -> None:
        for tree in self._trees:
            tree.draw()


# Example usage
if __name__ == "__main__":
    forest = Forest()

    print("-- Planting trees --")
    forest.plant(1,  2,  "Oak",   "dark green",   "rough")
    forest.plant(5,  8,  "Oak",   "dark green",   "rough")
    forest.plant(12, 3,  "Pine",  "bright green", "smooth")
    forest.plant(7,  15, "Oak",   "dark green",   "rough")
    forest.plant(9,  1,  "Pine",  "bright green", "smooth")
    forest.plant(3,  11, "Birch", "white",        "papery")

    print("\n-- Drawing forest --")
    forest.draw()

    print(f"\nTrees planted          : {len(forest._trees)}")
    print(f"TreeType objects (shared): {TreeTypeFactory.count()}")
