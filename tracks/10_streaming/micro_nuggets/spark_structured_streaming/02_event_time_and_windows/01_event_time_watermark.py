"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Event Time & Watermarks                                       ║
║  Processing-time vs event-time, watermarking, late data handling.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates event-time processing, watermarks, and how Spark handles late data.

USAGE
─────
    python 01_event_time_watermark.py
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

spark = get_spark("event-time-watermark")
ensure_lab_dirs()

print("\n── Event Time & Watermarks ───────────────────────────────")

# Use rate source for reliable testing
df = spark.readStream.format("rate").option("rowsPerSecond", 10).load()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Watermark concept demonstration
#    Since rate source uses processing-time timestamps, we demonstrate
#    the watermark pattern conceptually with a batch example.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Watermark Concept ─────────────────────────────────")
print("    Watermark = max_event_time - delay_threshold")
print("    Example: max event time = 10:00, delay = 10 min")
print("    Watermark = 09:50")
print("    Events before 09:50 → DROPPED")
print("    Events after 09:50 → PROCESSED")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Streaming aggregation with watermark (using rate source timestamp)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Streaming Aggregation with Watermark ──────────────")

from pyspark.sql.functions import window as spark_window

windowed = (
    df.withWatermark("timestamp", "10 seconds")
    .groupBy(spark_window(df.timestamp, "5 seconds"))
    .count()
)

query = (
    windowed.writeStream
    .format("console")
    .outputMode("complete")
    .option("truncate", False)
    .option("numRows", 5)
    .start()
)

time.sleep(10)
query.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 3. Late data demonstration
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Late Data Handling ────────────────────────────────")
print("    Scenario: Event at time=10:00 arrives after event at 10:05")
print("    With 10-minute watermark:")
print("      - If max time is 10:10, watermark = 10:00")
print("      - Event at 10:00 is AT boundary — still accepted")
print("      - Event at 09:55 would be DROPPED")

spark.stop()
print("\n  Event time & watermark complete!")
print()
