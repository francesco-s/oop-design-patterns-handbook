# OOP Design Patterns Handbook: Python vs Java (WIP)

This repository contains implementations of common design patterns in both Python and Java, with explanations and comparisons between the two languages.

## Purpose

The goal of this project is to:

1. Demonstrate how design patterns are implemented in Python and Java
2. Highlight the differences in implementation due to language features
3. Provide practical, working examples of each pattern
4. Serve as a learning resource for developers familiar with one language looking to understand the other

## Background

The patterns in this handbook are primarily based on the seminal book **"Design Patterns: Elements of Reusable Object-Oriented Software"** (1994) by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides — collectively known as the **Gang of Four (GoF)**. The book defines 23 foundational OOP design patterns, all of which are covered here. Python-specific patterns extend beyond the GoF catalog.

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

> Patterns within each section are ordered from **beginner-friendly to advanced**.

### Creational Patterns

- **Singleton** ⭐ — Ensure a class has only one instance
- **Factory Method** ⭐ — Create objects without specifying the exact class
- **Prototype** ⭐⭐ — Clone existing objects
- **Builder** ⭐⭐ — Construct complex objects step by step
- **Abstract Factory** ⭐⭐⭐ — Create families of related objects

### Structural Patterns

- **Facade** ⭐ — Provide a simplified interface to a complex subsystem
- **Proxy** ⭐ — Represent another object with controlled access
- **Adapter** ⭐⭐ — Allow incompatible interfaces to work together
- **Decorator** ⭐⭐ — Add responsibilities to objects dynamically
- **Composite** ⭐⭐ — Compose objects into tree structures
- **Bridge** ⭐⭐⭐ — Separate abstraction from implementation
- **Flyweight** ⭐⭐⭐ — Minimize memory usage by sharing common parts of state

### Behavioral Patterns

- **Strategy** ⭐ — Define a family of algorithms and make them interchangeable
- **Observer** ⭐ — Notify dependents when an object changes
- **Template Method** ⭐ — Define the skeleton of an algorithm
- **Iterator** ⭐⭐ — Access elements sequentially without exposing underlying representation
- **Command** ⭐⭐ — Turn a request into a stand-alone object
- **State** ⭐⭐ — Allow an object to alter its behavior when its state changes
- **Chain of Responsibility** ⭐⭐ — Pass requests along a chain of handlers
- **Interpreter** ⭐⭐⭐ — Define a grammar for a language and provide an interpreter to evaluate sentences in it
- **Memento** ⭐⭐⭐ — Capture and restore an object's internal state
- **Mediator** ⭐⭐⭐ — Reduce chaotic dependencies between objects
- **Visitor** ⭐⭐⭐ — Separate algorithm from object structure

### Python-Specific Patterns

- **Decorators** ⭐ — Wrap functions with reusable cross-cutting behavior
- **Context Managers** ⭐ — Guarantee setup/teardown for resource management
- **Generator Patterns** ⭐⭐ — Lazy, memory-efficient iteration
- **Descriptors** ⭐⭐⭐ — Control attribute access across multiple classes
- **Metaclasses** ⭐⭐⭐ — Customize class creation itself

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
