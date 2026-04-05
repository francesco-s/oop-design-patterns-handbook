import java.util.ArrayDeque;
import java.util.Deque;


// Memento — stores a snapshot of the editor's state
class Memento {
    private final String content;

    public Memento(String content) {
        this.content = content;
    }

    public String getContent() { return content; }
}


// Originator — creates and restores mementos
public class TextEditor {
    private String content = "";

    public void type(String text)        { content += text; }
    public String getContent()           { return content; }
    public Memento save()                { return new Memento(content); }
    public void restore(Memento memento) { content = memento.getContent(); }

    public static void main(String[] args) {
        TextEditor editor  = new TextEditor();
        History    history = new History();

        editor.type("Hello");
        history.push(editor.save());
        System.out.println("After typing  : '" + editor.getContent() + "'");

        editor.type(", World");
        history.push(editor.save());
        System.out.println("After typing  : '" + editor.getContent() + "'");

        editor.type("!!!");
        System.out.println("After typing  : '" + editor.getContent() + "'");

        System.out.println("\n-- Undo --");
        Memento snapshot = history.pop();
        if (snapshot != null) editor.restore(snapshot);
        System.out.println("After undo    : '" + editor.getContent() + "'");

        System.out.println("\n-- Undo again --");
        snapshot = history.pop();
        if (snapshot != null) editor.restore(snapshot);
        System.out.println("After undo    : '" + editor.getContent() + "'");
    }
}


// Caretaker — manages the memento history
class History {
    private final Deque<Memento> snapshots = new ArrayDeque<>();

    public void push(Memento memento) { snapshots.push(memento); }

    public Memento pop() {
        if (!snapshots.isEmpty()) return snapshots.pop();
        System.out.println("Nothing to undo");
        return null;
    }
}