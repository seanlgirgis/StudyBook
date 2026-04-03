from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 07-01 Job Run Audit Queries --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_ops")

    # Synthetic job run audit table (portable across workspace editions)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phase2_ops.job_run_audit (
          job_name STRING,
          run_id STRING,
          status STRING,
          started_at TIMESTAMP,
          finished_at TIMESTAMP,
          duration_sec INT
        ) USING DELTA
    """)

    cur.execute("DELETE FROM phase2_ops.job_run_audit")
    cur.execute("""
        INSERT INTO phase2_ops.job_run_audit VALUES
          ('bronze_to_silver', 'run_001', 'SUCCESS', current_timestamp() - INTERVAL 15 MINUTES, current_timestamp() - INTERVAL 10 MINUTES, 300),
          ('silver_to_gold',  'run_002', 'FAILED',  current_timestamp() - INTERVAL 9 MINUTES,  current_timestamp() - INTERVAL 7 MINUTES, 120),
          ('bronze_to_silver', 'run_003', 'SUCCESS', current_timestamp() - INTERVAL 6 MINUTES,  current_timestamp() - INTERVAL 2 MINUTES, 240)
    """)

    cur.execute("""
      SELECT status, COUNT(*) AS runs, AVG(duration_sec) AS avg_duration_sec
      FROM phase2_ops.job_run_audit
      GROUP BY status
      ORDER BY runs DESC
    """)
    rows = cur.fetchall()

conn.close()

print("  Job run summary by status:")
for r in rows:
    print(f"  - status={r[0]} runs={r[1]} avg_duration_sec={r[2]}")
print("\nDone. Pattern: maintain auditable run-history table for operational reporting.\n")
