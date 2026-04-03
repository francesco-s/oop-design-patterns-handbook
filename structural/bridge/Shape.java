// Shape.java


// Implementor interface
interface Renderer {
    void renderCircle(double radius);
    void renderSquare(double side);
}


// Concrete Implementors
class VectorRenderer implements Renderer {
    @Override
    public void renderCircle(double radius) {
        System.out.println("Drawing circle with radius " + radius + " as vector");
    }

    @Override
    public void renderSquare(double side) {
        System.out.println("Drawing square with side " + side + " as vector");
    }
}


class RasterRenderer implements Renderer {
    @Override
    public void renderCircle(double radius) {
        System.out.println("Drawing circle with radius " + radius + " as raster (pixels)");
    }

    @Override
    public void renderSquare(double side) {
        System.out.println("Drawing square with side " + side + " as raster (pixels)");
    }
}


// Abstraction
public abstract class Shape {
    protected final Renderer renderer;

    public Shape(Renderer renderer) {
        this.renderer = renderer;
    }

    public abstract void draw();
    public abstract void resize(double factor);

    public static void main(String[] args) {
        Renderer vector = new VectorRenderer();
        Renderer raster = new RasterRenderer();

        System.out.println("-- Vector rendering --");
        new Circle(vector, 5).draw();
        new Square(vector, 4).draw();

        System.out.println("\n-- Raster rendering --");
        new Circle(raster, 5).draw();
        new Square(raster, 4).draw();

        System.out.println("\n-- Resize then draw --");
        Circle c = new Circle(vector, 5);
        c.draw();
        c.resize(2);
        c.draw();
    }
}


// Refined Abstractions
class Circle extends Shape {
    private double radius;

    public Circle(Renderer renderer, double radius) {
        super(renderer);
        this.radius = radius;
    }

    @Override
    public void draw()                  { renderer.renderCircle(radius); }

    @Override
    public void resize(double factor)   { radius *= factor; }
}


class Square extends Shape {
    private double side;

    public Square(Renderer renderer, double side) {
        super(renderer);
        this.side = side;
    }

    @Override
    public void draw()                  { renderer.renderSquare(side); }

    @Override
    public void resize(double factor)   { side *= factor; }
}
