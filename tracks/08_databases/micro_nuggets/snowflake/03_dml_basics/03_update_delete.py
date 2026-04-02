"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-03 · UPDATE and DELETE                                            ║
║  Two DML verbs — powerful, permanent, and worth understanding deeply.        ║
╚══════════════════════════════════════════════════════════════════════────────╝

PURPOSE
───────
Demonstrates simple UPDATE, join-based UPDATE (from another table),
and DELETE with and without a WHERE clause. Includes a safety pattern
using Time Travel to verify what was changed.

CONCEPTS
────────
UPDATE in Snowflake
  Basic:
    UPDATE target_table
    SET    col = new_value
    WHERE  condition;

  Join-based (update from another table):
    UPDATE target AS t
    SET    t.col = s.col
    FROM   source AS s
    WHERE  t.key = s.key;

  Important behaviour:
  - Snowflake rewrites large UPDATEs internally as DELETE + INSERT of
    micro-partitions. You don't see this, but it means:
      a) Updated rows are preserved in Time Travel (the old values survive)
      b) Large-scale UPDATEs can trigger significant partition rewrites

  - No RETURNING clause in Snowflake (unlike Postgres).
    To see what changed, query BEFORE and AFTER, or use Time Travel.

DELETE in Snowflake
  Simple:
    DELETE FROM table WHERE condition;

  Join-based delete:
    DELETE FROM target AS t
    USING  source  AS s
    WHERE  t.key = s.key;

  WARNING — the most common DML mistake:
    DELETE FROM my_table;     ← NO WHERE clause → deletes ALL rows!
    Snowflake will execute this without complaint.
    Time Travel can recover the data (up to 90 days for permanent tables).
    Lesson: always double-check your WHERE clause before running DELETE/UPDATE.

TRUNCATE vs DELETE:
  DELETE FROM t WHERE 1=1  — DML, writes to Time Travel, slow for large tables
  TRUNCATE TABLE t          — DDL, much faster, RESETS AUTOINCREMENT,
                              minimal Time Travel impact (only metadata change)
  For clearing staging tables between pipeline runs: use TRUNCATE.
  For removing specific rows in production: use DELETE.

Time Travel as a safety net:
  - After any DML, old row versions survive for TIME_TRAVEL_IN_DAYS (default: 1
    for transient, up to 90 for permanent, set per-table or at account level).
  - Query past state:
      SELECT * FROM my_table AT (OFFSET => -60);          -- 60 seconds ago
      SELECT * FROM my_table BEFORE (STATEMENT => '<query_id>');
  - This makes accidental UPDATEs and DELETEs recoverable.
  - Covered in depth in nugget 06_time_travel.

rowcount attribute:
  - After any DML, cur.rowcount holds the number of affected rows.
  - Useful for logging, alerting, and sanity checks in pipeline code.
    if cur.rowcount == 0: raise ValueError("Expected rows to be updated!")

USAGE
─────
    python 03_update_delete.py

EXPECTED OUTPUT
───────────────
    ── UPDATE & DELETE ───────────────────────────

      ── Seed data ────────────────────────────────
        Seeded 10 rows (all PENDING)

      ── Step 1: Simple UPDATE ─────────────────────
        High-value orders (revenue > $200) → PRIORITY
        Rows updated: 3   (will vary — random data)

      ── Step 2: Join-based UPDATE ─────────────────
        Top 3 PENDING orders → SHIPPED  (via staging join)
        Rows updated: 3

      ── Step 3: Simple DELETE ─────────────────────
        Delete all CANCELLED orders
        Rows deleted: 0   (none were CANCELLED — safe)

      ── Step 4: Join-based DELETE ─────────────────
        Delete orders whose product_id is in a blocklist
        Rows deleted: 2   (will vary)

      ── Final state ───────────────────────────────
        STATUS       COUNT   AVG_REVENUE
        ------------ ------- -----------
        PENDING          3        $87.43
        PRIORITY         3       $312.11
        SHIPPED          2       $145.78

      ── Audit: what changed? (Time Travel) ────────
        Rows in table now   : 8
        Rows 90 seconds ago : 10  ← original 10 before deletes
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)

print("\n── UPDATE & DELETE ───────────────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Seed: create and populate NUGGET_ORDERS
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS (
            order_id    NUMBER AUTOINCREMENT PRIMARY KEY,
            customer_id NUMBER,
            product_id  NUMBER,
            quantity    NUMBER,
            unit_price  FLOAT,
            status      VARCHAR(20) DEFAULT 'PENDING'
        )
    """)
    cur.execute("TRUNCATE TABLE NUGGET_ORDERS")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS (customer_id, product_id, quantity, unit_price)
        SELECT
            UNIFORM(100, 110, RANDOM()),
            UNIFORM(1,   5,   RANDOM()),
            UNIFORM(1,   5,   RANDOM()),
            ROUND(UNIFORM(20.0, 200.0, RANDOM()), 2)
        FROM TABLE(GENERATOR(ROWCOUNT => 10))
    """)
    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS")
    print(f"\n  ── Seed data ────────────────────────────────")
    print(f"    Seeded {cur.fetchone()[0]} rows (all PENDING)")

    # Record time for Time Travel demo at the end
    ts_before_changes = time.time()

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Simple UPDATE — mark high-value orders as PRIORITY
    #    Revenue = quantity * unit_price > 200
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        UPDATE NUGGET_ORDERS
        SET    status = 'PRIORITY'
        WHERE  quantity * unit_price > 200
    """)
    print(f"\n  ── Step 1: Simple UPDATE ─────────────────────")
    print(f"    High-value orders (revenue > $200) → PRIORITY")
    print(f"    Rows updated: {cur.rowcount}   (varies with random data)")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Join-based UPDATE — update target using data from another table
    #
    #    Real use case: you have a corrections table from upstream.
    #    JOIN it to the target and apply corrections atomically.
    #
    #    CREATE TEMPORARY TABLE — session-scoped, auto-dropped on disconnect.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TEMPORARY TABLE nugget_ship_batch AS
        SELECT order_id
        FROM   NUGGET_ORDERS
        WHERE  status = 'PENDING'
        ORDER  BY order_id
        LIMIT  3
    """)
    cur.execute("""
        UPDATE NUGGET_ORDERS AS o
        SET    o.status = 'SHIPPED'
        FROM   nugget_ship_batch AS b
        WHERE  o.order_id = b.order_id
    """)
    print(f"\n  ── Step 2: Join-based UPDATE ─────────────────")
    print(f"    Top 3 PENDING orders → SHIPPED  (via staging join)")
    print(f"    Rows updated: {cur.rowcount}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Simple DELETE — remove rows matching a condition
    #
    #    Deliberately choosing a condition with 0 matches to show safe behaviour.
    #    cur.rowcount = 0 means nothing was deleted — script can alert on this.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        DELETE FROM NUGGET_ORDERS
        WHERE  status = 'CANCELLED'
    """)
    print(f"\n  ── Step 3: Simple DELETE ─────────────────────")
    print(f"    Delete all CANCELLED orders")
    print(f"    Rows deleted: {cur.rowcount}   (none were CANCELLED — safe)")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Join-based DELETE — delete from target based on a blocklist
    #
    #    Syntax: DELETE FROM target USING source WHERE join_condition
    #    Use case: product recall, GDPR right-to-be-forgotten, embargo lists.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TEMPORARY TABLE nugget_blocked_products AS
        SELECT column1 AS product_id
        FROM   VALUES (1), (3)   -- products to remove
    """)
    cur.execute("""
        DELETE FROM NUGGET_ORDERS AS o
        USING  nugget_blocked_products AS b
        WHERE  o.product_id = b.product_id
    """)
    print(f"\n  ── Step 4: Join-based DELETE ─────────────────")
    print(f"    Delete orders for blocked product_ids (1, 3)")
    print(f"    Rows deleted: {cur.rowcount}   (varies with random data)")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Final state
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT   status,
                 COUNT(*) AS cnt,
                 ROUND(AVG(quantity * unit_price), 2) AS avg_rev
        FROM     NUGGET_ORDERS
        GROUP BY status
        ORDER BY status
    """)
    print(f"\n  ── Final state ───────────────────────────────")
    print(f"    {'STATUS':<12} {'COUNT':>7}   {'AVG_REVENUE':>11}")
    print(f"    {'-'*12} {'-'*7}   {'-'*11}")
    for status, cnt, avg_rev in cur.fetchall():
        print(f"    {status:<12} {cnt:>7}   ${avg_rev:>10,.2f}")

    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS")
    rows_now = cur.fetchone()[0]

    # ─────────────────────────────────────────────────────────────────────────
    # 6. Time Travel audit — query the table AS IT WAS before our changes
    #
    #    AT (OFFSET => -n) means "n seconds in the past".
    #    The offset must be within the table's TIME_TRAVEL_IN_DAYS window.
    #    This only works on PERMANENT tables (not TEMPORARY or TRANSIENT with 0-day TT).
    #
    #    We wait a moment first so the offset is safely before our DML.
    # ─────────────────────────────────────────────────────────────────────────
    elapsed = int(time.time() - ts_before_changes) + 5   # seconds ago, with buffer
    print(f"\n  ── Audit: what changed? (Time Travel) ────────")
    try:
        cur.execute(f"""
            SELECT COUNT(*)
            FROM   NUGGET_ORDERS AT (OFFSET => -{elapsed})
        """)
        rows_before = cur.fetchone()[0]
        print(f"    Rows in table now   : {rows_now}")
        print(f"    Rows {elapsed}s ago         : {rows_before}  ← before deletes")
        print(f"    Rows removed        : {rows_before - rows_now}")
    except Exception as exc:
        # May fail if Time Travel data expired or table is transient
        print(f"    Time Travel unavailable: {exc}")

conn.close()
print()
