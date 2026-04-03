"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · Interview Drills                                              ║
║  Streaming interview scenarios with model solutions.                         ║
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
spark.sparkContext.setLogLevel("ERROR")
ensure_lab_dirs()
WINDOWS_MODE = sys.platform == "win32"

print("\n── Interview Drills ──────────────────────────────────────")

if WINDOWS_MODE:
    print("    [!] Windows mode: using fallback batch interview drill.")
    df = spark.range(0, 80).selectExpr("CAST(id AS BIGINT) AS value")
else:
    df = spark.readStream.format("rate").option("rowsPerSecond", 20).load()

# ─────────────────────────────────────────────────────────────────────────────
# Q1: Group by value range and count
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Q1: Event count per value group")

q1 = df.groupBy((df.value % 4).alias("value_group")).count()
if WINDOWS_MODE:
    q1.orderBy("value_group").show(5, truncate=False)
else:
    query1 = q1.writeStream.format("console").outputMode("update").trigger(processingTime="3 seconds").option("numRows", 5).start()
    time.sleep(8)
    query1.stop()
print("    ✓ Grouped aggregation complete")

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
    ("Q: How do you handle backpressure?",
     "A: Spark auto-throttles. Monitor inputRowsPerSecond vs processedRowsPerSecond. "
     "If processing < input, reduce shuffle partitions or increase parallelism."),
    ("Q: Trigger types?",
     "A: ProcessingTime (fixed interval), AvailableNow (process all then stop), "
     "Continuous (sub-second, experimental). Use ProcessingTime for production."),
]

for q, a in qa:
    print(f"\n    {q}")
    print(f"    {a}")

spark.stop()
print("\n  Interview drills complete!")
print()
