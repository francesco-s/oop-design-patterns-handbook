# Design Pattern Comparison

## Creational Patterns

| Pattern | Use When | Avoid When | Example |
|---|---|---|---|
| **Singleton** | You need exactly one shared instance (config, logger, DB connection pool) | You need testability or multiple environments (causes hidden global state) | `AppConfig`, `Logger` |
| **Factory Method** | Subclasses should decide which class to instantiate; you want to decouple creation from use | Object creation is simple and unlikely to vary | `ShapeFactory.create("circle")` |
| **Abstract Factory** | You need families of related objects that must be used together | Only one product type is needed; adds unnecessary complexity | UI toolkit: `WindowsFactory` vs `MacFactory` |
| **Builder** | Object construction requires many optional steps or configurations | The object is simple with few parameters | Building an HTTP request with headers, body, timeout |
| **Prototype** | Cloning is cheaper than creating from scratch; objects differ only slightly | Object state cannot be cleanly copied (e.g., holds open file handles) | Cloning a pre-configured graph node |

***

## Structural Patterns

| Pattern | Use When | Avoid When | Example |
|---|---|---|---|
| **Facade** | You want a simple interface over a complex subsystem | Clients need full access to subsystem internals | Single `GeoProcessor.run()` wrapping PostGIS + GeoPandas + OSM |
| **Proxy** | You need lazy loading, access control, logging, or caching around an object | Direct access is fine and wrapping adds overhead without benefit | Lazy-loading a heavy geospatial dataset only when accessed |
| **Adapter** | You need to integrate a third-party or legacy interface without modifying it | You control both interfaces — just refactor directly | Wrapping a legacy GeoJSON API to match a new spatial interface |
| **Decorator** | You want to add behavior dynamically without subclassing | You need to add core behavior — use inheritance or refactor | Adding logging, caching, or auth to a function/class |
| **Composite** | You need to treat individual objects and compositions uniformly (tree structures) | The hierarchy is fixed and shallow | File system: `File` and `Folder` both implement `Node` |
| **Bridge** | You want to vary abstraction and implementation independently | The abstraction and implementation are tightly coupled by nature | `Shape` (abstraction) + `Renderer` (implementation) |
| **Flyweight** | You have thousands of similar objects sharing common state | Objects have mostly unique state; sharing saves little | Shared tile metadata for map rendering |

***

## Behavioral Patterns

| Pattern | Use When | Avoid When | Example |
|---|---|---|---|
| **Strategy** | You want to swap algorithms at runtime without changing the client | Only one algorithm is ever used | Swapping Dijkstra vs A* vs Yen's for path planning |
| **Observer** | Multiple objects need to react to state changes in another object | Only one dependent exists, or tight coupling is acceptable | Event bus notifying UI components when network graph updates |
| **Template Method** | Subclasses share the same algorithm skeleton but differ in specific steps | Steps vary so much that a shared skeleton adds no value | Base `DataPipeline.run()` with abstract `extract()`, `transform()`, `load()` |
| **Iterator** | You need to traverse a collection without exposing its internals | The collection is already iterable and no custom traversal is needed | Custom graph traversal yielding nodes layer by layer |
| **Command** | You need undo/redo, queuing, or logging of operations | Simple one-off actions with no need for history | `MoveNodeCommand`, `AddEdgeCommand` in a graph editor |
| **State** | An object's behavior changes drastically based on internal state | State transitions are trivial (e.g., just a boolean flag) | Network node: `Active`, `Degraded`, `Offline` states |
| **Chain of Responsibility** | Multiple handlers may process a request, but you don't know which at compile time | The handler is always known — just call it directly | Validation pipeline: format check → auth check → business rule check |
| **Interpreter** | You need to define and evaluate a grammar or DSL (expression parsers, rule engines, query languages) | The grammar is complex or changes often — use a parser generator (ANTLR, PLY) instead | Evaluating filter expressions like `"status == active AND cost < 100"` |
| **Memento** | You need snapshots for undo/redo or rollback | Object state is large and copying it is expensive | Saving/restoring routing algorithm state at each step |
| **Mediator** | Many objects interact chaotically; you want centralized coordination | Only two objects communicate — a direct reference is clearer | Chat room coordinating messages between users |
| **Visitor** | You need to add operations to an object hierarchy without modifying it | The object structure changes frequently (requires updating all visitors) | Exporting graph nodes to GeoJSON, CSV, or KML without touching node classes |

***

## Python-Specific Patterns

| Pattern | Use When | Avoid When | Example |
|---|---|---|---|
| **Decorator** | You want to wrap functions/methods with reusable cross-cutting behavior | The wrapping logic is complex and hurts readability | `@lru_cache`, `@retry`, `@log_execution_time` |
| **Context Manager** | You need guaranteed setup/teardown (resources, locks, transactions) | Resource lifecycle is trivial or already managed elsewhere | `with db.transaction():` or `with open(file):` |
| **Generator** | You need lazy, memory-efficient iteration over large sequences | You need random access or the full collection in memory at once | Streaming millions of OSM way features without loading all into RAM |
| **Descriptor** | You need reusable, controlled attribute access across multiple classes | The logic only applies to one attribute in one class — use a `property` | Validating that a coordinate is within bounds on any spatial model |
| **Metaclass** | You need to control class creation itself (ORMs, plugin registration, enforcement) | You can achieve the same with decorators or `__init_subclass__` — far simpler | Django's `Model` metaclass auto-registering fields |
