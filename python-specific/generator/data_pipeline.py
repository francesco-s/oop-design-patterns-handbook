from typing import Generator
import time


# Generator 1 — simulates reading lines from a large log file lazily
def read_logs(filename: str) -> Generator[str, None, None]:
    fake_logs = [
        "2026-04-08 INFO  Server started",
        "2026-04-08 ERROR Disk quota exceeded",
        "2026-04-08 INFO  Request received from 192.168.1.1",
        "2026-04-08 ERROR Database connection timeout",
        "2026-04-08 WARNING High memory usage",
        "2026-04-08 ERROR Failed to write to cache",
        "2026-04-08 INFO  Scheduled job completed",
        "2026-04-08 ERROR Null pointer in payment service",
    ]
    print(f"[read_logs] Opening '{filename}'")
    for line in fake_logs:
        yield line  # produces one line at a time


# Generator 2 — filters only ERROR lines
def filter_errors(lines: Generator) -> Generator[str, None, None]:
    for line in lines:
        if "ERROR" in line:
            yield line


# Generator 3 — parses each error into a structured dict
def parse_errors(lines: Generator) -> Generator[dict, None, None]:
    for line in lines:
        parts = line.split(" ", 3)
        yield {
            "date":    parts[0],
            "time":    parts[1],
            "level":   parts[2],
            "message": parts[3],
        }


# Generator 4 — limits to first n results
def take(n: int, items: Generator) -> Generator:
    for i, item in enumerate(items):
        if i >= n:
            break
        yield item


# Example usage
if __name__ == "__main__":
    # Build the pipeline — nothing runs yet
    lines   = read_logs("app.log")
    errors  = filter_errors(lines)
    parsed  = parse_errors(errors)
    results = take(3, parsed)

    print("-- Processing pipeline (lazy) --")
    for entry in results:
        print(f"  [{entry['time']}] {entry['message']}")

    print()

    # Generator as infinite sequence
    print("-- Infinite Fibonacci (first 8) --")
    def fibonacci() -> Generator[int, None, None]:
        a, b = 0, 1
        while True:       # infinite — safe because we consume lazily
            yield a
            a, b = b, a + b

    fib = fibonacci()
    print([next(fib) for _ in range(8)])

    print()

    # Generator expression (one-liner)
    print("-- Generator expression --")
    squares = (x ** 2 for x in range(1, 6))  # not a list — no [] needed
    print(list(squares))
