import java.util.ArrayList;
import java.util.List;


// Iterator interface
interface Iterator<T> {
    boolean hasNext();
    T next();
}


// Iterable interface
interface IterableCollection<T> {
    Iterator<T> createIterator();
}


// Concrete Iterator
class BookIterator implements Iterator<String> {
    private final List<String> books;
    private int index = 0;

    public BookIterator(List<String> books) {
        this.books = books;
    }

    @Override
    public boolean hasNext() {
        return index < books.size();
    }

    @Override
    public String next() {
        return books.get(index++);
    }
}


// Concrete Collection
public class BookCollection implements IterableCollection<String> {
    private final List<String> books = new ArrayList<>();

    public void addBook(String book) {
        books.add(book);
    }

    @Override
    public Iterator<String> createIterator() {
        return new BookIterator(books);
    }

    public static void main(String[] args) {
        BookCollection library = new BookCollection();
        library.addBook("The Pragmatic Programmer");
        library.addBook("Clean Code");
        library.addBook("Design Patterns");
        library.addBook("Refactoring");

        Iterator<String> iterator = library.createIterator();

        System.out.println("Books in library:");
        while (iterator.hasNext()) {
            System.out.println("  - " + iterator.next());
        }
    }
}