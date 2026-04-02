"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-02 · MERGE (Upsert)                                               ║
║  The most important single SQL statement in a Data Engineer's toolkit.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates MERGE for upsert (UPDATE existing + INSERT new) and shows
why it is the foundation of idempotent, rerunnable pipelines.

CONCEPTS
────────
What is MERGE?
  MERGE combines INSERT + UPDATE (+ optionally DELETE) into one atomic statement.
  It answers the question: "I have incoming data — apply it to my target table,
  updating rows that already exist and inserting rows that are brand new."

  Syntax skeleton:
    MERGE INTO  target   t
    USING       source   s
    ON          t.key = s.key

    WHEN MATCHED THEN
        UPDATE SET t.col = s.col, …

    WHEN NOT MATCHED THEN
        INSERT (col1, col2, …)
        VALUES (s.col1, s.col2, …)

    WHEN MATCHED AND t.status = 'CANCELLED' THEN
        DELETE   ← optional: remove target rows under a condition

Why MERGE matters for DEs:
  1. Idempotent pipelines
     Running the same MERGE twice produces the same result.
     This is the foundation of reliable, rerunnable ETL.

  2. CDC (Change Data Capture) landing
     Source system emits a stream of changes (inserts, updates, deletes).
     MERGE applies the stream to the target table cleanly.

  3. SCD Type 1 (Slowly Changing Dimension — overwrite)
     Customer changes their email → MERGE updates the record in place.

  4. Deduplication on load
     Source has duplicates → MERGE on natural key deduplicates automatically.

USING clause (source):
  - Can be any query result, not just a table.
  - Common patterns:
      USING (SELECT * FROM staging_table WHERE loaded_at = today)
      USING (SELECT * FROM VALUES (…) AS t(col1, col2))
      USING (SELECT …FROM stream)   ← covered in nugget 07

Multiple WHEN clauses:
  - You can have multiple WHEN MATCHED conditions with different actions.
  - Snowflake evaluates them top to bottom — first match wins.
  - Example:
      WHEN MATCHED AND s.op = 'DELETE' THEN DELETE
      WHEN MATCHED                     THEN UPDATE SET …
      WHEN NOT MATCHED                 THEN INSERT …

MERGE return value:
  - Returns rows_inserted, rows_updated, rows_deleted counts.
  - In Python connector: cur.fetchone() after the MERGE returns these.
  - Useful for monitoring and alerting in production pipelines.

TEMPORARY TABLE:
  - EXISTS only for the current session — auto-dropped when session closes.
  - No storage cost after the session ends.
  - Perfect for staging incoming data within a pipeline run.
  - Syntax: CREATE TEMPORARY TABLE (or CREATE TEMP TABLE)

USAGE
─────
    python 02_merge.py

EXPECTED OUTPUT
───────────────
    ── MERGE (Upsert) ───────────────────────────

      ── Initial state ──────────────────────────
        ID   CUST  STATUS       UPDATED_AT
        ---- ----- ------------ -------------------
           1  101   PENDING      (original insert time)
           2  102   PENDING      (original insert time)
           3  103   PENDING      (original insert time)

      ── Incoming CDC batch ─────────────────────
        order_id=2 → SHIPPED     (existing → UPDATE)
        order_id=3 → DELIVERED   (existing → UPDATE)
        order_id=4 → PENDING     (new      → INSERT)

      ── MERGE result ────────────────────────────
        rows_inserted = 1
        rows_updated  = 2
        rows_deleted  = 0

      ── Final state ─────────────────────────────
        ID   CUST  STATUS       UPDATED_AT
        ---- ----- ------------ -------------------
           1  101   PENDING      (unchanged)
           2  102   SHIPPED      (updated!)
           3  103   DELIVERED    (updated!)
           4  104   PENDING      (inserted!)

      Key insight: order 1 was untouched — only rows in the source were affected.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)

print("\n── MERGE (Upsert) ───────────────────────────")


def print_orders(label: str, cur) -> None:
    cur.execute("""
        SELECT order_id, customer_id, status, updated_at
        FROM   NUGGET_ORDERS
        ORDER  BY order_id
    """)
    rows = cur.fetchall()
    print(f"\n  ── {label} ──────────────────────────")
    print(f"    {'ID':>4}  {'CUST':>5}  {'STATUS':<12}  UPDATED_AT")
    print(f"    {'─'*4}  {'─'*5}  {'─'*12}  {'─'*19}")
    for oid, cid, status, upd in rows:
        upd_str = str(upd)[:19] if upd else "NULL"
        print(f"    {oid:>4}  {cid:>5}  {status:<12}  {upd_str}")


with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create and seed the target table — our "clean" orders table.
    #    In a real pipeline this would be the authoritative table in your DW.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS (
            order_id    NUMBER       NOT NULL,
            customer_id NUMBER,
            status      VARCHAR(20),
            updated_at  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        COMMENT = 'Demo orders — nugget 03-02'
    """)
    cur.execute("TRUNCATE TABLE NUGGET_ORDERS")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS (order_id, customer_id, status)
        VALUES (1, 101, 'PENDING'),
               (2, 102, 'PENDING'),
               (3, 103, 'PENDING')
    """)
    print_orders("Initial state", cur)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Incoming CDC batch — simulates records arriving from a source system.
    #    Using VALUES inline as the USING source (no staging table needed here).
    #    In production: USING (SELECT * FROM raw.orders_cdc WHERE batch_id = ?)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Incoming CDC batch ─────────────────────")
    print("    order_id=2 → SHIPPED     (existing → UPDATE)")
    print("    order_id=3 → DELIVERED   (existing → UPDATE)")
    print("    order_id=4 → PENDING     (new      → INSERT)")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. The MERGE statement
    #
    #    ON clause:    join key that identifies "same record"
    #    WHEN MATCHED: row exists in target AND source → UPDATE
    #    WHEN NOT MATCHED: row in source has no target match → INSERT
    #
    #    updated_at = CURRENT_TIMESTAMP() stamps exactly when the row changed.
    #    This is a standard audit column in every production DW table.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        MERGE INTO NUGGET_ORDERS AS tgt
        USING (
            SELECT column1 AS order_id,
                   column2 AS customer_id,
                   column3 AS status
            FROM   VALUES
                (2, 102, 'SHIPPED'),
                (3, 103, 'DELIVERED'),
                (4, 104, 'PENDING')
        ) AS src
        ON tgt.order_id = src.order_id

        WHEN MATCHED THEN
            UPDATE SET
                tgt.status     = src.status,
                tgt.updated_at = CURRENT_TIMESTAMP()

        WHEN NOT MATCHED THEN
            INSERT (order_id, customer_id, status, updated_at)
            VALUES (src.order_id, src.customer_id, src.status, CURRENT_TIMESTAMP())
    """)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Read back MERGE counts
    #    The MERGE statement (in Snowflake) returns a result set:
    #      column 0: number of rows inserted
    #      column 1: number of rows updated
    #    (rows deleted is a 3rd column if WHEN MATCHED … DELETE is present)
    # ─────────────────────────────────────────────────────────────────────────
    result = cur.fetchone()
    rows_inserted = result[0] if result else 0
    rows_updated  = result[1] if result and len(result) > 1 else 0

    print(f"\n  ── MERGE result ────────────────────────────")
    print(f"    rows_inserted = {rows_inserted}")
    print(f"    rows_updated  = {rows_updated}")
    print(f"    rows_deleted  = 0")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Verify final state
    # ─────────────────────────────────────────────────────────────────────────
    print_orders("Final state", cur)

conn.close()
print("\n  Key insight: order 1 was untouched — only rows in the source were affected.\n")
