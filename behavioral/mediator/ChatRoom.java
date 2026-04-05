// ChatRoom.java

import java.util.ArrayList;
import java.util.List;


// Mediator interface
interface ChatMediator {
    void sendMessage(String message, User sender);
    void addUser(User user);
}


// Colleague
class User {
    public final String name;
    private final ChatMediator mediator;

    public User(String name, ChatMediator mediator) {
        this.name     = name;
        this.mediator = mediator;
        this.mediator.addUser(this);
    }

    public void send(String message) {
        System.out.println("[" + name + "] sends: '" + message + "'");
        mediator.sendMessage(message, this);
    }

    public void receive(String message, User sender) {
        System.out.println("[" + name + "] received from [" + sender.name + "]: '" + message + "'");
    }
}


// Concrete Mediator
public class ChatRoom implements ChatMediator {
    private final List<User> users = new ArrayList<>();

    @Override
    public void addUser(User user) { users.add(user); }

    @Override
    public void sendMessage(String message, User sender) {
        for (User user : users) {
            if (user != sender) {
                user.receive(message, sender);
            }
        }
    }

    public static void main(String[] args) {
        ChatRoom room = new ChatRoom();

        User alice   = new User("Alice",   room);
        User bob     = new User("Bob",     room);
        User charlie = new User("Charlie", room);

        System.out.println("-- Alice sends a message --");
        alice.send("Hello everyone!");

        System.out.println("\n-- Bob sends a message --");
        bob.send("Hey Alice!");
    }
}