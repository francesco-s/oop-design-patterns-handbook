from abc import abstractmethod
from typing import Dict, Type


# ── The Metaclass ─────────────────────────────────────────────────────────────

class PluginMeta(type):
    """
    Metaclass that:
      1. Maintains a global registry of every concrete plugin class.
      2. Enforces that each plugin declares a 'plugin_name' class attribute.
      3. Injects a 'plugin_id' attribute (lowercase class name) automatically.
      4. Blocks instantiation of abstract plugins (those with no plugin_name).
    """

    # Shared across ALL classes created by this metaclass
    _registry: Dict[str, "PluginMeta"] = {}

    # ── Called BEFORE the class object is created ──────────────────────────
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)

        # Skip the abstract base class itself (no plugin_name set)
        is_base = not any(isinstance(b, PluginMeta) for b in bases)
        if not is_base:
            # 1. Enforce plugin_name
            if "plugin_name" not in namespace:
                raise TypeError(
                    f"Plugin '{name}' must define a 'plugin_name' class attribute"
                )
            # 2. Inject plugin_id automatically
            cls.plugin_id = name.lower()

            # 3. Register the plugin
            key = namespace["plugin_name"]
            if key in mcs._registry:
                raise ValueError(f"Duplicate plugin_name '{key}' in class '{name}'")
            mcs._registry[key] = cls
            print(f"[PluginMeta] Registered '{name}' as '{key}'")

        return cls

    # ── Called when an INSTANCE is created (i.e. MyPlugin()) ──────────────
    def __call__(cls, *args, **kwargs):
        print(f"[PluginMeta] Instantiating '{cls.__name__}'")
        instance = super().__call__(*args, **kwargs)
        return instance

    # ── Class-level helper — callable on PluginBase itself ─────────────────
    def get_registry(cls) -> Dict[str, "PluginMeta"]:
        return dict(PluginMeta._registry)


# ── Abstract base class using the metaclass ───────────────────────────────────

class PluginBase(metaclass=PluginMeta):
    """All plugins inherit from this. No plugin_name required here."""

    @abstractmethod
    def run(self, payload: str) -> str:
        """Every concrete plugin must implement run()."""
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id='{self.plugin_id}'>"


# ── Concrete plugins — registered automatically at class definition time ───────

class EmailPlugin(PluginBase):
    plugin_name = "email"

    def run(self, payload: str) -> str:
        return f"[EmailPlugin] Sending email: '{payload}'"


class SMSPlugin(PluginBase):
    plugin_name = "sms"

    def run(self, payload: str) -> str:
        return f"[SMSPlugin] Sending SMS: '{payload}'"


class SlackPlugin(PluginBase):
    plugin_name = "slack"

    def run(self, payload: str) -> str:
        return f"[SlackPlugin] Posting to Slack: '{payload}'"


# ── Example usage ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("-- Registry built at class-definition time --")
    for name, cls in PluginBase.get_registry().items():
        print(f"  '{name}' → {cls} (plugin_id='{cls.plugin_id}')")

    print()
    print("-- Dispatch a notification via registry lookup --")
    def notify(channel: str, message: str) -> None:
        registry = PluginBase.get_registry()
        if channel not in registry:
            raise KeyError(f"No plugin registered for channel '{channel}'")
        plugin = registry[channel]()   # triggers PluginMeta.__call__
        print(plugin.run(message))

    notify("email", "Your order has shipped")
    notify("slack", "Deployment succeeded")

    print()
    print("-- Enforce plugin_name rule --")
    try:
        class BrokenPlugin(PluginBase):
            pass              # missing plugin_name → TypeError
    except TypeError as e:
        print(f"  TypeError: {e}")

    print()
    print("-- Enforce unique plugin_name rule --")
    try:
        class DuplicatePlugin(PluginBase):
            plugin_name = "email"   # already taken → ValueError
    except ValueError as e:
        print(f"  ValueError: {e}")
