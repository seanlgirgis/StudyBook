"""
NUGGET 04-03 (Bridge) -- Slowly Changing Dimension Type 2
===========================================================
Covers: SCD Type 2 table design, MERGE-based SCD2 update logic,
        effective_from / effective_to / is_current pattern.

SCD Type 2 keeps full history of dimension changes:
  - When a customer changes region, a new row is added
  - Old row gets effective_to = change date, is_current = false
  - New row gets effective_from = change date, is_current = true

PostgreSQL comparison:
  - Same MERGE logic (PG 15+) or manual UPDATE + INSERT (PG < 15)
  - PostgreSQL: BEGIN; UPDATE old_row; INSERT new_row; COMMIT;
  - Delta: MERGE handles it atomically in one statement

Snowflake comparison:
  - Identical MERGE-based SCD2 pattern

Usage:
    python 03_scd_type2.py
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
print("  Nugget 04-03: SCD Type 2")
print("=" * 64)

conn = get_connection()
with conn.cursor() as cur:

    # ── 1. Create SCD2 dimension table ────────────────────────────────────
    # surrogate_key: system-generated unique row ID (each history version)
    # natural_key (customer_id): business identifier
    # effective_from / effective_to: validity period
    # is_current: fast filter for current records
    print()
    print("  [1] Create customers_scd2 dimension table")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.customers_scd2")
        cur.execute(f"""
            CREATE TABLE {C}.{S}.customers_scd2 (
                surrogate_key   BIGINT      COMMENT 'Auto-incremented system key per version',
                customer_id     INT         COMMENT 'Business natural key',
                customer_name   STRING,
                email           STRING,
                region          STRING      COMMENT 'Tracked attribute -- drives SCD2',
                segment         STRING      COMMENT 'Tracked attribute -- drives SCD2',
                effective_from  DATE        COMMENT 'Row valid from this date',
                effective_to    DATE        COMMENT 'Row valid until this date (NULL = current)',
                is_current      BOOLEAN     COMMENT 'True for the active version'
            )
            USING DELTA
            COMMENT 'Customers SCD Type 2 -- bridge lab'
        """)
        check("customers_scd2 created", True)
    except Exception as exc:
        check("Create customers_scd2", False, str(exc)[:60])
        conn.close()
        sys.exit(1)

    # ── 2. Initial load: seed current state ───────────────────────────────
    print()
    print("  [2] Initial load: all customers as current rows")
    try:
        cur.execute(f"""
            INSERT INTO {C}.{S}.customers_scd2
            SELECT
                CAST(customer_id AS BIGINT)  AS surrogate_key,
                customer_id,
                customer_name,
                email,
                region,
                segment,
                created_at                   AS effective_from,
                CAST(NULL AS DATE)           AS effective_to,
                TRUE                         AS is_current
            FROM {C}.{S}.customers
        """)
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.customers_scd2 WHERE is_current = TRUE")
        loaded = cur.fetchone()[0]
        check("Initial SCD2 load", loaded == 20, f"current rows={loaded}")
    except Exception as exc:
        check("Initial SCD2 load", False, str(exc)[:60])

    # ── 3. SCD2 MERGE: process incoming changes ───────────────────────────
    # Change batch: customer 1 moves to 'South', customer 3 changes segment
    # SCD2 MERGE does TWO things:
    #   a) Expire old rows (UPDATE is_current=FALSE, set effective_to)
    #   b) Insert new rows (new version with is_current=TRUE)
    # This requires TWO MERGE passes in standard SQL (or a staged approach).
    # Here we use a two-step approach: expire first, then insert.
    print()
    print("  [3] SCD2 MERGE: expire old row and insert new version")
    change_date = "2024-10-01"
    try:
        # Step A: expire rows that are changing
        cur.execute(f"""
            MERGE INTO {C}.{S}.customers_scd2 AS target
            USING (
                SELECT 1 AS customer_id, 'South'     AS new_region, 'Corporate' AS new_segment
                UNION ALL
                SELECT 3, 'East', 'Corporate'
            ) AS changes
            ON target.customer_id = changes.customer_id
               AND target.is_current = TRUE
               AND (target.region != changes.new_region
                    OR target.segment != changes.new_segment)
            WHEN MATCHED THEN
                UPDATE SET
                    target.is_current   = FALSE,
                    target.effective_to = CAST('{change_date}' AS DATE)
        """)

        # Step B: insert new current versions for changed customers
        cur.execute(f"""
            INSERT INTO {C}.{S}.customers_scd2
            SELECT
                CAST(customer_id + 1000 AS BIGINT) AS surrogate_key,
                customer_id,
                customer_name,
                email,
                CASE customer_id WHEN 1 THEN 'South' ELSE region END AS region,
                CASE customer_id WHEN 3 THEN 'Corporate' ELSE segment END AS segment,
                CAST('{change_date}' AS DATE) AS effective_from,
                CAST(NULL AS DATE)            AS effective_to,
                TRUE                          AS is_current
            FROM {C}.{S}.customers
            WHERE customer_id IN (1, 3)
        """)

        # Verify: customer 1 should have 2 rows (old expired + new current)
        cur.execute(f"""
            SELECT customer_id, region, segment, effective_from, effective_to, is_current
            FROM {C}.{S}.customers_scd2
            WHERE customer_id = 1
            ORDER BY effective_from
        """)
        cust1_rows = cur.fetchall()
        check("Customer 1 has 2 SCD2 versions",
              len(cust1_rows) == 2,
              f"versions={len(cust1_rows)}")
        for r in cust1_rows:
            print(f"         {r}")

        # Verify: exactly 20 current rows remain
        cur.execute(f"SELECT COUNT(*) FROM {C}.{S}.customers_scd2 WHERE is_current = TRUE")
        current_count = cur.fetchone()[0]
        check("Still 20 current rows after SCD2 update",
              current_count == 20,
              f"current={current_count}")

    except Exception as exc:
        check("SCD2 MERGE update", False, str(exc)[:60])

    # ── 4. Query: point-in-time customer view ─────────────────────────────
    # A point-in-time query returns the record valid on a specific date.
    # Useful for: "What was the customer's region when this order was placed?"
    print()
    print("  [4] Point-in-time query: customer state as of 2024-09-15")
    cur.execute(f"""
        SELECT
            customer_id,
            customer_name,
            region,
            segment,
            effective_from,
            effective_to
        FROM {C}.{S}.customers_scd2
        WHERE CAST('2024-09-15' AS DATE) BETWEEN effective_from
              AND COALESCE(effective_to, CAST('9999-12-31' AS DATE))
        ORDER BY customer_id
        LIMIT 5
    """)
    pit_rows = cur.fetchall()
    check("Point-in-time query returned rows",
          len(pit_rows) > 0, f"{len(pit_rows)} rows")
    for r in pit_rows:
        print(f"         {r}")

    # ── 5. Cleanup ────────────────────────────────────────────────────────
    print()
    print("  [5] Cleanup")
    try:
        cur.execute(f"DROP TABLE IF EXISTS {C}.{S}.customers_scd2")
        print("  [OK]   Dropped customers_scd2")
    except Exception as exc:
        print(f"  [WARN] Cleanup: {str(exc)[:50]}")

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 04-03: {passed}/{total} checks passed")
print()
print("  SCD2 pattern:")
print("    MERGE step 1: expire old row (is_current=FALSE, set effective_to)")
print("    MERGE step 2: insert new row (is_current=TRUE, effective_from=today)")
print("    Point-in-time: WHERE date BETWEEN effective_from AND COALESCE(effective_to, '9999-12-31')")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
