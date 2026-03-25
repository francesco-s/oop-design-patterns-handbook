// Abstract Product interfaces
interface Button {
    String render();
}

interface TextField {
    String display();
}

// Concrete Products for Light Theme
class LightButton implements Button {
    @Override
    public String render() {
        return "Light theme button rendered";
    }
}

class LightTextField implements TextField {
    @Override
    public String display() {
        return "Light theme text field displayed";
    }
}

// Concrete Products for Dark Theme
class DarkButton implements Button {
    @Override
    public String render() {
        return "Dark theme button rendered";
    }
}

class DarkTextField implements TextField {
    @Override
    public String display() {
        return "Dark theme text field displayed";
    }
}

// Abstract Factory
interface UIFactory {
    Button createButton();
    TextField createTextField();
}

// Concrete Factories
class LightThemeFactory implements UIFactory {
    @Override
    public Button createButton() {
        return new LightButton();
    }

    @Override
    public TextField createTextField() {
        return new LightTextField();
    }
}

class DarkThemeFactory implements UIFactory {
    @Override
    public Button createButton() {
        return new DarkButton();
    }

    @Override
    public TextField createTextField() {
        return new DarkTextField();
    }
}

// Client
class UIClient {
    public static String createUI(UIFactory factory) {
        Button button = factory.createButton();
        TextField textField = factory.createTextField();
        return "UI created with: " + button.render() + " and " + textField.display();
    }
}

public class AbstractFactory {
    public static void main(String[] args) {
        // Application can use different themes
        UIFactory lightFactory = new LightThemeFactory();
        UIFactory darkFactory = new DarkThemeFactory();
        
        System.out.println(UIClient.createUI(lightFactory));
        System.out.println(UIClient.createUI(darkFactory));
    }
}