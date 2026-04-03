"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-01 · Create Tables with Delta Lake                                ║
║  Understanding Databricks' default table format.                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates tables using Delta Lake format, explores column types, and
understands what makes Delta different from traditional Parquet/CSV tables.

CONCEPTS
────────
Delta Lake — the default table format in Databricks:
  - Built on top of Parquet files — but adds ACID transactions.
  - Every write is atomic — no partial writes, no corrupted reads.
  - Maintains a transaction log (_delta_log/) alongside data files.
  - Supports Time Travel — query previous versions of your data.
  - Schema enforcement — prevents bad data from breaking your pipeline.
  - Schema evolution — ALTER TABLE ADD COLUMN works without rewriting data.

Why Delta over plain Parquet?
  - Plain Parquet: fast columnar storage, but NO transactions, NO updates.
  - Delta Lake: Parquet + transaction log = full ACID + Time Travel.
  - In Databricks, CREATE TABLE creates a Delta table by default.
  - You can explicitly say: CREATE TABLE ... USING DELTA  (for clarity)

Column types in Databricks:
  - Numeric:    TINYINT, SMALLINT, INT, BIGINT, FLOAT, DOUBLE, DECIMAL(p,s)
  - String:     STRING (UTF-8), VARCHAR(n), CHAR(n)
  - Boolean:    BOOLEAN (true/false)
  - Date/Time:  DATE, TIMESTAMP (with timezone), TIMESTAMP_NTZ (no timezone)
  - Binary:     BINARY (raw bytes)
  - Complex:    ARRAY<T>, MAP<K,V>, STRUCT<field1:T1, field2:T2>
  - Semi-structured: VARIANT (like Snowflake's VARIANT — holds JSON/XML)

    NOTE: VARIANT is available in Databricks Runtime 13.3+ with Unity Catalog.
    For older runtimes, use STRING to store JSON and parse with from_json().

Table types:
  - MANAGED (default): Databricks manages both metadata AND data files.
    DROP TABLE deletes both the metadata entry AND the underlying files.
  - EXTERNAL: You manage the data files, Databricks only tracks metadata.
    DROP TABLE removes the metadata entry but leaves files untouched.
    Use EXTERNAL when data is shared across systems or you want file-level control.

COMMENT clause:
  - First-class metadata — stored in Unity Catalog, visible in UI.
  - A professional DE documents every table and column with COMMENT.
  - Readable via INFORMATION_SCHEMA.COLUMNS and DESCRIBE TABLE.

USAGE
─────
    python 01_create_table.py

EXPECTED OUTPUT
───────────────
    ── Delta Lake Tables ────────────────────────────

      Current catalog: nugget_lab
      Current schema:  default

      Creating dim_product ... done.
      Creating fact_sales ... done.

      ── Tables in nugget_lab.default ──────────────────────
        TABLE_NAME          TABLE_TYPE    COMMENT
        ------------------- ------------- --------------------
        dim_product         MANAGED       Product dimension
        fact_sales          MANAGED       Sales fact table

      ── Columns in dim_product ────────────────────────────
        COLUMN_NAME     DATA_TYPE        NULLABLE  COMMENT
        --------------- ---------------- --------- --------------------
        product_id      INT              false     Surrogate key
        product_name    STRING           false     Product display name
        category        STRING           true      Product category
        price           DECIMAL(10,2)    true      Unit price (USD)
        is_active       BOOLEAN          true      Currently sold?
        created_at      TIMESTAMP        false     Row creation time
        attributes      VARIANT          true      Extra JSON metadata

      Note: Tables persist for later nuggets.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

conn = get_connection()

print("\n── Delta Lake Tables ────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Confirm we're in the right catalog/schema
# ─────────────────────────────────────────────────────────────────────────────
with conn.cursor() as cur:
    cur.execute("SELECT CURRENT_CATALOG(), CURRENT_SCHEMA()")
    current_catalog, current_schema = cur.fetchone()

print(f"\n  Current catalog: {current_catalog}")
print(f"  Current schema:  {current_schema}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create a dimension table
#    This is a typical slowly-changing dimension table.
#    Key design choices:
#      - product_id as INT (surrogate key — not auto-increment in Delta)
#      - price as DECIMAL(10,2) — NEVER use FLOAT for money (precision loss!)
#      - attributes as VARIANT — holds arbitrary JSON for flexibility
#      - COMMENT on every column — self-documenting schema
#
#    Delta does NOT support AUTO_INCREMENT / IDENTITY columns natively.
#    For auto-generated keys, use:
#      - IDENTITY() function (Databricks Runtime 11.3+)
#      - Or generate keys in your ETL pipeline (recommended for dimensions)
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Creating dim_product ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.dim_product (
            product_id      INT             NOT NULL COMMENT 'Surrogate key',
            product_name    STRING          NOT NULL COMMENT 'Product display name',
            category        STRING                  COMMENT 'Product category',
            price           DECIMAL(10,2)           COMMENT 'Unit price (USD)',
            is_active       BOOLEAN                 COMMENT 'Currently sold?',
            created_at      TIMESTAMP       NOT NULL COMMENT 'Row creation time',
            attributes      VARIANT                 COMMENT 'Extra JSON metadata'
        )
        USING DELTA
        COMMENT 'Product dimension table'
    """)
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Create a fact table
#    Fact tables are typically larger and have foreign keys to dimensions.
#    Key design choices:
#      - sale_id as BIGINT (fact tables can have billions of rows)
#      - quantity as INT (whole numbers only)
#      - total_amount as DECIMAL(12,2) (larger precision for totals)
#      - sale_date as DATE (no time component needed for daily grain)
#      - No foreign key constraints — Databricks doesn't enforce them!
#        (Unlike Postgres/SQL Server, FKs are documentation-only in Delta)
#        Why? Because data lakes prioritize read performance over write-time checks.
#        Data quality is enforced in the ETL pipeline, not at the database level.
# ─────────────────────────────────────────────────────────────────────────────
print("  Creating fact_sales ... ", end="", flush=True)
with conn.cursor() as cur:
    cur.execute(f"""
        CREATE OR REPLACE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.fact_sales (
            sale_id         BIGINT          NOT NULL COMMENT 'Surrogate key',
            product_id      INT             NOT NULL COMMENT 'FK to dim_product',
            customer_id     INT             NOT NULL COMMENT 'FK to dim_customer',
            sale_date       DATE            NOT NULL COMMENT 'Day of sale',
            quantity        INT             NOT NULL COMMENT 'Units sold',
            total_amount    DECIMAL(12,2)           COMMENT 'Total sale amount (USD)',
            channel         STRING                  COMMENT 'Sales channel: online, retail, wholesale'
        )
        USING DELTA
        COMMENT 'Sales fact table'
    """)
print("done.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. List all tables in the schema
#    SHOW TABLES is Databricks-specific (not standard SQL).
#    Returns: namespace, tableName, isTemporary
#    isTemporary = false means the table is registered in Unity Catalog.
#    Temporary views (isTemporary = true) exist only for the session.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Tables in {LAB_CATALOG}.{LAB_SCHEMA} ──────────────────────")
with conn.cursor() as cur:
    cur.execute("SHOW TABLES")
    rows = cur.fetchall()

print(f"    {'TABLE_NAME':<20} {'TABLE_TYPE':<14} COMMENT")
print(f"    {'-'*20} {'-'*14} {'-'*20}")
for row in rows:
    # SHOW TABLES returns: (namespace, tableName, isTemporary)
    table_name = row[1]
    # Get table comment via DESCRIBE — need a fresh cursor
    with conn.cursor() as cur2:
        cur2.execute(f"DESCRIBE TABLE EXTENDED {LAB_CATALOG}.{LAB_SCHEMA}.{table_name}")
        desc_rows = cur2.fetchall()
    comment = ""
    for col_name, data_type, col_comment in desc_rows:
        if col_name == "Comment" and data_type is None:
            comment = col_comment or ""
            break
    table_type = "MANAGED"
    print(f"    {table_name:<20} {table_type:<14} {comment}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Inspect columns of dim_product
#    DESCRIBE TABLE returns column metadata as rows (not columns).
#    Each row is: (column_name, data_type, comment)
#    The last few rows are table-level metadata (not columns).
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  ── Columns in dim_product ────────────────────────────")
with conn.cursor() as cur:
    cur.execute(f"DESCRIBE TABLE {LAB_CATALOG}.{LAB_SCHEMA}.dim_product")
    rows = cur.fetchall()

print(f"    {'COLUMN_NAME':<16} {'DATA_TYPE':<17} {'NULLABLE':<10} COMMENT")
print(f"    {'-'*16} {'-'*17} {'-'*10} {'-'*20}")
for col_name, data_type, comment in rows:
    # Skip table-level metadata rows (they have None for data_type)
    if data_type is None:
        continue
    # NULLABLE is inferred from NOT NULL constraint — DESCRIBE doesn't show it directly
    # We show the data_type and comment as-is
    print(f"    {col_name:<16} {data_type:<17} {'':<10} {comment or ''}")

conn.close()
print(f"\n  Note: Tables persist for later nuggets.")
print()
