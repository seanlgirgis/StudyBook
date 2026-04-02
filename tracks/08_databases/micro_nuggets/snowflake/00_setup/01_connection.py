"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-01 · Basic Connection                                             ║
║  The minimal pattern every other nugget builds on.                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Opens a Snowflake connection, runs one query, closes the connection.
This is the smallest possible working program — learn this shape first.

CONCEPTS
────────
snowflake.connector.connect()
  - Creates an authenticated session over HTTPS (port 443).
  - Returns a SnowflakeConnection object.
  - Key parameters:
      account   — your Snowflake account identifier
                  Format: <org>-<account>  (e.g. "myorg-myaccount")
                  or legacy: <account>.<region>.<cloud>
      user      — your Snowflake username (not email)
      password  — plaintext password (or use key-pair auth in production)
      warehouse — compute cluster that will process your queries
      database  — default database for unqualified table names
      schema    — default schema within that database

Warehouse (Virtual Warehouse):
  - Snowflake separates STORAGE from COMPUTE.
  - A warehouse is a cluster of cloud VMs that executes queries.
  - It auto-suspends when idle (no cost while suspended!).
  - Auto-resumes the moment you send a query.
  - Size: XS / S / M / L / XL / 2XL / 3XL / 4XL  (doubles credits per size)
  - A DE typically uses XS for development, S-M for production loads.

cursor:
  - A Cursor is your interface to execute SQL and fetch results.
  - Always use `with conn.cursor() as cur:` — auto-closes on exit.
  - cur.description  → list of Column objects (name, type, precision …)
  - cur.fetchone()   → one row as a tuple
  - cur.fetchall()   → all rows as list of tuples
  - cur.fetchmany(n) → n rows at a time (memory-friendly for large results)

Connection lifecycle — important for credit management:
  - Open connection    → warehouse auto-resumes   (credits start ticking)
  - Close connection   → warehouse stays running  (credits continue!)
  - Warehouse auto-suspends after its AUTO_SUSPEND timeout (default 600s)
  - Always close connections you no longer need.
  - For scripts: open → query → close. Don't hold connections open.

USAGE
─────
    python 01_connection.py

EXPECTED OUTPUT
───────────────
    ── Snowflake Session ────────────────────────
      ACCOUNT              MYORG-MYACCOUNT
      USER                 JOHN_DOE
      ROLE                 SYSADMIN
      WAREHOUSE            COMPUTE_WH
      DATABASE             DEMO_DB
      SCHEMA               PUBLIC
      REGION               AWS_US_EAST_1

    Connection closed cleanly.
"""
from __future__ import annotations

import sys
from pathlib import Path

# ── Path setup — same two lines at the top of every nugget ───────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

# ─────────────────────────────────────────────────────────────────────────────
# Open the connection
# _sf_connect.get_connection() reads credentials from env vars / .env.local
# and calls snowflake.connector.connect() for you.
# ─────────────────────────────────────────────────────────────────────────────
conn = get_connection()

# ─────────────────────────────────────────────────────────────────────────────
# CURRENT_* functions
# These are Snowflake session functions — they return what is active
# for THIS connection at THIS moment.  Useful for debugging "which env
# am I actually connected to?" in scripts that run across environments.
#
#   CURRENT_ACCOUNT()   → account locator (the short internal name)
#   CURRENT_USER()      → logged-in user
#   CURRENT_ROLE()      → active role (determines what you can see/do)
#   CURRENT_WAREHOUSE() → active compute warehouse
#   CURRENT_DATABASE()  → active database
#   CURRENT_SCHEMA()    → active schema
#   CURRENT_REGION()    → cloud+region (e.g. AWS_US_EAST_1)
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("""
        SELECT
            CURRENT_ACCOUNT()   AS account,
            CURRENT_USER()      AS user,
            CURRENT_ROLE()      AS role,
            CURRENT_WAREHOUSE() AS warehouse,
            CURRENT_DATABASE()  AS database,
            CURRENT_SCHEMA()    AS schema,
            CURRENT_REGION()    AS region
    """)

    # cur.description is a list of ResultMetadata objects.
    # [0] is the column name attribute.
    cols = [d[0] for d in cur.description]
    row  = cur.fetchone()   # only one row expected

# Always close — don't leak sessions.
# In production code, prefer: `with snowflake.connector.connect(...) as conn:`
conn.close()

# ─────────────────────────────────────────────────────────────────────────────
# Display results
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Snowflake Session ────────────────────────")
for col, val in zip(cols, row):
    print(f"  {col:<20} {val}")

print("\n  Connection closed cleanly.")
print()
