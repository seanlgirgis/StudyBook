"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-03 · Stream + Task Pipeline                                       ║
║  Wire a Stream to a Task to build a fully automated CDC pipeline.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Combines everything from 07-01 and 07-02: a Stream captures changes on a
source table, and a Task wakes up on a schedule, checks if the stream has
data, and applies the changes to a target table via MERGE.

This is the complete Snowflake-native ELT micro-batch pattern.

CONCEPTS
────────
The Full Pattern:
  ┌─────────────────────┐
  │  NUGGET_ORDERS      │  ← source: DE writes raw data here
  │  (source table)     │
  └────────┬────────────┘
           │ CDC
           ▼
  ┌─────────────────────┐
  │ NUGGET_ORDERS_STREAM│  ← stream: records every change
  └────────┬────────────┘
           │ consumed by
           ▼
  ┌─────────────────────┐
  │  NUGGET_CDC_TASK    │  ← task: runs every minute (or on demand)
  │  WHEN stream        │    WHEN clause = only fires if stream has data
  │  has data           │
  └────────┬────────────┘
           │ MERGE INTO
           ▼
  ┌─────────────────────┐
  │ NUGGET_ORDERS_CLEAN │  ← target: always up to date, deduplicated
  │  (target table)     │
  └─────────────────────┘

Why MERGE inside the task?
  The stream can contain INSERTs, UPDATEs (as DELETE+INSERT), and DELETEs.
  MERGE handles all three cases in one atomic statement:
    WHEN MATCHED AND ACTION = 'DELETE' THEN DELETE
    WHEN MATCHED AND ACTION = 'INSERT' THEN UPDATE SET ...
    WHEN NOT MATCHED                   THEN INSERT ...

  This keeps NUGGET_ORDERS_CLEAN in sync with NUGGET_ORDERS automatically.

Atomicity — the critical correctness guarantee:
  The MERGE that consumes the stream and the stream offset advance happen
  in the SAME transaction.  If the MERGE fails, the stream offset does NOT
  advance — changes stay in the stream for the next run.
  This means the pipeline is exactly-once: no data lost, no duplicates.

Task WHEN clause:
  WHEN SYSTEM$STREAM_HAS_DATA('NUGGET_ORDERS_STREAM')
  If the stream is empty when the task wakes up, the task body does NOT run.
  Zero compute cost for empty runs. Warehouse does not activate.

Scaling this pattern:
  - Multiple streams on the same source table (each has its own offset).
  - Chain tasks (AFTER parent_task) for multi-step pipelines.
  - Replace the MERGE with a stored procedure for complex logic.
  - Add NUGGET_CDC_TASK to a task graph for dependency management.

Real-world equivalent:
  This pattern replaces:
    Airflow DAG + custom Python scripts + manual CDC logic + retry handling
  With:
    3 SQL objects (table + stream + task) managed entirely inside Snowflake.

USAGE
─────
    python 03_stream_task_pipeline.py

EXPECTED OUTPUT
───────────────
    ── Stream + Task Pipeline ───────────────────

      ── Setup ─────────────────────────────────────────
        [✓] Source table  : NUGGET_ORDERS
        [✓] Target table  : NUGGET_ORDERS_CLEAN
        [✓] Stream        : NUGGET_ORDERS_STREAM
        [✓] Task          : NUGGET_CDC_TASK  (SUSPENDED initially)

      ── Round 1: insert into source ───────────────────
        Inserted 3 rows into NUGGET_ORDERS.
        Stream has data? True

        Triggering NUGGET_CDC_TASK ...
        Waiting ...

        NUGGET_ORDERS_CLEAN after task run:
          ORDER_ID  STATUS      AMOUNT
          --------- ----------- -------
                 1  PENDING       99.99
                 2  PENDING       49.99
                 3  PENDING      149.99

      ── Round 2: update + delete in source ────────────
        Updated order 2 → SHIPPED.  Deleted order 1.
        Triggering NUGGET_CDC_TASK ...
        Waiting ...

        NUGGET_ORDERS_CLEAN after task run:
          ORDER_ID  STATUS      AMOUNT
          --------- ----------- -------
                 2  SHIPPED      49.99
                 3  PENDING     149.99
          (order 1 deleted, order 2 updated — target in sync!)

      Task suspended. Pipeline demo complete.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection, LAB_DB, LAB_SCHEMA, get_creds

conn = get_connection(autocommit=True)
creds = get_creds()
warehouse = creds.get("SNOWFLAKE_WAREHOUSE") or "COMPUTE_WH"

print("\n── Stream + Task Pipeline ───────────────────")


def show_target(cur, label: str) -> None:
    cur.execute("""
        SELECT order_id, status, amount
        FROM   NUGGET_ORDERS_CLEAN
        ORDER  BY order_id
    """)
    rows = cur.fetchall()
    print(f"\n    {label}")
    if not rows:
        print("    (empty)")
        return
    print(f"    {'ORDER_ID':>9}  {'STATUS':<12}  AMOUNT")
    print(f"    {'─'*9}  {'─'*12}  {'─'*7}")
    for oid, status, amount in rows:
        print(f"    {oid:>9}  {status:<12}  {amount:>7.2f}")


def trigger_and_wait(cur, task_name: str, wait_sec: int = 12) -> None:
    cur.execute(f"EXECUTE TASK {task_name}")
    print(f"    Triggering {task_name} ... waiting {wait_sec}s ...")
    time.sleep(wait_sec)


with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create all three objects: source table, target table, stream, task
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Setup ─────────────────────────────────────────")

    # Source table
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS (
            order_id    NUMBER  NOT NULL,
            customer_id NUMBER,
            status      VARCHAR(20),
            amount      FLOAT
        ) DATA_RETENTION_TIME_IN_DAYS = 1
    """)
    print("    [✓] Source table  : NUGGET_ORDERS")

    # Target table — always stays in sync via the task
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS_CLEAN (
            order_id    NUMBER  NOT NULL,
            customer_id NUMBER,
            status      VARCHAR(20),
            amount      FLOAT,
            last_updated TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("    [✓] Target table  : NUGGET_ORDERS_CLEAN")

    # Stream on source
    cur.execute("""
        CREATE OR REPLACE STREAM NUGGET_ORDERS_STREAM
        ON TABLE NUGGET_ORDERS
    """)
    print("    [✓] Stream        : NUGGET_ORDERS_STREAM")

    # ─────────────────────────────────────────────────────────────────────────
    # Task body: MERGE from the stream into the clean target.
    #
    #   The stream rows have METADATA$ACTION = 'INSERT' or 'DELETE'
    #   and METADATA$ISUPDATE = TRUE/FALSE.
    #
    #   For a DELETE+INSERT UPDATE pair:
    #     Step A: WHEN MATCHED AND ACTION='DELETE' AND ISUPDATE=TRUE → skip
    #             (the paired INSERT below will UPDATE the target row)
    #     Step B: WHEN MATCHED AND ACTION='INSERT' AND ISUPDATE=TRUE → UPDATE
    #     Step C: WHEN MATCHED AND ACTION='DELETE' AND ISUPDATE=FALSE → DELETE
    #     Step D: WHEN NOT MATCHED AND ACTION='INSERT'               → INSERT
    #
    #   This logic is standard for Snowflake stream→table pipelines.
    # ─────────────────────────────────────────────────────────────────────────
    task_sql = f"""
        MERGE INTO {LAB_DB}.{LAB_SCHEMA}.NUGGET_ORDERS_CLEAN AS tgt
        USING (
            SELECT order_id,
                   customer_id,
                   status,
                   amount,
                   METADATA$ACTION   AS action,
                   METADATA$ISUPDATE AS is_update
            FROM   {LAB_DB}.{LAB_SCHEMA}.NUGGET_ORDERS_STREAM
        ) AS src
        ON tgt.order_id = src.order_id

        -- Hard delete: source deleted the row
        WHEN MATCHED AND src.action = 'DELETE' AND NOT src.is_update THEN
            DELETE

        -- Update: the INSERT half of a DELETE+INSERT pair
        WHEN MATCHED AND src.action = 'INSERT' AND src.is_update THEN
            UPDATE SET
                tgt.status       = src.status,
                tgt.amount       = src.amount,
                tgt.last_updated = CURRENT_TIMESTAMP()

        -- New row: pure INSERT (not part of an update pair)
        WHEN NOT MATCHED AND src.action = 'INSERT' THEN
            INSERT (order_id, customer_id, status, amount, last_updated)
            VALUES (src.order_id, src.customer_id, src.status, src.amount, CURRENT_TIMESTAMP())
    """

    cur.execute(f"""
        CREATE OR REPLACE TASK NUGGET_CDC_TASK
            WAREHOUSE = {warehouse}
            SCHEDULE  = '1 MINUTE'
            COMMENT   = 'Applies stream changes to NUGGET_ORDERS_CLEAN — nugget 07-03'
            WHEN      SYSTEM$STREAM_HAS_DATA('{LAB_DB}.{LAB_SCHEMA}.NUGGET_ORDERS_STREAM')
        AS
        {task_sql}
    """)
    cur.execute("ALTER TASK NUGGET_CDC_TASK RESUME")
    print("    [✓] Task          : NUGGET_CDC_TASK  (RESUMED — ready to run)")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Round 1 — insert rows into source, let task propagate them
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Round 1: insert into source ───────────────────")
    cur.execute("""
        INSERT INTO NUGGET_ORDERS VALUES
            (1, 101, 'PENDING',  99.99),
            (2, 102, 'PENDING',  49.99),
            (3, 103, 'PENDING', 149.99)
    """)
    cur.execute("SELECT SYSTEM$STREAM_HAS_DATA('NUGGET_ORDERS_STREAM')")
    print(f"    Inserted 3 rows into NUGGET_ORDERS.")
    print(f"    Stream has data? {cur.fetchone()[0]}")
    trigger_and_wait(cur, "NUGGET_CDC_TASK")
    show_target(cur, "NUGGET_ORDERS_CLEAN after Round 1:")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Round 2 — update and delete in source, task propagates again
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Round 2: update + delete in source ────────────")
    cur.execute("UPDATE NUGGET_ORDERS SET status = 'SHIPPED' WHERE order_id = 2")
    cur.execute("DELETE FROM NUGGET_ORDERS WHERE order_id = 1")
    print("    Updated order 2 → SHIPPED.  Deleted order 1.")
    trigger_and_wait(cur, "NUGGET_CDC_TASK")
    show_target(cur, "NUGGET_ORDERS_CLEAN after Round 2:")
    print("    (order 1 deleted, order 2 updated — target is in sync!)")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Cleanup — suspend the task
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("ALTER TASK NUGGET_CDC_TASK SUSPEND")
    print("\n  Task suspended. Pipeline demo complete.")
    print("  Run 00_setup/99_reset_lab.py to drop all nugget objects.\n")

conn.close()
