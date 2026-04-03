"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-01 · Streaming Basics                                               ║
║  readStream from rate source, parse, writeStream to console and memory.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates the minimal Structured Streaming pattern:
  1. Read streaming data from a source
  2. Transform
  3. Write to output sink

CONCEPTS
────────
readStream:
  - Creates a streaming DataFrame — looks like a static table but is unbounded.
  - Source types: rate (testing), kafka, socket, file.

writeStream:
  - Starts the streaming query.
  - Output modes: append, update, complete.
  - Sinks: console, memory, foreach.

USAGE
─────
    python 01_streaming_basics.py
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

spark = get_spark("streaming-basics")
ensure_lab_dirs()

print("\n── Streaming Basics ──────────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Read from rate source (generates rows at fixed rate for testing)
#    This is Spark's built-in test source — no files or Kafka needed.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── ReadStream from Rate Source ───────────────────────")

df = (
    spark.readStream
    .format("rate")
    .option("rowsPerSecond", 10)
    .option("numPartitions", 2)
    .load()
)

print(f"    Streaming DataFrame schema:")
df.printSchema()

# Simple transformation: filter even timestamps
filtered = df.filter(df.value % 2 == 0)

# Write stream — console sink (for demonstration)
query = (
    filtered.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option("numRows", 3)
    .start()
)

time.sleep(8)
query.stop()
print(f"\n    Query stopped after first batches.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Write to memory sink — queryable as a temp view
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── WriteStream to Memory Sink ────────────────────────")

query2 = (
    df.selectExpr("timestamp", "value")
    .writeStream
    .format("memory")
    .queryName("rate_stream")
    .outputMode("append")
    .start()
)

time.sleep(5)

# Query the memory sink as a regular DataFrame
result = spark.sql("SELECT COUNT(*) as total, MIN(value) as min_val, MAX(value) as max_val FROM rate_stream")
result.show()

query2.stop()

spark.stop()
print("\n  Basics complete!")
print()
