from abc import ABC, abstractmethod


# Subject interface
class Image(ABC):
    @abstractmethod
    def display(self) -> None:
        pass


# Real Subject
class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load()

    def _load(self) -> None:
        print(f"LoadingImage '{self._filename}' from disk...")

    def display(self) -> None:
        print(f"Displaying '{self._filename}'")


# Proxy
class ProxyImage():
    def __init__(self, filename: str):
        self._filename   = filename
        self._real_image = None  # not loaded yet

    def display(self) -> None:
        if self._real_image is None:
            print(f"[Proxy] First access — initializing real image")
            self._real_image = RealImage(self._filename)
        else:
            print(f"[Proxy] Returning cached image")
        self._real_image.display()


# Example usage
if __name__ == "__main__":
    image = ProxyImage("photo.jpg")

    print("-- First call --")
    image.display()

    print("\n-- Second call --")
    image.display()

    print("\n-- Third call --")
    image.display()