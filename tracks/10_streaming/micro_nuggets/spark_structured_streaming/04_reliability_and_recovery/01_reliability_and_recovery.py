"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · Reliability & Recovery                                        ║
║  Checkpoint recovery, idempotent writes, exactly-once semantics.             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates checkpoint-based recovery and idempotent write patterns.

USAGE
─────
    python 01_reliability_and_recovery.py
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
from _spark_stream_connect import get_spark, ensure_lab_dirs, clean_lab, LAB_CHECKPOINT

spark = get_spark("recovery-demo")
ensure_lab_dirs()

print("\n── Reliability & Recovery ────────────────────────────────")

cp = str(LAB_CHECKPOINT / "recovery")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Start a streaming query with checkpoint
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Phase 1: Start streaming query ────────────────────")

df = spark.readStream.format("rate").option("rowsPerSecond", 10).load()

query = (
    df.writeStream
    .format("console")
    .outputMode("append")
    .option("checkpointLocation", cp)
    .option("numRows", 2)
    .start()
)

time.sleep(5)
print("    Query running for 5 seconds...")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Stop the query (simulating failure)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Phase 2: Stop query (simulating failure) ──────────")
query.stop()
print("    Query stopped. Checkpoint saved.")

# Verify checkpoint exists
import os
if os.path.exists(cp):
    offsets_dir = os.path.join(cp, "offsets")
    if os.path.exists(offsets_dir):
        offset_files = os.listdir(offsets_dir)
        print(f"    Checkpoint: {len(offset_files)} offset files saved")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Restart the query — it should resume from checkpoint
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Phase 3: Restart query (resume from checkpoint) ───")

query2 = (
    df.writeStream
    .format("console")
    .outputMode("append")
    .option("checkpointLocation", cp)
    .option("numRows", 2)
    .start()
)

time.sleep(5)
query2.stop()
print("    Query resumed from checkpoint successfully.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Exactly-once explanation
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Exactly-Once Semantics ────────────────────────────")
print("    Spark guarantees exactly-once processing FROM source TO sink.")
print("    Requirements:")
print("      1. Replayable source (Kafka offsets, file positions)")
print("      2. Checkpoint saves query state")
print("      3. Idempotent sink (file sink writes unique paths)")
print("    On restart: replays from checkpoint → same output, no duplicates.")

spark.stop()
print("\n  Reliability & recovery complete!")
print()
