# Python Advanced Patterns — Documentation

## Overview

These 5 patterns are all **Python-native** — they leverage the language's object model directly rather than wrapping external abstractions. They operate at different levels of the execution stack, from function calls to class creation.

| Pattern | File(s) | Operates on | Python hook |
|---|---|---|---|
| **Decorator** | `decorator.py` | Functions / methods | `@syntax`, closures, `functools.wraps` |
| **Context Manager** | `connection_manager_class-based.py`, `connection_manage_generator.py` | Resource blocks | `__enter__` / `__exit__`, `@contextmanager` |
| **Generator** | `data_pipeline.py` | Iteration / sequences | `yield`, `StopIteration` |
| **Descriptor** | `descriptor.py` | Attribute access | `__get__` / `__set__` / `__delete__` |
| **Metaclass** | `plugin_system.py` | Class creation | `type.__new__`, `__call__` |

***

## 1. Decorator — `decorator.py`

### What it does
Wraps a function with additional behaviour **without modifying its source code**. Each decorator is a higher-order function that returns a new `wrapper` function.

### Structure
```
@timer           ← outermost — runs last on entry, first on exit
@logger
@requires_auth
@retry(max_attempts=2)
def get_profile(...): ...
```
Decorators stack bottom-up: `retry` wraps the raw function first, then `requires_auth` wraps that, and so on.

### Key details from your code
- `@functools.wraps(func)` — preserves `__name__`, `__doc__`, and `__module__` on the wrapper; without it, all wrapped functions would appear as `"wrapper"` in logs and tracebacks.
- `retry` is a **parametrized decorator** — a factory that returns the actual decorator, enabling `@retry(max_attempts=2)` syntax.
- `requires_auth` reads from `kwargs`, which means it is **order-sensitive**: it must sit above `retry` in the stack so the `user` kwarg is still available when auth runs.

### When to use
Adding cross-cutting concerns (logging, timing, auth, caching, rate-limiting) to functions without coupling that logic to business code.

***

## 2. Context Manager — `connection_manager_class-based.py` & `connection_manage_generator.py`

### What it does
Guarantees **setup and teardown** around a block of code — even when exceptions occur — by binding resource lifecycle to the `with` statement.
### Two styles, same contract

**Class-based** (`connection_manager_class-based.py`) — explicit, full control:
```python
def __enter__(self):   # setup — returns the resource
def __exit__(self, exc_type, exc_value, traceback):  # teardown
    return False       # False = don't suppress exceptions
```

**Generator-based** (`connection_manage_generator.py`) — less boilerplate:
```python
@contextmanager
def database_connection(db_name):
    # setup
    try:
        yield connection   # ← split point
    except Exception as e:
        # rollback
        raise
    finally:
        # teardown — always runs
```

### Key details from your code
- Both files use a **database connection** as the domain, making setup (connect) and teardown (close) immediately obvious.
- `return False` in `__exit__` re-raises the exception to the caller. Returning `True` would silently swallow it — almost never the right choice.
- In the generator style, `raise` inside `except` is mandatory to propagate the error after rolling back. Omitting it would suppress the exception entirely.
- The `finally` block in the generator style is the safe teardown zone — it runs whether `yield` returned normally or raised.

### When to use
Any resource that must be released: file handles, DB connections, network sockets, locks, temporary directories, or transaction scopes.

***

## 3. Generator — `data_pipeline.py`

### What it does
Produces values **one at a time** via `yield`, suspending execution between each value. The calling loop drives progress — the generator never runs ahead of consumption. [ppl-ai-file-upload.s3.amazonaws]

### Structure in your code
Four generators chained into a pipeline: [ppl-ai-file-upload.s3.amazonaws]
```
read_logs()        →  yields raw log lines one at a time
  └─ filter_errors()  →  yields only ERROR lines
       └─ parse_errors()  →  yields structured dicts
            └─ take(3, ...)   →  yields max 3 results
```
Nothing executes until the `for` loop at the end consumes the pipeline. [ppl-ai-file-upload.s3.amazonaws]

### Key details from your code
- **Lazy evaluation**: `read_logs` opens the file conceptually but only processes one line per `next()` call — no list is ever built in memory. [ppl-ai-file-upload.s3.amazonaws]()
- **Infinite sequence**: `fibonacci()` uses `while True` safely because the consumer (`take` or a list comprehension) controls termination. [ppl-ai-file-upload.s3.amazonaws]()
- **Generator expression**: `(x ** 2 for x in range(1, 6))` is syntactic sugar for a single-expression generator function — parentheses, not brackets. [ppl-ai-file-upload.s3.amazonaws]()
- `Generator[str, None, None]` type hint reads as: yields `str`, accepts nothing via `send()`, returns `None` on completion. [ppl-ai-file-upload.s3.amazonaws]()

### When to use
Processing large or infinite sequences, streaming data pipelines, reading large files line by line, or any case where building the full result list upfront is wasteful or impossible.

***

## 4. Descriptor — `descriptor.py`

### What it does
Intercepts **attribute access, assignment, and deletion** at the class level, enabling reusable validation and computed properties across any model that declares the descriptor as a class attribute.

### Structure in your code
Two reusable descriptors plug into the `User` model:
```python
class User:
    name  = TypedField(str)       # class-level — shared, not per-instance
    email = TypedField(str)
    age   = RangeField(0, 150)
```
Actual values are stored per-instance under private keys (`_name`, `_email`, `_age`) to avoid collisions with the descriptor objects themselves.

### Key details from your code
- `__set_name__` fires **at class body parse time**, automatically wiring `public_name = "age"` and `private_name = "_age"` without any manual configuration.
- `__get__` checks `if instance is None` — when accessed on the class (`User.age`), it returns the descriptor object itself rather than raising `AttributeError`. This is how `User.age` remains introspectable.
- Both descriptors implement `__set__`, making them **data descriptors** — they take priority over the instance `__dict__`, so no instance variable can shadow the validation.
- `TypedField` uses `isinstance()` (not `type() ==`) so subclasses pass validation correctly.

### When to use
Reusable field-level validation across multiple model classes — the same pattern used by Django's `models.Field`, SQLAlchemy's `Column`, and Python's built-in `@property`. Prefer `@property` for one-off computed attributes on a single class; use a full descriptor when the same logic appears on three or more classes.

***

## 5. Metaclass — `plugin_system.py`

### What it does
Controls **class creation itself** — `PluginMeta` intercepts the moment each subclass is defined and performs registration, validation, and attribute injection before any instance is ever created.

### Structure in your code
```python
class PluginMeta(type):
    def __new__(mcs, name, bases, namespace): ...   # fires at class definition
    def __call__(cls, *args, **kwargs): ...          # fires at instantiation

class PluginBase(metaclass=PluginMeta): ...         # base wires the metaclass
class EmailPlugin(PluginBase):                       # auto-registered on definition
    plugin_name = "email"
```

### Key details from your code
- **Registration at definition time** — `_registry["email"] = EmailPlugin` happens the moment Python finishes reading the `class EmailPlugin` block, before any `__init__` is called.
- The `is_base` guard (`not any(isinstance(b, PluginMeta) for b in bases)`) skips `PluginBase` itself so only concrete subclasses are validated and registered.
- `plugin_id` is **injected** via `cls.plugin_id = name.lower()` directly in `__new__` — concrete classes get this attribute for free without declaring it.
- Duplicate `plugin_name` raises `ValueError` at class definition time, not at runtime — a fail-fast guarantee.
- `get_registry` is defined on the metaclass, meaning it is a method on the **class** `PluginBase`, not on its instances.

### When to use
Framework-level concerns: auto-discovering and registering subclasses, enforcing a class-level contract across an entire hierarchy, or injecting shared behaviour into every class. Prefer `__init_subclass__` for simpler registration hooks — reach for a full metaclass only when you need `__new__`, `__call__`, or `__prepare__`.

***

## Pattern-Level Comparison

| | Decorator | Context Manager | Generator | Descriptor | Metaclass |
|---|---|---|---|---|---|
| **Controls** | Function behaviour | Resource lifecycle | Value production | Attribute access | Class creation |
| **Entry point** | `@` syntax | `with` statement | `for` / `next()` | `.attr` read/write | `class Foo(Base)` |
| **Key dunder(s)** | `__wrapped__` via `wraps` | `__enter__`, `__exit__` | `__iter__`, `__next__` | `__get__`, `__set__` | `__new__`, `__call__` |
| **Execution timing** | At every call | At block entry/exit | Lazily, on demand | At every attr access | At class definition |
| **Reusability scope** | Any callable | Any resource block | Any iteration | Any class attribute | Any subclass |
| **Boilerplate** | Low | Low–Medium | Low | Medium | High |
| **Real-world analog** | Flask `@app.route`, `@cache` | `open()`, DB sessions | `range()`, file readline | Django `Field`, `@property` | Django `ModelBase`, pytest |
| **Reach for it when** | Cross-cutting function concerns | Guaranteed cleanup | Large / infinite sequences | Reusable field validation | Framework-level class enforcement |

***

## Layering the Patterns

These patterns are not mutually exclusive — in production code they frequently combine:

```python
# Descriptor uses a Context Manager for thread-safe writes
class ThreadSafeField:
    def __set__(self, instance, value):
        with instance._lock:          # ← Context Manager inside Descriptor
            setattr(instance, self.private_name, value)

# Metaclass installs Descriptors automatically
class AutoValidateMeta(type):
    def __new__(mcs, name, bases, ns):
        for k, v in ns.items():
            if isinstance(v, type) and issubclass(v, int):
                ns[k] = RangeField(0, 100)   # ← Descriptor injected by Metaclass
        return super().__new__(mcs, name, bases, ns)

# Generator fed through a Decorator for logging
@logger                               # ← Decorator wraps a Generator function
def stream_events():
    for event in read_logs("events.log"):
        yield event
```