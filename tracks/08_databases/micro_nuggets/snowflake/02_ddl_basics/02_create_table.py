"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 02-02 · CREATE TABLE & Snowflake Data Types                          ║
║  Learn the column types a Data Engineer uses every day.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates two tables that showcase Snowflake's most important data types,
then inspects their definitions via INFORMATION_SCHEMA.COLUMNS.

CONCEPTS
────────
Snowflake Data Types (the ones a DE touches most)
──────────────────────────────────────────────────
NUMBER(p, s)   — exact numeric. p=precision (total digits), s=scale (decimal places)
                 Aliases: DECIMAL, NUMERIC, INT, INTEGER, BIGINT, SMALLINT
                 Use for: IDs, counts, monetary amounts (with scale)
                 Example: NUMBER(10, 2)  →  12345678.99

FLOAT          — IEEE 754 double precision (64-bit)
                 Use for: scientific values, ML features, approximate metrics
                 Avoid for money — rounding errors! Use NUMBER(p,2) for prices.

VARCHAR(n)     — variable-length string, max n characters, absolute max 16,777,216
                 VARCHAR without a length = VARCHAR(16777216) in Snowflake
                 Use for: names, codes, free-text, URLs

BOOLEAN        — TRUE / FALSE / NULL
                 Stored as 1 bit. Accepts 'true'/'false' strings on load.

DATE           — calendar date only (no time). YYYY-MM-DD
TIMESTAMP_NTZ  — datetime with NO timezone ("NTZ" = No TimeZone).
                 Most common in data warehouses — store everything in UTC,
                 convert to local time at the reporting layer.
TIMESTAMP_TZ   — datetime WITH timezone offset embedded.
                 Use for event streams where source timezone matters.
TIMESTAMP_LTZ  — datetime stored in UTC, displayed in session local timezone.

VARIANT        — Snowflake's semi-structured type.
                 Stores JSON, XML, Avro, Parquet internally as a binary tree.
                 A single VARIANT column can hold heterogeneous documents.
                 Max 16MB per value. Queried with colon notation: col:key:nested
                 Covered in depth in nugget 05_semi_structured.

AUTOINCREMENT / IDENTITY
  - Generates a unique sequential integer per row on INSERT.
  - Syntax:  col NUMBER AUTOINCREMENT   or   col NUMBER IDENTITY(start, step)
  - In Snowflake AUTOINCREMENT is NOT guaranteed to be gapless or ordered
    under concurrent inserts — use it for uniqueness, not sequencing.
  - Equivalent to SERIAL in Postgres or AUTO_INCREMENT in MySQL.

DEFAULT
  - CURRENT_TIMESTAMP() — wall-clock time at insert (session timezone aware)
  - CURRENT_DATE()      — today's date
  - Literal values:   DEFAULT 'PENDING',  DEFAULT 0,  DEFAULT TRUE

NOT NULL
  - Snowflake enforces NOT NULL (unlike some other constraints it does enforce).
  - PRIMARY KEY implies NOT NULL.

Constraints in Snowflake (important caveat!):
  - PRIMARY KEY, UNIQUE, FOREIGN KEY are defined but NOT ENFORCED by default.
  - Snowflake trusts you to maintain referential integrity in your pipeline.
  - They serve as documentation and are used by BI tools for ERD generation.
  - NOT NULL IS enforced — it's the one exception.

TRANSIENT vs PERMANENT tables:
  - PERMANENT (default): full Time Travel (up to 90 days) + Fail-Safe (7 days)
  - TRANSIENT: Time Travel up to 1 day, NO Fail-Safe
                Lower storage cost — good for staging/temp tables.
  - TEMPORARY: exists only for the current session, then auto-drops.

USAGE
─────
    python 02_create_table.py

EXPECTED OUTPUT
───────────────
    ── CREATE TABLE & Data Types ────────────────

      Created: NUGGET_PRODUCTS
      Created: NUGGET_EMPLOYEES (transient)

      ── NUGGET_PRODUCTS columns ─────────────────────────
        COLUMN               TYPE                 NULLABLE   DEFAULT
        -------------------- -------------------- ---------- --------------------
        PRODUCT_ID           NUMBER               N          AUTOINCREMENT
        PRODUCT_NAME         TEXT                 N
        CATEGORY             TEXT                 Y
        PRICE                FLOAT                Y
        IN_STOCK             BOOLEAN              Y          TRUE
        METADATA             VARIANT              Y
        CREATED_AT           TIMESTAMP_NTZ        Y          CURRENT_TIMESTAMP()
        UPDATED_AT           TIMESTAMP_NTZ        Y

      ── NUGGET_EMPLOYEES columns (transient table) ───────
        EMPLOYEE_ID          NUMBER               N          AUTOINCREMENT
        FULL_NAME            TEXT                 N
        DEPARTMENT           TEXT                 Y
        SALARY               NUMBER               Y
        HIRE_DATE            DATE                 Y
        IS_ACTIVE            BOOLEAN              Y          TRUE

      Note: tables persist — run 99_reset_lab.py to clean up.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── CREATE TABLE & Data Types ────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # Table 1: NUGGET_PRODUCTS — permanent table with common DE types
    #
    # AUTOINCREMENT replaces manually managing sequence generators.
    # VARIANT column lets us store arbitrary JSON per product (flexible schema).
    # TIMESTAMP_NTZ is the standard for DW timestamps — always store in UTC.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NUGGET_PRODUCTS (
            product_id    NUMBER        AUTOINCREMENT PRIMARY KEY
                                        COMMENT 'Surrogate key — auto-generated',
            product_name  VARCHAR(200)  NOT NULL
                                        COMMENT 'Display name',
            category      VARCHAR(100)  COMMENT 'Product category',
            price         FLOAT         COMMENT 'List price — use NUMBER(10,2) for exact money',
            in_stock      BOOLEAN       DEFAULT TRUE,
            metadata      VARIANT       COMMENT 'Flexible JSON attributes (color, weight, tags…)',
            created_at    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
                                        COMMENT 'Row creation time — always UTC',
            updated_at    TIMESTAMP_NTZ COMMENT 'Set by pipeline on each upsert'
        )
        COMMENT = 'Demo products table — nugget 02-02'
    """)
    print("\n  Created: NUGGET_PRODUCTS")

    # ─────────────────────────────────────────────────────────────────────────
    # Table 2: NUGGET_EMPLOYEES — TRANSIENT table
    #
    # TRANSIENT = no Fail-Safe storage (saves cost for staging/temp tables).
    # Good pattern: staging tables are TRANSIENT, final tables are PERMANENT.
    # NUMBER(10, 2) for salary — exact arithmetic, never use FLOAT for money.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TRANSIENT TABLE IF NOT EXISTS NUGGET_EMPLOYEES (
            employee_id   NUMBER        AUTOINCREMENT PRIMARY KEY,
            full_name     VARCHAR(200)  NOT NULL,
            department    VARCHAR(100),
            salary        NUMBER(10, 2) COMMENT 'Exact — NOT FLOAT for monetary values',
            hire_date     DATE,
            is_active     BOOLEAN       DEFAULT TRUE
        )
        COMMENT = 'Demo employees table (TRANSIENT — no Fail-Safe) — nugget 02-02'
    """)
    print("  Created: NUGGET_EMPLOYEES (transient)")

# ─────────────────────────────────────────────────────────────────────────────
# Inspect column definitions via INFORMATION_SCHEMA.COLUMNS
# This is the SQL-standard way — works in any SQL database.
# Note: Snowflake maps all VARCHAR → 'TEXT' in data_type column.
# ─────────────────────────────────────────────────────────────────────────────
def print_columns(table_name: str, label: str) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name,
                   data_type,
                   is_nullable,
                   column_default,
                   comment
            FROM   information_schema.columns
            WHERE  table_name = %s
            ORDER  BY ordinal_position
        """, (table_name,))
        rows = cur.fetchall()

    print(f"\n  ── {label} ─────────────────────────────────────")
    print(f"    {'COLUMN':<20} {'TYPE':<20} {'NULLABLE':<10} {'DEFAULT':<20} COMMENT")
    print(f"    {'-'*20} {'-'*20} {'-'*10} {'-'*20} {'─'*20}")
    for col_name, dtype, nullable, default, comment in rows:
        null_str = "Y" if nullable == "YES" else "N"
        print(
            f"    {col_name:<20} {dtype:<20} {null_str:<10} "
            f"{(default or ''):<20} {comment or ''}"
        )


print_columns("NUGGET_PRODUCTS",  "NUGGET_PRODUCTS columns")
print_columns("NUGGET_EMPLOYEES", "NUGGET_EMPLOYEES columns (transient table)")

conn.close()
print("\n  Note: tables persist — run 99_reset_lab.py to clean up.\n")
