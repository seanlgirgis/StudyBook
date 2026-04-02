# Story:
# Cache-aside: check cache first, then DB on miss, then store in cache.
# This demo simulates cache hits vs misses with timing.

import time


def _fake_db_fetch(key):
    # Simulate slow DB latency.
    time.sleep(0.08)
    return f"value-for-{key}"


def get_data(key, cache):
    if key in cache:
        return cache[key], "hit"
    value = _fake_db_fetch(key)
    cache[key] = value
    return value, "miss"


def _timed_call(label, key, cache):
    start = time.perf_counter()
    value, status = get_data(key, cache)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{label}: {status.upper()} in {elapsed_ms:.2f} ms -> {value}")
    return elapsed_ms, status


def run_cache_aside_demo():
    cache = {}
    key = "menu:burger"

    print("Cache-aside demo: cache hit vs miss")

    # Scenario A: first access is a miss (DB hit).
    miss_time, _ = _timed_call("Scenario A (first access)", key, cache)

    # Scenario B: repeated access is a hit (cache).
    hit_time, _ = _timed_call("Scenario B (repeat access)", key, cache)

    print("Summary")
    print(f"Miss time: {miss_time:.2f} ms")
    print(f"Hit time:  {hit_time:.2f} ms")
    if hit_time < miss_time:
        print("Result: cache hit is faster than cache miss.")
    else:
        print("Result: timing unexpected; check sleep settings.")


if __name__ == "__main__":
    run_cache_aside_demo()

# Takeaway:
# Cache-aside trades a slow miss for fast repeat hits.
