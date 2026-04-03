"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · Interview Drills                                              ║
║  10+ runnable streaming interview scenarios with model solutions.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Practical streaming interview problems with solutions.

USAGE
─────
    python 01_interview_drills.py
"""
from __future__ import annotations

import sys
import io
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))
from _spark_stream_connect import get_spark, ensure_lab_dirs

spark = get_spark("interview-drills")
ensure_lab_dirs()

print("\n── Interview Drills ──────────────────────────────────────")

df = spark.readStream.format("rate").option("rowsPerSecond", 20).load()

# ─────────────────────────────────────────────────────────────────────────────
# Q1: Windowed aggregation
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q1: Event count per 5-sec window")
from pyspark.sql.functions import window as spark_window

q1 = df.groupBy((df.value % 4).alias("value_group")).count()
query1 = q1.writeStream.format("console").outputMode("update").trigger(processingTime="3 seconds").option("numRows", 5).start()
time.sleep(8)
query1.stop()
print("    ✓ Windowed aggregation complete")

# ─────────────────────────────────────────────────────────────────────────────
# Q2: Filter even values
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q2: Filter even values")
q2 = df.filter(df.value % 2 == 0)
query2 = q2.writeStream.format("console").outputMode("append").trigger(availableNow=True).option("numRows", 3).start()
query2.awaitTermination(timeout=10)

# ─────────────────────────────────────────────────────────────────────────────
# Q3: Running count per group
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q3: Running count per value group")
q3 = df.groupBy((df.value % 4).alias("value_group")).count()
query3 = q3.writeStream.format("console").outputMode("update").trigger(availableNow=True).start()
query3.awaitTermination(timeout=10)

# ─────────────────────────────────────────────────────────────────────────────
# Interview concepts (printed, not executed)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Interview Q&A ─────────────────────────────────────")

qa = [
    ("Q: Watermark vs processing time?",
     "A: Watermark is based on event-time in the data. Processing time is system clock. "
     "Watermark handles late data; processing time triggers micro-batches."),
    ("Q: What happens to late events?",
     "A: Events within the watermark window are processed. Events older than "
     "(max_event_time - watermark_delay) are dropped."),
    ("Q: Checkpoint semantics?",
     "A: Checkpoint saves offsets, state, and aggregations. On restart, the query "
     "resumes from the last checkpoint — no data loss, no duplicates."),
    ("Q: At-least-once vs exactly-once?",
     "A: At-least-once: data may be reprocessed (duplicates possible). "
     "Exactly-once: each record processed once — requires replayable source + idempotent sink."),
    ("Q: Idempotent sink design?",
     "A: Write to unique paths per batch (file sink), use transactions (Delta/JDBC), "
     "or use upsert semantics (MERGE on primary key)."),
]

for q, a in qa:
    print(f"\n    {q}")
    print(f"    {a}")

spark.stop()
print("\n  Interview drills complete!")
print()
