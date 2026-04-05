// Visitor interface
public interface ShapeVisitor {
    void visitCircle(Circle circle);
    void visitRectangle(Rectangle rectangle);
    void visitTriangle(Triangle triangle);

    static void main(String[] args) {
        Shape[] shapes = {
            new Circle(5),
            new Rectangle(4, 6),
            new Triangle(3, 8)
        };

        System.out.println("-- Area --");
        AreaCalculator areaCalc = new AreaCalculator();
        for (Shape shape : shapes) shape.accept(areaCalc);

        System.out.println("\n-- Perimeter --");
        PerimeterCalculator perimCalc = new PerimeterCalculator();
        for (Shape shape : shapes) shape.accept(perimCalc);
    }
}


// Element interface
interface Shape {
    void accept(ShapeVisitor visitor);
}


// Concrete Elements
class Circle implements Shape {
    public final double radius;
    public Circle(double radius) { this.radius = radius; }

    @Override
    public void accept(ShapeVisitor visitor) { visitor.visitCircle(this); }
}


class Rectangle implements Shape {
    public final double width, height;
    public Rectangle(double width, double height) {
        this.width  = width;
        this.height = height;
    }

    @Override
    public void accept(ShapeVisitor visitor) { visitor.visitRectangle(this); }
}


class Triangle implements Shape {
    public final double base, height;
    public Triangle(double base, double height) {
        this.base   = base;
        this.height = height;
    }

    @Override
    public void accept(ShapeVisitor visitor) { visitor.visitTriangle(this); }
}


// Concrete Visitors
class AreaCalculator implements ShapeVisitor {
    @Override
    public void visitCircle(Circle c) {
        System.out.printf("Circle area        : %.2f%n", Math.PI * c.radius * c.radius);
    }

    @Override
    public void visitRectangle(Rectangle r) {
        System.out.printf("Rectangle area     : %.2f%n", r.width * r.height);
    }

    @Override
    public void visitTriangle(Triangle t) {
        System.out.printf("Triangle area      : %.2f%n", 0.5 * t.base * t.height);
    }
}


class PerimeterCalculator implements ShapeVisitor {
    @Override
    public void visitCircle(Circle c) {
        System.out.printf("Circle perimeter   : %.2f%n", 2 * Math.PI * c.radius);
    }

    @Override
    public void visitRectangle(Rectangle r) {
        System.out.printf("Rectangle perimeter: %.2f%n", 2 * (r.width + r.height));
    }

    @Override
    public void visitTriangle(Triangle t) {
        System.out.println("Triangle perimeter : requires all 3 sides");
    }
}