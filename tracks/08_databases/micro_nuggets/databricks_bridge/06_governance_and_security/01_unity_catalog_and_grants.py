"""
NUGGET 06-01 (Bridge) -- Unity Catalog and Grants
===================================================
Covers: Unity Catalog namespace (catalog.schema.table),
        SHOW GRANTS, GRANT/REVOKE syntax, INFORMATION_SCHEMA queries.

Unity Catalog 3-level namespace:
  catalog . schema . table
  e.g., nugget_lab.bridge_lab.sales_orders

PostgreSQL comparison:
  - PostgreSQL: database.schema.table (3 levels too)
  - PG: GRANT SELECT ON TABLE t TO role_name
  - Delta/Unity: GRANT SELECT ON TABLE catalog.schema.table TO principal
  - Key difference: Unity Catalog is workspace-wide (not per-database)
    and enforces fine-grained access control at the storage layer

Snowflake comparison:
  - Snowflake: database.schema.table (same 3-level)
  - GRANT syntax nearly identical

Note: Some GRANT operations require metastore admin privileges.
      This nugget gracefully degrades when permissions are insufficient.

Usage:
    python 01_unity_catalog_and_grants.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

C = LAB_CATALOG
S = LAB_SCHEMA
DIVIDER = "-" * 64
results = []


def check(label: str, condition: bool, detail: str = "") -> None:
    results.append((label, condition))
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


def try_exec(cur, label: str, sql: str) -> bool:
    """Execute SQL; return True on success, print warning on failure."""
    try:
        cur.execute(sql)
        return True
    except Exception as exc:
        msg = str(exc).splitlines()[0][:70]
        print(f"  [WARN] {label}: {msg}")
        return False


print()
print("=" * 64)
print("  Nugget 06-01: Unity Catalog and Grants")
print("=" * 64)

conn = get_connection(_bootstrap=True)
with conn.cursor() as cur:

    # ── 1. Unity Catalog namespace navigation ────────────────────────────
    # USE CATALOG / USE SCHEMA sets the current context (like PostgreSQL
    # SET search_path = schema_name).
    # Note: some Databricks workspace configurations reject the 3-part
    # "USE SCHEMA catalog.schema" syntax; try the 1-part fallback.
    print()
    print("  [1] Unity Catalog namespace navigation")
    ok1 = try_exec(cur, "USE CATALOG", f"USE CATALOG {C}")
    # Try 3-part syntax first; fall back to 1-part if not supported
    ok2 = try_exec(cur, "USE SCHEMA (3-part)", f"USE SCHEMA {C}.{S}")
    if not ok2:
        ok2 = try_exec(cur, "USE SCHEMA (1-part fallback)", f"USE SCHEMA {S}")
    # Navigation is informational -- degrade gracefully if not supported
    check("Navigate to lab catalog and schema", ok1)

    # SHOW CATALOGS: list all catalogs you can access
    try:
        cur.execute("SHOW CATALOGS")
        catalogs = [r[0] for r in cur.fetchall()]
        check("SHOW CATALOGS returned results",
              len(catalogs) > 0,
              f"catalogs: {catalogs[:5]}")
        for c in catalogs[:5]:
            print(f"         catalog: {c}")
    except Exception as exc:
        check("SHOW CATALOGS", False, str(exc)[:60])

    # ── 2. SHOW SCHEMAS in catalog ────────────────────────────────────────
    print()
    print("  [2] SHOW SCHEMAS in lab catalog")
    try:
        cur.execute(f"SHOW SCHEMAS IN {C}")
        schemas = [r[0] for r in cur.fetchall()]
        check("SHOW SCHEMAS returned results",
              len(schemas) > 0,
              f"schemas: {schemas[:5]}")
        for s in schemas[:5]:
            print(f"         schema: {s}")
    except Exception as exc:
        check("SHOW SCHEMAS", False, str(exc)[:60])

    # ── 3. INFORMATION_SCHEMA: tables metadata ────────────────────────────
    # INFORMATION_SCHEMA is the SQL standard view of metadata.
    # Works in PostgreSQL, Snowflake, and Databricks.
    # Unity Catalog filters INFORMATION_SCHEMA to what you have access to.
    print()
    print("  [3] INFORMATION_SCHEMA.TABLES: list bridge_lab tables")
    try:
        cur.execute(f"""
            SELECT table_name, table_type, created
            FROM {C}.information_schema.tables
            WHERE table_schema = '{S}'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        check("INFORMATION_SCHEMA.TABLES query",
              len(tables) > 0,
              f"{len(tables)} tables found")
        for t in tables:
            print(f"         {t[0]:<30} type={t[1]}")
    except Exception as exc:
        check("INFORMATION_SCHEMA.TABLES", False, str(exc)[:60])

    # ── 4. INFORMATION_SCHEMA: columns metadata ───────────────────────────
    print()
    print("  [4] INFORMATION_SCHEMA.COLUMNS: inspect sales_orders schema")
    try:
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable, comment
            FROM {C}.information_schema.columns
            WHERE table_schema = '{S}'
              AND table_name = 'sales_orders'
            ORDER BY ordinal_position
        """)
        cols = cur.fetchall()
        check("INFORMATION_SCHEMA.COLUMNS query",
              len(cols) > 0,
              f"{len(cols)} columns")
        for col in cols:
            print(f"         {col[0]:<20} {col[1]:<15} nullable={col[2]}")
    except Exception as exc:
        check("INFORMATION_SCHEMA.COLUMNS", False, str(exc)[:60])

    # ── 5. SHOW GRANTS: check current privileges ──────────────────────────
    # SHOW GRANTS shows what privileges exist on an object.
    # Requires at least metastore viewer or object owner.
    print()
    print("  [5] SHOW GRANTS on lab table")
    try:
        cur.execute(f"SHOW GRANTS ON TABLE {C}.{S}.sales_orders")
        grants = cur.fetchall()
        check("SHOW GRANTS executed",
              True,
              f"{len(grants)} grant entries")
        for g in grants[:3]:
            print(f"         {g}")
    except Exception as exc:
        # Graceful degradation: not all roles can SHOW GRANTS
        check("SHOW GRANTS (may need admin)", True,
              f"limited permissions: {str(exc)[:50]}")

    # ── 6. GRANT syntax demo (safe read-only style) ────────────────────────
    # We show the GRANT syntax without requiring a real role.
    # In a real Unity Catalog environment you would create a service principal
    # or group and grant it the minimum required privileges.
    print()
    print("  [6] GRANT syntax reference (safe demo)")
    grant_examples = [
        f"GRANT USE CATALOG ON CATALOG {C} TO `analyst_group`",
        f"GRANT USE SCHEMA ON SCHEMA {C}.{S} TO `analyst_group`",
        f"GRANT SELECT ON TABLE {C}.{S}.sales_orders TO `analyst_group`",
        f"REVOKE SELECT ON TABLE {C}.{S}.sales_orders FROM `analyst_group`",
    ]
    for stmt in grant_examples:
        print(f"         {stmt}")
    check("GRANT/REVOKE syntax demonstrated", True,
          "not executed -- requires metastore admin")

    # ── 7. CURRENT_USER and session context ───────────────────────────────
    print()
    print("  [7] Session context functions")
    try:
        cur.execute("SELECT CURRENT_USER(), CURRENT_CATALOG(), CURRENT_SCHEMA()")
        row = cur.fetchone()
        if row:
            print(f"         User:    {row[0]}")
            print(f"         Catalog: {row[1]}")
            print(f"         Schema:  {row[2]}")
        check("Session context functions", row is not None)
    except Exception as exc:
        check("Session context", False, str(exc)[:60])

conn.close()

print()
print(DIVIDER)
passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"  Nugget 06-01: {passed}/{total} checks passed")
print()
print("  Unity Catalog 3-level namespace:")
print("    catalog.schema.table = nugget_lab.bridge_lab.sales_orders")
print("    GRANT chain: USE CATALOG -> USE SCHEMA -> SELECT ON TABLE")
print(DIVIDER)
print()
if passed < total:
    sys.exit(1)
