import time
import functools


# Decorator 1 — measures execution time
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"[Timer]  '{func.__name__}' ran in {(end - start) * 1000:.2f}ms")
        return result
    return wrapper


# Decorator 2 — logs calls
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Logger] Calling '{func.__name__}' with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[Logger] '{func.__name__}' returned: {result}")
        return result
    return wrapper


# Decorator 3 — checks authentication
def requires_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user", "anonymous")
        if user == "anonymous":
            print(f"[Auth]   Access denied for anonymous user")
            return None
        print(f"[Auth]   Access granted for '{user}'")
        return func(*args, **kwargs)
    return wrapper


# Decorator 4 — retry with max attempts
def retry(max_attempts: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"[Retry]  Failed after {max_attempts} attempts: {e}")
                        raise
                    print(f"[Retry]  Attempt {attempt}/{max_attempts} failed, retrying...")
        return wrapper
    return decorator


# Stacking decorators — applied bottom-up: retry → requires_auth → logger → timer
@timer
@logger
@requires_auth
@retry(max_attempts=2)
def get_profile(user_id: int, user: str = "anonymous") -> dict:
    time.sleep(0.01)  # simulate work
    return {"id": user_id, "user": user}


# Example usage
if __name__ == "__main__":
    print("-- Authenticated request --")
    get_profile(42, user="alice")

    print()
    print("-- Unauthenticated request --")
    get_profile(42)
