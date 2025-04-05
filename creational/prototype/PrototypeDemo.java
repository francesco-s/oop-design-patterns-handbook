package creational.prototype;

import java.util.HashMap;
import java.util.Map;

// Prototype interface
interface Prototype {
    Prototype clone();
}

// Concrete prototype
abstract class Shape implements Prototype, Cloneable {
    private String id;
    private String type;
    
    public Shape() {
    }
    
    public Shape(String id, String type) {
        this.id = id;
        this.type = type;
    }
    
    public String getId() {
        return id;
    }
    
    public String getType() {
        return type;
    }
    
    @Override
    public Prototype clone() {
        try {
            return (Prototype) super.clone();
        } catch (CloneNotSupportedException e) {
            return null;
        }
    }
    
    @Override
    public String toString() {
        return type + " with ID: " + id;
    }
}

class Circle extends Shape {
    private int radius;
    
    public Circle() {
    }
    
    public Circle(String id, int radius) {
        super(id, "Circle");
        this.radius = radius;
    }
    
    public void setRadius(int radius) {
        this.radius = radius;
    }
    
    public int getRadius() {
        return radius;
    }
    
    @Override
    public String toString() {
        return super.toString() + ", radius: " + radius;
    }
}

class Rectangle extends Shape {
    private int width;
    private int height;
    
    public Rectangle() {
    }
    
    public Rectangle(String id, int width, int height) {
        super(id, "Rectangle");
        this.width = width;
        this.height = height;
    }
    
    public void setWidth(int width) {
        this.width = width;
    }
    
    public int getWidth() {
        return width;
    }
    
    public void setHeight(int height) {
        this.height = height;
    }
    
    public int getHeight() {
        return height;
    }
    
    @Override
    public String toString() {
        return super.toString() + ", width: " + width + ", height: " + height;
    }
}

// Prototype registry
class ShapeCache {
    private static Map<String, Shape> shapeMap = new HashMap<>();
    
    public static Shape getShape(String id) {
        Shape cachedShape = shapeMap.get(id);
        return (Shape) cachedShape.clone();
    }
    
    public static void loadCache() {
        Circle circle = new Circle("circle-1", 10);
        Rectangle rectangle = new Rectangle("rectangle-1", 20, 30);
        
        shapeMap.put(circle.getId(), circle);
        shapeMap.put(rectangle.getId(), rectangle);
    }
}

public class PrototypeDemo {
    public static void main(String[] args) {
        // Load predefined shapes to the cache
        ShapeCache.loadCache();
        
        // Clone the circle
        Circle clonedCircle = (Circle) ShapeCache.getShape("circle-1");
        System.out.println("Original: " + ShapeCache.getShape("circle-1"));
        System.out.println("Cloned: " + clonedCircle);
        
        // Change the cloned object - this won't affect the original
        clonedCircle.setRadius(15);
        System.out.println("Modified clone: " + clonedCircle);
        System.out.println("Original is unaffected: " + ShapeCache.getShape("circle-1"));
        
        // Clone and modify a rectangle
        Rectangle clonedRectangle = (Rectangle) ShapeCache.getShape("rectangle-1");
        clonedRectangle.setWidth(50);
        System.out.println("Original rectangle: " + ShapeCache.getShape("rectangle-1"));
        System.out.println("Modified rectangle clone: " + clonedRectangle);
    }
}