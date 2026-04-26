# ChatGPT Prompt — Python Concurrency for Data Engineers
# READY TO PASTE — fully specified, no placeholders
# Paste everything between the === markers into ChatGPT

===

TOPIC: Python Concurrency for Data Engineers
SLUG: python_concurrency
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — stdlib + aiohttp + aiofiles + pyarrow
NO AWS, NO DOCKER, NO CLEANUP RULES NEEDED.

===== CODING STANDARDS =====

FILE HEADER (every file must start with this block):
# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install aiohttp aiofiles pyarrow pandas
# Run     : python NN_filename.py
# ============================================================

CRITICAL — CODE QUALITY:
- Every function must be COMPLETE and FULLY RUNNABLE — no placeholders, no TODO
  comments, no pass statements, no "add logic here" stubs.
- Generate the ENTIRE file contents each time. Never truncate with "..." or "rest is same".
- Comments explain WHY — the GIL is the biggest misconception Python engineers have.
  Be explicit: threading releases the GIL on I/O; multiprocessing bypasses it entirely.
  Show REAL timing comparisons — print actual numbers, not assertions.
- No env vars required. Output to /tmp/studybook/concurrency/ (Linux/Mac)
  or C:/tmp/studybook/concurrency/ (Windows, detect with os.name).
- Every main() prints a clear section header before each demo block.
- Python 3.11+ syntax OK (TaskGroup, ExceptionGroup).

===== FILE 01: 01_threading_for_io_bound.py =====

Purpose: threading module — parallel I/O, the GIL, ThreadPoolExecutor, thread safety.
The GIL explanation is the #1 Python concurrency interview question.

Implement these functions in this exact order:

def simulate_api_call(endpoint: str, delay_s: float = None) -> dict:
    """
    Simulate an HTTP API call with I/O latency (time.sleep).
    delay_s defaults to random uniform 0.1–0.5s if None.
    Return:
      { endpoint: str, status: "ok", data: {"value": random_float},
        latency_ms: float, thread_name: str }
    Use threading.current_thread().name for thread_name.
    """

def fetch_sequential(endpoints: list[str]) -> list[dict]:
    """
    Fetch endpoints one at a time. Return list of results in order.
    Print total time at end.
    """

def fetch_threaded(endpoints: list[str], max_workers: int = 10) -> list[dict]:
    """
    Use ThreadPoolExecutor(max_workers=max_workers).
    Submit all endpoints, collect via futures in submission order.
    Return list of results in original order.
    Print total time at end.
    Note: order is preserved by zipping futures with endpoints.
    """

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

def demonstrate_thread_safety_bug() -> None:
    """
    Shared counter incremented by 10 threads, 10_000 times each.
    Expected: 100_000. Actual: less (race condition).
    Print both values. Explain:
      "WHY: counter += 1 is not atomic. It compiles to: LOAD counter, ADD 1, STORE counter.
       The GIL can switch threads between LOAD and STORE."
    Use threading.Thread directly (not ThreadPoolExecutor).
    """

def demonstrate_thread_safety_fix() -> None:
    """
    Same as bug demo but use threading.Lock() around counter += 1.
    Show final value == 100_000.
    Print lock acquire/release overhead estimate (time the whole operation).
    Explain:
      "Lock serialises the critical section. For high-contention counters, prefer
       threading.local() or queue.Queue to avoid lock overhead entirely."
    """

def producer_consumer_queue(n_producers: int = 3, n_consumers: int = 2,
                             n_items: int = 30) -> None:
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

===== FILE 02: 02_multiprocessing_for_cpu_bound.py =====

Purpose: multiprocessing — bypass the GIL for CPU-heavy work.
The process pool is the correct answer when threading doesn't help.

IMPORTANT: All functions passed to ProcessPoolExecutor must be defined at module level
(not inside other functions or lambdas) — they must be picklable.

def generate_records(n: int = 10_000, seed: int = 42) -> list[dict]:
    """
    Generate n fake sensor records:
      { id: int, raw_value: float, sensor_type: str (one of 4),
        timestamp: str (ISO format), plant: str (one of 3) }
    """

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

def transform_sequential(chunks: list[list[dict]]) -> list[list[dict]]:
    """Apply cpu_intensive_transform to each chunk serially. Return list of results."""

def transform_multiprocess(chunks: list[list[dict]],
                            n_workers: int = None) -> list[list[dict]]:
    """
    ProcessPoolExecutor with n_workers (default: os.cpu_count()).
    Use executor.map(cpu_intensive_transform, chunks) — preserves order.
    Return list of results.
    """

def benchmark_multiprocessing(n_chunks: int = 8,
                               chunk_size: int = 10_000) -> dict:
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

# Module-level worker for shared_memory_example
def _sum_slice_worker(shm_name: str, shape: tuple, start: int, end: int,
                      result_queue) -> None:
    """Open existing SharedMemory block, sum slice [start:end], put result in queue."""

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

===== FILE 03: 03_asyncio_for_data_pipelines.py =====

Purpose: asyncio — event loop, coroutines, semaphore-controlled concurrency, async pipelines.
No REAL HTTP calls — all "network" I/O is simulated with asyncio.sleep.

DO NOT use aiohttp for actual HTTP in this file. Instead:
  - Create a fake async_http_get coroutine that uses asyncio.sleep to simulate latency
  - This avoids network dependencies and makes the file fully self-contained.
  - Mention aiohttp in comments but don't import it.

def default_output_dir() -> str:
    """Return platform-appropriate default output dir. Create if missing."""

async def async_http_get(url: str, session_id: int = 0) -> dict:
    """
    Simulate async HTTP GET. Uses asyncio.sleep(random 0.05–0.3s).
    10% chance of raising aiohttp.ClientError-like exception (use a plain Exception
    with message "Simulated network error").
    Return:
      { url: str, status: 200, data: {"value": random_float, "ts": iso_string},
        latency_ms: float }
    """

async def fetch_all_urls(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    """
    Use asyncio.Semaphore(max_concurrent) to cap concurrent requests.
    Use asyncio.gather(*tasks, return_exceptions=True).
    For each result: if isinstance(result, Exception), replace with error dict
      {"url": url, "status": "error", "error": str(result)}.
    Return list of results in original URL order.
    """

async def read_file_async(path: str) -> str:
    """
    Read file using aiofiles. If aiofiles not installed, fall back to
    asyncio.get_event_loop().run_in_executor(None, open(path).read).
    Return file contents as string.
    """

async def write_file_async(path: str, content: str) -> None:
    """
    Write content to path using aiofiles (or executor fallback).
    Create parent directory if needed (use asyncio.to_thread for os.makedirs).
    """

async def pipeline_stage(items: list, processor, max_concurrent: int = 5) -> list:
    """
    Generic async pipeline stage. Applies async coroutine `processor` to each item.
    Uses asyncio.Semaphore(max_concurrent) for bounded parallelism.
    Returns results in original order (gather preserves order).
    processor must be an async function: async def processor(item) -> result
    """

async def run_etl_pipeline(source_urls: list[str], output_dir: str) -> dict:
    """
    Three-stage async pipeline:
      Stage 1 (fetch):     fetch_all_urls — async HTTP, max 10 concurrent
      Stage 2 (transform): apply transform to each successful result
                           transform = extract value, round to 2dp, add processed_at
                           skip error results (log them)
      Stage 3 (write):     write each result as JSON to output_dir/{i}.json
                           using write_file_async
    Return:
      { total_urls: int, fetched_ok: int, fetch_errors: int,
        files_written: int, total_ms: float }
    Print progress: "Stage 1 complete: 14/15 ok"  etc.
    """

async def demonstrate_taskgroup() -> None:
    """
    Python 3.11+ asyncio.TaskGroup for structured concurrency.
    Create 5 tasks that each sleep a random 0.1–0.5s and return a value.
    Collect results via task.result() after the group exits.
    Demonstrate cancellation: if one task raises, all others are cancelled
    (wrap in try/except* ExceptionGroup).
    Print each task result and total time.
    """

async def main_async():
    out = default_output_dir()
    urls = [f"http://sensors.internal/device/{i}/reading" for i in range(15)]

    print("\n=== ASYNC FETCH (15 URLs, max 10 concurrent) ===")
    results = await fetch_all_urls(urls, max_concurrent=10)
    ok = sum(1 for r in results if r.get("status") == 200)
    print(f"  OK: {ok}/15  Errors: {15-ok}/15")

    print("\n=== ETL PIPELINE (fetch → transform → write) ===")
    stats = await run_etl_pipeline(urls[:10], out)
    print(f"  Fetched: {stats['fetched_ok']}  Errors: {stats['fetch_errors']}  "
          f"Written: {stats['files_written']}  Time: {stats['total_ms']:.0f}ms")

    print("\n=== TASKGROUP (Python 3.11+) ===")
    await demonstrate_taskgroup()

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

===== FILE 04: 04_concurrent_futures_patterns.py =====

Purpose: concurrent.futures — the unified interface that works for both threading and
multiprocessing. Critical pattern for two-stage I/O → CPU pipelines.

All CPU worker functions must be at module level (pickling requirement).

def simulate_io_fetch(item: str) -> dict:
    """
    Simulate I/O (time.sleep 0.05–0.2s). Return {"item": item, "raw": random_float}.
    Module-level for pickling.
    """

def simulate_cpu_transform(record: dict) -> dict:
    """
    CPU-heavy: perform 500k arithmetic operations on record["raw"].
    Return record with added fields: transformed_value, quality, processed_by_pid.
    Module-level for pickling.
    """

def process_with_executor(items: list, worker_fn,
                           use_processes: bool = False,
                           max_workers: int = 4) -> list:
    """
    Generic executor wrapper.
    use_processes=False → ThreadPoolExecutor
    use_processes=True  → ProcessPoolExecutor
    Use executor.map(worker_fn, items) — preserves order.
    Return list of results. Print executor type and time taken.
    """

def fetch_and_transform(items: list[str]) -> list[dict]:
    """
    Two-stage pipeline:
      Stage 1: ThreadPoolExecutor — simulate_io_fetch for all items (I/O-bound)
      Stage 2: ProcessPoolExecutor — simulate_cpu_transform for all fetched records (CPU-bound)
    Return final results. Print time for each stage and total.
    """

def handle_partial_failures(items: list, worker_fn,
                             max_workers: int = 4) -> dict:
    """
    Submit all items with executor.submit(). Use as_completed() to collect results.
    For each future: catch exception individually.
    Return:
      { results: list, errors: list[{"item": ..., "error": str}],
        success_count: int, error_count: int }
    Do NOT let one failure stop the rest. Print a summary at end.
    """

def timeout_aware_executor(items: list, worker_fn,
                            timeout_s: float = 0.3) -> dict:
    """
    Submit all items. For each future in as_completed(futures, timeout=timeout_s):
      - collect result if done
      - on TimeoutError from as_completed: cancel remaining futures
    ALSO call future.result(timeout=timeout_s) on individual futures to handle
    per-task timeouts.
    Return:
      { completed: list, timed_out_count: int, total: int }
    """

def executor_context_manager_demo() -> None:
    """
    Show both executor types as context managers (with-block).
    Demonstrate that shutdown(wait=True) is called on __exit__ — no leaked threads/processes.
    Print thread/process count before and after the with block using
    threading.active_count() and len(multiprocessing.active_children()).
    """

def choose_executor(task_type: str, data_size_mb: float, n_items: int) -> str:
    """
    Decision function. Rules:
      task_type == "io"  → "ThreadPoolExecutor"
        reason: GIL releases on I/O; threads are lightweight; no pickling
      task_type == "cpu" and data_size_mb > 100 → "ProcessPoolExecutor"
        reason: CPU-bound; data large enough that compute time > pickling overhead
      task_type == "cpu" and data_size_mb <= 100 and n_items < 100 → "ThreadPoolExecutor"
        reason: pickling overhead exceeds speedup for small CPU tasks
      task_type == "cpu" and data_size_mb <= 100 and n_items >= 100 → "ProcessPoolExecutor"
    Print recommendation and one-line reason. Return executor type string.
    """

def main():
    items = [f"sensor_{i:03d}" for i in range(20)]

    print("\n=== TWO-STAGE PIPELINE (I/O threads → CPU processes) ===")
    results = fetch_and_transform(items)
    print(f"  Processed {len(results)} items")

    print("\n=== PARTIAL FAILURE HANDLING ===")
    def flaky_worker(item: str) -> dict:
        if hash(item) % 5 == 0:  # ~20% failure rate
            raise ValueError(f"Processing failed for {item}")
        time.sleep(0.02)
        return {"item": item, "value": random.random()}
    outcome = handle_partial_failures(items, flaky_worker)
    print(f"  Success: {outcome['success_count']}  Errors: {outcome['error_count']}")

    print("\n=== TIMEOUT-AWARE EXECUTOR ===")
    def slow_worker(item: str) -> dict:
        time.sleep(random.uniform(0.05, 0.5))  # some will exceed 0.3s
        return {"item": item}
    result = timeout_aware_executor(items, slow_worker, timeout_s=0.3)
    print(f"  Completed: {len(result['completed'])}  "
          f"Timed out: {result['timed_out_count']}")

    print("\n=== EXECUTOR CONTEXT MANAGER ===")
    executor_context_manager_demo()

    print("\n=== EXECUTOR CHOICE ADVISOR ===")
    choose_executor("io",  data_size_mb=0.1,  n_items=100)
    choose_executor("cpu", data_size_mb=500,  n_items=50)
    choose_executor("cpu", data_size_mb=5,    n_items=20)
    choose_executor("cpu", data_size_mb=5,    n_items=200)

if __name__ == "__main__":
    main()

===== FILE 05: 05_concurrency_patterns_for_de.py =====

Purpose: Real-world DE concurrency patterns — parallel ingestion, rate limiting,
fan-out/fan-in, bounded pipelines with backpressure. Interview gold.

All top-level callable workers must be module-level (pickle-safe).

class TokenBucketRateLimiter:
    """
    Token bucket algorithm for rate limiting.
    __init__(self, max_rps: float): set self.max_rps, self.tokens, self.last_refill
    acquire(self) → None: block until a token is available (thread-safe via threading.Lock)
    _refill(self) → None: add tokens based on elapsed time, cap at max_rps
    Explain in docstring:
      "Token bucket: tokens accumulate at max_rps/sec up to a burst cap.
       Each request consumes one token. If empty, block until refilled.
       This allows short bursts while enforcing average rate."
    """

def parallel_ingest(sources: list[dict], ingest_fn,
                    max_workers: int = 5) -> dict:
    """
    Ingest from N data sources concurrently using ThreadPoolExecutor.
    Each source dict: { id: str, endpoint: str, expected_rows: int }
    ingest_fn(source) → { id, rows_fetched, latency_ms, status: "ok"|"error" }
    Aggregate results into:
      { total_sources: int, successful: int, failed: int,
        total_rows: int, total_ms: float, throughput_rows_per_s: float }
    Print per-source status as results arrive (use as_completed).
    """

def rate_limited_executor(items: list, worker_fn,
                           max_rps: float = 10.0,
                           max_workers: int = 5) -> list:
    """
    Wrap ThreadPoolExecutor with TokenBucketRateLimiter.
    Before each submit, call limiter.acquire().
    Return results in completion order (use as_completed → append to results list).
    Print achieved RPS at end: total_items / total_time.
    """

def fan_out_fan_in(items: list, fan_out_fn, fan_in_fn,
                   workers: int = 5) -> list:
    """
    Fan-out: apply fan_out_fn(item) to each item concurrently (ThreadPoolExecutor).
             Each fan_out_fn call returns a LIST of sub-items (expansion).
    Fan-in:  collect all sub-items, apply fan_in_fn to reduce / aggregate.
             fan_in_fn(all_sub_items: list) → final_result (single value or list)
    Return final_result.
    Example use: fan_out = split record into N events; fan_in = deduplicate + sort.
    Print: items in, sub-items after fan-out, final items after fan-in.
    """

def bounded_pipeline(items: list,
                      stage1_fn,
                      stage2_fn,
                      buffer_size: int = 10) -> list:
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

def retry_with_jitter(max_attempts: int = 3,
                      base_delay_s: float = 1.0):
    """
    Decorator factory. The decorated function is retried up to max_attempts times.
    Delay between retries: base_delay_s * (2 ** attempt) + random.uniform(0, 0.5)
    (exponential backoff with jitter — avoids thundering herd).
    On final failure, re-raise the last exception.
    Print each retry: "Attempt 2/3 failed: <error>. Retrying in 2.3s..."
    Thread-safe (no shared state).
    """

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
        return {"id": source["id"], "rows_fetched": 1000,
                "latency_ms": random.randint(100, 500), "status": "ok"}
    stats = parallel_ingest(sources, mock_ingest, max_workers=5)
    print(f"  Total rows: {stats['total_rows']:,}  "
          f"Throughput: {stats['throughput_rows_per_s']:.0f} rows/s")

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
        time.sleep(0.05)   # consumer is 5× slower → backpressure fires
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

===== CAPSTONE PROJECT =====

Title: Concurrent Data Pipeline for Multi-Source IoT Ingestion
Scenario: 50 IoT sensor endpoints (simulated locally). Build a concurrent pipeline
that fetches all 50 in parallel, validates and enriches records (CPU-bound),
writes results to Parquet, and respects a 20 rps rate limit.

Directory layout:
  capstone/
    simulate_sources.py   ← 50 simulated sensor endpoints
    pipeline.py           ← three-stage concurrent pipeline
    test_capstone.py      ← pytest, 7 tests

===== CAPSTONE FILE: simulate_sources.py =====

"""
Defines 50 simulated IoT sensor endpoints.
Each endpoint is a regular function (synchronous) that simulates network latency.
"""
import time, random, datetime

PLANTS  = ["plant_A", "plant_B", "plant_C"]
SENSORS = ["temperature", "pressure", "vibration", "humidity"]
RANGES  = {
    "temperature": (15.0, 95.0),
    "pressure":    (1.0,  10.0),
    "vibration":   (0.0,  50.0),
    "humidity":    (20.0, 100.0),
}
UNITS   = {"temperature": "C", "pressure": "bar",
           "vibration": "mm/s", "humidity": "%"}

# Build 50 endpoint definitions at module level
ENDPOINTS: list[dict] = [
    {
        "id":          f"sensor_{i:03d}",
        "plant":       PLANTS[i % 3],
        "sensor_type": SENSORS[i % 4],
        "base_value":  random.uniform(*RANGES[SENSORS[i % 4]]),
    }
    for i in range(50)
]

def fetch_sensor(endpoint: dict, seed: int = None) -> dict:
    """
    Simulate fetching one sensor reading:
      - Sleep random 0.1–2.0s (network latency)
      - 10% chance: raise ConnectionError("Simulated network failure")
      - Return:
          { endpoint_id: str, plant: str, sensor_type: str,
            value: float (base_value + gaussian noise σ=2),
            unit: str, ts: str (ISO 8601),
            latency_ms: float }
    seed parameter sets numpy/random seed for reproducibility in tests.
    """

def fetch_all_sequential() -> list[dict]:
    """Fetch all 50 endpoints one at a time. For benchmarking baseline."""

Usage:
  from simulate_sources import ENDPOINTS, fetch_sensor

===== CAPSTONE FILE: pipeline.py =====

"""
Three-stage concurrent IoT ingestion pipeline.

Stage 1 — I/O  (ThreadPoolExecutor + rate limiter):
  Fetch all 50 sensor endpoints concurrently.
  Rate limit: 20 requests per second (TokenBucketRateLimiter).
  Retry: up to 3 times with exponential backoff + jitter.
  On permanent failure: log and skip (do not crash).

Stage 2 — CPU  (ProcessPoolExecutor):
  Validate and enrich each successful record:
    - Validate value is within expected range for sensor_type
    - Compute: normalised_value = (value - min) / (max - min)
    - Compute: anomaly_flag = value > 90th percentile threshold per sensor_type
    - Add: processed_at (ISO timestamp), pipeline_run_id (uuid4, shared across all records)

Stage 3 — Write (synchronous, thread-safe):
  Write all enriched records as Parquet to OUTPUT_DIR / capstone / results.parquet
  Schema: endpoint_id, plant, sensor_type, value, unit, normalised_value,
          anomaly_flag, ts, latency_ms, processed_at, pipeline_run_id

Final report printed to console:
  ╔══════════════════════════════════════╗
  ║  IoT Pipeline Run — Summary          ║
  ╠══════════════════════════════════════╣
  ║  Total endpoints      : 50           ║
  ║  Fetched OK           : 45           ║
  ║  Fetch errors         : 5            ║
  ║  Records written      : 45           ║
  ║  Anomalies flagged    : 3            ║
  ║  Total time           : 3.21 s       ║
  ║  Throughput           : 14.0 rec/s   ║
  ╚══════════════════════════════════════╝
"""

import os, uuid, time, logging, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from simulate_sources import ENDPOINTS, fetch_sensor, RANGES

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", ...))   # same platform default as setup files

# ── Rate Limiter (copy of pattern from file 05) ──────────────────────────────

class TokenBucketRateLimiter:
    """
    Thread-safe token bucket rate limiter.
    Full implementation — same logic as 05_concurrency_patterns_for_de.py.
    """

# ── Retry decorator ───────────────────────────────────────────────────────────

def retry_with_jitter(max_attempts: int = 3, base_delay_s: float = 0.5):
    """
    Decorator factory — same logic as 05_concurrency_patterns_for_de.py.
    """

# ── Stage 2 worker (module-level for pickling) ────────────────────────────────

ANOMALY_THRESHOLDS = {
    "temperature": 85.0,   # > 85°C = anomaly
    "pressure":    8.5,    # > 8.5 bar
    "vibration":   42.0,   # > 42 mm/s
    "humidity":    88.0,   # > 88 %
}

def enrich_record(record: dict) -> dict:
    """
    Module-level CPU enrichment function (picklable).
    - Compute normalised_value (0.0–1.0)
    - Set anomaly_flag (bool) based on ANOMALY_THRESHOLDS
    - Add processed_at (ISO timestamp)
    - Add pipeline_run_id (passed in via record["_run_id"])
    Return enriched record (remove _run_id before return).
    """

# ── Stage 1: Fetch (threaded + rate limited) ──────────────────────────────────

def stage1_fetch(endpoints: list[dict], max_rps: float = 20.0,
                 max_workers: int = 20) -> tuple[list[dict], list[dict]]:
    """
    ThreadPoolExecutor + TokenBucketRateLimiter.
    Wrap fetch_sensor with @retry_with_jitter(max_attempts=3).
    Return (successful_records, failed_endpoints).
    Log each failure: log.warning("FETCH FAILED: %s — %s", ep["id"], str(e))
    """

# ── Stage 2: Enrich (multiprocess) ───────────────────────────────────────────

def stage2_enrich(records: list[dict], run_id: str,
                  n_workers: int = None) -> list[dict]:
    """
    ProcessPoolExecutor — apply enrich_record to all records.
    Inject run_id into each record as "_run_id" before sending to pool.
    Return enriched records list.
    """

# ── Stage 3: Write Parquet ────────────────────────────────────────────────────

PARQUET_SCHEMA = pa.schema([
    ("endpoint_id",       pa.string()),
    ("plant",             pa.string()),
    ("sensor_type",       pa.string()),
    ("value",             pa.float64()),
    ("unit",              pa.string()),
    ("normalised_value",  pa.float64()),
    ("anomaly_flag",      pa.bool_()),
    ("ts",                pa.string()),
    ("latency_ms",        pa.float64()),
    ("processed_at",      pa.string()),
    ("pipeline_run_id",   pa.string()),
])

def stage3_write(records: list[dict], output_path: Path) -> None:
    """
    Convert records list to pyarrow Table using PARQUET_SCHEMA.
    Write as SNAPPY Parquet to output_path.
    Print: "Written {len(records)} records to {output_path}"
    """

# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(max_rps: float = 20.0) -> dict:
    """
    Orchestrate all 3 stages. Measure wall-clock time for each stage and total.
    Return:
      { run_id: str, total_endpoints: int, fetched_ok: int, fetch_errors: int,
        records_written: int, anomalies: int,
        stage1_ms: float, stage2_ms: float, stage3_ms: float, total_ms: float,
        throughput_rec_per_s: float }
    """

def print_summary(stats: dict) -> None:
    """
    Print the formatted box summary shown in the module docstring.
    """

def main():
    stats = run_pipeline(max_rps=20.0)
    print_summary(stats)

if __name__ == "__main__":
    main()

===== CAPSTONE FILE: test_capstone.py =====

"""
pytest — 7 tests validating the concurrent pipeline.
Run: pytest test_capstone.py -v
"""

import pytest, time, random, threading
from pathlib import Path
import pyarrow.parquet as pq
from simulate_sources import ENDPOINTS, fetch_sensor
from pipeline import (TokenBucketRateLimiter, retry_with_jitter,
                      stage1_fetch, stage2_enrich, enrich_record,
                      run_pipeline, PARQUET_SCHEMA, OUTPUT_DIR)

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def pipeline_stats():
    """Run the full pipeline once for the whole test session."""
    return run_pipeline(max_rps=20.0)

@pytest.fixture(scope="session")
def output_parquet(pipeline_stats):
    path = OUTPUT_DIR / "capstone" / "results.parquet"
    assert path.exists(), f"Pipeline must write results.parquet: {path} not found"
    return pq.read_table(path)

# ── Tests ─────────────────────────────────────────────────────────────────────

def test_pipeline_completes_all_50_endpoints(pipeline_stats):
    """total_endpoints must equal 50."""
    assert pipeline_stats["total_endpoints"] == 50

def test_pipeline_runs_under_10_seconds(pipeline_stats):
    """
    50 endpoints × average latency of ~1s sequential = ~50s.
    Concurrent pipeline must finish in under 10 seconds.
    """
    total_s = pipeline_stats["total_ms"] / 1000
    assert total_s < 10, f"Pipeline too slow: {total_s:.1f}s (expected < 10s)"

def test_rate_limiter_holds_throughput_below_max_rps():
    """
    Submit 20 instant tasks through rate limiter at max_rps=5.
    Wall time must be >= 20/5 - 0.5 = 3.5 seconds.
    """
    limiter = TokenBucketRateLimiter(max_rps=5.0)
    times = []
    def acquire_and_record():
        limiter.acquire()
        times.append(time.monotonic())
    threads = [threading.Thread(target=acquire_and_record) for _ in range(20)]
    t0 = time.monotonic()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.monotonic() - t0
    assert elapsed >= 3.5, \
        f"Rate limiter too fast: {elapsed:.2f}s for 20 items at 5 rps (expected >= 3.5s)"

def test_retry_attempts_exactly_n_times():
    """retry_with_jitter retries exactly max_attempts times then re-raises."""
    attempt_log = []
    @retry_with_jitter(max_attempts=3, base_delay_s=0.01)
    def always_fails():
        attempt_log.append(1)
        raise ValueError("always fails")
    with pytest.raises(ValueError):
        always_fails()
    assert len(attempt_log) == 3, \
        f"Expected 3 attempts, got {len(attempt_log)}"

def test_pipeline_handles_failures_without_crash(pipeline_stats):
    """
    10% of 50 endpoints fail randomly (seed-dependent).
    fetched_ok + fetch_errors must equal total_endpoints.
    Pipeline must NOT raise — any fetch error is caught and logged.
    """
    assert (pipeline_stats["fetched_ok"] + pipeline_stats["fetch_errors"]
            == pipeline_stats["total_endpoints"])

def test_output_parquet_has_correct_schema(output_parquet):
    """Parquet file must contain all 11 required columns."""
    required = {f.name for f in PARQUET_SCHEMA}
    actual   = set(output_parquet.schema.names)
    missing  = required - actual
    assert not missing, f"Missing columns in output: {missing}"

def test_output_parquet_row_count_matches_fetched_ok(pipeline_stats, output_parquet):
    """records_written in stats must equal row count in Parquet file."""
    parquet_rows = output_parquet.num_rows
    assert parquet_rows == pipeline_stats["records_written"], (
        f"Stats say {pipeline_stats['records_written']} written, "
        f"Parquet has {parquet_rows} rows"
    )

===== GENERATION SEQUENCE =====

Acknowledge these instructions, then wait for me to say "generate file 01".

After I confirm each file, I will say "generate file 02", etc.

Generation order:
  "generate file 01"    → 01_threading_for_io_bound.py
  "generate file 02"    → 02_multiprocessing_for_cpu_bound.py
  "generate file 03"    → 03_asyncio_for_data_pipelines.py
  "generate file 04"    → 04_concurrent_futures_patterns.py
  "generate file 05"    → 05_concurrency_patterns_for_de.py
  "generate readme"     → README.md
  "generate sources"    → capstone/simulate_sources.py
  "generate pipeline"   → capstone/pipeline.py
  "generate tests"      → capstone/test_capstone.py

Each file must be COMPLETE and FULLY RUNNABLE.
No placeholders. No TODO comments. No pass statements.
Generate the ENTIRE file contents every time.

===
