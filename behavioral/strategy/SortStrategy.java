// SortStrategy.java

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;


// Strategy interface
public interface SortStrategy {
    List<Integer> sort(List<Integer> data);

    static void main(String[] args) {
        List<Integer> data = Arrays.asList(5, 2, 8, 1, 9, 3);

        Sorter sorter = new Sorter(new BubbleSortStrategy());
        System.out.println("Original:    " + data);
        System.out.println("BubbleSort:  " + sorter.sort(data));

        sorter.setStrategy(new QuickSortStrategy());
        System.out.println("QuickSort:   " + sorter.sort(data));

        sorter.setStrategy(new ReverseSortStrategy());
        System.out.println("ReverseSort: " + sorter.sort(data));
    }
}


// Concrete Strategies
class BubbleSortStrategy implements SortStrategy {
    @Override
    public List<Integer> sort(List<Integer> data) {
        List<Integer> arr = new ArrayList<>(data);
        int n = arr.size();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr.get(j) > arr.get(j + 1)) {
                    int temp = arr.get(j);
                    arr.set(j, arr.get(j + 1));
                    arr.set(j + 1, temp);
                }
            }
        }
        return arr;
    }
}


class QuickSortStrategy implements SortStrategy {
    @Override
    public List<Integer> sort(List<Integer> data) {
        if (data.size() <= 1) return data;
        int pivot = data.get(data.size() / 2);
        List<Integer> left   = new ArrayList<>();
        List<Integer> middle = new ArrayList<>();
        List<Integer> right  = new ArrayList<>();
        for (int x : data) {
            if      (x < pivot) left.add(x);
            else if (x == pivot) middle.add(x);
            else                 right.add(x);
        }
        List<Integer> result = new ArrayList<>(sort(left));
        result.addAll(middle);
        result.addAll(sort(right));
        return result;
    }
}


class ReverseSortStrategy implements SortStrategy {
    @Override
    public List<Integer> sort(List<Integer> data) {
        List<Integer> arr = new ArrayList<>(data);
        arr.sort(Collections.reverseOrder());
        return arr;
    }
}


// Context
class Sorter {
    private SortStrategy strategy;

    public Sorter(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(SortStrategy strategy) {
        this.strategy = strategy;
    }

    public List<Integer> sort(List<Integer> data) {
        return strategy.sort(data);
    }
}