# Story:
# TTL cache: values expire after a window, so old data does not live forever.
# This demo shows hit before expiry and miss after expiry.

import time


TTL_SECONDS = 0.8


def _fake_db_fetch(key):
    # Simulate slow DB latency.
    time.sleep(0.08)
    return f"value-for-{key}-{int(time.time() * 1000)}"


def get_data(key, cache, ttl_seconds):
    now = time.time()
    entry = cache.get(key)
    if entry and entry["expires_at"] > now:
        return entry["value"], "hit"
    value = _fake_db_fetch(key)
    cache[key] = {
        "value": value,
        "expires_at": now + ttl_seconds,
    }
    if entry:
        return value, "expired"
    return value, "miss"


def _timed_call(label, key, cache, ttl_seconds):
    start = time.perf_counter()
    value, status = get_data(key, cache, ttl_seconds)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{label}: {status.upper()} in {elapsed_ms:.2f} ms -> {value}")
    return elapsed_ms, status


def run_ttl_demo():
    cache = {}
    key = "menu:soup"

    print("TTL demo: hit before expiry, miss after expiry")
    print(f"TTL seconds: {TTL_SECONDS}")

    # Scenario A: first access is a miss.
    miss_time, _ = _timed_call("Scenario A (first access)", key, cache, TTL_SECONDS)

    # Scenario B: access before expiry is a hit.
    time.sleep(TTL_SECONDS / 3)
    hit_time, _ = _timed_call("Scenario B (before expiry)", key, cache, TTL_SECONDS)

    # Scenario C: wait past expiry, should be a miss again.
    time.sleep(TTL_SECONDS + 0.1)
    expired_time, expired_status = _timed_call(
        "Scenario C (after expiry)",
        key,
        cache,
        TTL_SECONDS,
    )

    print("Summary")
    print(f"Miss time:    {miss_time:.2f} ms")
    print(f"Hit time:     {hit_time:.2f} ms")
    print(f"Expired time: {expired_time:.2f} ms ({expired_status})")

    if hit_time < miss_time and expired_time >= hit_time:
        print("Result: hit was fast, expiry forced a miss again.")
    else:
        print("Result: timing unexpected; check sleep settings.")


if __name__ == "__main__":
    run_ttl_demo()

# Takeaway:
# TTL trades freshness for speed inside the time window.
