"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-01 · Operations & Tuning                                           ║
║  Trigger intervals, micro-batch metrics, backpressure, troubleshooting.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates operational aspects of Structured Streaming.

USAGE
─────
    python 01_operations_and_tuning.py
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

spark = get_spark("operations-tuning")
ensure_lab_dirs()

print("\n── Operations & Tuning ───────────────────────────────────")

df = spark.readStream.format("rate").option("rowsPerSecond", 20).load()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Trigger: ProcessingTime — fixed-interval micro-batches
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Trigger: ProcessingTime (2 seconds) ───────────────")

query = (
    df.groupBy((df.value % 4).alias("value_group")).count()
    .writeStream
    .format("console")
    .outputMode("complete")
    .trigger(processingTime="2 seconds")
    .option("truncate", False)
    .option("numRows", 3)
    .start()
)

time.sleep(6)
query.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Micro-batch metrics via memory sink
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Micro-Batch Metrics ───────────────────────────────")

query2 = (
    df.writeStream
    .format("memory")
    .queryName("rate_table")
    .outputMode("append")
    .start()
)

time.sleep(5)

result = spark.sql("SELECT COUNT(*) as total, MIN(value) as min_val, MAX(value) as max_val FROM rate_table")
row = result.collect()[0]
print(f"    Total rows: {row['total']}, Min: {row['min_val']}, Max: {row['max_val']}")

progress = query2.recentProgress
if progress:
    for p in progress[-3:]:
        print(f"    Batch {p.get('batchId', '?')}: "
              f"input={p.get('numInputRows', 0)} rows, "
              f"duration={p.get('durationMs', {}).get('triggerExecution', 0)}ms")

query2.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Trigger: AvailableNow — process all data then stop
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Trigger: AvailableNow (process all, then stop) ────")

query3 = (
    df.writeStream
    .format("console")
    .outputMode("append")
    .trigger(processingTime="3 seconds")
    .option("truncate", False)
    .option("numRows", 3)
    .start()
)

time.sleep(6)
query3.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 4. Tuning tips
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Tuning Tips ───────────────────────────────────────")
print("    1. spark.sql.shuffle.partitions: reduce from 200 to 4-8 for small streams")
print("    2. maxFilesPerTrigger: limit file source batch size (default: unlimited)")
print("    3. maxOffsetsPerTrigger: limit Kafka batch size")
print("    4. Use AvailableNow for backfill, ProcessingTime for continuous")
print("    5. Monitor inputRowsPerSecond vs processedRowsPerSecond for backpressure")

spark.stop()
print("\n  Operations & tuning complete!")
print()
