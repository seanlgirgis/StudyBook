"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-02 · COPY INTO — Stage to Table                                   ║
║  The main bulk-load command every Snowflake DE uses daily.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Loads the CSV file uploaded in nugget 04-01 from the internal stage into
a relational table using COPY INTO.  Shows load validation, error handling,
and the load history audit trail.

CONCEPTS
────────
COPY INTO <table>:
  The primary bulk-load mechanism in Snowflake.

  Syntax:
    COPY INTO my_table
    FROM   @my_stage/my_file.csv.gz
    FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1)
    ON_ERROR = 'CONTINUE';

  Key facts:
  - Runs INSIDE Snowflake's warehouse (not on your laptop).
  - Parallel: the warehouse splits large files across nodes automatically.
  - Idempotent by default: Snowflake tracks loaded files in a "load history".
    Rerunning COPY INTO on the same file is a no-op (SKIPPED status).
    Reset with: COPY INTO ... FORCE = TRUE

  Performance tips:
  - Split large files into 100-250 MB compressed chunks before staging.
  - Use GZIP or SNAPPY compression (Snowflake handles decompression).
  - Use PARQUET for analytical workloads (schema preserved, columnar).

ON_ERROR options:
  ABORT_STATEMENT   — (default) rollback the entire COPY on first error
  CONTINUE          — skip bad rows, keep loading, report errors at end
  SKIP_FILE         — skip the entire file if it has any errors
  SKIP_FILE_<n>     — skip file if more than n errors found

  For learning/dev:  ON_ERROR = 'CONTINUE' is safer (you see what failed).
  For production:    ON_ERROR = 'ABORT_STATEMENT' (fail fast, fix source data).

VALIDATION_MODE:
  Before loading, run COPY INTO in validation-only mode to check for errors:
    COPY INTO my_table FROM @my_stage
    FILE_FORMAT = (...)
    VALIDATION_MODE = 'RETURN_ERRORS';
  Returns rows that WOULD fail — zero cost, no data is loaded.

Load history:
  Every successful COPY INTO is recorded in:
    INFORMATION_SCHEMA.LOAD_HISTORY     — last 14 days, per database
    SNOWFLAKE.ACCOUNT_USAGE.LOAD_HISTORY — up to 1 year, account-wide
  This is your audit trail: when was the file loaded, how many rows, errors?

COPY vs INSERT INTO … SELECT:
  COPY INTO is optimised for bulk file loading (GB/TB scale).
  INSERT INTO … SELECT is for transforming existing table data.
  Never use INSERT … VALUES for bulk loading — it's single-threaded and slow.

USAGE
─────
    python 02_copy_into_table.py
    (run 01_internal_stage_put.py first to upload the file)

EXPECTED OUTPUT
───────────────
    ── COPY INTO — Stage to Table ───────────────

      Created: NUGGET_ORDERS_STAGING

      ── Validation pass (no actual load) ──────────────
        VALIDATION_MODE result: 0 error(s) — file is clean

      ── COPY INTO ─────────────────────────────────────
        file                         rows_loaded  errors  status
        ---------------------------- ------------ ------- --------
        nugget_orders_sample.csv.gz            5       0  LOADED

      ── Rows in table ─────────────────────────────────
        5 rows loaded

        ORDER_ID  CUSTOMER_ID  PRODUCT_ID  QTY  PRICE  ORDER_DATE   STATUS
        --------  -----------  ----------  ---  -----  ----------   ---------
            1001          201          10    2  29.99  2024-01-10   SHIPPED
            1002          202          11    1  49.99  2024-01-11   PENDING
            ...

      ── Re-run COPY (idempotency demo) ────────────────
        Re-run result:  SKIPPED (already loaded — Snowflake's load history)

      ── Load history ──────────────────────────────────
        FILE                         ROW_COUNT  ERROR_COUNT  LAST_LOAD_TIME
        ---------------------------- ---------- ------------ -------------------------
        nugget_orders_sample.csv.gz          5           0  2024-01-17 10:25:01.000
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── COPY INTO — Stage to Table ───────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # Guard: check the stage and file exist (from nugget 04-01)
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("SHOW STAGES LIKE 'NUGGET_INTERNAL_STAGE'")
    if not cur.fetchone():
        print("\n  ERROR: NUGGET_INTERNAL_STAGE not found.")
        print("  Run 04_loading_data/01_internal_stage_put.py first.\n")
        conn.close()
        sys.exit(1)

    cur.execute("LIST @NUGGET_INTERNAL_STAGE")
    if not cur.fetchone():
        print("\n  ERROR: No files in NUGGET_INTERNAL_STAGE.")
        print("  Run 04_loading_data/01_internal_stage_put.py first.\n")
        conn.close()
        sys.exit(1)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Create the target table
    #    Column order must match the CSV column order (unless we use a
    #    SELECT transformation inside COPY INTO — covered below).
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE TABLE NUGGET_ORDERS_STAGING (
            order_id     NUMBER,
            customer_id  NUMBER,
            product_id   NUMBER,
            quantity     NUMBER,
            unit_price   FLOAT,
            order_date   DATE,
            status       VARCHAR(20)
        )
        COMMENT = 'Orders loaded from CSV via COPY INTO — nugget 04-02'
    """)
    print("\n  Created: NUGGET_ORDERS_STAGING")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Validation pass — check for errors WITHOUT loading data
    #    VALIDATION_MODE = 'RETURN_ERRORS' — returns bad rows, loads nothing.
    #    VALIDATION_MODE = 'RETURN_n_ROWS' — returns first n rows as they
    #    would be parsed (great for sanity-checking format assumptions).
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Validation pass (no actual load) ──────────────")
    try:
        cur.execute("""
            COPY INTO NUGGET_ORDERS_STAGING
            FROM   @NUGGET_INTERNAL_STAGE
            FILE_FORMAT = (
                TYPE        = CSV
                SKIP_HEADER = 1
                FIELD_OPTIONALLY_ENCLOSED_BY = '"'
                DATE_FORMAT = 'YYYY-MM-DD'
            )
            VALIDATION_MODE = 'RETURN_ERRORS'
        """)
        error_rows = cur.fetchall()
        print(f"    VALIDATION_MODE result: {len(error_rows)} error(s) — ", end="")
        print("file is clean" if not error_rows else "fix errors before loading!")
        for row in error_rows[:5]:
            print(f"    ERROR: {row}")
    except Exception as exc:
        # Some Snowflake editions surface validation errors differently
        print(f"    Validation result: {exc}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. COPY INTO — the actual load
    #
    #    FILE_FORMAT inline (no named format object):
    #      TYPE             = CSV
    #      SKIP_HEADER      = 1   ← skip the header row
    #      DATE_FORMAT      = 'YYYY-MM-DD'  ← parse date columns correctly
    #      FIELD_OPTIONALLY_ENCLOSED_BY = '"'  ← handle quoted fields
    #
    #    Named FILE_FORMAT objects (more reusable) → nugget 04-03.
    #
    #    Returns one row per file processed:
    #      file, status, rows_loaded, rows_parsed, first_error, etc.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── COPY INTO ─────────────────────────────────────")
    cur.execute("""
        COPY INTO NUGGET_ORDERS_STAGING
        FROM   @NUGGET_INTERNAL_STAGE
        FILE_FORMAT = (
            TYPE        = CSV
            SKIP_HEADER = 1
            FIELD_OPTIONALLY_ENCLOSED_BY = '"'
            DATE_FORMAT = 'YYYY-MM-DD'
        )
        ON_ERROR = 'CONTINUE'
    """)
    copy_rows = cur.fetchall()
    copy_cols = [d[0] for d in cur.description]

    print(f"    {'file':<28}  {'rows_loaded':>11}  {'errors':>6}  status")
    print(f"    {'─'*28}  {'─'*11}  {'─'*6}  {'─'*8}")
    for row in copy_rows:
        row_dict = dict(zip(copy_cols, row))
        fname    = str(row_dict.get("file", "")).split("/")[-1][:28]
        loaded   = row_dict.get("rows_loaded", 0) or 0
        errors   = row_dict.get("errors_seen", 0) or 0
        status   = row_dict.get("status", "")
        print(f"    {fname:<28}  {loaded:>11}  {errors:>6}  {status}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Verify loaded rows
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM NUGGET_ORDERS_STAGING")
    count = cur.fetchone()[0]
    print(f"\n  ── Rows in table ─────────────────────────────────")
    print(f"    {count} rows loaded\n")

    cur.execute("""
        SELECT order_id, customer_id, product_id, quantity,
               unit_price, order_date, status
        FROM   NUGGET_ORDERS_STAGING
        ORDER  BY order_id
    """)
    rows = cur.fetchall()
    print(f"    {'ORDER_ID':>8}  {'CUST':>5}  {'PROD':>5}  {'QTY':>4}  {'PRICE':>7}  {'DATE':<12}  STATUS")
    print(f"    {'─'*8}  {'─'*5}  {'─'*5}  {'─'*4}  {'─'*7}  {'─'*12}  {'─'*9}")
    for oid, cid, pid, qty, price, odate, status in rows:
        print(f"    {oid:>8}  {cid:>5}  {pid:>5}  {qty:>4}  {price:>7.2f}  {str(odate):<12}  {status}")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Idempotency demo — re-run the exact same COPY INTO
    #    Snowflake tracks loaded files by path + checksum in its load history.
    #    The same file will be SKIPPED automatically — no duplicate rows.
    #    This makes COPY INTO safe to run in a scheduled pipeline without
    #    checking "was this file already loaded?"
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── Re-run COPY (idempotency demo) ────────────────")
    cur.execute("""
        COPY INTO NUGGET_ORDERS_STAGING
        FROM   @NUGGET_INTERNAL_STAGE
        FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 DATE_FORMAT = 'YYYY-MM-DD')
    """)
    rerun_rows = cur.fetchall()
    rerun_cols = [d[0] for d in cur.description]
    for row in rerun_rows:
        row_dict = dict(zip(rerun_cols, row))
        status   = row_dict.get("status", "")
        print(f"    Re-run result: {status}  (Snowflake's load history prevented duplicates)")

    # ─────────────────────────────────────────────────────────────────────────
    # 6. Load history — the audit trail
    #    INFORMATION_SCHEMA.LOAD_HISTORY shows every COPY INTO in this database
    #    for the past 14 days.  Use it to monitor pipelines or debug failures.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── Load history ──────────────────────────────────")
    cur.execute("""
        SELECT file_name,
               row_count,
               error_count,
               last_load_time
        FROM   information_schema.load_history
        WHERE  table_name = 'NUGGET_ORDERS_STAGING'
        ORDER  BY last_load_time DESC
        LIMIT  5
    """)
    hist_rows = cur.fetchall()
    if hist_rows:
        print(f"    {'FILE':<30}  {'ROWS':>6}  {'ERRORS':>6}  LAST_LOAD_TIME")
        print(f"    {'─'*30}  {'─'*6}  {'─'*6}  {'─'*25}")
        for fname, rows_n, errs, load_ts in hist_rows:
            short_name = str(fname).split("/")[-1][:30]
            print(f"    {short_name:<30}  {rows_n:>6}  {errs:>6}  {load_ts}")
    else:
        print("    (load history may take a moment to refresh — check Snowsight UI)")

conn.close()
print()
