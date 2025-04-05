from abc import ABC, abstractmethod

# Abstract Product interfaces
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class TextField(ABC):
    @abstractmethod
    def display(self):
        pass

# Concrete Products for Light Theme
class LightButton(Button):
    def render(self):
        return "Light theme button rendered"

class LightTextField(TextField):
    def display(self):
        return "Light theme text field displayed"

# Concrete Products for Dark Theme
class DarkButton(Button):
    def render(self):
        return "Dark theme button rendered"

class DarkTextField(TextField):
    def display(self):
        return "Dark theme text field displayed"

# Abstract Factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self):
        pass

    @abstractmethod
    def create_text_field(self):
        pass

# Concrete Factories
class LightThemeFactory(UIFactory):
    def create_button(self):
        return LightButton()

    def create_text_field(self):
        return LightTextField()

class DarkThemeFactory(UIFactory):
    def create_button(self):
        return DarkButton()

    def create_text_field(self):
        return DarkTextField()

# Client code
def create_ui(factory):
    button = factory.create_button()
    text_field = factory.create_text_field()
    return f"UI created with: {button.render()} and {text_field.display()}"

if __name__ == "__main__":
    # Application can use different themes
    light_factory = LightThemeFactory()
    dark_factory = DarkThemeFactory()
    
    print(create_ui(light_factory))
    print(create_ui(dark_factory))