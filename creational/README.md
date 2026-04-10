# Creational Patterns — Documentation

## Overview

Creational patterns abstract the **instantiation process** — they decouple the code that creates objects from the code that uses them, giving you control over what gets created, who creates it, and how.

| Pattern | Files | Intent | Key question it answers |
|---|---|---|---|
| **Singleton** | `singleton.py`, `Singleton.java` | One instance only | How do I guarantee a class is instantiated exactly once? |
| **Factory Method** | `document_factory.py`, `DocumentFactory.java` | Centralize creation by type | How do I create objects without specifying the exact class? |
| **Abstract Factory** | `abstract_factory.py`, `AbstractFactory.java` | Create families of objects | How do I swap entire sets of related objects as one unit? |
| **Builder** | `builder.py`, `BuilderDemo.java` | Step-by-step construction | How do I build a complex object with many optional parts? |
| **Prototype** | `prototype.py`, `PrototypeDemo.java` | Clone instead of new | How do I create objects cheaply from existing ones? |

***

## 1. Singleton

### What it does
Ensures that **only one instance** of a class ever exists and provides a global access point to it. Any call to get the instance — no matter how many times — returns the same object.

### Structure in your code

**Python** — overrides `__new__` to intercept instance creation:
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance   # always returns the same object
```

**Java** — uses the *Initialization-on-Demand Holder* idiom:
```java
public class Singleton {
    private Singleton() {}   // private constructor blocks direct instantiation

    private static class SingletonHolder {
        private static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getInstance() {
        return SingletonHolder.INSTANCE;
    }
}
```

### Key details from your code
- In Python, `__new__` is called **before** `__init__`. The guard `if cls._instance is None` ensures `__init__` only initializes once because the same object is returned on every subsequent call.
- The Java holder idiom is **lazily initialized and thread-safe** without `synchronized` — the JVM guarantees class loading is thread-safe, so `INSTANCE` is created only when `getInstance()` is first called.
- Both implementations demonstrate that `s1 is s2` (Python) and `s1 == s2` (Java reference equality) both return `true`, proving only one instance exists.
- State is shared: incrementing `value` via `s2` is visible through `s1`, because they are the same object.

### When to use
Logging services, configuration managers, thread pools, database connection pools — any resource where exactly one coordinating object must exist.

***

## 2. Factory Method

### What it does
Delegates object creation to a **factory method**, decoupling client code from concrete product classes. The client asks for a document of type `"pdf"` — it never calls `PDFDocument()` directly.

### Structure in your code

```
DocumentCreator.create_document("pdf")
    └─ returns PDFDocument()   ← concrete class hidden from client

DocumentCreator.create_document("word")
    └─ returns WordDocument()
```

Both Python and Java implement this as a single static factory method with a type-dispatch block (`if/elif` in Python, `switch` in Java), returning an object typed as the abstract product interface (`Document`).

### Key details from your code
- Python uses `ABC` + `@abstractmethod` to declare the `Document` interface; Java uses a plain `interface`. Both enforce that every product implements `create()`.
- The factory method is `@staticmethod` in Python — it needs no instance of `DocumentCreator` to work.
- Invalid types raise `ValueError` (Python) and `IllegalArgumentException` (Java). The naming convention reflects each language's error taxonomy: Python uses general exceptions by value, Java uses specific checked/unchecked exception types.
- The client loop iterates over type strings and calls `document.create()` without knowing which concrete class it received — this is the core benefit of the pattern.

### When to use
When the exact type to create is determined at runtime (e.g. from config, user input, or a file extension), and you want to keep creation logic in one place rather than scattered across the codebase.

***

## 3. Abstract Factory

### What it does
Produces **families of related objects** through a single factory interface. Swapping the factory swaps the entire product family in one step — the client code touches nothing.

### Structure in your code

```
UIFactory (abstract)
├── LightThemeFactory → creates LightButton  + LightTextField
└── DarkThemeFactory  → creates DarkButton   + DarkTextField

create_ui(factory):          ← client never references Light or Dark directly
    button     = factory.create_button()
    text_field = factory.create_text_field()
```

### Key details from your code
- There are **two layers of abstraction**: product interfaces (`Button`, `TextField`) and the factory interface (`UIFactory`). Concrete factories implement the factory interface; concrete products implement the product interfaces.
- The client function `create_ui` (Python) / `UIClient.createUI` (Java) is typed against the abstract factory only — it is completely agnostic to which theme is active.
- In Python, `UIFactory` is an `ABC` with `@abstractmethod` methods. Java uses `interface UIFactory` — a lighter construct since Java interfaces are implicitly abstract.
- Adding a new theme (e.g. `HighContrastThemeFactory`) requires zero changes to client code — only a new factory class and two new product classes.

### When to use
UI theme systems, cross-platform widget toolkits, database driver abstraction (MySQL vs PostgreSQL families), or any case where you need guaranteed internal consistency within a product family.

***

## 4. Builder

### What it does
Separates the **construction** of a complex object from its **representation**, allowing the same building process to produce different variants. Parts are assembled step-by-step via a fluent API.

### Structure in your code

```
Director (optional — defines named presets)
└── build_gaming_pc(builder) → chains: cpu → ram → storage → gpu → get_computer()

ComputerBuilder (concrete builder)
└── each build_*() sets a field and returns self/this  ← enables method chaining

Computer (product)
└── plain data holder — no construction logic of its own
```

### Key details from your code
- **Method chaining** — each `build_*()` method returns `self` (Python) / `this` (Java), enabling the fluent interface `builder.build_cpu(...).build_ram(...).get_computer()`.
- The `Director` encapsulates **named configurations** (`build_gaming_pc`, `build_office_pc`). It is optional — the custom PC at the end of both examples builds directly on `ComputerBuilder` without a Director.
- The builder must be **reset** between builds. Both implementations do this by creating a new `ComputerBuilder()` instance before each separate product.
- Python has no separate `Builder` interface — `ComputerBuilder` acts as both interface and implementation. Java defines a `Builder` interface separately, then `ComputerBuilder implements Builder`, enforcing the contract at compile time.
- The `Computer` product class is a pure data holder with no construction logic — all assembly responsibility lives in the builder.

### When to use
Objects with many optional or interdependent parameters (replacing telescoping constructors), configuration objects, query builders, HTTP request builders, or any object where construction is a multi-step process.

***

## 5. Prototype

### What it does
Creates new objects by **cloning an existing one** (the prototype) rather than constructing from scratch. A registry stores pre-configured prototypes; consumers clone from the registry and customize their copy.

### Structure in your code

```
ShapeCache (registry)
├── load()       → stores Circle("circle-1", r=10) and Rectangle("rectangle-1", 20×30)
└── get_shape(id) → returns shape.clone()   ← always a fresh deep copy

Modifying the clone never affects the original in the registry.
```

### Key details from your code
- Python's `copy.deepcopy(self)` inside `clone()` handles the entire object graph recursively — including nested objects — with a single stdlib call. No manual field-by-field copying is needed.
- Java requires the class to implement the `Cloneable` marker interface and call `super.clone()` inside a `try/catch CloneNotSupportedException` block. The cast `(Prototype) super.clone()` is needed because `Object.clone()` returns `Object`.
- The registry (`ShapeCache`) decouples consumers from knowing which class to instantiate. Consumers ask for `"circle-1"` and receive a ready-to-modify clone.
- Both examples demonstrate the independence guarantee: setting `cloned_circle.radius = 15` leaves the original in the cache untouched at `radius = 10`.

### When to use
Expensive-to-construct objects (DB-backed, network-fetched), object templates with common defaults that users customize, game entities (enemies, tiles) spawned from a master prototype, or when bypassing complex constructor chains.

***

## Python vs Java — Per-Pattern Differences

| Aspect | Python | Java |
|---|---|---|
| **Interfaces / Abstract base** | `ABC` + `@abstractmethod` | `interface` keyword (implicitly abstract) |
| **Abstract enforcement** | Runtime — `TypeError` at instantiation | Compile time — won't compile if method unimplemented |
| **Access modifiers** | Convention only (`_instance` = protected by convention) | `private`, `protected`, `public` enforced by compiler |
| **Singleton hook** | `__new__` override | Private constructor + static factory method |
| **Singleton thread safety** | Not thread-safe by default; needs `threading.Lock` | Holder idiom is JVM-guaranteed thread-safe |
| **Factory dispatch** | `if/elif` chain | `switch` statement |
| **Invalid type error** | `ValueError` | `IllegalArgumentException` |
| **Builder interface** | Not declared separately — builder IS the concrete class | `Builder` interface declared, then `implements Builder` |
| **Method chaining** | `return self` | `return this` |
| **Builder type safety** | Duck-typed — no compile check | Compile-time checked via interface |
| **Clone mechanism** | `copy.deepcopy()` from stdlib — recursive, automatic | `Cloneable` + `super.clone()` + `try/catch` — manual, shallow by default |
| **Deep vs shallow copy** | `deepcopy` always deep; `copy.copy()` for shallow | `super.clone()` is shallow — deep copy must be implemented manually per field |
| **Prototype registry** | `dict` with string keys | `HashMap<String, Shape>` with generic type |
| **Client typing** | Duck-typed — no declared return type needed | Typed against interface (`UIFactory`, `Document`, etc.) |
| **File / class naming** | Multiple public classes per file allowed | One `public` class per file, filename must match class name |
| **Boilerplate** | Significantly less — no getters/setters, no `@Override` | More verbose — explicit `@Override`, typed fields, accessors |

***

## Pattern-Level Comparison

| | Singleton | Factory Method | Abstract Factory | Builder | Prototype |
|---|---|---|---|---|---|
| **Creates** | 1 shared instance | 1 product per call | A family of products | 1 complex product | A copy of an existing object |
| **Complexity** | Low | Low | Medium | Medium | Low–Medium |
| **Flexibility** | None — locked to one instance | Medium — add products without changing client | High — swap entire families | High — compose optional parts freely | Medium — clone then customize |
| **Typical domain** | Config, logger, connection pool | Document/file types, parsers | UI themes, DB drivers | Complex configs, query builders | Templates, game entities, expensive objects |
| **Real-world analog** | `logging.getLogger()`, Django settings | `json.loads()`, `open()` | Django ORM backends | `urllib.request.Request`, SQL query builders | `copy.deepcopy()`, ORM `Model.clone()` |