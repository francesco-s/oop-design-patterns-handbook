// singleton/java/Singleton.java

/**
 * A thread-safe Singleton implementation in Java.
 * This implementation uses the "initialization-on-demand holder" idiom.
 */
public class Singleton {
    // Private value to demonstrate state
    private int value = 0;
    
    // Private constructor prevents instantiation from other classes
    private Singleton() {
        System.out.println("Creating new Singleton instance");
    }
    
    // Static inner class holds instance
    private static class SingletonHolder {
        private static final Singleton INSTANCE = new Singleton();
    }
    
    // Public method to get the singleton instance
    public static Singleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
    
    // Sample method to demonstrate state is preserved
    public int increment() {
        return ++value;
    }
    
    public int getValue() {
        return value;
    }
    
    public static void main(String[] args) {
        // Get first instance
        Singleton s1 = Singleton.getInstance();
        System.out.println("s1 value: " + s1.getValue());
        
        // Increment the value
        s1.increment();
        System.out.println("s1 after increment: " + s1.getValue());
        
        // Get "second" instance (should be the same object)
        Singleton s2 = Singleton.getInstance();
        System.out.println("s2 value: " + s2.getValue());
        
        // Check if s1 and s2 are the same object
        System.out.println("s1 == s2: " + (s1 == s2));
        
        // Increment from s2 and check value in s1
        s2.increment();
        System.out.println("s2 after increment: " + s2.getValue());
        System.out.println("s1 value after s2 increment: " + s1.getValue());
    }
}