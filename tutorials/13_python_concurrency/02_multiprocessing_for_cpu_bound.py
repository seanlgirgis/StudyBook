# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : 02_multiprocessing_for_cpu_bound.py
# Covers  : multiprocessing for CPU-bound work, GIL bypass, pickling overhead, shared memory
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python 02_multiprocessing_for_cpu_bound.py
# ============================================================

from __future__ import annotations

import datetime as dt
import math
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Queue, shared_memory

import numpy as np


SENSOR_RANGES = {
    "temperature": (0.0, 120.0),
    "pressure": (0.0, 15.0),
    "vibration": (0.0, 60.0),
    "humidity": (0.0, 100.0),
}

SENSOR_TYPES = list(SENSOR_RANGES)
PLANTS = ["plant_A", "plant_B", "plant_C"]


def generate_records(n: int = 10_000, seed: int = 42) -> list[dict]:
    """
    Generate n fake sensor records:
      { id: int, raw_value: float, sensor_type: str (one of 4),
        timestamp: str (ISO format), plant: str (one of 3) }
    """
    rng = random.Random(seed)
    base_time = dt.datetime(2026, 1, 1, 0, 0, 0)

    records = []
    for i in range(n):
        sensor_type = SENSOR_TYPES[i % len(SENSOR_TYPES)]
        min_value, max_value = SENSOR_RANGES[sensor_type]

        # Some values intentionally fall outside the valid range so validation
        # has real work to do.
        raw_value = rng.uniform(min_value - 10.0, max_value + 10.0)

        records.append(
            {
                "id": i,
                "raw_value": raw_value,
                "sensor_type": sensor_type,
                "timestamp": (base_time + dt.timedelta(seconds=i)).isoformat(),
                "plant": PLANTS[i % len(PLANTS)],
            }
        )

    return records


def cpu_intensive_transform(records: list[dict]) -> list[dict]:
    """
    CPU-heavy transformation (no I/O, no sleep — pure computation):
      1. Parse timestamp string → datetime object
      2. Validate: raw_value must be in range per sensor_type
         (temperature: 0–120, pressure: 0–15, vibration: 0–60, humidity: 0–100)
      3. Compute derived fields:
           normalised_value = (raw_value - min_range) / (max_range - min_range)
           quality_flag = "GOOD" if in range else "BAD"
           processed_at = datetime.utcnow().isoformat()
      4. Return transformed records list.
    Must be defined at MODULE LEVEL so ProcessPoolExecutor can pickle it.
    """
    transformed = []

    for record in records:
        parsed_ts = dt.datetime.fromisoformat(record["timestamp"])
        sensor_type = record["sensor_type"]
        min_range, max_range = SENSOR_RANGES[sensor_type]
        raw_value = float(record["raw_value"])

        in_range = min_range <= raw_value <= max_range
        normalised_value = (raw_value - min_range) / (max_range - min_range)

        # Deliberate CPU work. This is pure Python math, so threads would fight
        # over the GIL. Processes bypass the GIL by using separate interpreters.
        checksum = 0.0
        for j in range(250):
            checksum += math.sin(raw_value + j) * math.cos(normalised_value + j)

        transformed.append(
            {
                "id": record["id"],
                "raw_value": raw_value,
                "sensor_type": sensor_type,
                "timestamp": record["timestamp"],
                "timestamp_dt": parsed_ts,
                "plant": record["plant"],
                "normalised_value": normalised_value,
                "quality_flag": "GOOD" if in_range else "BAD",
                "processed_at": dt.datetime.utcnow().isoformat(),
                "checksum": checksum,
            }
        )

    return transformed


def transform_sequential(chunks: list[list[dict]]) -> list[list[dict]]:
    """Apply cpu_intensive_transform to each chunk serially. Return list of results."""
    return [cpu_intensive_transform(chunk) for chunk in chunks]


def transform_multiprocess(
    chunks: list[list[dict]],
    n_workers: int = None,
) -> list[list[dict]]:
    """
    ProcessPoolExecutor with n_workers (default: os.cpu_count()).
    Use executor.map(cpu_intensive_transform, chunks) — preserves order.
    Return list of results.
    """
    if n_workers is None:
        n_workers = os.cpu_count() or 1

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        return list(executor.map(cpu_intensive_transform, chunks))


def benchmark_multiprocessing(n_chunks: int = 8, chunk_size: int = 10_000) -> dict:
    """
    Generate n_chunks × chunk_size records total.
    Time transform_sequential and transform_multiprocess.
    Return:
      { n_chunks: int, chunk_size: int, total_records: int,
        sequential_s: float, multiprocess_s: float,
        speedup_x: float, cpu_count: int }
    Print formatted result with cpu_count annotation:
      Sequential   : 8.40 s
      Multiprocess : 2.30 s  (4 workers on 4-core machine)
      Speedup      : 3.7×
    Also print:
      "WHY: Each process has its own Python interpreter and GIL.
       CPU-bound work runs truly in parallel. Speedup approaches cpu_count
       minus IPC (inter-process communication) overhead."
    """
    chunks = [
        generate_records(chunk_size, seed=42 + chunk_id)
        for chunk_id in range(n_chunks)
    ]

    cpu_count = os.cpu_count() or 1

    start = time.perf_counter()
    transform_sequential(chunks)
    sequential_s = time.perf_counter() - start

    start = time.perf_counter()
    transform_multiprocess(chunks, n_workers=cpu_count)
    multiprocess_s = time.perf_counter() - start

    speedup_x = sequential_s / multiprocess_s if multiprocess_s > 0 else float("inf")

    print(f"Sequential   : {sequential_s:.2f} s")
    print(f"Multiprocess : {multiprocess_s:.2f} s  ({cpu_count} workers on {cpu_count}-core machine)")
    print(f"Speedup      : {speedup_x:.1f}×")
    print(
        "WHY: Each process has its own Python interpreter and GIL.\n"
        "CPU-bound work runs truly in parallel. Speedup approaches cpu_count\n"
        "minus IPC (inter-process communication) overhead."
    )

    return {
        "n_chunks": n_chunks,
        "chunk_size": chunk_size,
        "total_records": n_chunks * chunk_size,
        "sequential_s": sequential_s,
        "multiprocess_s": multiprocess_s,
        "speedup_x": speedup_x,
        "cpu_count": cpu_count,
    }


def demonstrate_pickling_overhead() -> dict:
    """
    Show that multiprocessing hurts for tiny data.
    Run transform_multiprocess on:
      A. 8 chunks of 100 rows (tiny — pickling dominates)
      B. 8 chunks of 10_000 rows (medium — compute dominates)
    Compare multiprocess time vs sequential time for both.
    Return:
      { tiny_sequential_ms, tiny_multiprocess_ms, tiny_multiprocess_slower_by_x,
        medium_sequential_ms, medium_multiprocess_ms, medium_speedup_x }
    Print the crossover insight:
      "Rule of thumb: use multiprocessing only when each task takes > 10ms of CPU time.
       Below that, pickling overhead and process startup dominate."
    """
    cpu_count = os.cpu_count() or 1

    tiny_chunks = [generate_records(100, seed=100 + i) for i in range(8)]
    medium_chunks = [generate_records(10_000, seed=200 + i) for i in range(8)]

    start = time.perf_counter()
    transform_sequential(tiny_chunks)
    tiny_sequential_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    transform_multiprocess(tiny_chunks, n_workers=cpu_count)
    tiny_multiprocess_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    transform_sequential(medium_chunks)
    medium_sequential_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    transform_multiprocess(medium_chunks, n_workers=cpu_count)
    medium_multiprocess_ms = (time.perf_counter() - start) * 1000

    tiny_multiprocess_slower_by_x = (
        tiny_multiprocess_ms / tiny_sequential_ms
        if tiny_sequential_ms > 0
        else float("inf")
    )
    medium_speedup_x = (
        medium_sequential_ms / medium_multiprocess_ms
        if medium_multiprocess_ms > 0
        else float("inf")
    )

    print(f"Tiny sequential     : {tiny_sequential_ms:.1f} ms")
    print(f"Tiny multiprocess   : {tiny_multiprocess_ms:.1f} ms")
    print(f"Tiny slowdown       : {tiny_multiprocess_slower_by_x:.1f}×")
    print(f"Medium sequential   : {medium_sequential_ms:.1f} ms")
    print(f"Medium multiprocess : {medium_multiprocess_ms:.1f} ms")
    print(f"Medium speedup      : {medium_speedup_x:.1f}×")
    print(
        "Rule of thumb: use multiprocessing only when each task takes > 10ms of CPU time.\n"
        "Below that, pickling overhead and process startup dominate."
    )

    return {
        "tiny_sequential_ms": tiny_sequential_ms,
        "tiny_multiprocess_ms": tiny_multiprocess_ms,
        "tiny_multiprocess_slower_by_x": tiny_multiprocess_slower_by_x,
        "medium_sequential_ms": medium_sequential_ms,
        "medium_multiprocess_ms": medium_multiprocess_ms,
        "medium_speedup_x": medium_speedup_x,
    }


def _sum_slice_worker(
    shm_name: str,
    shape: tuple,
    start: int,
    end: int,
    result_queue,
) -> None:
    """Open existing SharedMemory block, sum slice [start:end], put result in queue."""
    existing_shm = shared_memory.SharedMemory(name=shm_name)

    try:
        shared_array = np.ndarray(shape, dtype=np.float64, buffer=existing_shm.buf)
        result_queue.put((start, end, float(shared_array[start:end].sum())))
    finally:
        existing_shm.close()


def shared_memory_example() -> None:
    """
    Demonstrate multiprocessing.shared_memory.SharedMemory to share a numpy array
    between processes without pickling.
    Steps:
      1. Create a shared memory block, write a numpy array of 1M floats into it
      2. Spawn 2 worker processes that each READ a slice of the shared array
         (compute sum of their slice) — no copying, zero serialisation cost
      3. Print the slice sums and total
      4. Release and unlink shared memory in a finally block
    Note: workers must be module-level functions for pickling.
    Explain:
      "SharedMemory is the escape hatch when you need processes to share large data
       without the serialisation penalty. Used in PySpark and Ray internally."
    """
    source_array = np.random.default_rng(seed=42).random(1_000_000, dtype=np.float64)
    shm = shared_memory.SharedMemory(create=True, size=source_array.nbytes)
    result_queue: Queue = Queue()

    try:
        shared_array = np.ndarray(source_array.shape, dtype=source_array.dtype, buffer=shm.buf)
        shared_array[:] = source_array[:]

        midpoint = source_array.size // 2
        workers = [
            Process(
                target=_sum_slice_worker,
                args=(shm.name, source_array.shape, 0, midpoint, result_queue),
            ),
            Process(
                target=_sum_slice_worker,
                args=(shm.name, source_array.shape, midpoint, source_array.size, result_queue),
            ),
        ]

        for worker in workers:
            worker.start()

        results = [result_queue.get() for _ in workers]

        for worker in workers:
            worker.join()

        results.sort(key=lambda item: item[0])
        total = sum(slice_sum for _, _, slice_sum in results)

        for start, end, slice_sum in results:
            print(f"Slice [{start:,}:{end:,}] sum: {slice_sum:,.2f}")

        print(f"Total from workers : {total:,.2f}")
        print(f"Direct numpy total : {source_array.sum():,.2f}")
        print(
            "SharedMemory is the escape hatch when you need processes to share large data\n"
            "without the serialisation penalty. Used in PySpark and Ray internally."
        )

    finally:
        shm.close()
        shm.unlink()


def main():
    print("\n=== MULTIPROCESSING BENCHMARK ===")
    stats = benchmark_multiprocessing(n_chunks=8, chunk_size=10_000)
    print(f"Speedup: {stats['speedup_x']:.1f}×  (CPU count: {stats['cpu_count']})")

    print("\n=== PICKLING OVERHEAD DEMO ===")
    overhead = demonstrate_pickling_overhead()
    print(f"Tiny data: multiprocess is {overhead['tiny_multiprocess_slower_by_x']:.1f}× SLOWER")
    print(f"Medium data: multiprocess is {overhead['medium_speedup_x']:.1f}× faster")

    print("\n=== SHARED MEMORY ===")
    shared_memory_example()


if __name__ == "__main__":
    main()