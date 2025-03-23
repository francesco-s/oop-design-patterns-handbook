from abc import ABC, abstractmethod
from typing import List

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

# Concrete Observer
class User(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"User {self.name} received: {message}")

# Subject (Observable)
class NewsPublisher:
    def __init__(self):
        self._observers: List[Observer] = []
        self._latest_news: str = ""
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self._latest_news)
    
    def publish_news(self, news: str) -> None:
        self._latest_news = news
        print(f"Publishing news: {news}")
        self.notify_observers()


# Example usage
if __name__ == "__main__":
    # Create publisher
    news_publisher = NewsPublisher()
    
    # Create subscribers
    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie")
    
    # Register subscribers
    news_publisher.attach(alice)
    news_publisher.attach(bob)
    news_publisher.attach(charlie)
    
    # Publish news
    news_publisher.publish_news("Python 3.11 released with major performance improvements!")
    
    # Unsubscribe Bob
    print("\nBob unsubscribed\n")
    news_publisher.detach(bob)
    
    # Publish another news
    news_publisher.publish_news("New design patterns book available!")