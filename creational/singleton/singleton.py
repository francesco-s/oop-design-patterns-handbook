class Singleton:
    """
    A classic Singleton implementation in Python.
    
    This implementation uses a class variable to store the instance
    and a class method to control access to this instance.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new Singleton instance")
            cls._instance = super(Singleton, cls).__new__(cls)
            # Initialize instance attributes here
            cls._instance.value = 0
        return cls._instance
    
    def increment(self):
        """Sample method to demonstrate state is preserved."""
        self.value += 1
        return self.value


if __name__ == "__main__":
    # Create first instance
    s1 = Singleton()
    print(f"s1 value: {s1.value}")
    
    # Increment the value
    s1.increment()
    print(f"s1 after increment: {s1.value}")
    
    # Create "second" instance (should be the same object)
    s2 = Singleton()
    print(f"s2 value: {s2.value}")
    
    # Check if s1 and s2 are the same object
    print(f"s1 is s2: {s1 is s2}")
    
    # Increment from s2 and check value in s1
    s2.increment()
    print(f"s2 after increment: {s2.value}")
    print(f"s1 value after s2 increment: {s1.value}")