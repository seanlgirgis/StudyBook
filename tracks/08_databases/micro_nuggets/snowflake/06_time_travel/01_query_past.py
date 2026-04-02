"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 06-01 · Time Travel — Query the Past                                 ║
║  Undo accidents, audit changes, and debug pipelines — without backups.       ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates Snowflake Time Travel: querying a table AT a past timestamp,
BEFORE a specific statement, and AT an OFFSET in seconds.
Shows how to recover accidentally deleted or corrupted rows.

CONCEPTS
────────
What is Time Travel?
  Snowflake retains every version of every row for a configurable window.
  You can query historical data without maintaining your own backups.

  Retention window:
    PERMANENT tables: 0–90 days (default: 1 day; Enterprise: up to 90)
    TRANSIENT tables: 0–1 day
    TEMPORARY tables: 0–1 day
    Set per object: ALTER TABLE t SET DATA_RETENTION_TIME_IN_DAYS = 7;

  After the retention window: Fail-Safe kicks in (7 more days, admin-only).
  After Fail-Safe: data is permanently gone.

Three ways to specify the historical point:

  1. AT (TIMESTAMP => <ts>)       — exact UTC datetime
       SELECT * FROM t AT (TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP_NTZ);

  2. AT (OFFSET => -<seconds>)    — N seconds before NOW
       SELECT * FROM t AT (OFFSET => -3600);   -- 1 hour ago

  3. AT (STATEMENT => '<query_id>') — state just after a specific query ran
     BEFORE (STATEMENT => '<query_id>') — state just BEFORE a query ran
       SELECT * FROM t BEFORE (STATEMENT => '01ab...');

Getting a query ID:
  In Python connector:   cur.sfqid  after any execute()
  In Snowsight:          query results panel → "Query ID" link
  In QUERY_HISTORY view: SELECT query_id FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY ...

Common DE use cases:
  1. Accidental DELETE or UPDATE → recover with INSERT INTO ... SELECT FROM AT
  2. Pipeline produced wrong results → compare current vs yesterday's data
  3. Audit: what did this table look like before the migration ran?
  4. Debug: was this row correct before the 3am job touched it?

Recovery pattern (the most important thing to remember):
  -- Step 1: Find the bad statement's query ID (from QUERY_HISTORY)
  -- Step 2: See what the table looked like BEFORE it ran
  SELECT * FROM my_table BEFORE (STATEMENT => '<bad_query_id>') LIMIT 10;
  -- Step 3: Restore the deleted/corrupted rows
  INSERT INTO my_table
  SELECT * FROM my_table BEFORE (STATEMENT => '<bad_query_id>')
  WHERE  id IN (1, 2, 3);  -- only the affected rows

USAGE
─────
    python 01_query_past.py

EXPECTED OUTPUT
───────────────
    ── Time Travel — Query the Past ─────────────

      Seeded NUGGET_ORDERS with 5 rows.
      Current count: 5

      ── Step 1: Destructive UPDATE (intentional mistake) ─
        Updating ALL rows to status='CORRUPTED' ...
        Update query ID: 01abc123...
        Rows after UPDATE: 5 (all CORRUPTED)

      ── Step 2: Query BEFORE the bad UPDATE ───────────────
        Rows before the UPDATE (using BEFORE STATEMENT):
          ID  STATUS
           1  SHIPPED
           2  PENDING
           3  DELIVERED
           4  SHIPPED
           5  PENDING

      ── Step 3: Recover — restore original data ───────────
        INSERT ... SELECT FROM BEFORE restored 5 rows.
        Current status distribution:
          SHIPPED    2
          PENDING    2
          DELIVERED  1

      ── Step 4: Query at a time offset ────────────────────
        Rows 30 seconds ago (AT OFFSET => -30): 5 rows
        (state before the UPDATE and recovery)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)

print("\n── Time Travel — Query the Past ─────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create a PERMANENT table with time travel enabled (DATA_RETENTION = 1)
    #    TRANSIENT tables have 0-day retention by default — time travel won't
    #    work on them unless you explicitly set DATA_RETENTION_TIME_IN_DAYS = 1.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS (
            order_id    NUMBER,
            customer_id NUMBER,
            status      VARCHAR(20),
            amount      FLOAT
        )
        DATA_RETENTION_TIME_IN_DAYS = 1
        COMMENT = 'Time travel demo table — nugget 06-01'
    """)

    cur.execute("""
        INSERT INTO NUGGET_ORDERS VALUES
            (1, 101, 'SHIPPED',    99.99),
            (2, 102, 'PENDING',    49.99),
            (3, 103, 'DELIVERED', 149.99),
            (4, 101, 'SHIPPED',    29.99),
            (5, 104, 'PENDING',    79.99)
    """)

    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS")
    print(f"\n  Seeded NUGGET_ORDERS with {cur.fetchone()[0]} rows.")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Simulate an accidental destructive UPDATE
    #    We capture the query ID immediately after execution.
    #    cur.sfqid is the Snowflake Query ID — unique identifier for the query.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 1: Destructive UPDATE (intentional mistake) ─")
    print("    Updating ALL rows to status='CORRUPTED' ...")

    # Small sleep so the offset-based query in step 4 has a clear boundary
    time.sleep(3)

    cur.execute("UPDATE NUGGET_ORDERS SET status = 'CORRUPTED'")
    bad_query_id = cur.sfqid   # capture the query ID before next execute

    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS WHERE status = 'CORRUPTED'")
    print(f"    Update query ID: {bad_query_id}")
    print(f"    Rows after UPDATE: {cur.fetchone()[0]} (all CORRUPTED)")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Query BEFORE the bad update using BEFORE (STATEMENT => ...)
    #    This shows the table as it was an instant before that query ran.
    #    The query_id we captured IS the bad query — BEFORE means "just before it".
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 2: Query BEFORE the bad UPDATE ───────────────")
    cur.execute(f"""
        SELECT order_id, status
        FROM   NUGGET_ORDERS BEFORE (STATEMENT => '{bad_query_id}')
        ORDER  BY order_id
    """)
    before_rows = cur.fetchall()
    print("    Rows before the UPDATE (using BEFORE STATEMENT):")
    print(f"    {'ID':>4}  STATUS")
    for oid, status in before_rows:
        print(f"    {oid:>4}  {status}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Recovery — restore the original rows from before the bad update
    #    Pattern: INSERT INTO table SELECT FROM table BEFORE (STATEMENT => ...)
    #    First TRUNCATE current (corrupted) data, then restore.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 3: Recover — restore original data ───────────")
    cur.execute("TRUNCATE TABLE NUGGET_ORDERS")
    cur.execute(f"""
        INSERT INTO NUGGET_ORDERS
        SELECT * FROM NUGGET_ORDERS BEFORE (STATEMENT => '{bad_query_id}')
    """)
    print(f"    INSERT ... SELECT FROM BEFORE restored {cur.rowcount} rows.")

    cur.execute("""
        SELECT status, COUNT(*) AS cnt
        FROM   NUGGET_ORDERS
        GROUP  BY status
        ORDER  BY cnt DESC
    """)
    print("    Current status distribution:")
    for status, cnt in cur.fetchall():
        print(f"      {status:<12} {cnt}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. AT (OFFSET => -n) — query N seconds in the past
    #    Useful when you don't have a query ID but know roughly when things
    #    broke (e.g., "the 3am job ran, things looked wrong by 3:05am").
    #    The 3-second sleep above ensures there's a clean before/after boundary.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 4: Query at a time offset ────────────────────")
    offset_sec = 10   # go back 10 seconds — should be before the UPDATE
    try:
        cur.execute(f"""
            SELECT COUNT(*) FROM NUGGET_ORDERS AT (OFFSET => -{offset_sec})
        """)
        count_then = cur.fetchone()[0]
        print(f"    Rows {offset_sec}s ago (AT OFFSET => -{offset_sec}): {count_then} rows")
        print(f"    (state before the UPDATE was applied)")
    except Exception as exc:
        print(f"    AT OFFSET query: {exc}")
        print("    (offset may be too small — try a larger value if the table is fresh)")

conn.close()
print()
