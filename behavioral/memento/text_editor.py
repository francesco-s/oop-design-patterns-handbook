from __future__ import annotations
from dataclasses import dataclass
from typing import List


# Memento — stores a snapshot of the editor's state
@dataclass(frozen=True)
class Memento:
    content: str


# Originator — creates and restores mementos
class TextEditor:
    def __init__(self):
        self._content: str = ""

    def type(self, text: str) -> None:
        self._content += text

    def get_content(self) -> str:
        return self._content

    def save(self) -> Memento:
        return Memento(self._content)

    def restore(self, memento: Memento) -> None:
        self._content = memento.content


# Caretaker — manages the memento history
class History:
    def __init__(self):
        self._snapshots: List[Memento] = []

    def push(self, memento: Memento) -> None:
        self._snapshots.append(memento)

    def pop(self) -> Memento | None:
        if self._snapshots:
            return self._snapshots.pop()
        print("Nothing to undo")
        return None


# Example usage
if __name__ == "__main__":
    editor  = TextEditor()
    history = History()

    editor.type("Hello")
    history.push(editor.save())
    print(f"After typing  : '{editor.get_content()}'")

    editor.type(", World")
    history.push(editor.save())
    print(f"After typing  : '{editor.get_content()}'")

    editor.type("!!!")
    print(f"After typing  : '{editor.get_content()}'")

    print("\n-- Undo --")
    snapshot = history.pop()
    if snapshot:
        editor.restore(snapshot)
    print(f"After undo    : '{editor.get_content()}'")

    print("\n-- Undo again --")
    snapshot = history.pop()
    if snapshot:
        editor.restore(snapshot)
    print(f"After undo    : '{editor.get_content()}'")
    