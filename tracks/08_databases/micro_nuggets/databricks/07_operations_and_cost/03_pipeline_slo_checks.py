from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import LAB_CATALOG, get_connection

print("\n-- Phase 2 · 07-03 Pipeline SLO Checks --")

conn = get_connection()
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {LAB_CATALOG}")
    cur.execute("CREATE SCHEMA IF NOT EXISTS phase2_ops")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phase2_ops.pipeline_slo (
          pipeline_name STRING,
          run_ts TIMESTAMP,
          freshness_min INT,
          rows_written INT,
          error_count INT
        ) USING DELTA
    """)

    cur.execute("DELETE FROM phase2_ops.pipeline_slo")
    cur.execute("""
        INSERT INTO phase2_ops.pipeline_slo VALUES
          ('orders_bronze_to_silver', current_timestamp() - INTERVAL 12 MINUTES, 12, 12500, 0),
          ('orders_bronze_to_silver', current_timestamp() - INTERVAL 5 MINUTES,  5, 13200, 0),
          ('orders_silver_to_gold',   current_timestamp() - INTERVAL 22 MINUTES, 22, 3900,  1)
    """)

    cur.execute("""
      SELECT
        pipeline_name,
        MAX(freshness_min) AS max_freshness_min,
        AVG(rows_written)  AS avg_rows_written,
        SUM(error_count)   AS total_errors
      FROM phase2_ops.pipeline_slo
      GROUP BY pipeline_name
      ORDER BY pipeline_name
    """)
    rows = cur.fetchall()

conn.close()

print("  SLO summary:")
for r in rows:
    freshness_breach = int(r[1]) > 15
    error_breach = int(r[3]) > 0
    state = "BREACH" if (freshness_breach or error_breach) else "OK"
    print(
        f"  - {r[0]} | max_freshness_min={r[1]} | avg_rows_written={r[2]} | total_errors={r[3]} | {state}"
    )

print("\nDone. Pattern: compute SLO health directly from pipeline telemetry tables.\n")
