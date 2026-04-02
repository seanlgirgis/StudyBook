"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Databases & Schemas                                          ║
║  Understanding and creating Snowflake's logical namespace.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates a demo schema, inspects the namespace, then explores what lives
inside INFORMATION_SCHEMA — the built-in metadata view every DE needs.

CONCEPTS
────────
Why separate databases?
  - Each database is a completely isolated storage namespace.
  - You can share a database across accounts (Data Sharing feature).
  - Typical setup:
      PROD_DB     — production data
      DEV_DB      — developer sandboxes
      RAW_DB      — raw ingested data (sometimes a separate DB for cost tracking)

Why separate schemas within a database?
  - Group related objects (tables, views, stages, tasks …).
  - Assign different RBAC permissions per schema.
  - Reflect pipeline layers:
      RAW        — data as received, no transforms
      STAGING    — typed, cleaned, deduplicated
      ANALYTICS  — aggregated models for BI
      MART_SALES — topic-specific data mart

IF NOT EXISTS:
  - Making DDL idempotent is a best practice — scripts should be re-runnable.
  - Always use CREATE ... IF NOT EXISTS for CREATE
  - Always use DROP ... IF EXISTS for DROP

COMMENT clause:
  - First-class metadata in Snowflake — stored, queryable, shows in UI.
  - A professional DE documents objects with COMMENT.
  - Readable via INFORMATION_SCHEMA.SCHEMATA.COMMENT
  - Also shown in the Snowsight web UI.

INFORMATION_SCHEMA:
  - A read-only schema that exists inside EVERY database.
  - Contains views exposing metadata about that database's objects.
  - Standard SQL (ISO/IEC 9075) — same concept in Postgres, SQL Server.
  - Key views:
      TABLES            — all tables & views in this database
      COLUMNS           — all columns with type info
      TABLE_STORAGE_METRICS — storage bytes (active / time-travel / fail-safe)
      STAGES            — internal and external stages
      FUNCTIONS         — UDFs
      SCHEMATA          — schemas in this database  ← used below

USAGE
─────
    python 01_create_db_schema.py

EXPECTED OUTPUT
───────────────
    ── Databases & Schemas ──────────────────────

      Current database: DEMO_DB

      Creating NUGGET_SCHEMA ... done.

      ── Schemas in DEMO_DB ──────────────────────────────
        SCHEMA                         OWNER                COMMENT
        ------------------------------ -------------------- --------------------
        INFORMATION_SCHEMA             SYSADMIN
        PUBLIC                         SYSADMIN
        NUGGET_SCHEMA                  SYSADMIN             Demo schema for micro-nuggets

      ── INFORMATION_SCHEMA tables (sample) ──────────────
        TABLE_NAME                     TABLE_TYPE
        ------------------------------ ----------
        APPLICABLE_ROLES               VIEW
        COLUMNS                        VIEW
        DATABASES                      VIEW
        ...
        (26 rows total in INFORMATION_SCHEMA)

      Note: NUGGET_SCHEMA persists for later nuggets.
            Run 00_setup/99_reset_lab.py to clean up.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── Databases & Schemas ──────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Show current database
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("SELECT CURRENT_DATABASE()")
    current_db = cur.fetchone()[0]
print(f"\n  Current database: {current_db}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create a demo schema
#    CREATE SCHEMA IF NOT EXISTS is idempotent — safe to run multiple times.
#    The COMMENT is stored in metadata and visible in Snowsight UI and
#    INFORMATION_SCHEMA.SCHEMATA.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Creating NUGGET_SCHEMA ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS NUGGET_SCHEMA
        COMMENT = 'Demo schema for micro-nuggets'
    """)
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. List all schemas via INFORMATION_SCHEMA.SCHEMATA
#    This is the SQL-standard way (vs SHOW SCHEMAS which is Snowflake-specific).
#    Prefer INFORMATION_SCHEMA for scripts — it returns a normal result set
#    you can filter/join like any table.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Schemas in {current_db} ──────────────────────────────")
with conn.cursor() as cur:
    cur.execute("""
        SELECT schema_name, schema_owner, comment
        FROM   information_schema.schemata
        ORDER  BY schema_name
    """)
    rows = cur.fetchall()

print(f"    {'SCHEMA':<30} {'OWNER':<20} COMMENT")
print(f"    {'-'*30} {'-'*20} {'-'*20}")
for schema_name, owner, comment in rows:
    print(f"    {schema_name:<30} {(owner or ''):<20} {comment or ''}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Peek inside INFORMATION_SCHEMA itself
#    INFORMATION_SCHEMA contains views, not base tables. Each view surfaces a
#    different category of metadata. Knowing what's there saves a lot of
#    Googling during real DE work.
# ─────────────────────────────────────────────────────────────────────────────
print("\n  ── INFORMATION_SCHEMA tables (sample) ──────────────")
with conn.cursor() as cur:
    cur.execute("""
        SELECT table_name, table_type
        FROM   information_schema.tables
        WHERE  table_schema = 'INFORMATION_SCHEMA'
        ORDER  BY table_name
        LIMIT  10
    """)
    rows = cur.fetchall()
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE  table_schema = 'INFORMATION_SCHEMA'
    """)
    total = cur.fetchone()[0]

print(f"    {'TABLE_NAME':<30} TABLE_TYPE")
print(f"    {'-'*30} ----------")
for table_name, table_type in rows:
    print(f"    {table_name:<30} {table_type}")
print(f"    ... ({total} rows total in INFORMATION_SCHEMA)")

conn.close()
print("\n  Note: NUGGET_SCHEMA persists for later nuggets.")
print("        Run 00_setup/99_reset_lab.py to clean up.\n")
