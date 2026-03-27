from abc import ABC, abstractmethod
from typing import List


# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


# Receiver
class Light:
    def __init__(self, location: str):
        self.location = location
        self._is_on = False

    def turn_on(self) -> None:
        self._is_on = True
        print(f"{self.location} light turned ON")

    def turn_off(self) -> None:
        self._is_on = False
        print(f"{self.location} light turned OFF")


# Concrete Commands
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()


class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()

    def undo(self) -> None:
        self._light.turn_on()


# Invoker
class RemoteControl:
    def __init__(self):
        self._history: List[Command] = []

    def press(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def press_undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
        else:
            print("Nothing to undo")


# Example usage
if __name__ == "__main__":
    remote = RemoteControl()

    living_room = Light("Living room")
    bedroom = Light("Bedroom")

    remote.press(TurnOnCommand(living_room))
    remote.press(TurnOnCommand(bedroom))
    remote.press(TurnOffCommand(living_room))

    print("\n-- Undo last 2 commands --")
    remote.press_undo()
    remote.press_undo()