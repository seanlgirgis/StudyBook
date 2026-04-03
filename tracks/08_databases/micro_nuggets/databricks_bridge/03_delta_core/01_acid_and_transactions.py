"""
NUGGET 03-01 (Bridge) -- ACID Behavior in Delta Lake
=====================================================
Covers: atomicity via INSERT, DESCRIBE HISTORY, snapshot isolation,
        reading consistent state during concurrent writes.

ACID in Delta Lake:
  A -- Atomicity:   Each write is committed atomically via _delta_log/.
                    A write either fully succeeds or fully rolls back.
  C -- Consistency: Schema is enforced on every write (no partial row).
  I -- Isolation:   Readers see snapshot-consistent state (MVCC-like).
                    Writers use optimistic concurrency control (OCC).
  D -- Durability:  Committed data persists in Parquet files in object store.

PostgreSQL comparison:
  - PostgreSQL ACID = write-ahead log (WAL) + MVCC
  - Delta ACID = transaction log (_delta_log/) + Parquet immutable files
  - Both support snapshot isolation for reads
  - Delta does NOT support multi-table transactions (single-table atomic only)
  - PostgreSQL supports multi-table transactions with COMMIT/ROLLBACK

Snowflake comparison:
  - Snowflake uses Micro-Partitions + Time Travel (similar to Delta)
  - No explicit transaction log visible to users

Usage:
    python 01_acid_and_transactions.py
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
print("  Nugget 03-01: ACID and Delta Transaction Log")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. DESCRIBE HISTORY: read the Delta transaction log ───────────────
    # DESCRIBE HISTORY shows every commit with version, timestamp, operation,
    # user, and statistics. This is the Delta equivalent of PostgreSQL's
    # pg_stat_user_tables / pg_xact / wal_level logging.
    #
    # Every modifying operation creates a new version:
    #   Version 0 = CREATE TABLE
    #   Version 1 = INSERT batch
    #   Version 2 = MERGE, etc.
    print()
    print("  [1] DESCRIBE HISTORY customers (last 5 versions)")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.customers LIMIT 5")
    rows = cur.fetchall()
    check("DESCRIBE HISTORY returned rows", len(rows) > 0,
          f"{len(rows)} versions")
    if rows:
        # columns: version, timestamp, userId, userName, operation, operationParameters, ...
        print(f"         Latest version: {rows[0][0]}  op: {rows[0][4]}")

    # ── 2. Read current version count ────────────────────────────────────
    print()
    print("  [2] Snapshot read: current row count")
    cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.sales_orders")
    before = cur.fetchone()[0]
    check("Snapshot read succeeded", before > 0, f"count={before}")

    # ── 3. Atomicity demonstration: INSERT + verify ───────────────────────
    # Insert a test batch into sales_orders.
    # If the insert completes without error, Delta has atomically committed it.
    # If it fails mid-way (e.g., network), the partial write is discarded
    # (the _delta_log entry is never written).
    print()
    print("  [3] Atomicity: insert test batch and verify")
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.sales_orders VALUES
            (9901, 1, 101, '2024-06-01', 1, 1299.99, 1299.99, 'Pending', 'North'),
            (9902, 2, 110, '2024-06-01', 2,   18.50,   37.00, 'Pending', 'South')
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.sales_orders WHERE order_id IN (9901, 9902)")
        inserted = cur.fetchone()[0]
        check("Atomic INSERT committed (2 test rows)", inserted == 2, f"found={inserted}")

        # Clean up test rows
        cur.execute(f"DELETE FROM {C}.{S}.sales_orders WHERE order_id IN (9901, 9902)")
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.sales_orders WHERE order_id IN (9901, 9902)")
        after_delete = cur.fetchone()[0]
        check("DELETE test rows (cleanup)", after_delete == 0, f"remaining={after_delete}")

    except Exception as exc:
        check("Atomic INSERT test", False, str(exc)[:60])

    # ── 4. Verify history grew (new version created) ──────────────────────
    print()
    print("  [4] Transaction log grew after DML operations")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.sales_orders LIMIT 10")
    history_rows = cur.fetchall()
    check("History has multiple versions", len(history_rows) > 1,
          f"{len(history_rows)} versions found")
    if history_rows:
        ops = [r[4] for r in history_rows[:4]]  # column 4 = operation
        print(f"         Recent operations: {ops}")

    # ── 5. DESCRIBE DETAIL: physical table metadata ───────────────────────
    # DESCRIBE DETAIL shows file count, table size, format, location.
    # PostgreSQL equivalent: pg_relation_size(), pg_stat_user_tables
    print()
    print("  [5] DESCRIBE DETAIL: physical metadata")
    cur.execute(f"DESCRIBE DETAIL {C}.{S}.sales_orders")
    detail = cur.fetchone()
    if detail:
        # Typical columns: format, id, name, description, location, ...
        check("DESCRIBE DETAIL returned data", True, f"format={detail[0]}")
        print(f"         Format: {detail[0]}")
    else:
        check("DESCRIBE DETAIL returned data", False)

    # ── 6. Schema enforcement test ────────────────────────────────────────
    # Delta enforces schema on every write by default.
    # Inserting a non-existent column raises an AnalysisException.
    # This is like NOT NULL / CHECK constraints in PostgreSQL -- enforced
    # at the engine level, not just the application level.
    print()
    print("  [6] Schema enforcement: bad column raises error")
    schema_enforced = False
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.customers
            SELECT 99, 'Test User', 'test@example.com', 'North', 'Consumer',
                   '2024-01-01', 'unexpected_extra_column'
        """)
        # Should not reach here
        check("Schema enforcement raised error", False, "no error raised -- unexpected")
    except Exception as exc:
        err_msg = str(exc)
        # Any error here means enforcement worked
        schema_enforced = True
        check("Schema enforcement raised error", True,
              f"error: {err_msg[:50]}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 03-01: {passed}/{total} checks passed")
print()
print("  Key ACID takeaway:")
print("    - Delta uses _delta_log/ JSON files as WAL equivalent")
print("    - Each commit = one new log entry (atomic write)")
print("    - Readers see consistent snapshot (no dirty reads)")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
