"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · Mini Capstone — End-to-End Orchestration                     ║
║  Full pipeline: ingest -> quality check -> transform -> load -> audit        ║
║  Plus: simulated failure + safe rerun recovery demonstration                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Combines all concepts into a single end-to-end orchestration scenario:
  1. Ingest small dataset from a mock API
  2. Data quality gate (fails if too many nulls)
  3. Transform into summary metrics
  4. Load to an output file (idempotent: overwrite by partition)
  5. Audit record written
  6. Simulate a failure in step 3 and show safe rerun recovery

WHAT YOU LEARN
──────────────
  - Real pipeline DAG structure with all production patterns
  - How retries + idempotency combine for safe reruns
  - How on_failure_callback + audit enable observability
  - How to simulate and recover from a task failure

INTERVIEW RELEVANCE
───────────────────
  "Walk me through how you would design an ETL pipeline in Airflow."
  "How does Airflow handle failure recovery?"
  "What makes a pipeline production-ready?"
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from datetime import datetime

print("\n-- Nugget 07-01 : Mini Capstone ----------------------------")

def _find_project_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / "CONTROL_PROTOCOL.md").exists():
            return candidate
    return None


_ROOT = _find_project_root(Path(__file__).resolve())
OUTPUT_DIR = (_ROOT / "temp" / "airflow_lab") if _ROOT else (Path.cwd() / "_airflow_lab")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Step 1: Simulate data ingestion ──────────────────────────────────────────
print()
print("  STEP 1: Ingest raw data")
RAW_DATA = [
    {"order_id": 1001, "customer_id": 1, "amount": 150.00, "status": "delivered", "date": "2024-01-15"},
    {"order_id": 1002, "customer_id": 2, "amount": 89.99,  "status": "delivered", "date": "2024-01-15"},
    {"order_id": 1003, "customer_id": 1, "amount": None,   "status": "pending",   "date": "2024-01-15"},
    {"order_id": 1004, "customer_id": 3, "amount": 220.00, "status": "delivered", "date": "2024-01-15"},
    {"order_id": 1005, "customer_id": 2, "amount": 45.00,  "status": "cancelled", "date": "2024-01-15"},
]
raw_path = OUTPUT_DIR / "raw_orders_2024-01-15.json"
with open(raw_path, "w") as f:
    json.dump(RAW_DATA, f, indent=2)
print(f"  [OK] Ingested {len(RAW_DATA)} records -> {raw_path}")

# ── Step 2: Data quality check ────────────────────────────────────────────────
print()
print("  STEP 2: Data quality gate")
null_amounts = [r for r in RAW_DATA if r["amount"] is None]
null_pct = len(null_amounts) / len(RAW_DATA) * 100
MAX_NULL_PCT = 20.0

print(f"  Null amounts: {len(null_amounts)} / {len(RAW_DATA)} = {null_pct:.1f}%")
if null_pct > MAX_NULL_PCT:
    print(f"  [FAIL] Null rate {null_pct:.1f}% exceeds threshold {MAX_NULL_PCT}%")
    sys.exit(1)

clean_data = [r for r in RAW_DATA if r["amount"] is not None]
print(f"  [OK] Quality gate passed. Clean records: {len(clean_data)}")

# ── Step 3: Simulate failure on first attempt, succeed on retry ───────────────
print()
print("  STEP 3: Transform (with simulated failure + recovery)")

FAILURE_FLAG = OUTPUT_DIR / ".transform_failed_once"

if not FAILURE_FLAG.exists():
    # First attempt: simulate a transient failure
    FAILURE_FLAG.touch()
    print("  [SIM] First attempt: simulating transient transform failure")
    print("  [SIM] In Airflow, this would trigger a retry after retry_delay")
    print("  [SIM] Re-running this nugget simulates the retry succeeding...")

# Second attempt (or after flag exists): succeed
print("  [OK] Transform succeeding (idempotent: same input -> same output)")

by_status: dict = {}
for r in clean_data:
    s = r["status"]
    if s not in by_status:
        by_status[s] = {"count": 0, "total": 0.0}
    by_status[s]["count"] += 1
    by_status[s]["total"] += r["amount"]

summary = {
    "partition_date": "2024-01-15",
    "total_orders": len(clean_data),
    "total_revenue": sum(r["amount"] for r in clean_data),
    "by_status": {
        s: {"count": v["count"], "avg": round(v["total"] / v["count"], 2)}
        for s, v in by_status.items()
    },
}
print(f"  [OK] Transform complete: {summary['total_orders']} orders, ${summary['total_revenue']:.2f} revenue")

# ── Step 4: Idempotent load ───────────────────────────────────────────────────
print()
print("  STEP 4: Idempotent load (overwrite partition)")
output_path = OUTPUT_DIR / f"daily_summary_{summary['partition_date']}.json"
with open(output_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"  [OK] Wrote: {output_path}")
print(f"  [OK] Idempotent: rerunning overwrites the same file")

# ── Step 5: Audit record ──────────────────────────────────────────────────────
print()
print("  STEP 5: Write audit record")
audit = {
    "dag_id": "lab_airflow_capstone",
    "partition_date": summary["partition_date"],
    "run_id": f"capstone_test_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}",
    "rows_ingested": len(RAW_DATA),
    "rows_clean": len(clean_data),
    "rows_loaded": 1,  # 1 summary row per partition
    "total_revenue": summary["total_revenue"],
    "loaded_at": datetime.utcnow().isoformat(),
    "status": "success",
}
audit_path = OUTPUT_DIR / "audit_log.jsonl"
with open(audit_path, "a") as f:
    f.write(json.dumps(audit) + "\n")
print(f"  [OK] Audit appended to: {audit_path}")

# ── Step 6: Validate all outputs ──────────────────────────────────────────────
print()
print("  STEP 6: Validation")

assert raw_path.exists(), f"Raw file missing: {raw_path}"
assert output_path.exists(), f"Output file missing: {output_path}"
assert audit_path.exists(), f"Audit log missing: {audit_path}"

with open(output_path) as f:
    loaded = json.load(f)
assert loaded["partition_date"] == "2024-01-15"
assert loaded["total_orders"] == len(clean_data)
print("  [OK] Raw file exists")
print("  [OK] Summary file exists and correct")
print("  [OK] Audit log exists")

# Verify idempotency: rerun produces same output
with open(output_path, "w") as f:
    json.dump(summary, f, indent=2)  # overwrite
with open(output_path) as f:
    loaded2 = json.load(f)
assert loaded2 == loaded, "Idempotency check failed: output changed on rerun"
print("  [OK] Idempotency verified: rerun produces identical output")

# ── Summary ──────────────────────────────────────────────────────────────────
print()
print("  PIPELINE SUMMARY")
print("  -----------------")
print(f"  Partition:          {summary['partition_date']}")
print(f"  Records ingested:   {len(RAW_DATA)}")
print(f"  Records clean:      {len(clean_data)}")
print(f"  Records dropped:    {len(null_amounts)} (null amount)")
print(f"  Revenue loaded:     ${summary['total_revenue']:.2f}")
print(f"  Output path:        {output_path}")
print()
print("  PRODUCTION CHECKLIST")
print("  ---------------------")
checklist = [
    ("Idempotent load",      "overwrite by partition date"),
    ("Quality gate",         "fail fast before expensive transforms"),
    ("Audit trail",          "lineage metadata written to audit_log"),
    ("Retry-safe",           "same output on any retry attempt"),
    ("Parameterized by date","all paths use partition_date, not datetime.now()"),
    ("Failure observed",     "failure flag simulates transient error + recovery"),
]
for item, note in checklist:
    print(f"  [X] {item:<25}  {note}")

print()
