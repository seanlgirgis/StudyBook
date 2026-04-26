# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : 05_concurrency_patterns_for_de.py
# Covers  : DE concurrency patterns: ingestion, rate limiting, fan-out/fan-in, backpressure, retries
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python 05_concurrency_patterns_for_de.py
# ============================================================

from __future__ import annotations

import functools
import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any


class TokenBucketRateLimiter:
    """
    Token bucket algorithm for rate limiting.

    Token bucket: tokens accumulate at max_rps/sec up to a burst cap.
    Each request consumes one token. If empty, block until refilled.
    This allows short bursts while enforcing average rate.
    """

    def __init__(self, max_rps: float):
        if max_rps <= 0:
            raise ValueError("max_rps must be > 0")

        self.max_rps = max_rps
        self.tokens = max_rps
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.max_rps, self.tokens + elapsed * self.max_rps)
        self.last_refill = now

    def acquire(self) -> None:
        while True:
            with self.lock:
                self._refill()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return

                missing_tokens = 1.0 - self.tokens
                sleep_s = missing_tokens / self.max_rps

            time.sleep(sleep_s)


def parallel_ingest(
    sources: list[dict],
    ingest_fn,
    max_workers: int = 5,
) -> dict:
    """
    Ingest from N data sources concurrently using ThreadPoolExecutor.
    Each source dict: { id: str, endpoint: str, expected_rows: int }
    ingest_fn(source) → { id, rows_fetched, latency_ms, status: "ok"|"error" }
    Aggregate results into:
      { total_sources: int, successful: int, failed: int,
        total_rows: int, total_ms: float, throughput_rows_per_s: float }
    Print per-source status as results arrive (use as_completed).
    """
    start = time.perf_counter()
    successful = 0
    failed = 0
    total_rows = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ingest_fn, source): source for source in sources}

        for future in as_completed(futures):
            source = futures[future]

            try:
                result = future.result()
                rows = int(result.get("rows_fetched", 0))
                total_rows += rows
                successful += 1

                print(
                    f"{result['id']} OK "
                    f"rows={rows:,} "
                    f"latency={result.get('latency_ms', 0):.0f}ms"
                )

            except Exception as exc:
                failed += 1
                print(f"{source['id']} ERROR {exc}")

    total_ms = (time.perf_counter() - start) * 1000
    total_s = total_ms / 1000
    throughput = total_rows / total_s if total_s > 0 else 0.0

    return {
        "total_sources": len(sources),
        "successful": successful,
        "failed": failed,
        "total_rows": total_rows,
        "total_ms": total_ms,
        "throughput_rows_per_s": throughput,
    }


def rate_limited_executor(
    items: list,
    worker_fn,
    max_rps: float = 10.0,
    max_workers: int = 5,
) -> list:
    """
    Wrap ThreadPoolExecutor with TokenBucketRateLimiter.
    Before each submit, call limiter.acquire().
    Return results in completion order (use as_completed → append to results list).
    Print achieved RPS at end: total_items / total_time.
    """
    limiter = TokenBucketRateLimiter(max_rps=max_rps)
    results = []
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for item in items:
            limiter.acquire()
            futures.append(executor.submit(worker_fn, item))

        for future in as_completed(futures):
            results.append(future.result())

    elapsed = time.perf_counter() - start
    achieved_rps = len(items) / elapsed if elapsed > 0 else 0.0

    print(f"Processed {len(items)} items in {elapsed:.2f}s")
    print(f"Configured max RPS: {max_rps:.1f}")
    print(f"Achieved RPS      : {achieved_rps:.1f}")

    return results


def fan_out_fan_in(
    items: list,
    fan_out_fn,
    fan_in_fn,
    workers: int = 5,
) -> list:
    """
    Fan-out: apply fan_out_fn(item) to each item concurrently (ThreadPoolExecutor).
             Each fan_out_fn call returns a LIST of sub-items (expansion).
    Fan-in:  collect all sub-items, apply fan_in_fn to reduce / aggregate.
             fan_in_fn(all_sub_items: list) → final_result (single value or list)
    Return final_result.
    Example use: fan_out = split record into N events; fan_in = deduplicate + sort.
    Print: items in, sub-items after fan-out, final items after fan-in.
    """
    with ThreadPoolExecutor(max_workers=workers) as executor:
        expanded_lists = list(executor.map(fan_out_fn, items))

    all_sub_items = [
        sub_item
        for expanded in expanded_lists
        for sub_item in expanded
    ]

    final_result = fan_in_fn(all_sub_items)

    try:
        final_count = len(final_result)
    except TypeError:
        final_count = 1

    print(f"Items in               : {len(items)}")
    print(f"Sub-items after fan-out: {len(all_sub_items)}")
    print(f"Final items after fan-in: {final_count}")

    return final_result


def bounded_pipeline(
    items: list,
    stage1_fn,
    stage2_fn,
    buffer_size: int = 10,
) -> list:
    """
    Two-stage pipeline with queue.Queue(maxsize=buffer_size) for backpressure.
    Stage 1 thread: apply stage1_fn to each item, put result in queue
                    (blocks if queue full — backpressure on fast producer)
    Stage 2 thread: get from queue, apply stage2_fn, append to results
    Sentinel: put None after all stage-1 items to stop stage-2.
    Print: "Producer blocked N times (backpressure events)" at end.
    Return all stage-2 results.
    Explain:
      "Queue(maxsize=buffer_size) creates natural backpressure: a slow consumer
       slows the producer to match. Prevents OOM from unbounded buffering."
    """
    if buffer_size <= 0:
        raise ValueError("buffer_size must be > 0")

    q: queue.Queue[Any] = queue.Queue(maxsize=buffer_size)
    results = []
    producer_blocked_count = 0
    results_lock = threading.Lock()

    def producer() -> None:
        nonlocal producer_blocked_count

        for item in items:
            result = stage1_fn(item)

            before_put = time.perf_counter()
            q.put(result)
            blocked_for = time.perf_counter() - before_put

            if blocked_for > 0.001:
                producer_blocked_count += 1

        q.put(None)

    def consumer() -> None:
        while True:
            item = q.get()

            try:
                if item is None:
                    return

                result = stage2_fn(item)

                with results_lock:
                    results.append(result)

            finally:
                q.task_done()

    start = time.perf_counter()

    producer_thread = threading.Thread(target=producer, name="BoundedPipelineProducer")
    consumer_thread = threading.Thread(target=consumer, name="BoundedPipelineConsumer")

    consumer_thread.start()
    producer_thread.start()

    producer_thread.join()
    q.join()
    consumer_thread.join()

    elapsed = time.perf_counter() - start

    print(f"Producer blocked {producer_blocked_count} times (backpressure events)")
    print(f"Pipeline completed in {elapsed:.2f}s")
    print(
        "Queue(maxsize=buffer_size) creates natural backpressure: a slow consumer\n"
        "slows the producer to match. Prevents OOM from unbounded buffering."
    )

    return results


def retry_with_jitter(max_attempts: int = 3, base_delay_s: float = 1.0):
    """
    Decorator factory. The decorated function is retried up to max_attempts times.
    Delay between retries: base_delay_s * (2 ** attempt) + random.uniform(0, 0.5)
    (exponential backoff with jitter — avoids thundering herd).
    On final failure, re-raise the last exception.
    Print each retry: "Attempt 2/3 failed: <error>. Retrying in 2.3s..."
    Thread-safe (no shared state).
    """
    if max_attempts <= 0:
        raise ValueError("max_attempts must be > 0")

    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc

                    if attempt == max_attempts:
                        raise

                    delay_s = base_delay_s * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
                    print(
                        f"Attempt {attempt}/{max_attempts} failed: {exc}. "
                        f"Retrying in {delay_s:.1f}s..."
                    )
                    time.sleep(delay_s)

            raise last_exc

        return wrapper

    return decorator


def main():
    print("\n=== PARALLEL INGESTION (10 sources, 5 workers) ===")
    sources = [
        {"id": f"src_{i:02d}", "endpoint": f"/data/{i}", "expected_rows": 1000}
        for i in range(10)
    ]

    def mock_ingest(source: dict) -> dict:
        time.sleep(random.uniform(0.1, 0.5))
        if random.random() < 0.1:
            raise ConnectionError(f"Source {source['id']} unreachable")
        return {
            "id": source["id"],
            "rows_fetched": 1000,
            "latency_ms": random.randint(100, 500),
            "status": "ok",
        }

    stats = parallel_ingest(sources, mock_ingest, max_workers=5)
    print(
        f"  Total rows: {stats['total_rows']:,}  "
        f"Throughput: {stats['throughput_rows_per_s']:.0f} rows/s"
    )

    print("\n=== RATE LIMITED EXECUTOR (max 5 rps) ===")
    items = [f"item_{i}" for i in range(20)]

    def fast_worker(item: str) -> str:
        time.sleep(0.01)
        return item.upper()

    rate_limited_executor(items, fast_worker, max_rps=5.0)

    print("\n=== FAN-OUT / FAN-IN ===")
    records = [{"id": i, "tags": ["a", "b", "c"]} for i in range(10)]

    def expand_tags(record: dict) -> list[dict]:
        return [{"id": record["id"], "tag": t} for t in record["tags"]]

    def deduplicate(items: list[dict]) -> list[dict]:
        seen = set()
        return [x for x in items if (k := x["tag"]) not in seen and not seen.add(k)]

    result = fan_out_fan_in(records, expand_tags, deduplicate, workers=5)
    print(f"  Final unique tags: {len(result)}")

    print("\n=== BOUNDED PIPELINE WITH BACKPRESSURE ===")
    pipeline_items = list(range(50))

    def fast_stage1(x):
        time.sleep(0.01)
        return x * 2

    def slow_stage2(x):
        time.sleep(0.05)
        return x + 1

    results = bounded_pipeline(pipeline_items, fast_stage1, slow_stage2, buffer_size=5)
    print(f"  Results: {len(results)} items processed")

    print("\n=== RETRY WITH JITTER ===")
    call_count = {"n": 0}

    @retry_with_jitter(max_attempts=3, base_delay_s=0.1)
    def flaky_function():
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise ValueError("Transient error")
        return "success"

    result = flaky_function()
    print(f"  Result: {result}  (took {call_count['n']} attempts)")


if __name__ == "__main__":
    main()