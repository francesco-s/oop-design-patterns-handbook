import time

# Style 1 — Class-based (__enter__ / __exit__)

class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name    = db_name
        self.connection = None

    # Called at the start of the `with` block
    def __enter__(self):
        print(f"[DB] Connecting to '{self.db_name}'...")
        self.connection = {"db": self.db_name, "open": True}  # simulate connection
        print(f"[DB] Connection established")
        return self.connection  # bound to the `as` variable

    # Called at the end of the `with` block — always, even on exception
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"[DB] Exception caught: {exc_value} — rolling back")
        print(f"[DB] Closing connection to '{self.db_name}'")
        self.connection["open"] = False
        return False  # False = don't suppress the exception


# Example usage
if __name__ == "__main__":
    print("-- Successful query --")
    with DatabaseConnection("users.db") as conn:
        print(f"     Querying open={conn['open']}")

    print()
    print("-- Query with exception --")
    try:
        with DatabaseConnection("orders.db") as conn:
            print(f"     Querying open={conn['open']}")
            raise ValueError("Malformed SQL query")
    except ValueError as e:
        print(f"     Handled: {e}")
