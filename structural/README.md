# Structural Patterns — Documentation

Structural patterns deal with **how classes and objects are composed** into larger structures. Where creational patterns ask "how do we build it?", structural patterns ask "how do we connect it?".

| # | Pattern | Files | Core question answered |
|---|---|---|---|
| 1 | **Facade** | `home_theater.py`, `HomeTheaterFacade.java` | How do I simplify a complex subsystem behind a single interface? |
| 2 | **Proxy** | `image_loader.py`, `ProxyImage.java` | How do I control access to an object without the caller knowing? |
| 3 | **Adapter** | `media_player.py`, `MediaAdapter.java` | How do I make two incompatible interfaces work together? |
| 4 | **Decorator** | `coffee_shop.py`, `CoffeeDecorator.java` | How do I add behaviour to an object at runtime without modifying its class? |
| 5 | **Composite** | `file_system_tree.py`, `FileSystemItem.java` | How do I treat individual objects and compositions of objects uniformly? |
| 6 | **Flyweight** | `forest.py`, `TreeTypeFactory.java` | How do I support a large number of fine-grained objects efficiently by sharing state? |
| 7 | **Bridge** | `shape_renderer.py`, `Shape.java` | How do I decouple an abstraction from its implementation so both can vary independently? |

***

## 1. Facade

### What it does
Provides a **single simplified entry point** into a complex subsystem. The client calls one method; the facade internally coordinates multiple subsystem objects in the right order.

### Structure in your code
```
HomeTheaterFacade
  ├── Amplifier
  ├── DVDPlayer
  ├── Projector
  └── Lights

theater.watch_movie("Inception")  ← one call replaces 7 subsystem calls
theater.end_movie()               ← one call replaces 5 subsystem calls
```

### Key details from your code
- The four subsystem objects (`Amplifier`, `DVDPlayer`, `Projector`, `Lights`) are instantiated inside the facade constructor — the client never creates or holds references to them directly.
- `watch_movie` encodes a specific sequence: dim lights → projector on → widescreen mode → amp on → set volume → DVD on → play. The ordering is the facade's knowledge, not the client's responsibility.
- The subsystem classes remain fully public and usable independently — the facade does not hide or lock them, it just provides a convenience layer on top.
- Python's subsystem classes have no base class or interface — they are plain classes with matching method names. Java uses the same approach, relying on no interface contract between subsystem classes.

### When to use
Wrapping legacy systems, simplifying third-party library setup sequences, or providing a clean API layer over a group of collaborating services (e.g., payment processing, notification dispatch, startup/shutdown sequences).

***

## 2. Proxy

### What it does
Provides a **stand-in object** that controls access to a real subject. The proxy and the real object share the same interface; the caller cannot tell the difference.

### Structure in your code
```
Image (interface)  ←── RealImage   (loads from disk on construction)
                   ←── ProxyImage  (defers loading until first display() call)
```

### Key details from your code
- `RealImage.__init__` calls `_load()` immediately — construction is expensive. `ProxyImage.__init__` does nothing except store the filename, deferring all cost.
- The lazy-initialization guard `if self._real_image is None` means the disk load happens exactly once — the second and third `display()` calls use the cached `_real_image`.
- There is an intentional inconsistency in `image_loader.py`: `ProxyImage` does not inherit from `Image`. In `ProxyImage.java`, it correctly implements `Image`. This means Python loses compile-time (and static-analysis-time) interface guarantees — the duck-typing contract is informal.
- The `[Proxy] Returning cached image` log message on subsequent calls makes the caching mechanism observable, which is useful for understanding and testing.

### When to use
Lazy initialization of expensive resources, access control (checking permissions before delegating), remote proxies (hiding network calls), and logging/monitoring proxies that wrap existing services.

***

## 3. Adapter

### What it does
Wraps an **incompatible interface** (the adaptee) and exposes the interface the client expects (the target). No modifications to either the client or the adaptee are needed.

### Structure in your code
```
MediaPlayer (target)  ←── AudioPlayer      (handles .mp3 natively)
                           └── MediaAdapter (delegates .vlc and .mp4 to AdvancedMediaPlayer)
                                └── AdvancedMediaPlayer (adaptee — play_vlc / play_mp4)
```

### Key details from your code
- `AudioPlayer` implements `MediaPlayer` and handles `.mp3` itself. For any other format, it delegates to `MediaAdapter`, which in turn calls the appropriate method on `AdvancedMediaPlayer`. This is **object composition adapter** — the adapter wraps an instance, not inherits from the adaptee.
- The file extension check (`endswith(".vlc")`) lives inside the adapter, keeping both `AudioPlayer` and `AdvancedMediaPlayer` free of routing logic.
- Unsupported formats (`.avi`) fall through to the adapter's `else` branch and print a message rather than raising — a graceful degradation choice.
- Python's `AdvancedMediaPlayer` uses `snake_case` (`play_vlc`, `play_mp4`); Java uses `camelCase` (`playVlc`, `playMp4`). The adapter in each language bridges both the interface mismatch and the naming convention of the adaptee.

### When to use
Integrating third-party libraries whose interfaces don't match your domain model, wrapping legacy code without touching it, or unifying multiple data sources behind a single interface.

***

## 4. Decorator (Structural)

### What it does
Attaches **additional responsibilities to an object at runtime** by wrapping it in decorator objects that share the same interface. Decorators can be stacked arbitrarily, with each layer adding behaviour before or after delegating to the wrapped object.

### Structure in your code
```
Coffee (interface)
  └── SimpleCoffee              ← base component ($1.00)
  └── CoffeeDecorator (base)    ← wraps any Coffee, delegates by default
        ├── MilkDecorator        ← +$0.25, appends ", milk"
        ├── SugarDecorator       ← +$0.10, appends ", sugar"
        └── WhipDecorator        ← +$0.50, appends ", whipped cream"
```

### Key details from your code
- `CoffeeDecorator` holds a reference `self._coffee` / `this.coffee` typed to the `Coffee` interface — not to any concrete class. This is what makes arbitrary stacking possible.
- `cost()` and `description()` in `CoffeeDecorator` both delegate to `self._coffee` unchanged. Concrete decorators only override what they add — they don't need to re-implement the full interface.
- The fancy order `WhipDecorator(MilkDecorator(MilkDecorator(SimpleCoffee())))` shows that the same decorator can appear multiple times in the chain — `MilkDecorator` is applied twice, adding `$0.50` extra.
- In Java, `CoffeeDecorator` is declared `abstract` and `coffee` is `protected final` — enforcing that every concrete decorator must call `super(coffee)`. Python's base decorator is a concrete class, relying on convention rather than compiler enforcement.

> **Note:** This is the structural Decorator pattern (object wrapping at runtime), which is distinct from Python's `@decorator` syntax covered in the Python-native patterns section. They solve related but different problems at different levels.

### When to use
Adding optional add-ons to objects when subclassing would cause a combinatorial explosion of subclasses — UI component styling, I/O stream wrapping (`BufferedReader` wraps `FileReader`), middleware pipelines, or feature flags applied per-request.

***

## 5. Composite

### What it does
Composes objects into **tree structures** and lets clients treat individual leaves and composite nodes through a single uniform interface. The client calls `size()` or `display()` on the root and the tree handles recursion internally.

### Structure in your code
```
FileSystemItem (component interface)
  ├── File   (leaf)     — has a fixed size, displays itself
  └── Folder (composite) — contains List[FileSystemItem], delegates to children

root.display()     ← one call, entire tree renders recursively
root.size()        ← one call, sums all nested file sizes recursively
```

### Key details from your code
- `Folder.size()` is elegantly recursive: `sum(child.size() for child in self._children)` / `children.stream().mapToInt(FileSystemItem::size).sum()`. A folder containing other folders naturally triggers recursive descent without any explicit loop management in the client.
- `Folder.display()` passes a deepened indent string (`indent + "  "`) on each recursive call, producing the visual tree indentation.
- Both `File` and `Folder` implement the same `FileSystemItem` interface — the client code building the tree (assigning `documents.add(file1)`) never needs to check what type it is adding.
- `Folder.remove()` uses `list.remove(item)` in Python (identity-based removal) and `ArrayList.remove(item)` in Java (equals-based removal). For correctness with multiple identical-name files, identity is safer.

### When to use
Any tree-shaped domain: file systems, UI component hierarchies, organizational charts, menus and submenus, abstract syntax trees, or bill-of-materials structures.

***

## 6. Flyweight

### What it does
Reduces memory usage by **sharing common state** (intrinsic state) across many objects, while each object retains only its unique state (extrinsic state). A factory ensures shared objects are created once and reused.

### Structure in your code
```
TreeType (flyweight)  — name, color, texture  ← shared, immutable, created once per variant
Tree     (context)    — x, y, tree_type ref   ← unique per instance, holds extrinsic state
TreeTypeFactory       — Dict/Map cache keyed by (name, color, texture)
Forest                — plants trees, manages the context list
```
Result: 6 trees planted, only 3 `TreeType` objects ever created.

### Key details from your code
- Python uses `@dataclass(frozen=True)` on `TreeType` — the `frozen=True` enforces immutability at runtime (attempts to mutate raise `FrozenInstanceError`) and auto-generates `__hash__`, making it safe to use as a dict key. Java's `TreeType` achieves the same with `private final` fields and no setters, but immutability is enforced by convention, not runtime checks.
- The Python cache key is a `Tuple` `(name, color, texture)` — structurally typed and hashable. Java concatenates strings: `name + "-" + color + "-" + texture` — simpler but fragile if values contain the separator.
- `Tree` (context) stores only `x`, `y`, and a reference to the shared `TreeType` — it holds no copy of the heavy state. Thousands of `Tree` objects all point to the same 3 `TreeType` instances in memory.
- The `Forest.draw()` / `forest.draw()` loop calls `tree.draw()`, which delegates to `tree_type.draw(self.x, self.y)` — extrinsic coordinates are passed as arguments at draw time, not stored in the flyweight.

### When to use
Rendering large numbers of similar objects (game particles, map tiles, UI icons, text glyphs), or any scenario where object count is in the thousands and memory is constrained.

***

## 7. Bridge

### What it does
**Decouples an abstraction from its implementation** by holding a reference to an implementor rather than inheriting from one. Both the abstraction hierarchy and the implementor hierarchy can grow independently.

### Structure in your code
```
Renderer (implementor interface)
  ├── VectorRenderer   ← render_circle / render_square as vector
  └── RasterRenderer   ← render_circle / render_square as pixels

Shape (abstraction)    — holds self._renderer / this.renderer
  ├── Circle           ← draw() calls self._renderer.render_circle(radius)
  └── Square           ← draw() calls self._renderer.render_square(side)
```
2 shapes × 2 renderers = 4 combinations from 4 classes. Without Bridge, you'd need `VectorCircle`, `RasterCircle`, `VectorSquare`, `RasterSquare` — 4 subclasses just for 2×2, scaling as M×N.

### Key details from your code
- The renderer is **injected at construction time**: `Circle(vector, 5)` — the shape doesn't decide how it is rendered; the caller does. Swapping `vector` for `raster` changes the rendering backend without touching `Circle`.
- `resize()` modifies `self._radius` / `this.radius` directly. The next `draw()` call picks up the new value and delegates to the renderer — the renderer itself is stateless.
- There is a minor typo in `shape_renderer.py`: `Shape.__init__` is defined as `__init_Circle_` (likely a copy-paste artefact). The `Circle` and `Square` subclasses call `super().__init__(renderer)` which bypasses this, so the code still works — but the base `Shape.__init__` itself is never invoked correctly.
- Java's `Shape` declares `renderer` as `protected final Renderer` — subclasses access it directly without a getter. Python uses `self._renderer` (private by convention), accessed only within the subclass methods.

### When to use
When both the abstraction and implementation need to be extensible independently — rendering engines with multiple backends, database drivers behind a query abstraction, platform-specific UI controls, or any system where a M×N inheritance explosion is approaching.

***

## Python vs Java Comparison

| Dimension | Python | Java |
|---|---|---|
| **Interface definition** | `ABC` + `@abstractmethod` | `interface` keyword |
| **Interface enforcement** | Runtime `TypeError` on instantiation | Compile-time error |
| **Proxy interface compliance** | `ProxyImage` skips inheriting `Image` — informal duck typing | `ProxyImage implements Image` — compiler enforced |
| **Flyweight immutability** | `@dataclass(frozen=True)` — runtime-enforced, auto-hashes | `private final` fields — convention only, no runtime lock |
| **Flyweight cache key** | `Tuple` — structural, hashable, type-safe | Concatenated `String` — fragile if values contain separator |
| **Composite child storage** | `List[FileSystemItem]` — typed with generics via hint | `List<FileSystemItem>` — compile-time generic type check |
| **Composite size aggregation** | `sum(child.size() for child in ...)` — one-liner generator | `stream().mapToInt(...).sum()` — streams API, more verbose |
| **Decorator base class** | Concrete class — no `abstract` keyword | `abstract class` — compiler prevents direct instantiation |
| **Decorator field access** | `self._coffee` — private by convention | `protected final Coffee coffee` — enforced by compiler |
| **Bridge renderer field** | `self._renderer` — private by convention | `protected final Renderer renderer` — accessible in subclass |
| **Method naming** | `snake_case` (`play_vlc`, `render_circle`) | `camelCase` (`playVlc`, `renderCircle`) |
| **Null / None guard** | `if self._real_image is None` | `if (realImage == null)` |
| **Boilerplate per class** | Low — no getters/setters, no `@Override` | High — setters, `@Override`, access modifiers on every member |
| **Overall verbosity** | Significantly lower | Higher — explicit typing and access control everywhere |

***

## Pattern Comparison by Concern

| | Facade | Proxy | Adapter | Decorator | Composite | Flyweight | Bridge |
|---|---|---|---|---|---|---|---|
| **Solves** | Subsystem complexity | Access control | Interface mismatch | Runtime behaviour extension | Tree uniformity | Memory overconsumption | Abstraction/impl coupling |
| **Wraps** | Multiple objects | One real subject | One adaptee | One component | Its own children | Shared state object | An implementor hierarchy |
| **Client aware of wrapping?** | No | No | No | Yes — builds the chain | No | No | Yes — injects implementor |
| **Recursive?** | No | No | No | Yes — chain delegation | Yes — tree traversal | No | No |
| **Grows in** | Subsystem size | Access logic | Adaptee methods | Decorator count | Tree depth | Object count | M × N combinations |
| **Real-world analog** | API gateway, SDK facade | Lazy load, auth proxy, cache | Legacy wrapper, ORM adapter | Middleware, I/O streams | DOM tree, UI hierarchy | Text glyphs, game particles | DB drivers, render backends |