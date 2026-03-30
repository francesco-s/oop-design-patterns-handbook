from abc import ABC, abstractmethod
from typing import Optional


# Handler interface
class SupportHandler(ABC):
    def __init__(self):
        self._next: Optional["SupportHandler"] = None

    def set_next(self, handler: "SupportHandler") -> "SupportHandler":
        self._next = handler
        return handler  # allows chaining: a.set_next(b).set_next(c)

    @abstractmethod
    def handle(self, level: int, issue: str) -> None:
        pass

    def pass_to_next(self, level: int, issue: str) -> None:
        if self._next:
            self._next.handle(level, issue)
        else:
            print(f"Issue '{issue}' could not be resolved")


# Concrete Handlers
class BasicSupport(SupportHandler):
    def handle(self, level: int, issue: str) -> None:
        if level == 1:
            print(f"[Basic Support]        Resolved: '{issue}'")
        else:
            print(f"[Basic Support]        Escalating: '{issue}'")
            self.pass_to_next(level, issue)


class IntermediateSupport(SupportHandler):
    def handle(self, level: int, issue: str) -> None:
        if level == 2:
            print(f"[Intermediate Support] Resolved: '{issue}'")
        else:
            print(f"[Intermediate Support] Escalating: '{issue}'")
            self.pass_to_next(level, issue)


class AdvancedSupport(SupportHandler):
    def handle(self, level: int, issue: str) -> None:
        if level == 3:
            print(f"[Advanced Support]     Resolved: '{issue}'")
        else:
            print(f"[Advanced Support]     Escalating: '{issue}'")
            self.pass_to_next(level, issue)


# Example usage
if __name__ == "__main__":
    basic        = BasicSupport()
    intermediate = IntermediateSupport()
    advanced     = AdvancedSupport()

    # Build the chain: basic → intermediate → advanced
    basic.set_next(intermediate).set_next(advanced)

    print("-- Ticket 1 (level 1) --")
    basic.handle(1, "Password reset")

    print("\n-- Ticket 2 (level 2) --")
    basic.handle(2, "Software installation failure")

    print("\n-- Ticket 3 (level 3) --")
    basic.handle(3, "Critical database corruption")

    print("\n-- Ticket 4 (level 4 - unhandled) --")
    basic.handle(4, "Unknown hardware malfunction")