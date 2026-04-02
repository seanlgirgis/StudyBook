"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · INSERT and INSERT INTO … SELECT                              ║
║  The two DML patterns a DE uses to load data into Snowflake tables.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates literal-value inserts (for seeding/testing) and the
transform-and-load INSERT INTO … SELECT pattern (the real DE workhorse),
using Snowflake's built-in data generators.

CONCEPTS
────────
INSERT INTO … VALUES
  - Inserts explicit literal rows.
  - Good for: unit test fixtures, seeding reference tables, quick demos.
  - Bad for: large volumes — each values list is one statement, one transaction.

INSERT INTO … SELECT
  - Reads from any query result and writes rows into the target.
  - This is the core pipeline pattern:
      INSERT INTO analytics.orders_daily
      SELECT date_trunc('day', order_ts), SUM(amount)
      FROM   raw.orders
      GROUP  BY 1;
  - Runs in a single transaction — atomic, all-or-nothing.
  - Snowflake parallelises this across the warehouse — scales with data volume.

Snowflake data generation functions (very useful for test data):
  TABLE(GENERATOR(ROWCOUNT => n))
    - A table-valued function that emits n empty rows.
    - Combine with other functions to synthesise realistic data.

  SEQ4()   — 32-bit sequential integer (restarts each query)
  SEQ8()   — 64-bit version (use when > 4 billion rows)
  RANDOM() — random 64-bit integer seed
  UNIFORM(a, b, RANDOM()) — uniformly random value in [a, b]
  NORMAL(mean, stddev, RANDOM()) — normally distributed float
  DATEADD('day', -UNIFORM(0, 90, RANDOM()), CURRENT_DATE())
            — random date in the past 90 days

  CASE UNIFORM(1, 3, RANDOM()) WHEN 1 THEN … END — random enum pick

Autocommit in snowflake-connector-python:
  - Default: autocommit=False (transactions are explicit).
  - Call conn.commit() after DML to make changes permanent.
  - Or use conn.cursor().execute("BEGIN") / "COMMIT" explicitly.
  - For these nuggets we set autocommit=True in the connection options
    so each execute() commits immediately (simpler for learning).
  - In production pipelines: manage transactions explicitly for atomicity.

TRUNCATE vs DELETE:
  - TRUNCATE TABLE t   — removes all rows, resets AUTOINCREMENT, minimal logging
                          much faster than DELETE for full-table wipe
  - DELETE FROM t       — DML, logged, can have WHERE, preserved in Time Travel
  For resetting between test runs: always TRUNCATE.

USAGE
─────
    python 01_insert_select.py

EXPECTED OUTPUT
───────────────
    ── INSERT & INSERT INTO … SELECT ────────────

      Table ready: NUGGET_ORDERS (0 rows after truncate)

      ── Step 1: INSERT VALUES (3 literal rows) ──────────
        Inserted: 3 rows

      ── Step 2: INSERT INTO … SELECT (20 generated rows) ─
        Inserted: 20 rows

      ── Result: 23 rows total ────────────────────────────
        Date range  : 2023-10-03 → 2024-01-02
        Total revenue: $5,421.87

      ── Orders by status ─────────────────────────────────
        STATUS       COUNT   REVENUE
        ------------ ------- -----------
        DELIVERED        8     2,103.44
        PENDING          7     1,899.21
        SHIPPED          8     1,419.22
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

# autocommit=True: each execute() is immediately committed.
# Fine for learning nuggets. In production pipelines, manage transactions.
conn = get_connection(autocommit=True)

print("\n── INSERT & INSERT INTO … SELECT ────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create the target table (idempotent) and reset it.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NUGGET_ORDERS (
            order_id     NUMBER,
            customer_id  NUMBER,
            product_id   NUMBER,
            quantity     NUMBER,
            unit_price   FLOAT,
            order_date   DATE,
            status       VARCHAR(20)
        )
        COMMENT = 'Demo orders table — nugget 03-01'
    """)
    cur.execute("TRUNCATE TABLE NUGGET_ORDERS")
    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS")
    print(f"\n  Table ready: NUGGET_ORDERS ({cur.fetchone()[0]} rows after truncate)")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. INSERT INTO … VALUES — literal rows
    #
    #    Use for seeding known reference data or test fixtures.
    #    Multi-row VALUES is a single round-trip to Snowflake.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 1: INSERT VALUES (3 literal rows) ──────────")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS
            (order_id, customer_id, product_id, quantity, unit_price, order_date, status)
        VALUES
            (1, 101, 10, 2,  29.99, '2024-01-15', 'SHIPPED'),
            (2, 102, 11, 1,  49.99, '2024-01-16', 'PENDING'),
            (3, 101, 12, 5,   9.99, '2024-01-17', 'DELIVERED')
    """)
    # cur.rowcount returns the number of rows affected by the last DML
    print(f"    Inserted: {cur.rowcount} rows")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. INSERT INTO … SELECT — the core pipeline pattern
    #
    #    TABLE(GENERATOR(ROWCOUNT => 20)) emits 20 empty rows.
    #    Each function (SEQ4, UNIFORM, RANDOM, DATEADD) runs per-row,
    #    producing a unique synthetic dataset.
    #
    #    This pattern scales: swap the generator for a real source table
    #    and the same SQL loads millions of rows in the same statement.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 2: INSERT INTO … SELECT (20 generated rows) ─")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS
        SELECT
            SEQ4() + 100                                          AS order_id,
            UNIFORM(100, 199, RANDOM())                           AS customer_id,
            UNIFORM(10,  20,  RANDOM())                           AS product_id,
            UNIFORM(1,   10,  RANDOM())                           AS quantity,
            ROUND(UNIFORM(5.0, 200.0, RANDOM()), 2)               AS unit_price,
            DATEADD('day', -UNIFORM(0, 90, RANDOM()), '2024-01-02'::DATE)
                                                                  AS order_date,
            CASE UNIFORM(1, 3, RANDOM())
                WHEN 1 THEN 'SHIPPED'
                WHEN 2 THEN 'PENDING'
                ELSE        'DELIVERED'
            END                                                   AS status
        FROM TABLE(GENERATOR(ROWCOUNT => 20))
    """)
    print(f"    Inserted: {cur.rowcount} rows")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Verify totals
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT
            COUNT(*)                               AS total_rows,
            MIN(order_date)                        AS earliest,
            MAX(order_date)                        AS latest,
            ROUND(SUM(quantity * unit_price), 2)   AS total_revenue
        FROM NUGGET_ORDERS
    """)
    total, earliest, latest, revenue = cur.fetchone()
    print(f"\n  ── Result: {total} rows total ────────────────────────────")
    print(f"    Date range   : {earliest} → {latest}")
    print(f"    Total revenue: ${revenue:,.2f}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Group by status — shows aggregate query on freshly inserted data
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        SELECT   status,
                 COUNT(*)                             AS cnt,
                 ROUND(SUM(quantity * unit_price), 2) AS revenue
        FROM     NUGGET_ORDERS
        GROUP BY status
        ORDER BY revenue DESC
    """)
    print(f"\n  ── Orders by status ─────────────────────────────────")
    print(f"    {'STATUS':<12} {'COUNT':>7}   {'REVENUE':>11}")
    print(f"    {'-'*12} {'-'*7}   {'-'*11}")
    for status, cnt, rev in cur.fetchall():
        print(f"    {status:<12} {cnt:>7}   {rev:>11,.2f}")

conn.close()
print()
