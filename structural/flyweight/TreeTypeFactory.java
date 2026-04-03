import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


// Flyweight — stores shared (intrinsic) state
class TreeType {
    private final String name;
    private final String color;
    private final String texture;

    public TreeType(String name, String color, String texture) {
        this.name    = name;
        this.color   = color;
        this.texture = texture;
    }

    public void draw(int x, int y) {
        System.out.println(
            "Drawing '" + name + "' tree [" + color + ", " + texture + "] at (" + x + ", " + y + ")"
        );
    }
}


// Flyweight Factory — caches and reuses TreeType instances
public class TreeTypeFactory {
    private static final Map<String, TreeType> cache = new HashMap<>();

    public static TreeType get(String name, String color, String texture) {
        String key = name + "-" + color + "-" + texture;
        if (!cache.containsKey(key)) {
            cache.put(key, new TreeType(name, color, texture));
            System.out.println("  [Factory] Created new TreeType: '" + name + "'");
        }
        return cache.get(key);
    }

    public static int count() { return cache.size(); }

    public static void main(String[] args) {
        Forest forest = new Forest();

        System.out.println("-- Planting trees --");
        forest.plant(1,  2,  "Oak",   "dark green",   "rough");
        forest.plant(5,  8,  "Oak",   "dark green",   "rough");
        forest.plant(12, 3,  "Pine",  "bright green", "smooth");
        forest.plant(7,  15, "Oak",   "dark green",   "rough");
        forest.plant(9,  1,  "Pine",  "bright green", "smooth");
        forest.plant(3,  11, "Birch", "white",        "papery");

        System.out.println("\n-- Drawing forest --");
        forest.draw();

        System.out.println("\nTrees planted            : " + forest.size());
        System.out.println("TreeType objects (shared): " + TreeTypeFactory.count());
    }
}


// Context — stores unique (extrinsic) state + reference to flyweight
class Tree {
    private final int x;
    private final int y;
    private final TreeType treeType;

    public Tree(int x, int y, TreeType treeType) {
        this.x        = x;
        this.y        = y;
        this.treeType = treeType;
    }

    public void draw() { treeType.draw(x, y); }
}


// Client
class Forest {
    private final List<Tree> trees = new ArrayList<>();

    public void plant(int x, int y, String name, String color, String texture) {
        TreeType treeType = TreeTypeFactory.get(name, color, texture);
        trees.add(new Tree(x, y, treeType));
    }

    public void draw() {
        for (Tree tree : trees) tree.draw();
    }

    public int size() { return trees.size(); }
}
