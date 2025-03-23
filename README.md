# OOP Design Patterns Handbook: Python vs Java (WIP)

This repository contains implementations of common design patterns in both Python and Java, with explanations and comparisons between the two languages.

## Purpose

The goal of this project is to:

1. Demonstrate how design patterns are implemented in Python and Java
2. Highlight the differences in implementation due to language features
3. Provide practical, working examples of each pattern
4. Serve as a learning resource for developers familiar with one language looking to understand the other

## Repository Structure

```
oop-design-patterns-handbook/
├── creational/         # Creational design patterns
├── structural/         # Structural design patterns
├── behavioral/         # Behavioral design patterns
└── python-specific/    # Patterns unique to Python
```

Each pattern directory contains:

- Python implementation with examples and tests
- Java implementation with examples and tests

## Design Patterns Included

### Creational Patterns

- Singleton: Ensure a class has only one instance
- Factory Method: Create objects without specifying the exact class
- Abstract Factory: Create families of related objects
- Builder: Construct complex objects step by step
- Prototype: Clone existing objects

### Structural Patterns

- Adapter: Allow incompatible interfaces to work together
- Bridge: Separate abstraction from implementation
- Composite: Compose objects into tree structures
- Decorator: Add responsibilities to objects dynamically
- Facade: Provide simplified interface to a complex subsystem
- Flyweight: Minimize memory usage by sharing common parts of state
- Proxy: Represent another object

### Behavioral Patterns

- Chain of Responsibility: Pass requests along a chain of handlers
- Command: Turn a request into a stand-alone object
- Iterator: Access elements sequentially without exposing underlying representation
- Mediator: Reduce chaotic dependencies between objects
- Memento: Capture and restore an object's internal state
- Observer: Notify dependents when an object changes
- State: Allow an object to alter its behavior when its state changes
- Strategy: Define a family of algorithms and make them interchangeable
- Template Method: Define the skeleton of an algorithm
- Visitor: Separate algorithm from object structure

### Python-Specific Patterns

- Context Managers
- Decorators
- Descriptors
- Generator Patterns
- Metaclasses

## Usage

Each pattern directory contains standalone examples that can be run independently.

For Python examples:

```bash
cd pattern_name/python
python pattern_example.py
```

For Java examples:

```bash
cd pattern_name/java
javac PatternExample.java
java PatternExample
```

## Requirements

- Python 3.6+
- Java 11+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
