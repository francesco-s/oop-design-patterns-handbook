from abc import ABC, abstractmethod
from typing import List


# Component interface
class FileSystemItem(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass


# Leaf
class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def size(self) -> int:
        return self._size

    def display(self, indent: str = "") -> None:
        print(f"{indent}- {self.name} ({self._size} KB)")


# Composite
class Folder(FileSystemItem):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> None:
        self._children.append(item)

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def size(self) -> int:
        return sum(child.size() for child in self._children)

    def display(self, indent: str = "") -> None:
        print(f"{indent}|- {self.name} ({self.size()} KB)")
        for child in self._children:
            child.display(indent + "   ")


# Example usage
if __name__ == "__main__":
    file1 = File("resume.pdf",   120)
    file2 = File("photo.jpg",    340)
    file3 = File("notes.txt",     18)
    file4 = File("project.zip", 2048)
    file5 = File("budget.xlsx",   95)

    documents = Folder("Documents")
    documents.add(file1)
    documents.add(file3)

    pictures = Folder("Pictures")
    pictures.add(file2)

    work = Folder("Work")
    work.add(file4)
    work.add(file5)

    root = Folder("Root")
    root.add(documents)
    root.add(pictures)
    root.add(work)

    root.display()
    print(f"\nTotal size: {root.size()} KB")
