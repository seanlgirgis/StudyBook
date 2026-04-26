# 🚀 Python Concurrency for Data Engineers

**Priority:** Toyota Interview Prep
**Focus:** Practical, production-ready concurrency patterns in Python
**Scope:** Threading, Multiprocessing, AsyncIO, Executors, and Real-World Data Engineering Patterns

---

## 📚 Overview

This study module is designed to take you from **conceptual understanding → production-ready implementation** of Python concurrency.

You will learn:

* ✅ When to use **threading vs multiprocessing vs asyncio**
* ✅ How the **GIL actually works** (and when it matters)
* ✅ How to build **real data pipelines with concurrency**
* ✅ How to handle **failures, retries, rate limits, and backpressure**
* ✅ How to explain all of this clearly in interviews

---

## 🧠 The One Thing You Must Understand (Interview Core)

> **The GIL is NOT the problem — misunderstanding it is.**

| Work Type      | Best Tool       | Why                               |
| -------------- | --------------- | --------------------------------- |
| I/O-bound      | Threading       | GIL releases during I/O           |
| CPU-bound      | Multiprocessing | Each process has its own GIL      |
| High-scale I/O | AsyncIO         | Event loop avoids thread overhead |

---

## 📂 Project Structure

```
13_python_concurrency/
│
├── 01_threading_for_io_bound.py
├── 02_multiprocessing_for_cpu_bound.py
├── 03_asyncio_for_data_pipelines.py
├── 04_concurrent_futures_patterns.py
├── 05_concurrency_patterns_for_de.py
│
└── capstone/
    ├── simulate_sources.py
    ├── pipeline.py
    └── test_capstone.py
```

---

## 🧵 01 — Threading (I/O-bound Work)

**Key Concepts:**

* ThreadPoolExecutor
* GIL behavior with I/O
* Race conditions
* Locks vs queues

**What You Learn:**

* Why threading is fast for APIs / DB calls
* Why `counter += 1` is NOT safe
* Producer-consumer pipeline

**Interview Soundbite:**

> “Threading works for I/O because blocking calls release the GIL.”

---

## ⚙️ 02 — Multiprocessing (CPU-bound Work)

**Key Concepts:**

* ProcessPoolExecutor
* True parallelism
* Pickling overhead
* Shared memory

**What You Learn:**

* Why threads fail for CPU work
* When multiprocessing is slower (!)
* How to avoid serialization cost

**Rule of Thumb:**

> Use multiprocessing only if task > ~10ms CPU

---

## ⚡ 03 — AsyncIO (Event-Driven Pipelines)

**Key Concepts:**

* Coroutines & event loop
* asyncio.gather
* Semaphores (rate limiting)
* TaskGroup (Python 3.11+)

**What You Learn:**

* How to build async ETL pipelines
* Structured concurrency
* Error handling without crashing pipeline

**Interview Soundbite:**

> “AsyncIO scales I/O concurrency without threads by using cooperative multitasking.”

---

## 🔁 04 — concurrent.futures Patterns

**Key Concepts:**

* Unified API (threads + processes)
* Two-stage pipelines (I/O → CPU)
* as_completed()
* Timeout handling

**What You Learn:**

* Real production pipeline design
* Failure isolation
* Executor selection logic

---

## 🏗️ 05 — Data Engineering Patterns

**Key Concepts:**

* Rate limiting (Token Bucket)
* Fan-out / fan-in
* Backpressure (bounded queues)
* Retry with exponential backoff + jitter

**What You Learn:**

* How real pipelines behave under load
* Preventing system overload
* Designing resilient ingestion systems

---

## 🧪 Capstone Project (Real Interview-Level)

### 🎯 Goal:

Build a **Concurrent IoT Data Pipeline**

### Features:

* Fetch 50 endpoints concurrently
* Rate limit: **20 requests/sec**
* Retry with backoff
* CPU-based enrichment (multiprocessing)
* Write results to **Parquet**
* Full **pytest test suite**

### Pipeline:

```
[ThreadPool] → Fetch (I/O)
        ↓
[ProcessPool] → Transform (CPU)
        ↓
[Write] → Parquet Output
```

---

## 🧠 Key Patterns to Memorize

### 1. I/O vs CPU Decision

```python
if task == "io":
    use ThreadPoolExecutor
elif task == "cpu":
    use ProcessPoolExecutor
```

---

### 2. Two-Stage Pipeline

```python
data = thread_pool(fetch)
result = process_pool(transform)
```

---

### 3. Backpressure

```python
queue.Queue(maxsize=N)
```

---

### 4. Retry Pattern

```python
delay = base * (2 ** attempt) + jitter
```

---

### 5. Rate Limiting

```python
TokenBucket(max_rps)
```

---

## ⚠️ Common Mistakes (Interview Traps)

| Mistake                               | Why It’s Wrong                 |
| ------------------------------------- | ------------------------------ |
| “Threads are useless because of GIL”  | ❌ Wrong — great for I/O        |
| Using multiprocessing for small tasks | ❌ Slower due to pickling       |
| Ignoring backpressure                 | ❌ Leads to memory blowups      |
| No retry logic                        | ❌ Production systems WILL fail |
| Using async without limits            | ❌ Can overload services        |

---

## 🏁 Final Takeaways

* **Threading = I/O parallelism**
* **Multiprocessing = CPU parallelism**
* **AsyncIO = scalable I/O orchestration**
* **Queues + rate limits = production safety**
* **Retries + jitter = resilience**

---

## 💬 Interview Cheat Answer

> “For data pipelines, I typically use threads for ingestion (I/O-bound), processes for transformations (CPU-bound), and enforce rate limits and backpressure using queues. If I need massive I/O scale, I switch to asyncio.”

---

## ▶️ How to Run

```bash
python 01_threading_for_io_bound.py
python 02_multiprocessing_for_cpu_bound.py
python 03_asyncio_for_data_pipelines.py
python 04_concurrent_futures_patterns.py
python 05_concurrency_patterns_for_de.py
```

---

## 🔥 What You Now Know

You can now:

* Explain the GIL correctly (rare skill)
* Build concurrent pipelines from scratch
* Choose the right concurrency model instantly
* Handle real-world failure scenarios
* Pass **senior-level Python interviews**

---

**Next Step:**
👉 Run the capstone project and tests.

Say: **"generate sources"**
