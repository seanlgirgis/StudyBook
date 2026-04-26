# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : 04_concurrent_futures_patterns.py
# Covers  : unified executor patterns, threading vs multiprocessing, pipelines, failures
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python 04_concurrent_futures_patterns.py
# ============================================================

from __future__ import annotations

import multiprocessing
import os
import random
import threading
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
    TimeoutError,
)


# ─────────────────────────────────────────────────────────────
# Module-level workers (REQUIRED for multiprocessing pickling)
# ─────────────────────────────────────────────────────────────

def simulate_io_fetch(item: str) -> dict:
    """
    Simulate I/O (time.sleep 0.05–0.2s).
    Threading works well here because sleep releases the GIL.
    """
    delay = random.uniform(0.05, 0.2)
    time.sleep(delay)
    return {"item": item, "raw": random.random()}


def simulate_cpu_transform(record: dict) -> dict:
    """
    CPU-heavy transformation.
    Threads would fight over the GIL here — processes are required for parallelism.
    """
    raw = record["raw"]

    # Simulate CPU work (pure Python math)
    value = raw
    for _ in range(500_000):
        value = (value * 1.000001 + 0.000001) % 1.0

    return {
        "item": record["item"],
        "transformed_value": value,
        "quality": "GOOD" if value > 0.1 else "LOW",
        "processed_by_pid": os.getpid(),
    }


# ─────────────────────────────────────────────────────────────
# Generic executor wrapper
# ─────────────────────────────────────────────────────────────

def process_with_executor(
    items: list,
    worker_fn,
    use_processes: bool = False,
    max_workers: int = 4,
) -> list:
    """
    Generic executor wrapper.
    """
    executor_cls = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    executor_name = "ProcessPoolExecutor" if use_processes else "ThreadPoolExecutor"

    start = time.perf_counter()

    with executor_cls(max_workers=max_workers) as executor:
        results = list(executor.map(worker_fn, items))

    elapsed = time.perf_counter() - start

    print(f"{executor_name} completed in {elapsed:.2f} s")
    return results


# ─────────────────────────────────────────────────────────────
# Two-stage pipeline (I/O → CPU)
# ─────────────────────────────────────────────────────────────

def fetch_and_transform(items: list[str]) -> list[dict]:
    """
    Two-stage pipeline:
      Stage 1: ThreadPoolExecutor (I/O)
      Stage 2: ProcessPoolExecutor (CPU)
    """
    print("Stage 1 (I/O - threads)...")
    t1 = time.perf_counter()
    fetched = process_with_executor(items, simulate_io_fetch, use_processes=False, max_workers=10)
    t1_elapsed = time.perf_counter() - t1

    print("Stage 2 (CPU - processes)...")
    t2 = time.perf_counter()
    transformed = process_with_executor(fetched, simulate_cpu_transform, use_processes=True, max_workers=os.cpu_count())
    t2_elapsed = time.perf_counter() - t2

    print(f"Stage 1 time: {t1_elapsed:.2f} s")
    print(f"Stage 2 time: {t2_elapsed:.2f} s")
    print(f"Total time : {t1_elapsed + t2_elapsed:.2f} s")

    return transformed


# ─────────────────────────────────────────────────────────────
# Partial failure handling
# ─────────────────────────────────────────────────────────────

def handle_partial_failures(items: list, worker_fn, max_workers: int = 4) -> dict:
    """
    Execute all items, but handle failures individually.
    """
    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker_fn, item): item for item in items}

        for future in as_completed(futures):
            item = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                errors.append({"item": item, "error": str(e)})

    print(f"Completed with {len(results)} successes and {len(errors)} errors")

    return {
        "results": results,
        "errors": errors,
        "success_count": len(results),
        "error_count": len(errors),
    }


# ─────────────────────────────────────────────────────────────
# Timeout-aware execution
# ─────────────────────────────────────────────────────────────

def timeout_aware_executor(items: list, worker_fn, timeout_s: float = 0.3) -> dict:
    """
    Handle global and per-task timeouts.
    """
    completed = []
    timed_out = 0

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_fn, item) for item in items]

        try:
            for future in as_completed(futures, timeout=timeout_s):
                try:
                    result = future.result(timeout=timeout_s)
                    completed.append(result)
                except TimeoutError:
                    timed_out += 1
        except TimeoutError:
            # Global timeout reached — cancel remaining
            for f in futures:
                f.cancel()
            timed_out = len(futures) - len(completed)

    return {
        "completed": completed,
        "timed_out_count": timed_out,
        "total": len(items),
    }


# ─────────────────────────────────────────────────────────────
# Context manager demo
# ─────────────────────────────────────────────────────────────

def executor_context_manager_demo() -> None:
    """
    Show that executors clean up resources properly.
    """
    print(f"Threads before: {threading.active_count()}")
    print(f"Processes before: {len(multiprocessing.active_children())}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(lambda x: x * 2, range(10)))

    with ProcessPoolExecutor(max_workers=2) as executor:
        list(executor.map(int, range(10)))

    print(f"Threads after: {threading.active_count()}")
    print(f"Processes after: {len(multiprocessing.active_children())}")

    print("Executors auto-clean via shutdown(wait=True) on exit.")


# ─────────────────────────────────────────────────────────────
# Decision helper
# ─────────────────────────────────────────────────────────────

def choose_executor(task_type: str, data_size_mb: float, n_items: int) -> str:
    """
    Decide which executor to use.
    """
    if task_type == "io":
        choice = "ThreadPoolExecutor"
        reason = "GIL releases on I/O; threads are lightweight"
    elif task_type == "cpu" and data_size_mb > 100:
        choice = "ProcessPoolExecutor"
        reason = "CPU-bound; compute dominates pickling overhead"
    elif task_type == "cpu" and data_size_mb <= 100 and n_items < 100:
        choice = "ThreadPoolExecutor"
        reason = "Small workload; pickling overhead too high"
    else:
        choice = "ProcessPoolExecutor"
        reason = "Many tasks; parallel CPU wins"

    print(f"Recommend: {choice} → {reason}")
    return choice


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    items = [f"sensor_{i:03d}" for i in range(20)]

    print("\n=== TWO-STAGE PIPELINE (I/O threads → CPU processes) ===")
    results = fetch_and_transform(items)
    print(f"  Processed {len(results)} items")

    print("\n=== PARTIAL FAILURE HANDLING ===")

    def flaky_worker(item: str) -> dict:
        if hash(item) % 5 == 0:
            raise ValueError(f"Processing failed for {item}")
        time.sleep(0.02)
        return {"item": item, "value": random.random()}

    outcome = handle_partial_failures(items, flaky_worker)
    print(f"  Success: {outcome['success_count']}  Errors: {outcome['error_count']}")

    print("\n=== TIMEOUT-AWARE EXECUTOR ===")

    def slow_worker(item: str) -> dict:
        time.sleep(random.uniform(0.05, 0.5))
        return {"item": item}

    result = timeout_aware_executor(items, slow_worker, timeout_s=0.3)
    print(f"  Completed: {len(result['completed'])}  Timed out: {result['timed_out_count']}")

    print("\n=== EXECUTOR CONTEXT MANAGER ===")
    executor_context_manager_demo()

    print("\n=== EXECUTOR CHOICE ADVISOR ===")
    choose_executor("io",  data_size_mb=0.1, n_items=100)
    choose_executor("cpu", data_size_mb=500, n_items=50)
    choose_executor("cpu", data_size_mb=5,   n_items=20)
    choose_executor("cpu", data_size_mb=5,   n_items=200)


if __name__ == "__main__":
    main()