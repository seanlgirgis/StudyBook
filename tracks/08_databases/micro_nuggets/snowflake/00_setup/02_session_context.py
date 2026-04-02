"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-02 · Session Context & USE Commands                               ║
║  How Snowflake's 4-level namespace works and how to navigate it.             ║
╚════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Shows how to read and change the active context (warehouse / database / schema)
within a live session without reconnecting.

CONCEPTS
────────
Snowflake's Namespace Hierarchy
  ACCOUNT
    └── DATABASE          ← isolated storage container (think: a "project")
          └── SCHEMA      ← groups related objects (think: a "folder")
                └── TABLE | VIEW | STAGE | STREAM | TASK | ...

Fully qualified object name:
    database.schema.table       (3-part)
    schema.table                (2-part — uses active database)
    table                       (1-part — uses active database + schema)

A DE usually has:
    RAW        schema — data exactly as received from sources
    STAGING    schema — cleaned / typed / deduplicated
    ANALYTICS  schema — aggregated models, ready for BI tools

USE commands — switch context mid-session:
    USE DATABASE my_db;
    USE SCHEMA   my_db.my_schema;
    USE WAREHOUSE COMPUTE_WH_LARGE;   ← switch to bigger compute on the fly!
    USE ROLE     TRANSFORMER;

Why switch context in code?
  - A single pipeline may write to RAW schema, read from STAGING,
    then write to ANALYTICS — all in one Python script.
  - You can upsize your warehouse before a heavy load and downsize after.
  - Role switching lets one script act as LOADER then TRANSFORMER.

SHOW commands:
  - SHOW WAREHOUSES  → list all warehouses your role can see
  - SHOW DATABASES   → list all databases you have USAGE on
  - SHOW SCHEMAS     → list schemas in the active database
  - SHOW TABLES      → list tables in the active schema
  Results come back as rows you can fetch with the cursor,
  but column names are fixed by Snowflake (not your aliases).

USAGE
─────
    python 02_session_context.py

EXPECTED OUTPUT
───────────────
    ── Session Context Demo ─────────────────────

      [initial context]
        warehouse = COMPUTE_WH
        database  = DEMO_DB
        schema    = PUBLIC

      [after USE SCHEMA INFORMATION_SCHEMA]
        warehouse = COMPUTE_WH
        database  = DEMO_DB
        schema    = INFORMATION_SCHEMA

      [restored to original]
        warehouse = COMPUTE_WH
        database  = DEMO_DB
        schema    = PUBLIC

    ── Warehouses visible to your role ──────────
      COMPUTE_WH                     size=X-Small  state=STARTED
      LOAD_WH                        size=Small    state=SUSPENDED

    ── Schemas in DEMO_DB ────────────────────────
      INFORMATION_SCHEMA             owner=SYSADMIN
      PUBLIC                         owner=SYSADMIN
      NUGGET_SCHEMA                  owner=SYSADMIN   (comment: Demo schema)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection, LAB_DB, LAB_SCHEMA

# get_connection() always targets NUGGET_LAB (created by 00_bootstrap.py)
conn = get_connection()

# Read the actual active database/schema from the live session — never assume
# the credentials value matches what Snowflake accepted at connect time.
with conn.cursor() as _ctx:
    _ctx.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
    _cur_db, _cur_schema = _ctx.fetchone()

orig_db     = _cur_db     or LAB_DB
orig_schema = _cur_schema or LAB_SCHEMA


def show_context(label: str) -> None:
    """Query and print the three most important context values."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
        )
        wh, db, schema = cur.fetchone()
    print(f"\n  [{label}]")
    print(f"    warehouse = {wh}")
    print(f"    database  = {db}")
    print(f"    schema    = {schema}")


print("\n── Session Context Demo ─────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Initial context — set by the connection parameters
# ─────────────────────────────────────────────────────────────────────────────
show_context("initial context")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Switch schema with USE
#
#    INFORMATION_SCHEMA is a special read-only schema that exists in EVERY
#    Snowflake database. It contains views like:
#      TABLES, COLUMNS, TABLE_STORAGE_METRICS, QUERY_HISTORY, STAGES …
#    It's the SQL standard way to inspect metadata.
#    (Snowflake also has ACCOUNT_USAGE in the SNOWFLAKE database — covered
#    in nugget 10 — which has broader, account-wide history.)
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f'USE DATABASE "{orig_db}"')
    cur.execute("USE SCHEMA INFORMATION_SCHEMA")

show_context("after USE SCHEMA INFORMATION_SCHEMA")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Restore original context
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute(f'USE DATABASE "{orig_db}"')
    cur.execute(f'USE SCHEMA "{orig_schema}"')

show_context("restored to original")

# ─────────────────────────────────────────────────────────────────────────────
# 4. SHOW WAREHOUSES
#    Each row represents one virtual warehouse in the account.
#    Key columns:
#      name    — warehouse identifier
#      size    — X-Small / Small / Medium / Large / X-Large / …
#      state   — STARTED (running, billing) | SUSPENDED (idle, no cost)
#      auto_suspend — seconds of idle before auto-suspend
#      auto_resume  — TRUE means a query auto-starts it (almost always TRUE)
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Warehouses visible to your role ──────────")
with conn.cursor() as cur:
    cur.execute("SHOW WAREHOUSES")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()

name_idx  = cols.index("name")
size_idx  = cols.index("size")
state_idx = cols.index("state")

for row in rows:
    print(
        f"  {row[name_idx]:<30} "
        f"size={row[size_idx]:<10} "
        f"state={row[state_idx]}"
    )

# ─────────────────────────────────────────────────────────────────────────────
# 5. SHOW SCHEMAS — list schemas in the active database
#    Useful to see your pipeline layers (raw / staging / analytics) at a glance.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n── Schemas in {orig_db} ────────────────────────")
with conn.cursor() as cur:
    cur.execute("SHOW SCHEMAS")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()

name_idx    = cols.index("name")
owner_idx   = cols.index("owner")
comment_idx = cols.index("comment")

for row in rows:
    comment = f"  comment: {row[comment_idx]}" if row[comment_idx] else ""
    print(f"  {row[name_idx]:<30} owner={row[owner_idx]}{comment}")

conn.close()
print()
