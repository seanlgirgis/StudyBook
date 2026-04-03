"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Basic Connection                                             ║
║  The minimal pattern every other nugget builds on.                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Opens a Databricks connection, runs one query, closes the connection.
This is the smallest possible working program — learn this shape first.

CONCEPTS
────────
databricks.sql.connect()
  - Creates an authenticated session over HTTPS (port 443).
  - Returns a Connection object implementing Python DB-API 2.0 (PEP 249).
  - Key parameters:
      server_hostname — your workspace host (without https://)
                        e.g. "dbc-xxxx.cloud.databricks.com"
      access_token    — your Personal Access Token (PAT)
                        Starts with "dapi", long-lived, user-scoped
      http_path       — path to the SQL Warehouse endpoint
                        Format: /sql/1.0/warehouses/<warehouse_id>
                        Found in: SQL Warehouses → Connection Details
      catalog         — Unity Catalog catalog name (default: "hive_metastore")
      schema          — schema within that catalog (default: "default")

SQL Warehouse (Compute Engine):
  - Databricks separates STORAGE from COMPUTE (like Snowflake).
  - A SQL Warehouse is a serverless or provisioned compute cluster.
  - Serverless: auto-scales, pay-per-use, no management (recommended for dev)
  - Provisioned: fixed size, predictable cost, faster cold-start
  - Auto-suspends when idle (serverless) or after timeout (provisioned)
  - Auto-resumes the moment you send a query.

Cursor (DB-API 2.0):
  - A Cursor is your interface to execute SQL and fetch results.
  - Always use `with conn.cursor() as cur:` — auto-closes on exit.
  - cur.description  → list of tuples: (name, type_code, display_size, ...)
  - cur.fetchone()   → one row as a tuple
  - cur.fetchall()   → all rows as list of tuples
  - cur.fetchmany(n) → n rows at a time (memory-friendly for large results)

Unity Catalog:
  - Databricks' unified governance layer for data, AI, and analytics.
  - 3-level namespace: catalog.schema.table  (like database.schema.table)
  - Replaces the older hive_metastore as the recommended catalog.
  - Supports fine-grained access control (row/column level).
  - Every Databricks workspace now ships with a default "main" catalog.

Connection lifecycle — important for cost management:
  - Open connection    → warehouse auto-resumes   (compute starts billing)
  - Close connection   → warehouse may auto-suspend (billing stops)
  - For scripts: open → query → close. Don't hold connections open.
  - Unlike Snowflake, Databricks SQL Warehouse cold-start takes 30-60s.

USAGE
─────
    python 01_connection.py

EXPECTED OUTPUT
───────────────
    ── Databricks Session ─────────────────────────
      CATALOG              nugget_lab
      SCHEMA               default
      CURRENT_USER()       john.doe@company.com
      CURRENT_CATALOG()    nugget_lab
      CURRENT_SCHEMA()     default
      VERSION()            3.5.0

    Connection closed cleanly.
"""
from __future__ import annotations

import sys
from pathlib import Path

# ── Path setup — same two lines at the top of every nugget ───────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection

# ─────────────────────────────────────────────────────────────────────────────
# Open the connection
# _db_connect.get_connection() reads credentials from env vars / encrypted secrets
# and calls databricks.sql.connect() for you.
# By default, connects to LAB_CATALOG (nugget_lab) / LAB_SCHEMA (default).
# ─────────────────────────────────────────────────────────────────────────────
conn = get_connection()

# ─────────────────────────────────────────────────────────────────────────────
# CURRENT_* functions
# These are Databricks SQL session functions — they return what is active
# for THIS connection at THIS moment.  Useful for debugging "which env
# am I actually connected to?" in scripts that run across environments.
#
#   CURRENT_USER()      → logged-in user email
#   CURRENT_CATALOG()   → active Unity Catalog catalog
#   CURRENT_SCHEMA()    → active schema within that catalog
#   CURRENT_DATABASE()  → alias for CURRENT_SCHEMA() (legacy name)
#   VERSION()           → Databricks Runtime version (e.g. 3.5.0)
#
# Note: Databricks does NOT have CURRENT_ACCOUNT() or CURRENT_WAREHOUSE()
# as SQL functions — those are accessed via the REST API instead.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("""
        SELECT
            CURRENT_USER()      AS current_user,
            CURRENT_CATALOG()   AS current_catalog,
            CURRENT_SCHEMA()    AS current_schema,
            VERSION()           AS version
    """)

    # cur.description is a list of tuples.
    # [0] is the column name.
    cols = [d[0] for d in cur.description]
    row  = cur.fetchone()   # only one row expected

# Always close — don't leak sessions.
# In production code, prefer: `with databricks.sql.connect(...) as conn:`
conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# Display results
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Databricks Session ─────────────────────────")
for col, val in zip(cols, row):
    print(f"  {col:<20} {val}")

print("\n  Connection closed cleanly.")
print()
