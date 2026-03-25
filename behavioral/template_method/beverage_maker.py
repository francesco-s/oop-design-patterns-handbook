from abc import ABC, abstractmethod


# Abstract class with the template method
class BeverageMaker(ABC):

    # Template method — defines the fixed algorithm skeleton
    def make_beverage(self) -> None:
        self._boil_water()
        self._brew()
        self._pour_in_cup()
        self._add_condiments()

    # Common steps (shared implementation)
    def _boil_water(self) -> None:
        print("Boiling water")

    def _pour_in_cup(self) -> None:
        print("Pouring into cup")

    # Variable steps — subclasses must implement these
    @abstractmethod
    def _brew(self) -> None:
        pass

    @abstractmethod
    def _add_condiments(self) -> None:
        pass


# Concrete subclasses
class TeaMaker(BeverageMaker):
    def _brew(self) -> None:
        print("Steeping the tea")

    def _add_condiments(self) -> None:
        print("Adding lemon")


class CoffeeMaker(BeverageMaker):
    def _brew(self) -> None:
        print("Dripping coffee through filter")

    def _add_condiments(self) -> None:
        print("Adding sugar and milk")


# Example usage
if __name__ == "__main__":
    tea = TeaMaker()
    print("Making tea:")
    tea.make_beverage()

    print()

    coffee = CoffeeMaker()
    print("Making coffee:")
    coffee.make_beverage()