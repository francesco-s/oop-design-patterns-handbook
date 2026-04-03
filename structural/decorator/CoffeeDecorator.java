// Component interface
interface Coffee {
    double cost();
    String description();
}


// Concrete Component
class SimpleCoffee implements Coffee {
    @Override
    public double cost()        { return 1.00; }

    @Override
    public String description() { return "Simple coffee"; }
}


// Base Decorator
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee;

    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }

    @Override
    public double cost()        { return coffee.cost(); }

    @Override
    public String description() { return coffee.description(); }

    public static void main(String[] args) {
        Coffee coffee = new SimpleCoffee();
        System.out.printf("%-40s $%.2f%n", coffee.description(), coffee.cost());

        coffee = new MilkDecorator(coffee);
        System.out.printf("%-40s $%.2f%n", coffee.description(), coffee.cost());

        coffee = new SugarDecorator(coffee);
        System.out.printf("%-40s $%.2f%n", coffee.description(), coffee.cost());

        coffee = new WhipDecorator(coffee);
        System.out.printf("%-40s $%.2f%n", coffee.description(), coffee.cost());

        System.out.println();
        Coffee fancy = new WhipDecorator(new MilkDecorator(new MilkDecorator(new SimpleCoffee())));
        System.out.printf("%-40s $%.2f%n", fancy.description(), fancy.cost());
    }
}


// Concrete Decorators
class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double cost()        { return coffee.cost() + 0.25; }

    @Override
    public String description() { return coffee.description() + ", milk"; }
}


class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double cost()        { return coffee.cost() + 0.10; }

    @Override
    public String description() { return coffee.description() + ", sugar"; }
}


class WhipDecorator extends CoffeeDecorator {
    public WhipDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double cost()        { return coffee.cost() + 0.50; }

    @Override
    public String description() { return coffee.description() + ", whipped cream"; }
}
