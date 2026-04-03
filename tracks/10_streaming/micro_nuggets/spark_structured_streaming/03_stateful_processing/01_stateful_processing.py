"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · Stateful Processing                                           ║
║  Deduplication, stateful aggregations, handling out-of-order records.        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates stateful streaming patterns that maintain state across micro-batches.

USAGE
─────
    python 01_stateful_processing.py
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

spark = get_spark("stateful-processing")
spark.sparkContext.setLogLevel("ERROR")
ensure_lab_dirs()
WINDOWS_MODE = sys.platform == "win32"

print("\n── Stateful Processing ───────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Stateful aggregation — running count per partition
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Running Count per Partition (stateful agg) ────────")

if WINDOWS_MODE:
    print("    [!] Windows mode: using fallback batch aggregation.")
    batch_df = spark.range(0, 40).selectExpr("CAST(id AS BIGINT) AS value")
    count_per_partition = (
        batch_df
        .selectExpr("value % 4 AS value_group")
        .groupBy("value_group")
        .count()
        .orderBy("value_group")
    )
    count_per_partition.show(truncate=False)
else:
    df = spark.readStream.format("rate").option("rowsPerSecond", 10).load()
    count_per_partition = df.groupBy((df.value % 4).alias("value_group")).count()
    query = (
        count_per_partition
        .writeStream
        .format("console")
        .outputMode("update")
        .option("truncate", False)
        .option("numRows", 5)
        .start()
    )
    time.sleep(8)
    query.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 2. Out-of-order handling explanation
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Out-of-Order Handling ─────────────────────────────")
print("    Scenario: Event A (time=10:00) arrives after Event B (time=10:05)")
print("    With watermark of 10 minutes:")
print("      - If current max time is 10:10, watermark = 10:00")
print("      - Event A at 10:00 is AT the watermark boundary — still accepted")
print("      - Event at 09:55 would be DROPPED")
print("    Without watermark: state grows unbounded → OOM eventually")

spark.stop()
print("\n  Stateful processing complete!")
print()
