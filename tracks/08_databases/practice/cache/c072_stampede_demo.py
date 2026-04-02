# Story:
# Cache stampede: many threads miss at the same time and all hit the DB.
# This demo compares unprotected vs protected (single-flight) rebuilds.

import threading
import time


THREADS = 10
DB_DELAY = 0.08


def _fake_db_fetch(key, counter, counter_lock):
    # Simulate slow DB latency with a visible counter.
    time.sleep(DB_DELAY)
    with counter_lock:
        counter["count"] += 1
    return f"value-for-{key}-{int(time.time() * 1000)}"


def _worker_no_protection(key, cache, counter, counter_lock, start_barrier):
    start_barrier.wait()
    if key in cache:
        return
    value = _fake_db_fetch(key, counter, counter_lock)
    cache[key] = value


def _worker_with_lock(key, cache, counter, counter_lock, rebuild_lock, start_barrier):
    start_barrier.wait()
    if key in cache:
        return
    with rebuild_lock:
        if key in cache:
            return
        value = _fake_db_fetch(key, counter, counter_lock)
        cache[key] = value


def _run_mode(label, worker_fn, use_lock=False):
    cache = {}
    counter = {"count": 0}
    counter_lock = threading.Lock()
    rebuild_lock = threading.Lock()
    start_barrier = threading.Barrier(THREADS)

    threads = []
    start = time.perf_counter()
    for _ in range(THREADS):
        if use_lock:
            thread = threading.Thread(
                target=worker_fn,
                args=(
                    "menu:pizza",
                    cache,
                    counter,
                    counter_lock,
                    rebuild_lock,
                    start_barrier,
                ),
            )
        else:
            thread = threading.Thread(
                target=worker_fn,
                args=(
                    "menu:pizza",
                    cache,
                    counter,
                    counter_lock,
                    start_barrier,
                ),
            )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    elapsed_ms = (time.perf_counter() - start) * 1000
    print("=" * 72)
    print(label)
    print(f"Threads: {THREADS}")
    print(f"DB fetch count: {counter['count']}")
    print(f"Total elapsed: {elapsed_ms:.2f} ms")
    return counter["count"], elapsed_ms


def run_stampede_demo():
    print("Cache stampede demo: unprotected vs single-flight")

    unprotected_count, _ = _run_mode(
        "Mode A - no protection",
        _worker_no_protection,
        use_lock=False,
    )

    protected_count, _ = _run_mode(
        "Mode B - protected (single-flight lock)",
        _worker_with_lock,
        use_lock=True,
    )

    print("=" * 72)
    print("Summary")
    print(f"Unprotected DB fetches: {unprotected_count}")
    print(f"Protected DB fetches:   {protected_count}")

    if protected_count == 1 and unprotected_count > 1:
        print("Result: lock prevented the stampede.")
    else:
        print("Result: behavior unexpected; check threading settings.")


if __name__ == "__main__":
    run_stampede_demo()

# Takeaway:
# Stampede happens when many misses rebuild the same key at once.
