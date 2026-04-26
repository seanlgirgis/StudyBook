# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : 01_threading_for_io_bound.py
# Covers  : threading for I/O-bound work, GIL behavior, thread safety, queues
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python 01_threading_for_io_bound.py
# ============================================================

from __future__ import annotations

import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def simulate_api_call(endpoint: str, delay_s: float = None) -> dict:
    """
    Simulate an HTTP API call with I/O latency (time.sleep).
    delay_s defaults to random uniform 0.1–0.5s if None.
    Return:
      { endpoint: str, status: "ok", data: {"value": random_float},
        latency_ms: float, thread_name: str }
    Use threading.current_thread().name for thread_name.
    """
    if delay_s is None:
        delay_s = random.uniform(0.1, 0.5)

    start = time.perf_counter()
    time.sleep(delay_s)
    latency_ms = (time.perf_counter() - start) * 1000

    return {
        "endpoint": endpoint,
        "status": "ok",
        "data": {"value": random.random()},
        "latency_ms": latency_ms,
        "thread_name": threading.current_thread().name,
    }


def fetch_sequential(endpoints: list[str]) -> list[dict]:
    """
    Fetch endpoints one at a time. Return list of results in order.
    Print total time at end.
    """
    start = time.perf_counter()
    results = [simulate_api_call(endpoint) for endpoint in endpoints]
    elapsed = time.perf_counter() - start

    print(f"Sequential fetch completed in {elapsed:.2f} s")
    return results


def fetch_threaded(endpoints: list[str], max_workers: int = 10) -> list[dict]:
    """
    Use ThreadPoolExecutor(max_workers=max_workers).
    Submit all endpoints, collect via futures in submission order.
    Return list of results in original order.
    Print total time at end.
    Note: order is preserved by zipping futures with endpoints.
    """
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(simulate_api_call, endpoint) for endpoint in endpoints]

        results = []
        for endpoint, future in zip(endpoints, futures):
            result = future.result()
            result["endpoint"] = endpoint
            results.append(result)

    elapsed = time.perf_counter() - start

    print(f"Threaded fetch completed in {elapsed:.2f} s")
    return results


def benchmark_threading(n_endpoints: int = 20) -> dict:
    """
    Generate n_endpoints fake URLs: ["http://api.example.com/sensor/{i}" for i in range(n)]
    Time fetch_sequential and fetch_threaded on same list.
    Return:
      { n_endpoints: int, sequential_s: float, threaded_s: float,
        speedup_x: float, max_workers: int }
    Print formatted result:
      Sequential : 4.82 s
      Threaded   : 0.51 s
      Speedup    : 9.5×  ← approaches max_workers because GIL releases on sleep()
    Also print the GIL explanation:
      "WHY: time.sleep() (and real I/O) releases the GIL. While one thread waits,
       others run. Threading is effective for I/O-bound work precisely because of this."
    """
    endpoints = [f"http://api.example.com/sensor/{i}" for i in range(n_endpoints)]
    max_workers = 10

    start = time.perf_counter()
    fetch_sequential(endpoints)
    sequential_s = time.perf_counter() - start

    start = time.perf_counter()
    fetch_threaded(endpoints, max_workers=max_workers)
    threaded_s = time.perf_counter() - start

    speedup_x = sequential_s / threaded_s if threaded_s > 0 else float("inf")

    print(f"Sequential : {sequential_s:.2f} s")
    print(f"Threaded   : {threaded_s:.2f} s")
    print(
        f"Speedup    : {speedup_x:.1f}×  "
        f"← approaches max_workers because GIL releases on sleep()"
    )
    print(
        "WHY: time.sleep() (and real I/O) releases the GIL. While one thread waits,\n"
        "others run. Threading is effective for I/O-bound work precisely because of this."
    )

    return {
        "n_endpoints": n_endpoints,
        "sequential_s": sequential_s,
        "threaded_s": threaded_s,
        "speedup_x": speedup_x,
        "max_workers": max_workers,
    }


def demonstrate_thread_safety_bug() -> None:
    """
    Shared counter incremented by 10 threads, 10_000 times each.
    Expected: 100_000. Actual: less (race condition).
    Print both values. Explain:
      "WHY: counter += 1 is not atomic. It compiles to: LOAD counter, ADD 1, STORE counter.
       The GIL can switch threads between LOAD and STORE."
    Use threading.Thread directly (not ThreadPoolExecutor).
    """
    counter = 0
    n_threads = 10
    increments_per_thread = 10_000

    def worker() -> None:
        nonlocal counter
        for _ in range(increments_per_thread):
            current = counter
            if random.random() < 0.0005:
                time.sleep(0)
            counter = current + 1

    threads = [
        threading.Thread(target=worker, name=f"CounterBug-{i}")
        for i in range(n_threads)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    expected = n_threads * increments_per_thread

    print(f"Expected: {expected:,}")
    print(f"Actual  : {counter:,}")
    print(
        "WHY: counter += 1 is not atomic. It compiles to: LOAD counter, ADD 1, STORE counter.\n"
        "The GIL can switch threads between LOAD and STORE."
    )


def demonstrate_thread_safety_fix() -> None:
    """
    Same as bug demo but use threading.Lock() around counter += 1.
    Show final value == 100_000.
    Print lock acquire/release overhead estimate (time the whole operation).
    Explain:
      "Lock serialises the critical section. For high-contention counters, prefer
       threading.local() or queue.Queue to avoid lock overhead entirely."
    """
    counter = 0
    lock = threading.Lock()
    n_threads = 10
    increments_per_thread = 10_000

    def worker() -> None:
        nonlocal counter
        for _ in range(increments_per_thread):
            with lock:
                counter += 1

    threads = [
        threading.Thread(target=worker, name=f"CounterFix-{i}")
        for i in range(n_threads)
    ]

    start = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start
    expected = n_threads * increments_per_thread
    overhead_us = (elapsed / expected) * 1_000_000

    print(f"Expected: {expected:,}")
    print(f"Actual  : {counter:,}")
    print(f"Lock timing: {elapsed:.4f} s total, about {overhead_us:.2f} µs per increment")
    print(
        "Lock serialises the critical section. For high-contention counters, prefer\n"
        "threading.local() or queue.Queue to avoid lock overhead entirely."
    )


def producer_consumer_queue(
    n_producers: int = 3,
    n_consumers: int = 2,
    n_items: int = 30,
) -> None:
    """
    Classic producer-consumer using queue.Queue (thread-safe, built-in blocking).
    Producers: put items {"id": i, "value": random_float, "producer": name}
    Consumers: get items, "process" them (time.sleep 0.05), track count
    Use sentinel value None to signal consumers to stop (one per consumer).
    Print:
      Producer-0 put item 0
      Consumer-1 processed item 0
      ...
      All done. Items produced: 30  Items consumed: 30  Time: 1.23s
    Explain:
      "queue.Queue.get() blocks without spinning, releasing the GIL while waiting.
       This is the canonical thread-safe handoff in Python pipelines."
    """
    work_queue: queue.Queue[dict | None] = queue.Queue()
    produced_count = 0
    consumed_count = 0
    produced_lock = threading.Lock()
    consumed_lock = threading.Lock()

    items_by_producer = [[] for _ in range(n_producers)]
    for item_id in range(n_items):
        items_by_producer[item_id % n_producers].append(item_id)

    def producer(producer_index: int) -> None:
        nonlocal produced_count
        producer_name = f"Producer-{producer_index}"

        for item_id in items_by_producer[producer_index]:
            item = {
                "id": item_id,
                "value": random.random(),
                "producer": producer_name,
            }
            work_queue.put(item)

            with produced_lock:
                produced_count += 1

            print(f"{producer_name} put item {item_id}")

    def consumer(consumer_index: int) -> None:
        nonlocal consumed_count
        consumer_name = f"Consumer-{consumer_index}"

        while True:
            item = work_queue.get()

            try:
                if item is None:
                    print(f"{consumer_name} received stop signal")
                    return

                time.sleep(0.05)

                with consumed_lock:
                    consumed_count += 1

                print(f"{consumer_name} processed item {item['id']}")
            finally:
                work_queue.task_done()

    start = time.perf_counter()

    consumer_threads = [
        threading.Thread(target=consumer, args=(i,), name=f"ConsumerThread-{i}")
        for i in range(n_consumers)
    ]
    producer_threads = [
        threading.Thread(target=producer, args=(i,), name=f"ProducerThread-{i}")
        for i in range(n_producers)
    ]

    for thread in consumer_threads:
        thread.start()

    for thread in producer_threads:
        thread.start()

    for thread in producer_threads:
        thread.join()

    for _ in range(n_consumers):
        work_queue.put(None)

    work_queue.join()

    for thread in consumer_threads:
        thread.join()

    elapsed = time.perf_counter() - start

    print(
        f"All done. Items produced: {produced_count}  "
        f"Items consumed: {consumed_count}  Time: {elapsed:.2f}s"
    )
    print(
        "queue.Queue.get() blocks without spinning, releasing the GIL while waiting.\n"
        "This is the canonical thread-safe handoff in Python pipelines."
    )


def main():
    print("\n=== THREADING BENCHMARK: Sequential vs Threaded ===")
    stats = benchmark_threading(n_endpoints=20)
    print(f"Speedup: {stats['speedup_x']:.1f}×")

    print("\n=== THREAD SAFETY BUG ===")
    demonstrate_thread_safety_bug()

    print("\n=== THREAD SAFETY FIX ===")
    demonstrate_thread_safety_fix()

    print("\n=== PRODUCER-CONSUMER QUEUE ===")
    producer_consumer_queue(n_producers=3, n_consumers=2, n_items=30)


if __name__ == "__main__":
    main()