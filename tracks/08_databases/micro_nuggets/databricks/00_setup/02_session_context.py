"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-02 · Session Context & USE Commands                               ║
║  How to switch catalogs, schemas, and inspect your workspace.                ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Demonstrates the USE commands that control your session context and
shows how to list available catalogs and schemas.

CONCEPTS
────────
USE CATALOG <name>:
  - Switches the active catalog for the current session.
  - Like Snowflake's USE DATABASE.
  - Does NOT persist across connections — each connection starts fresh.

USE SCHEMA <name>:
  - Switches the active schema within the current catalog.
  - Like Snowflake's USE SCHEMA.
  - Can also use: USE <catalog>.<schema>  (switches both at once)

SHOW CATALOGS:
  - Lists all Unity Catalog catalogs visible to your user.
  - Common catalogs:
      main          — default catalog, contains system objects
      samples       — sample datasets (provided by Databricks)
      hive_metastore — legacy metastore (pre-Unity Catalog)
      <custom>      — catalogs you create for your org

SHOW SCHEMAS:
  - Lists all schemas in the active catalog.
  - Like Snowflake's SHOW SCHEMAS.
  - Returns schemas you have permission to see (RBAC-filtered).

DESCRIBE CATALOG <name>:
  - Shows metadata about a catalog: name, comment, location, owner.
  - Useful for understanding data governance and ownership.

Workspace vs. Catalog:
  - A Databricks Workspace is your entire tenant (like a Snowflake account).
  - A Catalog is a top-level data namespace within that workspace.
  - Think of it like: Workspace → Catalog → Schema → Table
  - This is different from Snowflake: Account → Organization → Database → Schema → Table

USAGE
─────
    python 02_session_context.py

EXPECTED OUTPUT
───────────────
    ── Session Context ──────────────────────────────

      Current catalog: main
      Current schema:  default

      ── Available Catalogs ─────────────────────────
        main
        samples
        hive_metastore

      ── Schemas in 'main' catalog ──────────────────
        INFORMATION_SCHEMA
        default

      ── DESCRIBE CATALOG main ──────────────────────
        catalog_name    main
        comment         Main catalog
        location        None
        owner           account users
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection

conn = get_connection()

print("\n── Session Context ──────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Show current catalog and schema
#    These are set by _db_connect.get_connection() to LAB_CATALOG/LAB_SCHEMA.
#    If you connect without specifying catalog/schema, you get the defaults
#    from your SQL Warehouse configuration.
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("SELECT CURRENT_CATALOG(), CURRENT_SCHEMA()")
    current_catalog, current_schema = cur.fetchone()

print(f"\n  Current catalog: {current_catalog or '(none)'}")
print(f"  Current schema:  {current_schema or '(none)'}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. List all available catalogs
#    SHOW CATALOGS is a Databricks-specific command (not standard SQL).
#    It returns all catalogs your user has USE_CATALOG permission on.
#    If you don't see a catalog, you either lack permission or it doesn't exist.
#
#    In Unity Catalog, permissions are hierarchical:
#      Metastore Admin → creates catalogs → assigns catalog owners
#      Catalog Owner   → creates schemas  → assigns schema owners
#      Schema Owner    → creates tables   → assigns table owners
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Available Catalogs ─────────────────────────")
with conn.cursor() as cur:
    cur.execute("SHOW CATALOGS")
    catalogs = cur.fetchall()

for (cat_name,) in catalogs:
    print(f"    {cat_name}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. List schemas in the current catalog
#    SHOW SCHEMAS returns schemas in the ACTIVE catalog (set by USE CATALOG).
#    Every catalog has an INFORMATION_SCHEMA (read-only metadata views).
#    The "default" schema is created automatically with each catalog.
#
#    INFORMATION_SCHEMA in Databricks:
#      - Contains views like TABLES, COLUMNS, SCHEMATA (similar to Snowflake)
#      - But fewer views than Snowflake — Databricks prefers REST API for admin
#      - Key views: TABLES, COLUMNS, VIEWS
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Schemas in '{current_catalog}' catalog ──────────────────")
with conn.cursor() as cur:
    cur.execute("SHOW SCHEMAS")
    schemas = cur.fetchall()

for (schema_name,) in schemas:
    print(f"    {schema_name}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. DESCRIBE CATALOG
#    Shows metadata about a specific catalog.
#    Returns key-value pairs (not columns) — unusual but standard in Databricks.
#    Key fields:
#      catalog_name  — the name
#      comment       — description (set at creation time)
#      location      — external storage location (if configured)
#      owner         — principal who owns this catalog
#
#    Note: DESCRIBE CATALOG may not be available on all workspace editions.
#    If it fails, we fall back to SHOW CREATE CATALOG.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── DESCRIBE CATALOG {current_catalog} ──────────────────────")
with conn.cursor() as cur:
    try:
        cur.execute(f"DESCRIBE CATALOG {current_catalog}")
        rows = cur.fetchall()
        for key, value in rows:
            print(f"    {key:<16} {value}")
    except Exception as e:
        print(f"    DESCRIBE CATALOG not available on this workspace.")
        print(f"    ({e})")
        # Fallback: show what we know from SHOW CATALOGS
        print(f"    Catalog '{current_catalog}' is available and accessible.")

conn.close()
print()
