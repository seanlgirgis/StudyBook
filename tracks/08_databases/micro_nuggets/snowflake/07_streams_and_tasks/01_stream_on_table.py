"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · Streams — Change Data Capture on a Table                     ║
║  Track every INSERT, UPDATE, and DELETE without touching the source table.   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates a STREAM on NUGGET_ORDERS, performs DML, then reads the stream
to see exactly what changed — the foundation of Snowflake CDC pipelines.

CONCEPTS
────────
What is a Stream?
  A Stream is a Snowflake object that records the DML changes (INSERT, UPDATE,
  DELETE) made to a source table since the stream was last consumed.

  Think of it as a commit log or a Kafka topic — every change appended,
  read once, then the offset advances.  Unlike Kafka, it's SQL-native.

  CREATE STREAM my_stream ON TABLE my_source_table;

How streams work (offset tracking):
  ┌─────────────┐      ┌──────────────┐      ┌─────────────┐
  │ Source table │  →  │    Stream    │  →   │ Target table │
  │ (orders)     │      │ (CDC log)    │      │ (analytics) │
  └─────────────┘      └──────────────┘      └─────────────┘
  The stream maintains an "offset" pointer to the last consumed change.
  When you SELECT from the stream, you see changes SINCE the last offset.
  When a DML statement consumes the stream (INSERT INTO ... SELECT FROM stream),
  the offset advances — those changes are now "gone" from the stream view.

System columns added by streams (metadata):
  METADATA$ACTION       — 'INSERT' or 'DELETE'
                          (an UPDATE is represented as DELETE + INSERT pair!)
  METADATA$ISUPDATE     — TRUE if this row is part of an UPDATE pair
  METADATA$ROW_ID       — unique identifier for the row version

  The DELETE + INSERT pair for UPDATE:
    When a row is UPDATED, the stream shows TWO rows:
      Row 1: METADATA$ACTION = 'DELETE', METADATA$ISUPDATE = TRUE  ← old values
      Row 2: METADATA$ACTION = 'INSERT', METADATA$ISUPDATE = TRUE  ← new values
    This lets you see BOTH the before and after state.

Stream types:
  DEFAULT (APPEND_ONLY = FALSE):
    Captures INSERTs, UPDATEs, and DELETEs.
    Most powerful — used for full CDC pipelines.
  APPEND_ONLY (APPEND_ONLY = TRUE):
    Captures only INSERTs. Ignores UPDATEs and DELETEs.
    Lower overhead — perfect for append-only event logs or staging tables.
  INSERT_ONLY:
    For external tables — only INSERT tracking.

SYSTEM$STREAM_HAS_DATA():
  Returns TRUE if the stream has unconsumed changes.
  Use in Task conditions to avoid unnecessary processing:
    WHEN SYSTEM$STREAM_HAS_DATA('my_stream')
  Covered in nugget 07-02.

Stream staleness:
  A stream becomes STALE if its offset falls outside the source table's
  Time Travel retention window (e.g., if the table has 1-day retention
  and the stream wasn't consumed for 2 days).
  Stale streams must be recreated.  Monitor with:
    SHOW STREAMS;
    Check "stale" column.

USAGE
─────
    python 01_stream_on_table.py

EXPECTED OUTPUT
───────────────
    ── Streams — Change Data Capture ────────────

      Created table: NUGGET_ORDERS
      Created stream: NUGGET_ORDERS_STREAM

      Stream has data? False  ← no changes yet

      ── Step 1: INSERT 3 rows ───────────────────────────
        Stream has data? True

        ACTION  IS_UPDATE  ORDER_ID  STATUS
        ------- ---------- --------- ---------
        INSERT  False             1  PENDING
        INSERT  False             2  PENDING
        INSERT  False             3  PENDING

      ── Step 2: UPDATE 1 row ────────────────────────────
        Stream shows UPDATE as DELETE + INSERT pair:

        ACTION  IS_UPDATE  ORDER_ID  STATUS
        ------- ---------- --------- ---------
        DELETE  True              2  PENDING    ← old value
        INSERT  True              2  SHIPPED    ← new value
        INSERT  False             4  PENDING    ← new row from step1 leftovers
        ...

      ── Step 3: DELETE 1 row ────────────────────────────
        ACTION  IS_UPDATE  ORDER_ID  STATUS
        ------- ---------- --------- ---------
        DELETE  False             1  PENDING

      ── Stream is now empty ─────────────────────────────
        Stream has data? False  ← all changes consumed
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection(autocommit=True)

print("\n── Streams — Change Data Capture ────────────")


def read_stream(cur, label: str) -> None:
    """Read and print all pending changes from the stream."""
    cur.execute("""
        SELECT METADATA$ACTION    AS action,
               METADATA$ISUPDATE  AS is_update,
               order_id,
               status
        FROM   NUGGET_ORDERS_STREAM
        ORDER  BY order_id, METADATA$ACTION DESC
    """)
    rows = cur.fetchall()
    print(f"\n    {label}")
    if not rows:
        print("    (stream is empty)")
        return
    print(f"    {'ACTION':<7}  {'IS_UPDATE':<10}  {'ORDER_ID':>9}  STATUS")
    print(f"    {'─'*7}  {'─'*10}  {'─'*9}  {'─'*9}")
    for action, is_upd, oid, status in rows:
        print(f"    {str(action):<7}  {str(is_upd):<10}  {oid:>9}  {status}")


def has_data(cur) -> bool:
    cur.execute("SELECT SYSTEM$STREAM_HAS_DATA('NUGGET_ORDERS_STREAM')")
    return bool(cur.fetchone()[0])


with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create source table and stream
    #    The stream records changes from this point forward — not historical.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS (
            order_id    NUMBER,
            customer_id NUMBER,
            status      VARCHAR(20),
            amount      FLOAT
        )
        DATA_RETENTION_TIME_IN_DAYS = 1
    """)
    print("\n  Created table: NUGGET_ORDERS")

    cur.execute("""
        CREATE OR REPLACE STREAM NUGGET_ORDERS_STREAM
        ON TABLE NUGGET_ORDERS
        COMMENT = 'CDC stream on NUGGET_ORDERS — nugget 07-01'
    """)
    print("  Created stream: NUGGET_ORDERS_STREAM")

    print(f"\n  Stream has data? {has_data(cur)}  ← no changes yet")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. INSERT rows → stream captures them as INSERT actions
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 1: INSERT 3 rows ───────────────────────────")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS VALUES
            (1, 101, 'PENDING', 99.99),
            (2, 102, 'PENDING', 49.99),
            (3, 103, 'PENDING', 149.99)
    """)
    print(f"  Stream has data? {has_data(cur)}")
    read_stream(cur, "Stream after INSERT:")

    # ─────────────────────────────────────────────────────────────────────────
    # IMPORTANT: reading the stream with SELECT does NOT advance the offset.
    # Only a DML statement (INSERT INTO ... SELECT FROM stream) consumes it.
    # So the stream above still shows all 3 inserts.
    # We consume it now by inserting into a "processed" temp table.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TEMPORARY TABLE nugget_stream_consumed AS
        SELECT * FROM NUGGET_ORDERS_STREAM
    """)
    # Now the stream offset has advanced — those 3 changes are consumed.

    # ─────────────────────────────────────────────────────────────────────────
    # 2. UPDATE → stream shows DELETE (old) + INSERT (new) pair
    #    This is the most important concept to understand about streams.
    #    You can reconstruct the "before" value from the DELETE row.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 2: UPDATE 1 row ────────────────────────────")
    print("  (stream shows UPDATE as DELETE old-value + INSERT new-value)")
    cur.execute("UPDATE NUGGET_ORDERS SET status = 'SHIPPED' WHERE order_id = 2")

    read_stream(cur, "Stream after UPDATE — notice DELETE + INSERT pair:")
    print()
    print("    The DELETE row shows the BEFORE value (PENDING).")
    print("    The INSERT row shows the AFTER  value (SHIPPED).")
    print("    Both have METADATA$ISUPDATE = True — they are a matched pair.")

    # Consume again
    cur.execute("""
        CREATE OR REPLACE TEMPORARY TABLE nugget_stream_consumed AS
        SELECT * FROM NUGGET_ORDERS_STREAM
    """)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. DELETE → stream shows it as a DELETE action
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Step 3: DELETE 1 row ────────────────────────────")
    cur.execute("DELETE FROM NUGGET_ORDERS WHERE order_id = 1")
    read_stream(cur, "Stream after DELETE:")

    # Consume
    cur.execute("""
        CREATE OR REPLACE TEMPORARY TABLE nugget_stream_consumed AS
        SELECT * FROM NUGGET_ORDERS_STREAM
    """)

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Stream metadata
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── Stream is now empty ─────────────────────────────")
    print(f"  Stream has data? {has_data(cur)}  ← all changes consumed")

    print(f"\n  ── SHOW STREAMS ────────────────────────────────────")
    cur.execute("SHOW STREAMS LIKE 'NUGGET_ORDERS_STREAM'")
    stream_rows = cur.fetchall()
    stream_cols = [d[0] for d in cur.description]
    for row in stream_rows:
        row_dict = dict(zip(stream_cols, row))
        print(f"    name         : {row_dict.get('name')}")
        print(f"    source table : {row_dict.get('table_name')}")
        print(f"    type         : {row_dict.get('type')}")
        print(f"    stale        : {row_dict.get('stale')}")
        print(f"    stale_after  : {row_dict.get('stale_after')}")

conn.close()
print()
