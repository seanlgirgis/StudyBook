"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · Time Travel with Delta Lake                                 ║
║  Querying previous versions of your data — the killer feature.               ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates Delta Lake's Time Travel feature — query any previous version
of your table, audit changes, and recover from accidental data loss.

CONCEPTS
────────
Time Travel — what it is:
  - Every change to a Delta table creates a new version (commit) in the
    transaction log (_delta_log/).
  - You can query ANY previous version by version number or timestamp.
  - This is NOT a backup — it's a built-in feature of Delta's architecture.
  - Default retention: 30 days (configurable via delta.logRetentionDuration).

Why Time Travel matters in DE:
  - **Audit**: "What did this table look like yesterday at 3pm?"
  - **Debugging**: "When did this bad data get introduced?"
  - **Recovery**: "I accidentally deleted 1M rows — restore the table!"
  - **Reproducibility**: "Re-run this report using the data as of Jan 15."
  - **Compliance**: "Show me the state of this data on the audit date."

How it works under the hood:
  - Delta's transaction log tracks every file added/removed per commit.
  - Each commit has a version number (monotonically increasing).
  - Each commit has a timestamp and user metadata.
  - To query version N, Delta reads the files that were active at version N.
  - Old data files are NOT deleted immediately — they're kept for the
    retention period (default 30 days) so Time Travel works.

DESCRIBE HISTORY:
  - Shows every commit to the table: version, timestamp, operation, user.
  - Like git log for your data.
  - Key columns: version, timestamp, operation, operationParameters.

Querying by version:
  SELECT * FROM table VERSION AS OF 5

Querying by timestamp:
  SELECT * FROM table TIMESTAMP AS OF '2024-01-15 14:30:00'

RESTORE:
  RESTORE TABLE table TO VERSION AS OF 5
  RESTORE TABLE table TO TIMESTAMP AS OF '2024-01-15 14:30:00'
  - Rolls back the table to a previous version.
  - Creates a NEW commit (doesn't delete history — adds to it).
  - Readers see the restored state immediately.

VACUUM:
  VACUUM table RETAIN 168 HOURS  -- 7 days
  - Permanently deletes old data files that are no longer referenced.
  - After VACUUM, you CANNOT Time Travel past the vacuum point.
  - Default retention: 168 hours (7 days) for data files.
  - NEVER set retention to 0 in production — you lose Time Travel!

USAGE
─────
    python 01_time_travel.py

EXPECTED OUTPUT
───────────────
    ── Delta Time Travel ──────────────────────────────

      ── Initial state ──────────────────────────────
        ID  Name                Price
        --  ------------------  ---------
         1  Laptop Pro 15       1299.99
         2  Wireless Mouse        29.99
         3  USB-C Hub             49.99

      ── After UPDATE (version 1) ───────────────────
        ID  Name                Price
        --  ------------------  ---------
         1  Laptop Pro 15       1399.99   ← price changed
         2  Wireless Mouse        29.99
         3  USB-C Hub             49.99

      ── After DELETE (version 2) ───────────────────
        ID  Name                Price
        --  ------------------  ---------
         1  Laptop Pro 15       1399.99
         2  Wireless Mouse        29.99
         ← Product 3 deleted

      ── Time Travel: version 0 (original) ──────────
        ID  Name                Price
        --  ------------------  ---------
         1  Laptop Pro 15       1299.99
         2  Wireless Mouse        29.99
         3  USB-C Hub             49.99

      ── DESCRIBE HISTORY ───────────────────────────
        Ver  Timestamp                    Operation
        ---  ---------------------------  ----------
          0  2024-01-15 14:30:00         CREATE OR REPLACE TABLE
          1  2024-01-15 14:30:05         UPDATE
          2  2024-01-15 14:30:10         DELETE

      ── RESTORE to version 0 ───────────────────────
        Table restored to version 0.

      ── After RESTORE ──────────────────────────────
        ID  Name                Price
        --  ------------------  ---------
         1  Laptop Pro 15       1299.99
         2  Wireless Mouse        29.99
         3  USB-C Hub             49.99
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── Delta Time Travel ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Create a table for Time Travel demonstration
#    We'll make several changes to this table, then travel back in time.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo (
            product_id      INT             NOT NULL,
            product_name    STRING          NOT NULL,
            price           DECIMAL(10,2)
        )
        USING DELTA
        COMMENT 'Demo table for Time Travel'
    """)

    # Insert initial data — this is VERSION 0
    cur.execute(f"""
        INSERT INTO {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        VALUES
            (1, 'Laptop Pro 15', 1299.99),
            (2, 'Wireless Mouse', 29.99),
            (3, 'USB-C Hub', 49.99)
    """)

print("\n  ── Initial state (version 0) ─────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Price'}")
print(f"    {'--':<4} {'-'*20} {'-'*10}")
for pid, name, price in rows:
    print(f"    {pid:<4} {name:<20} ${price:,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. UPDATE — changes the price of product 1
#    This creates VERSION 1 in the Delta log.
#    The old data files still exist — they're just no longer the "current" version.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f"""
        UPDATE {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        SET    price = 1399.99
        WHERE  product_id = 1
    """)

print("\n  ── After UPDATE (version 1) ───────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Price'}")
print(f"    {'--':<4} {'-'*20} {'-'*10}")
for pid, name, price in rows:
    print(f"    {pid:<4} {name:<20} ${price:,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. DELETE — removes product 3
#    This creates VERSION 2.
#    The deleted row's data file still exists on disk — it's just marked as
#    "removed" in the transaction log. Time Travel can still read it.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f"""
        DELETE FROM {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        WHERE  product_id = 3
    """)

print("\n  ── After DELETE (version 2) ───────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Price'}")
print(f"    {'--':<4} {'-'*20} {'-'*10}")
for pid, name, price in rows:
    print(f"    {pid:<4} {name:<20} ${price:,.2f}")
print("    ← Product 3 deleted")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Time Travel — query version 1 (the initial data state)
#    Version 0 = CREATE TABLE (empty).
#    Version 1 = INSERT (our initial 3 rows).
#    Version 2 = UPDATE (price change).
#    Version 3 = DELETE (product 3 removed).
#
#    Syntax: TABLE <table_name> VERSION AS OF <version_number>
#    Also works with: TABLE <table_name> TIMESTAMP AS OF '<timestamp>'
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── Time Travel: version 1 (initial data) ──────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo VERSION AS OF 1
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Price'}")
print(f"    {'--':<4} {'-'*20} {'-'*10}")
for pid, name, price in rows:
    print(f"    {pid:<4} {name:<20} ${price:,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. DESCRIBE HISTORY — the "git log" of your Delta table
#    Shows every commit: version, timestamp, operation, user, and parameters.
#    This is your audit trail — who changed what and when.
#
#    Key columns:
#      version          — monotonically increasing commit number
#      timestamp        — when the commit happened
#      operation        — CREATE, UPDATE, DELETE, MERGE, RESTORE, etc.
#      operationParameters — details about what was changed
#      userName         — who ran the command (if available)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── DESCRIBE HISTORY ───────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        DESCRIBE HISTORY {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
    """)
    rows = cur.fetchall()

# DESCRIBE HISTORY returns many columns — we show the key ones
# Columns: version, timestamp, userId, userName, operation, operationParameters, ...
print(f"    {'Ver':<5} {'Timestamp':<28} {'Operation':<25}")
print(f"    {'---':<5} {'-'*28} {'-'*25}")
for row in rows:
    version = row[0]
    timestamp = row[1]
    operation = row[4] if len(row) > 4 else "unknown"
    # Truncate timestamp for display
    ts_str = str(timestamp)[:27] if timestamp else "unknown"
    print(f"    {version:<5} {ts_str:<28} {operation:<25}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. RESTORE — roll back to a previous version
#    This is the "undo" button for your data.
#    RESTORE creates a NEW commit that reverts the table to the target version.
#    It does NOT delete history — it adds to it.
#
#    After RESTORE:
#      - The table looks exactly like it did at the target version.
#      - You can still Time Travel to versions AFTER the restore point.
#      - The RESTORE itself appears in DESCRIBE HISTORY.
#
#    Use cases:
#      - Accidental DELETE or UPDATE → restore to before the mistake
#      - Bad data pipeline run → restore to the last known-good version
#      - Compliance requirement → show the table as of a specific date
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── RESTORE to version 1 ───────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        RESTORE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        TO VERSION AS OF 1
    """)
    print("    Table restored to version 1.")

print("\n  ── After RESTORE ──────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT product_id, product_name, price
        FROM   {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo
        ORDER  BY product_id
    """)
    rows = cur.fetchall()

print(f"    {'ID':<4} {'Name':<20} {'Price'}")
print(f"    {'--':<4} {'-'*20} {'-'*10}")
for pid, name, price in rows:
    print(f"    {pid:<4} {name:<20} ${price:,.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. VACUUM — clean up old data files
#    WARNING: After VACUUM, you CANNOT Time Travel past the vacuum point.
#    Only VACUUM when you're sure you don't need older versions.
#
#    Default retention: 168 hours (7 days).
#    You can set a shorter retention, but NEVER 0 in production.
#
#    VACUUM DRY RUN shows what would be deleted without actually deleting.
#    Always run DRY RUN first in production!
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── VACUUM DRY RUN (what would be cleaned) ─────")
with conn.cursor() as cur:
    # Databricks requires min 168 hours (7 days) retention by default.
    # Setting it to 0 requires disabling the safety check.
    # For this demo, we use 168 hours to show the safe pattern.
    try:
        cur.execute(f"""
            VACUUM {LAB_CATALOG}.{LAB_SCHEMA}.time_travel_demo RETAIN 168 HOURS DRY RUN
        """)
        rows = cur.fetchall()
        if rows:
            print(f"    {len(rows)} old file(s) would be removed")
            for (path,) in rows[:3]:
                print(f"      {path}")
            if len(rows) > 3:
                print(f"      ... and {len(rows) - 3} more")
        else:
            print("    No old files to clean (table is too new)")
    except Exception as e:
        print(f"    VACUUM not available: {str(e)[:80]}")

print("\n  Note: Time Travel is one of Delta's most powerful features.")
print("        Use it for auditing, debugging, and disaster recovery.")
print("        NEVER VACUUM with 0-hour retention in production!")

conn.close()
print()
