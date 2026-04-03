"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 05-01 · Kafka to Data Lake Patterns                                   ║
║  Bronze → Silver → Gold streaming pipeline pattern.                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates the canonical streaming lakehouse pattern using rate source
(simulating Kafka ingestion for Windows compatibility).

CONCEPTS
────────
Bronze layer: Raw, unmodified data from source.
Silver layer: Parsed, validated, deduplicated.
Gold layer: Aggregated, business-ready metrics.

USAGE
─────
    python 01_kafka_to_lake.py
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

spark = get_spark("kafka-to-lake")
ensure_lab_dirs()

print("\n── Kafka to Data Lake Patterns ───────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# BRONZE: Read raw stream (using rate source to simulate Kafka)
# In production: spark.readStream.format("kafka").option("subscribe", "topic")
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ══ BRONZE: Raw Ingestion ════════════════════════════")

df = spark.readStream.format("rate").option("rowsPerSecond", 20).load()
print(f"    Bronze schema: {df.columns}")

# ─────────────────────────────────────────────────────────────────────────────
# SILVER: Transform and filter
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ══ SILVER: Cleaned & Filtered ═══════════════════════")

silver = df.filter(df.value % 2 == 0)  # Simulate filtering valid records

query = (
    silver.writeStream
    .format("memory")
    .queryName("silver_table")
    .outputMode("append")
    .start()
)

time.sleep(5)
query.stop()

silver_count = spark.sql("SELECT COUNT(*) FROM silver_table").collect()[0][0]
print(f"    Silver records processed: {silver_count}")

# ─────────────────────────────────────────────────────────────────────────────
# GOLD: Aggregated metrics
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ══ GOLD: Aggregated Metrics ═════════════════════════")

gold = spark.sql("""
    SELECT
        (value % 4) AS value_group,
        COUNT(*) AS event_count,
        MIN(value) AS min_value,
        MAX(value) AS max_value,
        ROUND(AVG(value), 1) AS avg_value
    FROM silver_table
    GROUP BY value % 4
    ORDER BY value_group
""")

print(f"    {'Partition':<10} {'Count':<8} {'Min':<6} {'Max':<6} {'Avg'}")
print(f"    {'-'*10} {'-'*8} {'-'*6} {'-'*6} {'-'*6}")
for row in gold.collect():
    print(f"    {row['partition_id']:<10} {row['event_count']:<8} {row['min_value']:<6} {row['max_value']:<6} {row['avg_value']:.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# Kafka pattern explanation
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Kafka Source Pattern (production) ─────────────────")
print("    df = spark.readStream.format('kafka')")
print("        .option('kafka.bootstrap.servers', 'localhost:9092')")
print("        .option('subscribe', 'raw_events')")
print("        .option('startingOffsets', 'earliest')")
print("        .load()")
print("        .selectExpr('CAST(value AS STRING) as json_str')")

spark.stop()
print("\n  Kafka to lake pipeline complete!")
print()
