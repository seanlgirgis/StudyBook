# ChatGPT Prompt — Python Concurrency Tutorial
# Paste everything between the === markers into ChatGPT

===

TOPIC: Python Concurrency for Data Engineers
SLUG: python-concurrency
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python — stdlib only (threading, multiprocessing, asyncio, concurrent.futures)

===== CODING STANDARDS =====

FILE HEADER:
# ============================================================
# Topic   : Python Concurrency for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install aiohttp aiofiles | no AWS or Docker needed
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY. The GIL is the single biggest misconception Python engineers have.
Be explicit: threading is for I/O-bound, multiprocessing for CPU-bound. Explain WHY
with concrete DE examples (API calls, file I/O, CPU-heavy transformations).
Show real timing comparisons — don't just assert things are faster.
No env vars required.

===== FILES TO GENERATE =====

01_threading_for_io_bound.py
  Purpose: threading module — parallel I/O, the GIL, ThreadPoolExecutor, thread safety
  Key concepts: GIL (Global Interpreter Lock) — releases on I/O, not CPU;
    daemon threads, thread safety, Lock vs RLock, queue.Queue for producer-consumer
  Functions:
    - simulate_api_call(endpoint: str, delay_s: float) → dict
      — simulate HTTP latency with time.sleep (I/O-bound proxy)
    - fetch_sequential(endpoints: list[str]) → list[dict]
      — baseline: fetch one at a time, return results
    - fetch_threaded(endpoints: list[str], max_workers: int = 10) → list[dict]
      — ThreadPoolExecutor: fetch all concurrently, collect results
    - benchmark_threading(n_endpoints: int = 20) → dict
      — time both approaches, return {sequential_s, threaded_s, speedup_x}
    - demonstrate_thread_safety_bug() → None
      — shared counter incremented by 10 threads without Lock → show wrong result
    - demonstrate_thread_safety_fix() → None
      — same with threading.Lock → show correct result
    - producer_consumer_queue(n_producers: int, n_consumers: int, n_items: int) → None
      — queue.Queue pipeline: producers put items, consumers process, show throughput
  Main block: benchmark 20 simulated API calls (sequential vs threaded), show speedup,
    demonstrate Lock bug and fix, run producer-consumer

02_multiprocessing_for_cpu_bound.py
  Purpose: multiprocessing — bypass the GIL, ProcessPoolExecutor, shared memory, pitfalls
  Key concepts: GIL bypass via separate processes, pickling overhead, shared memory,
    process pool vs thread pool, when NOT to use multiprocessing (small data, IPC overhead)
  Functions:
    - cpu_intensive_transform(records: list[dict]) → list[dict]
      — simulate CPU-heavy work: parse, validate, compute derived fields (no I/O)
    - transform_sequential(dataset: list[list[dict]]) → list[list[dict]]
      — process each chunk serially
    - transform_multiprocess(dataset: list[list[dict]], n_workers: int = 4) → list[list[dict]]
      — ProcessPoolExecutor: each chunk processed in separate process
    - benchmark_multiprocessing(n_chunks: int = 8, chunk_size: int = 10_000) → dict
      — time both, show speedup, note CPU core count
    - demonstrate_pickling_overhead() → dict
      — time multiprocess on tiny vs large chunks; show why small chunks hurt
    - shared_memory_example() → None
      — multiprocessing.shared_memory: share array between processes without pickling
  Main block: generate 80k records in 8 chunks, benchmark sequential vs multiprocess,
    explain when the crossover point is (where multiprocess stops being worth it)

03_asyncio_for_data_pipelines.py
  Purpose: asyncio — event loop, async/await, aiohttp, aiofiles, structured concurrency
  Key concepts: event loop, coroutines vs threads, asyncio.gather, TaskGroup (3.11+),
    when asyncio wins vs threading (single-process, no GIL release needed for pure async I/O)
  Functions:
    - async fetch_url(session: aiohttp.ClientSession, url: str) → dict
      — single async HTTP GET with error handling
    - async fetch_all_urls(urls: list[str], max_concurrent: int = 10) → list[dict]
      — asyncio.Semaphore to limit concurrency + asyncio.gather
    - async read_file_async(path: str) → str — aiofiles async file read
    - async write_file_async(path: str, content: str) → None — aiofiles async write
    - async pipeline_stage(items: list, processor: Callable, max_concurrent: int) → list
      — generic async pipeline stage with semaphore-controlled concurrency
    - async run_etl_pipeline(source_urls: list[str], output_dir: str) → dict
      — fetch → parse → write: fully async, show how stages chain
    - demonstrate_taskgroup() → None — Python 3.11+ TaskGroup for structured concurrency
  Main block: fetch 15 public URLs concurrently (use httpbin.org or similar), show
    gather with semaphore, pipe results through async transformation, write to files

04_concurrent_futures_patterns.py
  Purpose: concurrent.futures — the unified interface for threading and multiprocessing
  Key concepts: Future, as_completed, map vs submit, cancellation, exception propagation,
    choosing between ThreadPoolExecutor and ProcessPoolExecutor at call site
  Functions:
    - process_with_executor(items: list, worker_fn: Callable,
        use_processes: bool = False, max_workers: int = 4) → list
      — generic executor wrapper: ThreadPool or ProcessPool based on flag
    - fetch_and_transform(items: list[str]) → list[dict]
      — I/O phase (threads) → CPU phase (processes): two-stage pipeline
    - handle_partial_failures(items: list, worker_fn: Callable) → dict
      — as_completed with per-item exception catching; return {results, errors}
    - timeout_aware_executor(items: list, worker_fn: Callable,
        timeout_s: float = 30) → dict
      — submit all, cancel futures that exceed timeout, report cancelled vs completed
    - executor_context_manager_demo() → None
      — show both executor types as context managers (auto-shutdown)
    - choose_executor(task_type: str, data_size_mb: float,
        n_items: int) → str
      — decision function: returns "ThreadPool" or "ProcessPool" with reasoning
  Main block: two-stage pipeline — 20 simulated API calls (threads) → 20 CPU transforms
    (processes); show timeline and total vs sequential time; handle 2 deliberate failures

05_concurrency_patterns_for_de.py
  Purpose: Real-world DE concurrency patterns — parallel ingestion, fan-out, rate limiting
  Key concepts: fan-out/fan-in, bounded parallelism, rate limiting (tokens/sec),
    pipeline stages with queues, backpressure
  Functions:
    - parallel_ingest(sources: list[dict], ingest_fn: Callable,
        max_workers: int = 5) → dict
      — ingest from N data sources concurrently, aggregate stats
    - rate_limited_executor(items: list, worker_fn: Callable,
        max_rps: float = 10) → list
      — token bucket rate limiter wrapping ThreadPoolExecutor (e.g., for API rate limits)
    - fan_out_fan_in(items: list, fan_out_fn: Callable,
        fan_in_fn: Callable, workers: int) → list
      — expand items → process concurrently → reduce results
    - bounded_pipeline(source_iter, stage1_fn: Callable, stage2_fn: Callable,
        buffer_size: int = 100) → None
      — two-stage pipeline with queue.Queue for backpressure between stages
    - retry_with_jitter(fn: Callable, max_attempts: int = 3,
        base_delay_s: float = 1.0) → Callable
      — decorator: exponential backoff with jitter, thread-safe
    - monitor_executor_health(executor, interval_s: float = 5.0) → None
      — log thread count, queue depth, completed tasks periodically (in background thread)
  Main block: simulate parallel ingestion from 10 "sources" with rate limiting,
    fan-out → process → fan-in, show throughput; demonstrate backpressure with slow consumer

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Concurrent Data Pipeline for Multi-Source Ingestion
  Scenario: An IoT fleet has 50 sensor endpoints (simulated via local functions).
    Build a concurrent ingestion pipeline that fetches from all 50 in parallel,
    transforms the data (CPU-bound validation + enrichment), writes results to Parquet files,
    and respects a 20 requests/second rate limit.
  What to build:
    - simulate_sources.py: 50 "sensor API" functions — random latency 0.1-2.0s,
        10% chance of failure (simulate network errors), return dict with sensor data
    - pipeline.py:
        Stage 1 (I/O): ThreadPoolExecutor — fetch all 50 sources concurrently, rate-limited to 20 rps
        Stage 2 (CPU): ProcessPoolExecutor — validate + enrich records (CPU-bound)
        Stage 3 (I/O): async write results to Parquet via aiofiles
        Handle failures: retry up to 3 times with jitter; log failures without crashing
        Report: total time, records fetched, records failed, throughput (records/sec)
    - test_capstone.py: pytest —
        test rate limiter holds throughput below 20 rps
        test fan-out-fan-in preserves all records
        test retry with jitter retries exactly N times then gives up
        test pipeline handles 10% failure rate without crashing

  Acceptance criteria:
    - Pipeline completes all 50 sources in < 5 seconds (sequential would take 25-100s)
    - Rate limiter keeps throughput ≤ 20 rps (verified by timing)
    - 10% deliberate failure rate handled gracefully (no crash, logged, reported)
    - Output Parquet file has correct row count (successful fetches only)

capstone/capstone.py — pipeline.py (as above)
capstone/test_capstone.py — pytest file

===== INFRASTRUCTURE NOTES =====

Pure Python — no AWS, no Docker required.
Install: pip install aiohttp aiofiles pyarrow pandas
Python 3.11+ recommended (TaskGroup, improved asyncio).
No external APIs called — all "network" calls are simulated with time.sleep / asyncio.sleep.
Output to OUTPUT_DIR env var or /tmp/studybook/concurrency/

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
