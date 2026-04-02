# Story:
# Cache locks: protect shared state with a lock to avoid races.
# This demo shows incorrect results without a lock, correct with a lock.

import threading
import time


THREADS = 12
INCREMENTS_PER_THREAD = 400


def _worker_no_lock(state, start_barrier):
    start_barrier.wait()
    for _ in range(INCREMENTS_PER_THREAD):
        value = state["counter"]
        time.sleep(0.0001)
        state["counter"] = value + 1


def _worker_with_lock(state, lock, start_barrier):
    start_barrier.wait()
    for _ in range(INCREMENTS_PER_THREAD):
        with lock:
            value = state["counter"]
            time.sleep(0.0001)
            state["counter"] = value + 1


def _run_mode(label, worker_fn, use_lock=False):
    state = {"counter": 0}
    lock = threading.Lock()
    start_barrier = threading.Barrier(THREADS)

    threads = []
    start = time.perf_counter()
    for _ in range(THREADS):
        if use_lock:
            thread = threading.Thread(
                target=worker_fn,
                args=(state, lock, start_barrier),
            )
        else:
            thread = threading.Thread(
                target=worker_fn,
                args=(state, start_barrier),
            )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    elapsed_ms = (time.perf_counter() - start) * 1000
    expected = THREADS * INCREMENTS_PER_THREAD

    print("=" * 72)
    print(label)
    print(f"Threads: {THREADS}")
    print(f"Expected final value: {expected}")
    print(f"Actual final value:   {state['counter']}")
    print(f"Elapsed: {elapsed_ms:.2f} ms")

    return expected, state["counter"], elapsed_ms


def run_locks_demo():
    print("Cache locks demo: race vs protected update")

    expected, actual_no_lock, _ = _run_mode(
        "Mode A - no lock",
        _worker_no_lock,
        use_lock=False,
    )

    _, actual_with_lock, _ = _run_mode(
        "Mode B - with lock",
        _worker_with_lock,
        use_lock=True,
    )

    print("=" * 72)
    print("Summary")
    print(f"Expected: {expected}")
    print(f"No lock actual:  {actual_no_lock}")
    print(f"With lock actual:{actual_with_lock}")

    if actual_with_lock == expected and actual_no_lock != expected:
        print("Result: lock fixed the race.")
    else:
        print("Result: behavior unexpected; tweak thread settings if needed.")


if __name__ == "__main__":
    run_locks_demo()

# Takeaway:
# Locks coordinate access; they do not make the work faster.
