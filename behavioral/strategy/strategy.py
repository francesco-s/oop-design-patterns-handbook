# State vs Strategy
# They look structurally identical but differ in intent:
#     Strategy — the context never changes strategy on its own; the client swaps it from outside
#     State — states transition themselves by calling machine.set_state(...) internally, forming a self-driving state machine

from abc import ABC, abstractmethod


# Strategy interface
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass


# Concrete Strategies
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left   = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right  = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class ReverseSortStrategy(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, reverse=True)


# Context
class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)


# Example usage
if __name__ == "__main__":
    data = [5, 2, 8, 1, 9, 3]

    sorter = Sorter(BubbleSortStrategy())
    print(f"Original:    {data}")
    print(f"BubbleSort:  {sorter.sort(data)}")

    sorter.set_strategy(QuickSortStrategy())
    print(f"QuickSort:   {sorter.sort(data)}")

    sorter.set_strategy(ReverseSortStrategy())
    print(f"ReverseSort: {sorter.sort(data)}")