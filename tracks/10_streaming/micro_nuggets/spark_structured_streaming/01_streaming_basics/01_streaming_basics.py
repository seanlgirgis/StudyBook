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
import shutil
import uuid
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))
from _spark_stream_connect import get_spark, ensure_lab_dirs, LAB_CHECKPOINT

spark = get_spark("streaming-basics")
ensure_lab_dirs()
spark.sparkContext.setLogLevel("ERROR")

print("\n── Streaming Basics ──────────────────────────────────────")
WINDOWS_MODE = sys.platform == "win32"


def _is_windows_nativeio_error(err: object) -> bool:
    return "NativeIO$Windows.access0" in str(err)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Read from rate source (generates rows at fixed rate for testing)
#    This is Spark's built-in test source — no files or Kafka needed.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── ReadStream from Rate Source ───────────────────────")

if WINDOWS_MODE:
    print("    [!] Windows mode: using fallback path to avoid Hadoop NativeIO noise.")
    print("    [!] Streaming query startup skipped on Windows.")
    fallback_mode = True
    df = spark.range(0, 20).selectExpr(
        "current_timestamp() as timestamp",
        "CAST(id AS BIGINT) as value",
    )
else:
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
    fallback_mode = False
    query = (
        filtered.writeStream
        .format("console")
        .outputMode("append")
        .option("truncate", False)
        .option("numRows", 3)
        .option("checkpointLocation", str(LAB_CHECKPOINT / f"basics_console_{uuid.uuid4().hex[:8]}"))
        .start()
    )

    try:
        try:
            query.awaitTermination(8)
        except Exception as exc:
            if _is_windows_nativeio_error(exc):
                fallback_mode = True
            else:
                raise
        q_err = query.exception()
        if q_err and _is_windows_nativeio_error(q_err):
            fallback_mode = True
    finally:
        if query.isActive:
            query.stop()
    print(f"\n    Query stopped after first batches.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Write to memory sink — queryable as a temp view
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── WriteStream to Memory Sink ────────────────────────")

memory_ckpt = LAB_CHECKPOINT / "basics_memory"
if memory_ckpt.exists():
    shutil.rmtree(memory_ckpt, ignore_errors=True)

if fallback_mode:
    print("    [!] Windows Hadoop native IO limitation detected.")
    print("    [!] Running fallback static summary for this nugget.")
    static_df = spark.range(0, 20).selectExpr("CAST(id AS BIGINT) AS value")
    static_df.createOrReplaceTempView("rate_stream_fallback")
    result = spark.sql(
        "SELECT COUNT(*) as total, MIN(value) as min_val, MAX(value) as max_val "
        "FROM rate_stream_fallback"
    )
    result.show()
else:
    query2 = (
        df.selectExpr("timestamp", "value")
        .writeStream
        .format("memory")
        .queryName(f"rate_stream_{uuid.uuid4().hex[:8]}")
        .outputMode("append")
        .option("checkpointLocation", str(memory_ckpt))
        .start()
    )

    try:
        try:
            query2.awaitTermination(5)
        except Exception as exc:
            if _is_windows_nativeio_error(exc):
                q2_err = exc
            else:
                raise
        else:
            q2_err = query2.exception()
        if q2_err and _is_windows_nativeio_error(q2_err):
            print("    [!] Memory sink hit Windows native IO limitation.")
            print("    [!] Showing fallback static summary.")
            static_df = spark.range(0, 20).selectExpr("CAST(id AS BIGINT) AS value")
            static_df.createOrReplaceTempView("rate_stream_fallback")
            result = spark.sql(
                "SELECT COUNT(*) as total, MIN(value) as min_val, MAX(value) as max_val "
                "FROM rate_stream_fallback"
            )
            result.show()
        else:
            result = spark.sql(
                "SELECT COUNT(*) as total, MIN(value) as min_val, MAX(value) as max_val "
                f"FROM {query2.name}"
            )
            result.show()
    finally:
        if query2.isActive:
            query2.stop()

spark.stop()
print("\n  Basics complete!")
print()
