# Behavioral Patterns — Documentation

Behavioral patterns deal with **algorithms and the assignment of responsibilities** between objects. They characterize complex control flow that's difficult to follow at runtime.

| # | Pattern | Files | Core question answered |
|---|---|---|---|
| 1 | **Template Method**| `beverage_maker.py`, `BeverageMaker.java` | How do I define the skeleton of an algorithm but let subclasses override specific steps? |
| 2 | **Strategy** | `strategy.py`, `SortStrategy.java` | How do I make an algorithm interchangeable at runtime without modifying the context? |
| 3 | **State** | `vending_machine.py`, `VendingMachine.java` | How do I alter an object's behavior when its internal state changes, without massive `if-else` blocks? |
| 4 | **Observer** | `observer.py`, `ObserverPattern.java` | How do I notify multiple objects about an event without coupling the sender to the receivers? |
| 5 | **Iterator** | `book_iterator.py`, `BookCollection.java` | How do I traverse a collection without exposing its underlying representation? |
| 6 | **Command** | `remote_control.py`, `RemoteControl.java` | How do I encapsulate a request as an object, so I can queue, log, or undo it? |
| 7 | **Memento** | `text_editor.py`, `TextEditor.java` | How do I capture and restore an object's internal state without violating encapsulation? |
| 8 | **Chain of Resp.** | `support_handler.py`, `SupportHandler.java` | How do I pass a request along a chain of potential handlers until one of them handles it? |
| 9 | **Mediator** | `chat_room.py`, `ChatRoom.java` | How do I reduce chaotic dependencies between interacting objects by centralizing their communication? |
| 10| **Visitor** | `geometric_shapes.py`, `ShapeVisitor.java` | How do I add new operations to an existing object hierarchy without modifying the objects themselves? |

***

## 1. Template Method

### What it does
Defines the skeleton of an algorithm in a base class, deferring some steps to subclasses. Subclasses can redefine certain steps without changing the algorithm's structure.

### Structure in your code
```
BeverageMaker (abstract base)
  ├── make_beverage()   ← The template method (boil -> brew -> pour -> add)
  ├── _boil_water()     ← Common step (implemented in base)
  ├── _brew()           ← Abstract step (must be overridden)
  └── _add_condiments() ← Abstract step (must be overridden)

TeaMaker (subclass)     ← overrides _brew (steep) and _add_condiments (lemon)
CoffeeMaker (subclass)  ← overrides _brew (drip) and _add_condiments (sugar/milk)
```

### Key details from your code
- The `make_beverage()` method encodes the exact sequence of steps. The caller just calls `tea.make_beverage()`.
- Java uses the `final` keyword on `makeBeverage()` to strictly prevent subclasses from altering the sequence. Python lacks a built-in `final` method modifier (though `typing.final` exists, it's a type-hint, not a runtime lock), so it relies on the convention that callers don't override it.
- Java uses `protected abstract` for the steps subclasses must implement, keeping them hidden from the public API. Python uses the `_` prefix convention (`_brew`) combined with `@abstractmethod`.

### When to use
Frameworks where the engine controls the lifecycle but the user fills in the blanks (e.g., UI lifecycle `on_start()`, `on_resume()`), or when you have multiple algorithms that share the exact same structural flow but differ in local details.

***

## 2. Strategy

### What it does
Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

### Structure in your code
```
SortStrategy (interface)
  ├── BubbleSortStrategy
  ├── QuickSortStrategy
  └── ReverseSortStrategy

Sorter (context) ← holds a reference to a SortStrategy and delegates sort() to it
```

### Key details from your code
- The `Sorter` context delegates the heavy lifting: `return self._strategy.sort(data)`.
- The strategy can be swapped at runtime using `set_strategy(...)` without modifying the context class.
- Java implements this via `interface SortStrategy`, while Python uses an `ABC`.
- **Contrast with State:** Strategy and State look structurally identical. The difference is intent: a Strategy is usually swapped by the *client* from the outside (e.g., user selects "QuickSort"), whereas States usually transition *themselves* internally based on events.

### When to use
Different sorting algorithms, varied routing/navigation algorithms, different payment gateways (PayPal, Stripe), or replacing massive `switch/case` statements that pick a behavior based on a flag.

***

## 3. State

### What it does
Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.

### Structure in your code
```
State (interface)  ← insert_coin(), press_button(), dispense()
  ├── IdleState        ← transitions to HasCoinState
  ├── HasCoinState     ← transitions to DispensingState
  ├── DispensingState  ← transitions to IdleState or OutOfStockState
  └── OutOfStockState

VendingMachine (context) ← delegates requests to its current _state
```

### Key details from your code
- Instead of the `VendingMachine` having a giant `if state == IDLE: ... elif state == HAS_COIN: ...` block in every method, the machine just calls `self._state.insert_coin(self)`.
- The *State objects themselves* decide when to transition by calling `machine.set_state(...)`. This forms a self-driving state machine.
- The `VendingMachine` passes a reference to `self` (`this` in Java) into every state method so the state objects can interact with the machine (decrementing count, changing state).
- Java creates singleton-like state instances inside the machine (`public final State idleState = new IdleState()`), avoiding object allocation on every transition. Python does exactly the same in `__init__`.

### When to use
Complex state machines like media players (play, pause, stop), document publishing workflows (draft, review, published), or game character states (running, jumping, attacking).

***

## 4. Observer

### What it does
Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

### Structure in your code
```
Observer (interface)  ← update(message)
  └── User            ← prints the received message

NewsPublisher (subject)
  ├── attach(observer)
  ├── detach(observer)
  └── notify_observers() ← loops through observers calling update()
```

### Key details from your code
- The `NewsPublisher` maintains a `List` of observers. It doesn't know who the observers are (Alice, Bob, etc.), only that they implement the `Observer` interface.
- Python uses `if observer not in self._observers:` and `self._observers.remove()`. Java uses `List.contains()` and `List.remove()`.
- This is a "push" model—the publisher pushes the `latest_news` string directly into the `update()` method. (Alternatively, a "pull" model would pass the subject itself, letting the observer query what it needs).

### When to use
Event handling systems (UI button clicks), publish-subscribe architectures, MVC frameworks (updating views when the model changes), or stock ticker feeds.

***

## 5. Iterator

### What it does
Provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

### Structure in your code
```
Iterator (interface)
  └── BookIterator      ← keeps track of index, implements has_next() / next()

IterableCollection (interface)
  └── BookCollection    ← manages the List of books, creates the iterator
```

### Key details from your code
- `BookCollection` holds the list of books, but does not track traversal. `BookIterator` tracks the `_index`. This allows multiple independent iterators to traverse the same collection simultaneously.
- Python defines `has_next` and `next`, mirroring Java's `hasNext()` and `next()`.
- *(Note: In real-world Python, you would implement `__iter__` and `__next__`. In Java, you would implement `java.lang.Iterable` and `java.util.Iterator`. The manual interfaces here are purely for demonstrating the GoF pattern mechanics).*

### When to use
Traversing complex data structures (trees, graphs) where you want a flat sequence, hiding the complexity of the internal data structure (arrays, linked lists, hash maps) behind a unified iteration interface.

***

## 6. Command

### What it does
Encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

### Structure in your code
```
Command (interface)
  ├── TurnOnCommand    ← calls light.turn_on() in execute(), turn_off() in undo()
  └── TurnOffCommand   ← calls light.turn_off() in execute(), turn_on() in undo()

Light (receiver)       ← actually does the work
RemoteControl (invoker)← holds a history stack, calls execute() and undo()
```

### Key details from your code
- The pattern involves 4 roles: Command interface, Concrete Command, Receiver (`Light`), and Invoker (`RemoteControl`).
- The `RemoteControl` (invoker) just calls `command.execute()`. It doesn't know it's turning on a light; it just triggers a generic command.
- The `undo()` history is implemented cleanly using a stack (`List.pop()` in Python, `Deque.pop()` in Java). Because the Command object holds the parameters and the receiver reference, it knows exactly how to reverse itself.

### When to use
GUI buttons/menu items, macro recording, multi-level undo/redo systems, or deferring execution (job queues, thread pools).

***

## 7. Memento

### What it does
Without violating encapsulation, captures and externalizes an object's internal state so that the object can be restored to this state later.

### Structure in your code
```
Memento (state snapshot) ← immutable, holds "content"
TextEditor (originator)  ← creates Mementos (save), consumes Mementos (restore)
History (caretaker)      ← manages the stack of Mementos
```

### Key details from your code
- The `History` (caretaker) holds the stack of Mementos but never inspects their contents. It treats the Memento as a black box.
- The `TextEditor` (originator) creates the Memento via `save()`, freezing its current state.
- In Python, `Memento` is implemented securely as a `@dataclass(frozen=True)`. In Java, it's a class with a `private final` field and only a getter.
- Python handles the empty undo case by returning `None` and checking `if snapshot:`. Java does the same returning `null` and checking `if (snapshot != null)`.

### When to use
Undo/redo mechanisms, saving checkpoints in video games, or restoring database states after failed transactions.

***

## 8. Chain of Responsibility

### What it does
Avoids coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chains the receiving objects and passes the request along the chain until an object handles it.

### Structure in your code
```
SupportHandler (base)    ← manages the _next reference and pass_to_next()
  ├── BasicSupport       ← handles level 1, else passes
  ├── IntermediateSupport← handles level 2, else passes
  └── AdvancedSupport    ← handles level 3, else passes
```

### Key details from your code
- Handlers are linked at runtime: `basic.set_next(intermediate).set_next(advanced)`.
- If a handler can't process the request, it delegates strictly to its `_next` handler via `pass_to_next()`.
- The base class handles the fallback: if `_next` is null, the request falls off the end of the chain, triggering a default "could not be resolved" behavior.
- Python's `Optional["SupportHandler"]` forward-reference string matches Java's typed object reference.

### When to use
Event bubbling in UI frameworks (clicking a button bubbles up to the window), HTTP middleware/filter pipelines (authentication -> logging -> routing), or sequential validation checks.

***

## 9. Mediator

### What it does
Defines an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

### Structure in your code
```
ChatMediator (interface)
  └── ChatRoom       ← concrete mediator, holds a list of Users, routes messages

User (colleague)     ← holds a reference to the Mediator, calls mediator.send_message()
```

### Key details from your code
- `Alice`, `Bob`, and `Charlie` (`User` objects) never hold references to each other. When Alice speaks, she tells the `ChatRoom`. The `ChatRoom` loops through its users and invokes `receive()` on everyone else.
- This changes a many-to-many chaotic dependency matrix (where every user knows every other user) into a star topology (all users know only the mediator).
- The `User` registers itself with the mediator during initialization (`self._mediator.add_user(self)`).

### When to use
Chat applications, complex UI dialogues where changing one form field updates 5 other fields (instead of fields listening to each other, they listen to a dialogue mediator), or air traffic control systems.

***

## 10. Visitor

### What it does
Represents an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

### Structure in your code
```
Shape (element interface)  ← declare accept(Visitor)
  ├── Circle               ← accept() calls visitor.visit_circle(self)
  ├── Rectangle            ← accept() calls visitor.visit_rectangle(self)
  └── Triangle             ← accept() calls visitor.visit_triangle(self)

ShapeVisitor (visitor)     ← declares visit methods for EVERY concrete shape
  ├── AreaCalculator       ← implements area formulas
  └── PerimeterCalculator  ← implements perimeter formulas
```

### Key details from your code
- Relies on "Double Dispatch":
  1. The client calls `shape.accept(visitor)`
  2. The shape executes `visitor.visit_circle(self)`
  This guarantees that the exact correct method is called on the visitor, resolving the concrete type of the shape.
- If you add a new operation (e.g., `ExportToXMLVisitor`), you create one new Visitor class without touching `Circle` or `Rectangle`.
- **The downside:** If you add a new *Shape* (e.g., `Pentagon`), you must update the `ShapeVisitor` interface and *every single concrete Visitor class* to implement `visit_pentagon()`.

### When to use
Operating on Abstract Syntax Trees (ASTs) in compilers (type checking, code generation, optimization are all distinct Visitors), or exporting diverse object hierarchies into different formats (JSON, XML, CSV).

***

## Python vs Java Comparison

| Dimension | Python | Java |
|---|---|---|
| **Interface Definition** | `ABC` + `@abstractmethod` | `interface` keyword |
| **Preventing overrides** | Convention (no `final` method keyword) | `final` method modifier (Template Method) |
| **Method visibility** | `_method_name` (convention) | `protected abstract` (Template Method) |
| **State transition ref** | `self` (passed to state method) | `this` (passed to state method) |
| **Undo stack type** | `List` with `append()` / `pop()` | `Deque` with `push()` / `pop()` |
| **Memento protection** | `@dataclass(frozen=True)` | `private final` fields + no setters |
| **Type Hint Forward Ref**| `Optional["SupportHandler"]` (string) | Native `SupportHandler` type |
| **List membership check**| `if observer not in self._observers` | `!observers.contains(observer)` |
| **Double Dispatch (Visitor)**| Supported via explicit method names | Supported via explicit method names (no native multiple dispatch) |
| **Boilerplate** | Low | High (Types, access modifiers, `@Override`) |