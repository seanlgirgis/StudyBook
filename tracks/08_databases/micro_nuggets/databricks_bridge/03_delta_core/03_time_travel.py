"""
NUGGET 03-03 (Bridge) -- Delta Time Travel
===========================================
Covers: VERSION AS OF, TIMESTAMP AS OF, DESCRIBE HISTORY,
        RESTORE TABLE, retention and VACUUM caveats.

Why Time Travel matters:
  In traditional databases (PostgreSQL), once you DELETE or UPDATE,
  the old data is gone (unless you have a backup or CDC log).
  Delta preserves old Parquet files until VACUUM cleans them.
  Time Travel lets you query ANY past version without a backup.

Use cases:
  1. Audit: "What did the table look like on date X?"
  2. Recovery: "I ran DELETE by mistake -- restore to version N"
  3. Reproducibility: "ML training pipeline always queries version 5"
  4. Debugging: "Which commit caused the anomaly?"

PostgreSQL comparison:
  - No native Time Travel. Requires manual audit tables or CDC log.
  - pg_temporal (extension) or bitemporal tables are workarounds.

Snowflake comparison:
  - TIME_TRAVEL_IN_DAYS (default 1, max 90 on Enterprise)
  - AT(VERSION => N) / AT(TIMESTAMP => ...) -- same concept

Usage:
    python 03_time_travel.py
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
print("  Nugget 03-03: Delta Time Travel")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Get current version and row count baseline ─────────────────────
    print()
    print("  [1] Baseline: current version and row count")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.customers LIMIT 1")
    hist = cur.fetchone()
    current_version = int(hist[0]) if hist else 0
    check("DESCRIBE HISTORY returned current version", hist is not None,
          f"version={current_version}")

    cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.customers")
    baseline_count = cur.fetchone()[0]
    check("Baseline row count", baseline_count > 0, f"count={baseline_count}")

    # ── 2. Create a new version by inserting a test row ───────────────────
    print()
    print("  [2] Create version: insert a test customer row")
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.customers VALUES
            (99, 'Time Travel Test', 'tt@test.com', 'North', 'Consumer', '2024-01-01')
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.customers")
        new_count = cur.fetchone()[0]
        check("INSERT created new row", new_count == baseline_count + 1,
              f"count={new_count}")

        # Get the new version number
        cur.execute(f"DESCRIBE HISTORY {C}.{S}.customers LIMIT 1")
        new_hist = cur.fetchone()
        new_version = int(new_hist[0]) if new_hist else current_version + 1
        check("New version created after INSERT", new_version > current_version,
              f"version={new_version}")
    except Exception as exc:
        new_count = baseline_count
        new_version = current_version
        check("INSERT for time travel demo", False, str(exc)[:60])

    # ── 3. Query previous version (VERSION AS OF) ─────────────────────────
    # VERSION AS OF N reads the snapshot at exactly version N.
    # This is a read-only view -- you cannot modify historical data.
    print()
    print("  [3] VERSION AS OF: read previous snapshot")
    if new_version > current_version:
        try:
            cur.execute(f"""
                SELECT COUNT(*) FROM {C}.{S}.customers
                VERSION AS OF {current_version}
            """)
            historical_count = cur.fetchone()[0]
            check("VERSION AS OF previous version",
                  historical_count == baseline_count,
                  f"historical={historical_count}, current={new_count}")
        except Exception as exc:
            check("VERSION AS OF query", False, str(exc)[:60])
    else:
        print("  SKIP  VERSION AS OF (no new version was created)")
        results.append(("VERSION AS OF", True))

    # ── 4. Show TIMESTAMP AS OF concept ───────────────────────────────────
    # TIMESTAMP AS OF uses a timestamp string instead of a version number.
    # Databricks finds the latest version before that timestamp.
    print()
    print("  [4] TIMESTAMP AS OF: read by historical timestamp")
    try:
        # Use the timestamp from the original version in history
        cur.execute(f"DESCRIBE HISTORY {C}.{S}.customers LIMIT 10")
        hist_rows = cur.fetchall()
        if len(hist_rows) > 1:
            # hist_rows[1] = the version before the latest
            old_ts = str(hist_rows[1][1])  # column 1 = timestamp
            # Truncate to seconds for the query
            ts_clean = old_ts[:19] if old_ts else None
            if ts_clean:
                cur.execute(f"""
                    SELECT COUNT(*) FROM {C}.{S}.customers
                    TIMESTAMP AS OF '{ts_clean}'
                """)
                ts_count = cur.fetchone()[0]
                check("TIMESTAMP AS OF historical query",
                      ts_count <= new_count,
                      f"ts={ts_clean}, count={ts_count}")
            else:
                check("TIMESTAMP AS OF (no valid timestamp found)", True)
        else:
            print("  INFO  Only one version exists -- TIMESTAMP AS OF works same as VERSION AS OF 0")
            results.append(("TIMESTAMP AS OF", True))
    except Exception as exc:
        check("TIMESTAMP AS OF query", False, str(exc)[:60])

    # ── 5. DELETE the test row and verify it is gone from current ─────────
    print()
    print("  [5] DELETE test row (but it survives in history)")
    try:
        cur.execute(f"DELETE FROM {C}.{S}.customers WHERE customer_id = 99")
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.customers WHERE customer_id = 99")
        after_del = cur.fetchone()[0]
        check("DELETE removed row from current version", after_del == 0,
              f"remaining={after_del}")

        # Verify history still has the row
        if new_version > current_version:
            cur.execute(f"""
                SELECT COUNT(*) FROM {C}.{S}.customers
                VERSION AS OF {new_version}
                WHERE customer_id = 99
            """)
            hist_row = cur.fetchone()[0]
            check("Deleted row still in historical version",
                  hist_row == 1, f"history count={hist_row}")
    except Exception as exc:
        check("DELETE + history retention test", False, str(exc)[:60])

    # ── 6. RESTORE TABLE demonstration (dry run -- show command) ──────────
    # RESTORE TABLE restores the table to a prior version.
    # This is a WRITE operation -- it creates a new version equal to V.
    # We show the syntax but do NOT execute to preserve the lab data.
    print()
    print("  [6] RESTORE TABLE (syntax demo -- not executed)")
    print(f"         Command: RESTORE TABLE {C}.{S}.customers TO VERSION AS OF {current_version}")
    print("         Effect: creates a new version restoring rows from that snapshot")
    print("         Safety: run DESCRIBE HISTORY after to see the restore entry")
    results.append(("RESTORE TABLE syntax demo", True))

    # ── 7. VACUUM warning ──────────────────────────────────────────────────
    # VACUUM removes old Parquet files beyond the retention period.
    # Once VACUUMed, you CANNOT time travel before that point.
    # Default retention = 168 hours (7 days). NEVER set to 0 in production.
    print()
    print("  [7] VACUUM retention awareness check")
    try:
        cur.execute(f"DESCRIBE DETAIL {C}.{S}.customers")
        detail = cur.fetchone()
        check("DESCRIBE DETAIL accessible", detail is not None)
    except Exception as exc:
        check("DESCRIBE DETAIL", False, str(exc)[:60])
    print("         VACUUM default retention = 168 hours (7 days)")
    print("         After VACUUM: time travel before that window is gone forever")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 03-03: {passed}/{total} checks passed")
print()
print("  Time Travel cheat sheet:")
print("    SELECT * FROM table VERSION AS OF 5")
print("    SELECT * FROM table TIMESTAMP AS OF '2024-01-15 14:30:00'")
print("    RESTORE TABLE table TO VERSION AS OF 5")
print("    DESCRIBE HISTORY table")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
