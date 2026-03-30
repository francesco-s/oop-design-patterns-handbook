from abc import ABC, abstractmethod


# State interface
class State(ABC):
    @abstractmethod
    def insert_coin(self, machine: "VendingMachine") -> None:
        pass

    @abstractmethod
    def press_button(self, machine: "VendingMachine") -> None:
        pass

    @abstractmethod
    def dispense(self, machine: "VendingMachine") -> None:
        pass


# Concrete States
class IdleState(State):
    def insert_coin(self, machine: "VendingMachine") -> None:
        print("Coin inserted")
        machine.set_state(machine.has_coin_state)

    def press_button(self, machine: "VendingMachine") -> None:
        print("Insert a coin first")

    def dispense(self, machine: "VendingMachine") -> None:
        print("Insert a coin first")


class HasCoinState(State):
    def insert_coin(self, machine: "VendingMachine") -> None:
        print("Coin already inserted")

    def press_button(self, machine: "VendingMachine") -> None:
        print("Button pressed")
        machine.set_state(machine.dispensing_state)

    def dispense(self, machine: "VendingMachine") -> None:
        print("Press the button first")


class DispensingState(State):
    def insert_coin(self, machine: "VendingMachine") -> None:
        print("Please wait, dispensing in progress")

    def press_button(self, machine: "VendingMachine") -> None:
        print("Already dispensing")

    def dispense(self, machine: "VendingMachine") -> None:
        if machine.count > 0:
            machine.count -= 1
            print("Item dispensed!")
        if machine.count == 0:
            print("Out of stock!")
            machine.set_state(machine.out_of_stock_state)
        else:
            machine.set_state(machine.idle_state)


class OutOfStockState(State):
    def insert_coin(self, machine: "VendingMachine") -> None:
        print("Machine is out of stock")

    def press_button(self, machine: "VendingMachine") -> None:
        print("Machine is out of stock")

    def dispense(self, machine: "VendingMachine") -> None:
        print("Machine is out of stock")


# Context
class VendingMachine:
    def __init__(self, count: int):
        self.idle_state         = IdleState()
        self.has_coin_state     = HasCoinState()
        self.dispensing_state   = DispensingState()
        self.out_of_stock_state = OutOfStockState()

        self.count = count
        self._state: State = self.idle_state if count > 0 else self.out_of_stock_state

    def set_state(self, state: State) -> None:
        self._state = state

    def insert_coin(self) -> None:
        self._state.insert_coin(self)

    def press_button(self) -> None:
        self._state.press_button(self)

    def dispense(self) -> None:
        self._state.dispense(self)


# Example usage
if __name__ == "__main__":
    machine = VendingMachine(count=2)

    print("-- Normal purchase --")
    machine.insert_coin()
    machine.press_button()
    machine.dispense()

    print("\n-- Invalid actions --")
    machine.press_button()
    machine.dispense()

    print("\n-- Last item --")
    machine.insert_coin()
    machine.press_button()
    machine.dispense()

    print("\n-- Out of stock --")
    machine.insert_coin()
    