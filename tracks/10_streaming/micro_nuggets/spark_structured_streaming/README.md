# Spark Structured Streaming Micro-Nuggets

Quick, focused, runnable lessons on Spark Structured Streaming for Data Engineering.

Each nugget is a standalone Python script that:
- **Teaches one concept** with inline comments
- **Runs end-to-end** — file-based (Kafka optional)
- **Prints expected output** in the docstring
- **Builds on previous nuggets**

---

## Structure

```
spark_structured_streaming/
│
├── _spark_stream_connect.py                ← shared Spark/Kafka helper
├── run_all_spark_streaming_nuggets.py      ← one-command validation runner
│
├── 00_setup/
│   ├── 00_prereq_check.py                  ← Python, PySpark, Kafka, Java checks
│   └── 01_seed_lab.py                      ← Create topics, seed events (idempotent)
│
├── 01_streaming_basics/
│   └── 01_streaming_basics.py              ← readStream, parse JSON, writeStream, console/file sinks
│
├── 02_event_time_and_windows/
│   └── 01_event_time_watermark.py          ← event-time, watermark, tumbling windows, late data
│
├── 03_stateful_processing/
│   └── 01_stateful_processing.py           ← dedup, stateful aggs, out-of-order handling
│
├── 04_reliability_and_recovery/
│   └── 01_reliability_and_recovery.py      ← checkpoint recovery, idempotent writes, exactly-once
│
├── 05_kafka_to_lake_patterns/
│   └── 01_kafka_to_lake.py                 ← Bronze→Silver→Gold from Kafka
│
├── 06_operations_and_tuning/
│   └── 01_operations_and_tuning.py         ← triggers, metrics, backpressure, troubleshooting
│
├── 07_interview_drills/
│   └── 01_interview_drills.py              ← 5 runnable scenarios + 5 Q&A
│
└── 08_mini_capstone/
    └── 01_mini_capstone.py                 ← End-to-end pipeline + bad batch + recovery
```

---

## Prerequisites

1. **Python venv:**
   ```powershell
   cd D:\StudyBook\tracks\10_streaming\micro_nuggets\spark_structured_streaming
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install --upgrade pip
   pip install pyspark kafka-python requests
   ```

2. **Java (required by PySpark):**
   - Install JDK 11 or 17
   - Set `JAVA_HOME`: `setx JAVA_HOME "C:\path\to\jdk"`

3. **Docker (optional, for Kafka):**
   ```powershell
   pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group streaming
   pwsh D:\StudyBook\_infra\scripts\infra_up.ps1 -Group pipeline
   ```

---

## Running Order

```powershell
cd D:\StudyBook\tracks\10_streaming\micro_nuggets\spark_structured_streaming

# 1. Check prerequisites
python 00_setup/00_prereq_check.py

# 2. Seed lab environment
python 00_setup/01_seed_lab.py

# 3. Run all nuggets
python run_all_spark_streaming_nuggets.py

# Or run individually:
python 01_streaming_basics/01_streaming_basics.py
```

---

## Reset Lab

```powershell
python 00_setup/01_seed_lab.py --reset
```

---

## Key Concepts Covered

| Module | Concepts | Interview Relevance |
|--------|----------|---------------------|
| Streaming Basics | readStream, writeStream, output modes, sinks | ★★★★★ |
| Event Time & Windows | Watermark, tumbling/sliding windows, late data | ★★★★★ |
| Stateful Processing | Dedup, stateful aggs, out-of-order | ★★★★★ |
| Reliability | Checkpoint recovery, idempotent writes, exactly-once | ★★★★ |
| Kafka to Lake | Bronze→Silver→Gold, schema evolution | ★★★★★ |
| Operations | Triggers, metrics, backpressure, tuning | ★★★★ |
| Interview Drills | Windowing, dedup, running totals, Q&A | ★★★★★ |
| Capstone | End-to-end pipeline, bad batch, recovery | ★★★★ |

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `JAVA_HOME not set` | Java not found | Install JDK 11/17, set JAVA_HOME |
| `pyspark not found` | Package not installed | `pip install pyspark` |
| `Kafka unreachable` | Docker not running | `infra_up.ps1 -Group streaming` |
| `Checkpoint path error` | Permission issue | Use absolute path in `_lab/checkpoint/` |
| `Stream already active` | Previous query not stopped | Call `query.stop()` before new query |
| `Execution policy` | PowerShell blocks scripts | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

---

Last updated: 2026-04-02
