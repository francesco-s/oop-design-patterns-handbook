import java.util.ArrayDeque;
import java.util.Deque;


// Command interface
interface Command {
    void execute();
    void undo();
}


// Receiver
class Light {
    private final String location;
    private boolean isOn = false;

    public Light(String location) {
        this.location = location;
    }

    public void turnOn() {
        isOn = true;
        System.out.println(location + " light turned ON");
    }

    public void turnOff() {
        isOn = false;
        System.out.println(location + " light turned OFF");
    }
}


// Concrete Commands
class TurnOnCommand implements Command {
    private final Light light;

    public TurnOnCommand(Light light) {
        this.light = light;
    }

    @Override
    public void execute() { light.turnOn(); }

    @Override
    public void undo() { light.turnOff(); }
}


class TurnOffCommand implements Command {
    private final Light light;

    public TurnOffCommand(Light light) {
        this.light = light;
    }

    @Override
    public void execute() { light.turnOff(); }

    @Override
    public void undo() { light.turnOn(); }
}


// Invoker
public class RemoteControl {
    private final Deque<Command> history = new ArrayDeque<>();

    public void press(Command command) {
        command.execute();
        history.push(command);
    }

    public void pressUndo() {
        if (!history.isEmpty()) {
            history.pop().undo();
        } else {
            System.out.println("Nothing to undo");
        }
    }

    public static void main(String[] args) {
        RemoteControl remote = new RemoteControl();

        Light livingRoom = new Light("Living room");
        Light bedroom    = new Light("Bedroom");

        remote.press(new TurnOnCommand(livingRoom));
        remote.press(new TurnOnCommand(bedroom));
        remote.press(new TurnOffCommand(livingRoom));

        System.out.println("\n-- Undo last 2 commands --");
        remote.pressUndo();
        remote.pressUndo();
    }
}