import java.util.ArrayList;
import java.util.List;


// Component interface
public abstract class FileSystemItem {
    protected final String name;

    public FileSystemItem(String name) {
        this.name = name;
    }

    public abstract int size();
    public abstract void display(String indent);

    public static void main(String[] args) {
        File file1 = new File("resume.pdf",   120);
        File file2 = new File("photo.jpg",    340);
        File file3 = new File("notes.txt",     18);
        File file4 = new File("project.zip", 2048);
        File file5 = new File("budget.xlsx",   95);

        Folder documents = new Folder("Documents");
        documents.add(file1);
        documents.add(file3);

        Folder pictures = new Folder("Pictures");
        pictures.add(file2);

        Folder work = new Folder("Work");
        work.add(file4);
        work.add(file5);

        Folder root = new Folder("Root");
        root.add(documents);
        root.add(pictures);
        root.add(work);

        root.display("");
        System.out.println("\nTotal size: " + root.size() + " KB");
    }
}


// Leaf
class File extends FileSystemItem {
    private final int fileSize;

    public File(String name, int fileSize) {
        super(name);
        this.fileSize = fileSize;
    }

    @Override
    public int size() { return fileSize; }

    @Override
    public void display(String indent) {
        System.out.println(indent + "- " + name + " (" + fileSize + " KB)");
    }
}


// Composite
class Folder extends FileSystemItem {
    private final List<FileSystemItem> children = new ArrayList<>();

    public Folder(String name) { super(name); }

    public void add(FileSystemItem item)    { children.add(item); }
    public void remove(FileSystemItem item) { children.remove(item); }

    @Override
    public int size() {
        return children.stream().mapToInt(FileSystemItem::size).sum();
    }

    @Override
    public void display(String indent) {
        System.out.println(indent + "|- " + name + " (" + size() + " KB)");
        for (FileSystemItem child : children) {
            child.display(indent + "   ");
        }
    }
}
