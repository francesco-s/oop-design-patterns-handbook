// BeverageMaker.java

// Abstract class with the template method
public abstract class BeverageMaker {

    // Template method — final so subclasses cannot override the skeleton
    public final void makeBeverage() {
        boilWater();
        brew();
        pourInCup();
        addCondiments();
    }

    // Common steps (shared implementation)
    private void boilWater() {
        System.out.println("Boiling water");
    }

    private void pourInCup() {
        System.out.println("Pouring into cup");
    }

    // Variable steps — subclasses must implement these
    protected abstract void brew();
    protected abstract void addCondiments();

    public static void main(String[] args) {
        BeverageMaker tea = new TeaMaker();
        System.out.println("Making tea:");
        tea.makeBeverage();

        System.out.println();

        BeverageMaker coffee = new CoffeeMaker();
        System.out.println("Making coffee:");
        coffee.makeBeverage();
    }
}


// Concrete subclasses
class TeaMaker extends BeverageMaker {
    @Override
    protected void brew() {
        System.out.println("Steeping the tea");
    }

    @Override
    protected void addCondiments() {
        System.out.println("Adding lemon");
    }
}


class CoffeeMaker extends BeverageMaker {
    @Override
    protected void brew() {
        System.out.println("Dripping coffee through filter");
    }

    @Override
    protected void addCondiments() {
        System.out.println("Adding sugar and milk");
    }
}