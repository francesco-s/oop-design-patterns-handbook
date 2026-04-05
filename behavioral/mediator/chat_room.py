from abc import ABC, abstractmethod
from typing import List


# Mediator interface
class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: "User") -> None:
        pass

    @abstractmethod
    def add_user(self, user: "User") -> None:
        pass


# Colleague
class User:
    def __init__(self, name: str, mediator: ChatMediator):
        self.name     = name
        self._mediator = mediator
        self._mediator.add_user(self)

    def send(self, message: str) -> None:
        print(f"[{self.name}] sends: '{message}'")
        self._mediator.send_message(message, self)

    def receive(self, message: str, sender: "User") -> None:
        print(f"[{self.name}] received from [{sender.name}]: '{message}'")


# Concrete Mediator
class ChatRoom(ChatMediator):
    def __init__(self):
        self._users: List[User] = []

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def send_message(self, message: str, sender: User) -> None:
        for user in self._users:
            if user is not sender:
                user.receive(message, sender)


# Example usage
if __name__ == "__main__":
    room = ChatRoom()

    alice   = User("Alice",   room)
    bob     = User("Bob",     room)
    charlie = User("Charlie", room)

    print("-- Alice sends a message --")
    alice.send("Hello everyone!")

    print("\n-- Bob sends a message --")
    bob.send("Hey Alice!")
