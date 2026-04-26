# Python Concurrency for Data Engineers — ChatGPT Project Prompts

Priority: 🟠 Important — multiprocessing used in HorizonScale Phase 1, asked at senior level

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Python Concurrency for Data Engineers
Slug: python-concurrency

Extra coverage required:
- The GIL — the Global Interpreter Lock allows only one thread to execute Python bytecode at a time; why threads don't help CPU-bound work
- Threading vs multiprocessing — threads share memory, useful for I/O-bound tasks (waiting on network/disk); processes have separate memory, required for CPU-bound work
- concurrent.futures — ThreadPoolExecutor for I/O-bound tasks, ProcessPoolExecutor for CPU-bound tasks; the clean high-level API hiding OS-level complexity
- ProcessPoolExecutor in practice — executor.map() for simple iteration, executor.submit() for futures with individual result handling; max_workers sizing
- Handling exceptions in workers — exceptions are raised when you call future.result(); use as_completed() to process results as they arrive and catch per-future errors
- Pickling requirements — arguments and return values must be picklable to cross the process boundary; common failures with lambda functions and class methods
- asyncio — single-threaded event loop; async/await syntax; cooperative multitasking; correct for async I/O (HTTP, async DB), wrong for CPU work
- asyncio for data engineering — async HTTP requests with aiohttp, async S3 with aiobotocore, async PostgreSQL with asyncpg; parallelizing API ingestion
- multiprocessing.Queue — producer-consumer pattern; one process produces work items, pool of worker processes consumes them; backpressure via maxsize
- Rate limiting in concurrent code — asyncio.Semaphore to cap concurrent requests; tenacity for retry with exponential backoff on API rate limit errors
- The embarrassingly parallel pattern — when every task is independent with no shared state; the ideal case for ProcessPoolExecutor or Spark
- When to move to Spark — when the data exceeds a single machine's memory, when you need fault tolerance, when cluster resources are available

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. The GIL — why it matters for data engineers
  2. Threading vs Multiprocessing — the decision rule
  3. concurrent.futures — ThreadPoolExecutor & ProcessPoolExecutor
  4. Exception Handling & Pickling
  5. asyncio — event loop, async/await, when to use it
  6. asyncio for Data Engineering — aiohttp, aiobotocore, asyncpg
  7. Queue-Based Producer-Consumer Pattern
  8. Rate Limiting & The Embarrassingly Parallel Pattern
  9. When to Move to Spark
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\python-concurrency.html
