"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 01-01 · Create Catalog & Schema                                      ║
║  Understanding Databricks' logical namespace hierarchy.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates a demo catalog and schema, inspects the namespace, then explores
what lives inside INFORMATION_SCHEMA — the built-in metadata view.

CONCEPTS
────────
Why separate catalogs?
  - Each catalog is a completely isolated storage namespace.
  - You can share catalogs across workspaces (Unity Catalog sharing).
  - Typical setup:
      PROD        — production data
      DEV         — developer sandboxes
      RAW         — raw ingested data (sometimes separate for cost tracking)
      ANALYTICS   — transformed models for BI

Why separate schemas within a catalog?
  - Group related objects (tables, views, functions).
  - Assign different RBAC permissions per schema.
  - Reflect pipeline layers:
      bronze       — data as received, no transforms (aka "raw")
      silver       — typed, cleaned, deduplicated (aka "staging")
      gold         — aggregated models for BI (aka "analytics")
      mart_sales   — topic-specific data mart

CREATE CATALOG IF NOT EXISTS:
  - Making DDL idempotent is a best practice — scripts should be re-runnable.
  - Always use CREATE ... IF NOT EXISTS for CREATE
  - Always use DROP ... IF EXISTS for DROP
  - Requires CREATE_CATALOG privilege on the metastore.

COMMENT clause:
  - First-class metadata in Databricks — stored, queryable, shows in UI.
  - A professional DE documents objects with COMMENT.
  - Readable via INFORMATION_SCHEMA.SCHEMATA.COMMENT
  - Also shown in the Databricks Unity Catalog UI.

INFORMATION_SCHEMA:
  - A read-only schema that exists inside EVERY catalog.
  - Contains views exposing metadata about that catalog's objects.
  - Standard SQL (ISO/IEC 9075) — same concept in Postgres, SQL Server, Snowflake.
  - Key views:
      TABLES            — all tables & views in this catalog
      COLUMNS           — all columns with type info
      SCHEMATA          — schemas in this catalog  ← used below

USAGE
─────
    python 01_create_catalog_schema.py

EXPECTED OUTPUT
───────────────
    ── Catalogs & Schemas ─────────────────────────

      Current catalog: main

      Creating NUGGET_LAB catalog ... done.
      Creating NUGGET_SCHEMA schema ... done.

      ── Schemas in NUGGET_LAB ──────────────────────────────
        SCHEMA                         COMMENT
        ------------------------------ --------------------
        INFORMATION_SCHEMA
        default
        NUGGET_SCHEMA                  Demo schema for micro-nuggets

      ── INFORMATION_SCHEMA tables (sample) ──────────────
        TABLE_NAME                     TABLE_TYPE
        ------------------------------ ----------
        COLUMNS                        VIEW
        SCHEMATA                       VIEW
        TABLES                         VIEW
        ...
        (3 rows total in INFORMATION_SCHEMA)

      Note: NUGGET_LAB.NUGGET_SCHEMA persists for later nuggets.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_SCHEMA

# The catalog we create in this nugget — separate from the default LAB_CATALOG.
# This gives you a dedicated study catalog while keeping 'workspace' as the default.
TARGET_CATALOG = "nugget_lab"

# ─────────────────────────────────────────────────────────────────────────────
# Bootstrap connection — connects without catalog/schema so we can CREATE.
# Normal nuggets use get_connection() which targets LAB_CATALOG/LAB_SCHEMA.
# But we need to CREATE the catalog first, so we connect at metastore level.
# ─────────────────────────────────────────────────────────────────────────────
conn = get_connection(_bootstrap=True)

print("\n── Catalogs & Schemas ─────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Show current catalog (should be none/default in bootstrap mode)
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("SELECT CURRENT_CATALOG()")
    row = cur.fetchone()
    current_catalog = row[0] if row else "(none)"
print(f"\n  Current catalog: {current_catalog}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create the demo catalog
#    CREATE CATALOG IF NOT EXISTS is idempotent — safe to run multiple times.
#    Requires metastore-level CREATE_CATALOG privilege.
#    If you get a permission error, ask your admin to grant you:
#      GRANT CREATE CATALOG ON METASTORE TO `<your-user>`;
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Creating {TARGET_CATALOG} catalog ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute(f"CREATE CATALOG IF NOT EXISTS {TARGET_CATALOG}")
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Create the demo schema inside our catalog
#    Now that the catalog exists, we can create a schema inside it.
#    USE CATALOG switches the session context — subsequent unqualified
#    CREATE SCHEMA commands will target this catalog.
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Creating {LAB_SCHEMA} schema ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute(f"USE CATALOG {TARGET_CATALOG}")
    cur.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {LAB_SCHEMA}
        COMMENT 'Default schema for micro-nuggets'
    """)
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Create an additional schema to demonstrate multi-schema support
#    This schema will be used in later nuggets for table creation.
# ─────────────────────────────────────────────────────────────────────────────
print(f"  Creating demo_schema schema ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE SCHEMA IF NOT EXISTS demo_schema
        COMMENT 'Demo schema for DDL and DML nuggets'
    """)
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. List all schemas via INFORMATION_SCHEMA.SCHEMATA
#    This is the SQL-standard way (vs SHOW SCHEMAS which is Databricks-specific).
#    Prefer INFORMATION_SCHEMA for scripts — it returns a normal result set
#    you can filter/join like any table.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Schemas in {TARGET_CATALOG} ──────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT schema_name, comment
        FROM   {TARGET_CATALOG}.information_schema.schemata
        ORDER  BY schema_name
    """)
    rows = cur.fetchall()

print(f"    {'SCHEMA':<30} COMMENT")
print(f"    {'-'*30} {'-'*20}")
for schema_name, comment in rows:
    print(f"    {schema_name:<30} {comment or ''}")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Peek inside INFORMATION_SCHEMA itself
#    INFORMATION_SCHEMA contains views, not base tables. Each view surfaces a
#    different category of metadata. Knowing what's there saves a lot of
#    Googling during real DE work.
#
#    Note: Databricks INFORMATION_SCHEMA has fewer views than Snowflake.
#    For advanced metadata (lineage, permissions), use the Unity Catalog
#    REST API: GET /api/2.1/unity-catalog/tables
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── INFORMATION_SCHEMA tables ─────────────────────")
with conn.cursor() as cur:
    cur.execute(f"""
        SELECT table_name, table_type
        FROM   {TARGET_CATALOG}.information_schema.tables
        WHERE  table_schema = 'INFORMATION_SCHEMA'
        ORDER  BY table_name
    """)
    rows = cur.fetchall()

if rows:
    print(f"    {'TABLE_NAME':<30} TABLE_TYPE")
    print(f"    {'-'*30} ----------")
    for table_name, table_type in rows:
        print(f"    {table_name:<30} {table_type}")
    print(f"    ({len(rows)} rows total in INFORMATION_SCHEMA)")
else:
    print("    (empty — INFORMATION_SCHEMA populates once tables are created)")
    print("    This is normal for Databricks on a fresh catalog.")

conn.close()
print(f"\n  Note: {TARGET_CATALOG}.{LAB_SCHEMA} persists for later nuggets.")
print(f"        To use it, change LAB_CATALOG in _db_connect.py to '{TARGET_CATALOG}'.")
print()
