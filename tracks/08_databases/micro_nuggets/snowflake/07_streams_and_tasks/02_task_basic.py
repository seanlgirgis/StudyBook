"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-02 · Tasks — Scheduled SQL Jobs                                   ║
║  Snowflake's built-in scheduler: no Airflow, no cron, just SQL.              ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates a Task that runs a SQL statement on a schedule, manually triggers
it to prove it works, and reads the execution history. This is the core
building block for automated pipelines inside Snowflake.

CONCEPTS
────────
What is a Task?
  A Task is a named object that runs a single SQL statement (or a stored
  procedure call) on a defined schedule or as part of a task graph.

  CREATE TASK my_task
      WAREHOUSE   = COMPUTE_WH
      SCHEDULE    = '1 MINUTE'          -- or USING CRON '0 * * * * UTC'
      WHEN        SYSTEM$STREAM_HAS_DATA('my_stream')   -- optional condition
  AS
      INSERT INTO target SELECT * FROM source_stream;

  After creating: RESUME the task before it executes.
  ALTER TASK my_task RESUME;

Schedule formats:
  'n MINUTE'   — every n minutes (min 1)
  'n HOUR'     — every n hours
  USING CRON   — full cron expression with timezone:
    '0 2 * * * UTC'   — every day at 02:00 UTC
    '0 */6 * * * UTC' — every 6 hours
    '0 9 * * 1 UTC'   — every Monday at 09:00 UTC

WHEN clause (conditional execution):
  WHEN SYSTEM$STREAM_HAS_DATA('my_stream')
    Only runs if the stream has unconsumed changes.
    Prevents empty/no-op executions and saves compute credits.

Serverless Tasks (Snowflake manages the compute):
  If you omit WAREHOUSE, the task runs on Snowflake-managed serverless compute.
  Billed per second of actual execution (not warehouse running time).
  Better for: short tasks, frequent tasks, tasks with variable duration.
  Standard tasks: you specify WAREHOUSE — uses your warehouse's billing.

Task graph (DAG):
  Tasks can depend on each other:
    CREATE TASK child_task ... AFTER parent_task AS ...;
  Snowflake manages dependencies — child runs after parent succeeds.
  Covered in nugget 07-03.

Task states:
  STARTED   — active, will run on schedule
  SUSPENDED — paused, will not run
  New tasks start SUSPENDED — always RESUME after creation.

Execution history:
  TASK_HISTORY() table function:
    SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
        TASK_NAME => 'MY_TASK',
        RESULT_LIMIT => 10
    ));
  Columns: SCHEDULED_TIME, QUERY_START_TIME, COMPLETED_TIME, STATE, ERROR_CODE

EXECUTE TASK (manual trigger):
  EXECUTE TASK my_task;
  Runs the task immediately regardless of schedule — great for testing.
  Shows up in TASK_HISTORY just like a scheduled run.

Cost management:
  A task keeps the warehouse alive while it runs (minimum 60-second billing).
  For frequent short tasks: use serverless mode.
  For tasks that rarely run: the warehouse auto-suspends between runs.

USAGE
─────
    python 02_task_basic.py

EXPECTED OUTPUT
───────────────
    ── Tasks — Scheduled SQL Jobs ───────────────

      Created table: NUGGET_TASK_LOG
      Created task:  NUGGET_HEARTBEAT_TASK  (SUSPENDED)

      Resuming task ...
      Task state: STARTED

      Manually triggering task with EXECUTE TASK ...
      Waiting for execution to complete ...

      Task execution history (last 5 runs):
        SCHEDULED_TIME           STATE       DURATION_MS  ERROR
        ------------------------ ----------- ------------ -----
        2024-01-17 10:35:00.000  SUCCEEDED           312  None
        (may be empty on first run — history appears with a short delay)

      Log table contents after task run:
        TS                       MESSAGE
        ------------------------ ---------------------------
        2024-01-17 10:35:00.123  heartbeat from NUGGET_HEARTBEAT_TASK

      Suspending task (cleanup) ...
      Task state: SUSPENDED
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection, LAB_DB, LAB_SCHEMA

conn = get_connection(autocommit=True)

print("\n── Tasks — Scheduled SQL Jobs ───────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 0. Create a log table that the task will write into
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_TASK_LOG (
            run_ts   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            message  VARCHAR(500)
        )
    """)
    print("\n  Created table: NUGGET_TASK_LOG")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Create the task
    #
    #    WAREHOUSE = COMPUTE_WH  — use our existing warehouse
    #    SCHEDULE  = '1 MINUTE'  — would run every minute when STARTED
    #    AS INSERT INTO ...      — the SQL to execute
    #
    #    Note: new tasks are SUSPENDED by default.
    #    The SCHEDULE here is 1 minute — we won't wait for it to fire naturally.
    #    Instead we use EXECUTE TASK to trigger it manually.
    # ─────────────────────────────────────────────────────────────────────────
    from _sf_connect import get_creds
    creds = get_creds()
    warehouse = creds.get("SNOWFLAKE_WAREHOUSE") or "COMPUTE_WH"

    cur.execute(f"""
        CREATE OR REPLACE TASK NUGGET_HEARTBEAT_TASK
            WAREHOUSE = {warehouse}
            SCHEDULE  = '1 MINUTE'
            COMMENT   = 'Demo heartbeat task — writes one row per run — nugget 07-02'
        AS
            INSERT INTO {LAB_DB}.{LAB_SCHEMA}.NUGGET_TASK_LOG (message)
            VALUES ('heartbeat from NUGGET_HEARTBEAT_TASK — ran at ' || CURRENT_TIMESTAMP()::VARCHAR)
    """)
    print("  Created task:  NUGGET_HEARTBEAT_TASK  (SUSPENDED)")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. RESUME the task — makes it active (it will fire on schedule)
    #    Without RESUME the task never runs, even past its scheduled time.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("ALTER TASK NUGGET_HEARTBEAT_TASK RESUME")
    cur.execute("SHOW TASKS LIKE 'NUGGET_HEARTBEAT_TASK'")
    task_row  = cur.fetchone()
    task_cols = [d[0] for d in cur.description]
    state_idx = task_cols.index("state")
    print(f"\n  Resuming task ...")
    print(f"  Task state: {task_row[state_idx]}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. EXECUTE TASK — manually trigger one run immediately
    #    This is the most useful command for testing tasks during development.
    #    No need to wait for the scheduled time.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  Manually triggering task with EXECUTE TASK ...")
    cur.execute("EXECUTE TASK NUGGET_HEARTBEAT_TASK")
    print("  Waiting 10 seconds for execution to complete ...")
    time.sleep(10)

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Check execution history
    #    TASK_HISTORY() is a table function in INFORMATION_SCHEMA.
    #    Note: there is a short propagation delay — history may not appear
    #    immediately. The sleep above should cover it for most accounts.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  Task execution history (last 5 runs):")
    try:
        cur.execute(f"""
            SELECT scheduled_time,
                   state,
                   DATEDIFF('millisecond', query_start_time, completed_time) AS duration_ms,
                   error_code
            FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
                TASK_NAME    => 'NUGGET_HEARTBEAT_TASK',
                RESULT_LIMIT => 5
            ))
            ORDER BY scheduled_time DESC
        """)
        hist_rows = cur.fetchall()
        print(f"    {'SCHEDULED_TIME':<25}  {'STATE':<11}  {'DURATION_MS':>11}  ERROR")
        print(f"    {'─'*25}  {'─'*11}  {'─'*11}  {'─'*5}")
        if hist_rows:
            for sched, state, dur, err in hist_rows:
                print(f"    {str(sched)[:25]:<25}  {str(state):<11}  {str(dur or 'N/A'):>11}  {err or 'None'}")
        else:
            print("    (empty — history appears with a short delay. Check again in 30s.)")
    except Exception as exc:
        print(f"    TASK_HISTORY query: {exc}")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Check the log table — did the task actually write a row?
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  Log table contents after task run:")
    cur.execute("SELECT run_ts, message FROM NUGGET_TASK_LOG ORDER BY run_ts DESC LIMIT 5")
    log_rows = cur.fetchall()
    if log_rows:
        print(f"    {'TS':<25}  MESSAGE")
        print(f"    {'─'*25}  {'─'*45}")
        for ts, msg in log_rows:
            print(f"    {str(ts)[:25]:<25}  {str(msg)[:60]}")
    else:
        print("    (no rows yet — task may still be executing. Rerun in 15 seconds.)")

    # ─────────────────────────────────────────────────────────────────────────
    # 6. SUSPEND the task — stop it from firing on schedule
    #    Always suspend tasks you don't need running — they cost credits!
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  Suspending task (cleanup) ...")
    cur.execute("ALTER TASK NUGGET_HEARTBEAT_TASK SUSPEND")
    cur.execute("SHOW TASKS LIKE 'NUGGET_HEARTBEAT_TASK'")
    task_row  = cur.fetchone()
    print(f"  Task state: {task_row[state_idx]}")

conn.close()
print()
