# Python Concurrency for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — multiprocessing used in HorizonScale Phase 1, asked about at senior level

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Python Concurrency for Data Engineers
Slug: python-concurrency
Extra coverage required: the GIL — what the Global Interpreter Lock is, why it prevents true thread parallelism for CPU-bound work,
threading vs multiprocessing — the core distinction, when threads work (I/O-bound), when processes are required (CPU-bound),
concurrent.futures — ThreadPoolExecutor for I/O-bound tasks, ProcessPoolExecutor for CPU-bound tasks — the clean high-level API,
ProcessPoolExecutor in practice — submitting tasks, map vs submit, futures, handling exceptions from workers,
multiprocessing.Pool — map, starmap, imap_unordered — when to use each,
avoiding pitfalls — pickling requirements for multiprocessing, shared state dangers, deadlocks,
asyncio — the event loop model, async/await syntax, when asyncio is the right tool (async I/O, not CPU work),
asyncio for data engineering — async HTTP calls, async database drivers (asyncpg, aiobotocore),
process-based parallelism for ML models — running Prophet fits in parallel with ProcessPoolExecutor before moving to Spark,
queue-based patterns — multiprocessing.Queue for producer-consumer pipelines,
threading for pipeline I/O — parallel S3 uploads, parallel database inserts with connection pooling,
concurrent.futures.as_completed — processing results as they arrive rather than waiting for all,
rate limiting in concurrent code — semaphores, throttling API calls,
the embarrassingly parallel pattern — when a problem has zero shared state and every task is independent,
real scenario: local parallel forecasting across 2,000+ series before Spark migration in HorizonScale.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug python-concurrency -ChunkSize 750
```

Upload final_python-concurrency.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_python-concurrency.mp3` is live on R2.

```
Topic: Python Concurrency for Data Engineers
Slug: python-concurrency
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_python-concurrency.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\python-concurrency.html
