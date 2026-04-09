from typing import Any, Type


# ── Descriptor 1: enforces a type ────────────────────────────────────────────

class TypedField:
    """Data descriptor: validates type on every assignment."""

    def __set_name__(self, owner: Type, name: str) -> None:
        # Called automatically when the class body is processed.
        # Stores both the public name ('name') and private storage key ('_name').
        self.public_name  = name
        self.private_name = f"_{name}"

    def __init__(self, expected_type: Type) -> None:
        self.expected_type = expected_type

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            # Accessed on the class itself (e.g. User.name) → return the descriptor
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"'{self.public_name}' expects {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, self.private_name, value)

    def __delete__(self, instance: Any) -> None:
        print(f"[TypedField] Deleting '{self.public_name}'")
        setattr(instance, self.private_name, None)


# ── Descriptor 2: enforces a numeric range ────────────────────────────────────

class RangeField:
    """Data descriptor: validates type AND range on every assignment."""

    def __set_name__(self, owner: Type, name: str) -> None:
        self.public_name  = name
        self.private_name = f"_{name}"

    def __init__(self, min_value: float, max_value: float) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"'{self.public_name}' must be a number, got {type(value).__name__}"
            )
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"'{self.public_name}' must be between "
                f"{self.min_value} and {self.max_value}, got {value}"
            )
        setattr(instance, self.private_name, value)


# ── Model using the descriptors ───────────────────────────────────────────────

class User:
    # Each descriptor is a CLASS-level attribute, shared across all instances.
    # __set_name__ fires here, wiring 'name' → '_name', 'email' → '_email', etc.
    name  = TypedField(str)
    email = TypedField(str)
    age   = RangeField(0, 150)

    def __init__(self, name: str, email: str, age: int) -> None:
        self.name  = name    # triggers TypedField.__set__
        self.email = email   # triggers TypedField.__set__
        self.age   = age     # triggers RangeField.__set__

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r}, age={self.age})"


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("-- Valid user --")
    u = User("Alice", "alice@example.com", 30)
    print(u) # Calls User.__repr__, which accesses the descriptors via self.name, self.email, self.age

    print()
    print("-- Update age --")
    u.age = 31 # Calls RangeField.__set__ to validate and update the age value
    print(f"  New age: {u.age}") # Calls RangeField.__get__ to retrieve the age value

    print()
    print("-- Delete name --")
    del u.name # Calls TypedField.__delete__, which sets _name to None
    print(f"  Name after delete: {u.name}") # Calls TypedField.__get__ to retrieve the name value

    print()
    print("-- Access descriptor on the class (not an instance) --")
    print(f"  User.age → {User.age}")   # returns the descriptor itself

    print()
    print("-- Type error --")
    try:
        u.name = 42               # int instead of str
    except TypeError as e:
        print(f"  TypeError: {e}")

    print()
    print("-- Range error --")
    try:
        u.age = 200               # exceeds max 150
    except ValueError as e:
        print(f"  ValueError: {e}")
