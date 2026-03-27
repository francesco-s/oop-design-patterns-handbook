from abc import ABC, abstractmethod
from typing import Any


# Iterator interface
class Iterator(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Any:
        pass


# Iterable interface
class IterableCollection(ABC):
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass


# Concrete Iterator
class BookIterator(Iterator):
    def __init__(self, books: list):
        self._books = books
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._books)

    def next(self) -> str:
        book = self._books[self._index]
        self._index += 1
        return book


# Concrete Collection
class BookCollection(IterableCollection):
    def __init__(self):
        self._books: list = []

    def add_book(self, book: str) -> None:
        self._books.append(book)

    def create_iterator(self) -> Iterator:
        return BookIterator(self._books)


# Example usage
if __name__ == "__main__":
    library = BookCollection()
    library.add_book("The Pragmatic Programmer")
    library.add_book("Clean Code")
    library.add_book("Design Patterns")
    library.add_book("Refactoring")

    iterator = library.create_iterator()

    print("Books in library:")
    while iterator.has_next():
        print(f"  - {iterator.next()}")