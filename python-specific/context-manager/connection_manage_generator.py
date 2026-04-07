from contextlib import contextmanager


@contextmanager
def database_connection(db_name: str):
    # __enter__ phase
    print(f"[DB] Connecting to '{db_name}'...")
    connection = {"db": db_name, "open": True}
    print(f"[DB] Connection established")

    try:
        yield connection          # hands control to the `with` block
    except Exception as e:
        print(f"[DB] Exception caught: {e} — rolling back")
        raise                     # re-raise so the caller sees it
    finally:
        # __exit__ phase — always runs
        print(f"[DB] Closing connection to '{db_name}'")
        connection["open"] = False


# Example usage
if __name__ == "__main__":
    print("-- Successful query --")
    with database_connection("users.db") as conn:
        print(f"     Querying open={conn['open']}")

    print()
    print("-- Query with exception --")
    try:
        with database_connection("orders.db") as conn:
            print(f"     Querying open={conn['open']}")
            raise ValueError("Malformed SQL query")
    except ValueError as e:
        print(f"     Handled: {e}")

