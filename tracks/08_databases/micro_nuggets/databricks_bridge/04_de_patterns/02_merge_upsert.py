"""
NUGGET 04-02 (Bridge) -- MERGE / Upsert
=========================================
Covers: MERGE INTO ... USING ... ON, WHEN MATCHED UPDATE,
        WHEN NOT MATCHED INSERT, CDC merge, conditional updates.

MERGE is the cornerstone upsert operation in Delta Lake.
One atomic statement handles INSERT + UPDATE + DELETE.

PostgreSQL comparison:
  - PostgreSQL 15+ has MERGE (SQL standard)
  - Earlier PG: INSERT ... ON CONFLICT DO UPDATE (UPSERT)
  - Delta MERGE is more expressive (multiple WHEN clauses)

Snowflake comparison:
  - Identical MERGE syntax

Usage:
    python 02_merge_upsert.py
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
print("  Nugget 04-02: MERGE / Upsert")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Setup: create target table ────────────────────────────────────
    print()
    print("  [1] Setup: create orders_staging for MERGE demo")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.orders_staging")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.orders_staging
            USING DELTA
            COMMENT 'MERGE target table -- bridge lab'
            AS SELECT * FROM {C}.{S}.sales_orders
            WHERE order_id <= 1010
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.orders_staging")
        staging_count = cur.fetchone()[0]
        check("Staging target created", staging_count == 10,
              f"rows={staging_count}")
    except Exception as exc:
        check("Staging table creation", False, str(exc)[:60])
        conn.close()
        sys.exit(1)

    # ── 2. Basic MERGE: upsert from source ───────────────────────────────
    # Source has:
    #   - Updated rows (existing order_ids with changed total_amount)
    #   - New rows (order_ids not in target)
    # MERGE handles both atomically.
    print()
    print("  [2] Basic MERGE: update existing + insert new orders")
    try:
        cur.execute(f"""
            MERGE INTO {C}.{S}.orders_staging AS target
            USING (
                SELECT order_id, customer_id, product_id, order_date,
                       quantity, unit_price, total_amount, status, region
                FROM {C}.{S}.sales_orders
                WHERE order_id BETWEEN 1008 AND 1015
            ) AS source
            ON target.order_id = source.order_id
            WHEN MATCHED AND target.status != source.status THEN
                UPDATE SET
                    target.status       = source.status,
                    target.total_amount = source.total_amount
            WHEN NOT MATCHED THEN
                INSERT (order_id, customer_id, product_id, order_date,
                        quantity, unit_price, total_amount, status, region)
                VALUES (source.order_id, source.customer_id, source.product_id,
                        source.order_date, source.quantity, source.unit_price,
                        source.total_amount, source.status, source.region)
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.orders_staging")
        after_merge = cur.fetchone()[0]
        check("MERGE upsert expanded table",
              after_merge > 10,
              f"rows after merge={after_merge}")
    except Exception as exc:
        check("MERGE upsert", False, str(exc)[:60])

    # ── 3. MERGE with DELETE clause ───────────────────────────────────────
    # WHEN MATCHED AND <condition> THEN DELETE handles CDC delete events.
    # PostgreSQL INSERT ... ON CONFLICT cannot delete -- requires a separate
    # DELETE statement. Delta MERGE handles all three operations atomically.
    print()
    print("  [3] MERGE with DELETE: remove cancelled orders from staging")
    try:
        cur.execute(f"""
            MERGE INTO {C}.{S}.orders_staging AS target
            USING (
                SELECT order_id FROM {C}.{S}.sales_orders
                WHERE status = 'Cancelled'
            ) AS to_delete
            ON target.order_id = to_delete.order_id
            WHEN MATCHED THEN DELETE
        """)
        cur.execute(f"""
            SELECT COUNT(*) FROM {C}.{S}.orders_staging
            WHERE status = 'Cancelled'
        """)
        cancelled_remaining = cur.fetchone()[0]
        check("MERGE DELETE removed cancelled orders",
              cancelled_remaining == 0,
              f"remaining cancelled={cancelled_remaining}")
    except Exception as exc:
        check("MERGE with DELETE", False, str(exc)[:60])

    # ── 4. CDC MERGE pattern (Insert/Update/Delete from CDC feed) ─────────
    # In Change Data Capture pipelines, each CDC record has an _op column:
    #   'I' = Insert, 'U' = Update, 'D' = Delete
    # MERGE handles all three cases in one statement.
    print()
    print("  [4] CDC MERGE: apply I/U/D operations from change feed")
    try:
        # Build a CDC-like source inline
        cur.execute(f"""
            MERGE INTO {C}.{S}.orders_staging AS target
            USING (
                SELECT
                    9001 AS order_id, 1 AS customer_id, 101 AS product_id,
                    CAST('2024-08-01' AS DATE) AS order_date, 1 AS quantity,
                    999.00 AS unit_price, 999.00 AS total_amount,
                    'Pending' AS status, 'North' AS region, 'I' AS _op
                UNION ALL
                SELECT
                    1001, 1, 101, CAST('2024-01-05' AS DATE), 1,
                    1299.99, 1299.99, 'Returned', 'North', 'U'
            ) AS cdc
            ON target.order_id = cdc.order_id
            WHEN MATCHED AND cdc._op = 'D' THEN DELETE
            WHEN MATCHED AND cdc._op = 'U' THEN
                UPDATE SET
                    target.status = cdc.status,
                    target.total_amount = cdc.total_amount
            WHEN NOT MATCHED AND cdc._op = 'I' THEN
                INSERT (order_id, customer_id, product_id, order_date,
                        quantity, unit_price, total_amount, status, region)
                VALUES (cdc.order_id, cdc.customer_id, cdc.product_id,
                        cdc.order_date, cdc.quantity, cdc.unit_price,
                        cdc.total_amount, cdc.status, cdc.region)
        """)
        # Verify the new row was inserted
        cur.execute(f"SELECT order_id, status FROM {C}.{S}.orders_staging WHERE order_id = 9001")
        inserted = cur.fetchone()
        check("CDC INSERT applied", inserted is not None,
              f"order_id=9001 status={inserted[1] if inserted else 'missing'}")

        # Verify the update was applied (1001 -> Returned)
        cur.execute(f"SELECT status FROM {C}.{S}.orders_staging WHERE order_id = 1001")
        updated = cur.fetchone()
        check("CDC UPDATE applied",
              updated is not None and updated[0] == "Returned",
              f"status={updated[0] if updated else 'missing'}")
    except Exception as exc:
        check("CDC MERGE (I/U/D)", False, str(exc)[:60])

    # ── 5. Verify MERGE history ───────────────────────────────────────────
    print()
    print("  [5] MERGE operations in DESCRIBE HISTORY")
    cur.execute(f"DESCRIBE HISTORY {C}.{S}.orders_staging LIMIT 5")
    hist = cur.fetchall()
    ops = [r[4] for r in hist] if hist else []
    merge_ops = [op for op in ops if op and "MERGE" in str(op).upper()]
    check("MERGE visible in DESCRIBE HISTORY", len(merge_ops) > 0,
          f"merge ops found: {len(merge_ops)}")

    # ── 6. Cleanup ────────────────────────────────────────────────────────
    print()
    print("  [6] Cleanup")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.orders_staging")
        print("  [OK]   Dropped orders_staging")
    except Exception as exc:
        print(f"  [WARN] Cleanup: {str(exc)[:50]}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 04-02: {passed}/{total} checks passed")
print()
print("  MERGE cheat sheet:")
print("    MERGE INTO target USING source ON target.id = source.id")
print("    WHEN MATCHED THEN UPDATE SET ...")
print("    WHEN NOT MATCHED THEN INSERT ...")
print("    WHEN MATCHED AND _op='D' THEN DELETE")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
