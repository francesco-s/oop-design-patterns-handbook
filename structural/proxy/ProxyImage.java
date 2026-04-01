// Subject interface
interface Image {
    void display();
}


// Real Subject
class RealImage implements Image {
    private final String filename;

    public RealImage(String filename) {
        this.filename = filename;
        load();
    }

    private void load() {
        System.out.println("Loading '" + filename + "' from disk...");
    }

    @Override
    public void display() {
        System.out.println("Displaying '" + filename + "'");
    }
}


// Proxy
public class ProxyImage implements Image {
    private final String filename;
    private RealImage realImage = null;  // not loaded yet

    public ProxyImage(String filename) {
        this.filename = filename;
    }

    @Override
    public void display() {
        if (realImage == null) {
            System.out.println("[Proxy] First access — initializing real image");
            realImage = new RealImage(filename);
        } else {
            System.out.println("[Proxy] Returning cached image");
        }
        realImage.display();
    }

    public static void main(String[] args) {
        Image image = new ProxyImage("photo.jpg");

        System.out.println("-- First call --");
        image.display();

        System.out.println("\n-- Second call --");
        image.display();

        System.out.println("\n-- Third call --");
        image.display();
    }
}