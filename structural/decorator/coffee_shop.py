from abc import ABC, abstractmethod


# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


# Concrete Component
class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 1.00

    def description(self) -> str:
        return "Simple coffee"


# Base Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25

    def description(self) -> str:
        return self._coffee.description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.10

    def description(self) -> str:
        return self._coffee.description() + ", sugar"


class WhipDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

    def description(self) -> str:
        return self._coffee.description() + ", whipped cream"


# Example usage
if __name__ == "__main__":
    coffee = SimpleCoffee()
    print(f"{coffee.description():<40} ${coffee.cost():.2f}")

    coffee = MilkDecorator(coffee)
    print(f"{coffee.description():<40} ${coffee.cost():.2f}")

    coffee = SugarDecorator(coffee)
    print(f"{coffee.description():<40} ${coffee.cost():.2f}")

    coffee = WhipDecorator(coffee)
    print(f"{coffee.description():<40} ${coffee.cost():.2f}")

    print()
    fancy = WhipDecorator(MilkDecorator(MilkDecorator(SimpleCoffee())))
    print(f"{fancy.description():<40} ${fancy.cost():.2f}")
    