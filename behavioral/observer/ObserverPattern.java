import java.util.ArrayList;
import java.util.List;

// Observer interface
interface Observer {
    void update(String message);
}

// Concrete Observer
class User implements Observer {
    private String name;
    
    public User(String name) {
        this.name = name;
    }
    
    @Override
    public void update(String message) {
        System.out.println("User " + name + " received: " + message);
    }
}

// Subject (Observable)
class NewsPublisher {
    private List<Observer> observers = new ArrayList<>();
    private String latestNews;
    
    public void attach(Observer observer) {
        if (!observers.contains(observer)) {
            observers.add(observer);
        }
    }
    
    public void detach(Observer observer) {
        observers.remove(observer);
    }
    
    private void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(latestNews);
        }
    }
    
    public void publishNews(String news) {
        this.latestNews = news;
        System.out.println("Publishing news: " + news);
        notifyObservers();
    }
}

// Example usage
public class ObserverPattern {
    public static void main(String[] args) {
        // Create publisher
        NewsPublisher newsPublisher = new NewsPublisher();
        
        // Create subscribers
        Observer alice = new User("Alice");
        Observer bob = new User("Bob");
        Observer charlie = new User("Charlie");
        
        // Register subscribers
        newsPublisher.attach(alice);
        newsPublisher.attach(bob);
        newsPublisher.attach(charlie);
        
        // Publish news
        newsPublisher.publishNews("Java 17 released with new features!");
        
        // Unsubscribe Bob
        System.out.println("\nBob unsubscribed\n");
        newsPublisher.detach(bob);
        
        // Publish another news
        newsPublisher.publishNews("New design patterns book available!");
    }
}