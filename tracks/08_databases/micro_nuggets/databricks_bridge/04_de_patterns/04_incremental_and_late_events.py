"""
NUGGET 04-04 (Bridge) -- Incremental Loads and Late-Arriving Events
=====================================================================
Covers: watermark-based incremental load, idempotent batch control,
        late event detection, reprocessing strategy.

Key DE concepts:
  Incremental load  = only process new/changed records since last run
  Watermark         = a timestamp or version marker tracking progress
  Late-arriving     = events that arrive after their window has closed
  Idempotency       = running the pipeline twice produces the same result

PostgreSQL comparison:
  - Similar watermark pattern using a control table
  - PostgreSQL: WHERE updated_at > (SELECT last_run FROM control)
  - Delta adds version-based watermarks (DESCRIBE HISTORY version)

Usage:
    python 04_incremental_and_late_events.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

C = LAB_CATALOG
S = LAB_SCHEMA
DIVIDER = "-" * 64
results = []


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


print()
print("=" * 64)
print("  Nugget 04-04: Incremental Loads and Late-Arriving Events")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Create incremental control table ───────────────────────────────
    # The control table is the watermark ledger.
    # Each successful pipeline run updates last_processed_date.
    # On failure: the run is not recorded, so reprocessing is safe.
    print()
    print("  [1] Create incremental control table")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.incremental_control")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.incremental_control (
                source_table        STRING  NOT NULL  COMMENT 'Source table name',
                last_processed_date DATE              COMMENT 'Watermark: last fully-processed date',
                last_run_ts         TIMESTAMP         COMMENT 'When the last run completed',
                rows_processed      BIGINT            COMMENT 'Rows loaded in last run',
                status              STRING            COMMENT 'success / failed'
            )
            USING DELTA
            COMMENT 'Incremental load watermark control -- bridge lab'
        """)
        # Seed with initial watermark (before the data starts)
        cur.execute(f"""
            INSERT INTO {C}.{S}.incremental_control VALUES
            ('sales_orders', CAST('2024-02-28' AS DATE),
             CURRENT_TIMESTAMP(), 0, 'success')
        """)
        check("Control table created with initial watermark", True)
    except Exception as exc:
        check("Create control table", False, str(exc)[:60])
        conn.close()
        sys.exit(1)

    # ── 2. Simulate incremental load using watermark ──────────────────────
    # Read watermark -> query only new records -> load -> update watermark
    # This is the foundational pattern for all batch incremental pipelines.
    print()
    print("  [2] Incremental load: fetch orders after watermark")
    try:
        cur.execute(f"""
            SELECT last_processed_date
            FROM {C}.{S}.incremental_control
            WHERE source_table = 'sales_orders'
        """)
        watermark_row = cur.fetchone()
        watermark = str(watermark_row[0]) if watermark_row else "2024-01-01"
        check("Watermark read from control table", watermark_row is not None,
              f"watermark={watermark}")

        # Simulate incremental query: only records after watermark
        cur.execute(f"""
            SELECT
                order_date,
                COUNT(*)          AS orders,
                SUM(total_amount) AS revenue
            FROM {C}.{S}.sales_orders
            WHERE order_date > CAST('{watermark}' AS DATE)
              AND status != 'Cancelled'
            GROUP BY order_date
            ORDER BY order_date
        """)
        incremental_rows = cur.fetchall()
        check("Incremental query returned new rows",
              len(incremental_rows) > 0,
              f"{len(incremental_rows)} new order dates")
        for r in incremental_rows[:4]:
            print(f"         {r}")
    except Exception as exc:
        check("Incremental query", False, str(exc)[:60])
        incremental_rows = []

    # ── 3. Update watermark after successful load ─────────────────────────
    # Only update the watermark AFTER the load completes successfully.
    # If the load fails, the watermark stays at the old value -> safe retry.
    print()
    print("  [3] Update watermark to new high-water mark")
    if incremental_rows:
        new_watermark = str(incremental_rows[-1][0])  # last order_date processed
        try:
            cur.execute(f"""
                MERGE INTO {C}.{S}.incremental_control AS ctrl
                USING (
                    SELECT
                        'sales_orders' AS source_table,
                        CAST('{new_watermark}' AS DATE) AS new_wm,
                        {len(incremental_rows)} AS rows_processed
                ) AS upd
                ON ctrl.source_table = upd.source_table
                WHEN MATCHED THEN
                    UPDATE SET
                        ctrl.last_processed_date = upd.new_wm,
                        ctrl.last_run_ts         = CURRENT_TIMESTAMP(),
                        ctrl.rows_processed      = upd.rows_processed,
                        ctrl.status              = 'success'
            """)
            check("Watermark updated after load", True,
                  f"new watermark={new_watermark}")
        except Exception as exc:
            check("Watermark update", False, str(exc)[:60])
    else:
        check("Watermark update (no new rows to process)", True)

    # ── 4. Late-arriving events: detect and handle ────────────────────────
    # A late event arrives AFTER its event_date window has been processed.
    # Example: event from 2024-05-01 arrives on 2024-05-15.
    # Strategy A: reprocess the affected window (recompute aggregates)
    # Strategy B: accept and flag late events; correct downstream reports
    print()
    print("  [4] Late-arriving event detection")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.late_events_target")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.late_events_target
            USING DELTA
            COMMENT 'Demo target for late event handling'
            AS
            SELECT
                DATE(event_ts)    AS event_date,
                event_type,
                COUNT(*)          AS event_count,
                CURRENT_TIMESTAMP() AS computed_at
            FROM {C}.{S}.events_stream
            GROUP BY DATE(event_ts), event_type
        """)

        # Simulate a late event arriving 10 days after its event date
        # (event_ts = 2024-05-01 but _ingest_ts = 2024-05-11)
        late_events_query = f"""
            SELECT
                event_id,
                event_type,
                event_ts,
                _ingest_ts,
                DATEDIFF(_ingest_ts, event_ts) AS latency_days
            FROM {C}.{S}.events_stream
            WHERE DATEDIFF(_ingest_ts, event_ts) > 0
            ORDER BY latency_days DESC
            LIMIT 5
        """
        cur.execute(late_events_query)
        late_rows = cur.fetchall()
        check("Late event detection query ran", True,
              f"{len(late_rows)} late events detected")
        for r in late_rows[:3]:
            print(f"         event_id={r[0]}  latency={r[4]}d")

    except Exception as exc:
        check("Late event detection", False, str(exc)[:60])

    # ── 5. Idempotency check: rerun produces same result ──────────────────
    # Run the incremental query again -- should return 0 new rows (already processed)
    print()
    print("  [5] Idempotency: rerun returns 0 new rows (watermark prevents re-load)")
    try:
        cur.execute(f"""
            SELECT last_processed_date FROM {C}.{S}.incremental_control
            WHERE source_table = 'sales_orders'
        """)
        current_wm = str(cur.fetchone()[0])
        cur.execute(f"""
            SELECT COUNT(*) FROM {C}.{S}.sales_orders
            WHERE order_date > CAST('{current_wm}' AS DATE)
              AND status != 'Cancelled'
        """)
        rerun_count = cur.fetchone()[0]
        check("Rerun finds no new rows (idempotent)",
              rerun_count == 0,
              f"rows after watermark={rerun_count}")
    except Exception as exc:
        check("Idempotency check", False, str(exc)[:60])

    # ── 6. Cleanup ────────────────────────────────────────────────────────
    print()
    print("  [6] Cleanup")
    for tbl in ["incremental_control", "late_events_target"]:
        try:
            cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.{tbl}")
            print(f"  [OK]   Dropped {tbl}")
        except Exception as exc:
            print(f"  [WARN] Drop {tbl}: {str(exc)[:50]}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 04-04: {passed}/{total} checks passed")
print()
print("  Incremental load pattern:")
print("    1. Read watermark from control table")
print("    2. Query source WHERE event_date > watermark")
print("    3. Load results to target")
print("    4. Update watermark only on SUCCESS (never on failure)")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
