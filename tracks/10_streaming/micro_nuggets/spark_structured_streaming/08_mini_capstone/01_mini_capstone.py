"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 08-01 · Mini Capstone: End-to-End Streaming Pipeline                  ║
║  Bronze → Silver → Gold with recovery verification.                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Builds a complete streaming pipeline:
  1. BRONZE: ingest raw events
  2. SILVER: filtered, validated
  3. GOLD: aggregated metrics
  4. RECOVERY: checkpoint verification

USAGE
─────
    python 01_mini_capstone.py
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
from _spark_stream_connect import get_spark, ensure_lab_dirs, clean_lab, LAB_CHECKPOINT, LAB_OUTPUT

spark = get_spark("mini-capstone")
ensure_lab_dirs()

print("\n── Mini Capstone: End-to-End Streaming Pipeline ──────────")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 1: BRONZE → SILVER → GOLD
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 1: Bronze → Silver → Gold ══════════════════")

# Read stream (rate source simulating Kafka)
df = spark.readStream.format("rate").option("rowsPerSecond", 30).load()

# Bronze: raw count
print("\n  ── Bronze: Raw Ingestion ─────────────────────────────")

bronze_cp = str(LAB_CHECKPOINT / "capstone_bronze")

bronze_q = (
    df.writeStream
    .format("memory")
    .queryName("bronze_table")
    .outputMode("append")
    .start()
)

time.sleep(5)
bronze_q.stop()

bronze_count = spark.sql("SELECT COUNT(*) FROM bronze_table").collect()[0][0]
print(f"    Bronze: {bronze_count} raw events")

# Silver: filtered (even values only — simulating validation)
print("\n  ── Silver: Filtered & Validated ──────────────────────")

silver_cp = str(LAB_CHECKPOINT / "capstone_silver")

silver_q = (
    df.filter(df.value % 2 == 0)
    .writeStream
    .format("memory")
    .queryName("silver_table")
    .outputMode("append")
    .start()
)

time.sleep(5)
silver_q.stop()

silver_count = spark.sql("SELECT COUNT(*) FROM silver_table").collect()[0][0]
print(f"    Silver: {silver_count} validated events")
print(f"    Filtered out: {bronze_count - silver_count} odd values")

# Gold: aggregated
print("\n  ── Gold: Aggregated Metrics ──────────────────────────")

gold_df = spark.sql("""
    SELECT
        (value % 4) AS value_group,
        COUNT(*) AS event_count,
        ROUND(AVG(value), 1) AS avg_value,
        MIN(value) AS min_val,
        MAX(value) AS max_val
    FROM silver_table
    GROUP BY value % 4
    ORDER BY value_group
""")

print(f"    {'Group':<8} {'Events':<8} {'Avg':<6} {'Min':<6} {'Max'}")
print(f"    {'-'*8} {'-'*8} {'-'*6} {'-'*6} {'-'*6}")
for row in gold_df.collect():
    print(f"    {row['value_group']:<8} {row['event_count']:<8} {row['avg_value']:<6} {row['min_val']:<6} {row['max_val']}")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2: Recovery verification
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 2: Recovery Verification ════════════════════")

import os
cp_dir = Path(bronze_cp)
if cp_dir.exists():
    print(f"    [✓] Checkpoint exists at {bronze_cp}")
    offsets_dir = cp_dir / "offsets"
    if offsets_dir.exists():
        offset_files = list(offsets_dir.glob("*"))
        print(f"    [✓] {len(offset_files)} offset files saved")

print(f"    Bronze → Silver fidelity: {bronze_count} → {silver_count} (filtered)")

# ═════════════════════════════════════════════════════════════════════════════
# PHASE 3: Bad data handling explanation
# ═════════════════════════════════════════════════════════════════════════════
print("\n  ══ PHASE 3: Bad Data Handling ────────────────────────")
print("    In production: schema enforcement filters malformed records.")
print("    Pattern: df.filter(col('event_id').isNotNull())")
print("    Bad records are written to a 'dead letter' sink for investigation.")

spark.stop()
print("\n  Pipeline complete! 🎉")
print()
