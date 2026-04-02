"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-03 · File Format Objects                                          ║
║  Define once, reuse everywhere — the right way to specify file schemas.      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates named FILE FORMAT objects for CSV, JSON, and Parquet. Demonstrates
why named formats are better than inline format specs for production pipelines,
and shows how each format type affects the COPY INTO command.

CONCEPTS
────────
What is a FILE FORMAT object?
  A reusable, named set of parsing rules for a file type.
  Stored in Snowflake like any other schema object.
  Referenced in COPY INTO, SELECT from stage, Snowpipe, etc.

  Without named format (inline — what nugget 04-02 used):
    COPY INTO t FROM @s FILE_FORMAT = (TYPE=CSV SKIP_HEADER=1 ...)

  With named format (reusable):
    CREATE FILE FORMAT my_csv_fmt TYPE=CSV SKIP_HEADER=1 ...;
    COPY INTO t FROM @s FILE_FORMAT = my_csv_fmt;   ← clean, consistent

  Benefits:
  - One place to update parsing rules → all COPY jobs pick up the change.
  - Reduces copy-paste errors across pipeline scripts.
  - Visible in INFORMATION_SCHEMA.FILE_FORMATS for auditing.

CSV FILE FORMAT options (the important ones):
  TYPE                      = CSV
  FIELD_DELIMITER           = ','      — character separating fields
  RECORD_DELIMITER          = '\n'     — character ending each row
  SKIP_HEADER               = 1        — rows to skip at top (0 = no header)
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'  — quote character for fields with commas
  NULL_IF               = ('\\N', '')  — strings treated as SQL NULL
  EMPTY_FIELD_AS_NULL       = TRUE     — empty string → NULL
  DATE_FORMAT               = 'AUTO'  — AUTO lets Snowflake detect date format
  TIMESTAMP_FORMAT          = 'AUTO'
  COMPRESSION               = 'AUTO'  — AUTO detects gzip/bz2/zstd by extension
  ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE — fail if row has wrong column count

JSON FILE FORMAT options:
  TYPE                      = JSON
  COMPRESSION               = 'AUTO'
  STRIP_OUTER_ARRAY         = TRUE  — if file is [{...},{...}], strip outer []
                                       FALSE = expect one JSON doc per line (NDJSON)
  STRIP_NULL_VALUES         = FALSE — keep null fields in the VARIANT
  IGNORE_UTF8_ERRORS        = FALSE — fail on bad encoding (recommended)

PARQUET FILE FORMAT options:
  TYPE                      = PARQUET
  COMPRESSION               = 'AUTO'  — detects SNAPPY / GZIP etc.
  BINARY_AS_TEXT            = FALSE   — keep binary columns as binary
  USE_LOGICAL_TYPE          = TRUE    — maps Parquet logical types to SQL types

ORC and AVRO are also supported with TYPE = ORC / AVRO.

Combining FILE FORMAT with STAGE:
  You can attach a FILE FORMAT directly to a STAGE definition:
    CREATE STAGE my_stage FILE_FORMAT = my_csv_fmt;
  Then COPY INTO needs no FILE_FORMAT clause — it inherits from the stage.
  Useful when one stage always receives one file type.

USAGE
─────
    python 03_file_formats.py

EXPECTED OUTPUT
───────────────
    ── File Format Objects ───────────────────────

      ── Created formats ─────────────────────────────────
        [✓] NUGGET_CSV_FORMAT    (CSV)
        [✓] NUGGET_JSON_FORMAT   (JSON)
        [✓] NUGGET_PARQUET_FORMAT (PARQUET)

      ── INFORMATION_SCHEMA.FILE_FORMATS ─────────────────
        FORMAT_NAME            TYPE     FIELD_DELIM  SKIP_HEADER  COMPRESSION
        ---------------------- -------- ------------ ------------ -----------
        NUGGET_CSV_FORMAT      CSV      ,                       1 AUTO
        NUGGET_JSON_FORMAT     JSON                                AUTO
        NUGGET_PARQUET_FORMAT  PARQUET                             AUTO

      ── Use named format in COPY INTO ───────────────────
        Re-loading with NUGGET_CSV_FORMAT ...
        Result: SKIPPED  (same file, same checksum — idempotent)

      ── Describe a format ───────────────────────────────
        Property               Value
        ---------------------- ------------------------------------------
        TYPE                   CSV
        FIELD_DELIMITER        ,
        RECORD_DELIMITER       \n
        SKIP_HEADER            1
        ...
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── File Format Objects ───────────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 1. CSV format — the most common for data ingestion from legacy systems,
    #    data exports, and simple ETL feeds.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE FILE FORMAT NUGGET_CSV_FORMAT
            TYPE                          = CSV
            FIELD_DELIMITER               = ','
            RECORD_DELIMITER              = '\\n'
            SKIP_HEADER                   = 1
            FIELD_OPTIONALLY_ENCLOSED_BY  = '"'
            NULL_IF                       = ('\\\\N', 'NULL', '')
            EMPTY_FIELD_AS_NULL           = TRUE
            DATE_FORMAT                   = 'YYYY-MM-DD'
            TIMESTAMP_FORMAT              = 'AUTO'
            COMPRESSION                   = 'AUTO'
            ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE
            COMMENT                       = 'Standard CSV with header — nugget 04-03'
    """)

    # ─────────────────────────────────────────────────────────────────────────
    # 2. JSON format — for API responses, webhook payloads, event streams.
    #    STRIP_OUTER_ARRAY = TRUE: file looks like [{...},{...}]
    #                       FALSE: NDJSON — one JSON object per line (more common
    #                              for streaming/Kafka exports)
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE FILE FORMAT NUGGET_JSON_FORMAT
            TYPE                = JSON
            STRIP_OUTER_ARRAY   = TRUE
            STRIP_NULL_VALUES   = FALSE
            IGNORE_UTF8_ERRORS  = FALSE
            COMPRESSION         = 'AUTO'
            COMMENT             = 'JSON array format (strip outer []) — nugget 04-03'
    """)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. Parquet format — columnar binary format.
    #    Used for: dbt models exported from Spark/pandas, AWS Glue outputs,
    #    Iceberg table files, large analytical datasets.
    #    USE_LOGICAL_TYPE preserves DATE/TIMESTAMP/DECIMAL semantics from Parquet
    #    metadata rather than loading everything as raw bytes.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE OR REPLACE FILE FORMAT NUGGET_PARQUET_FORMAT
            TYPE             = PARQUET
            COMPRESSION      = 'AUTO'
            BINARY_AS_TEXT   = FALSE
            USE_LOGICAL_TYPE = TRUE
            COMMENT          = 'Parquet format with logical type mapping — nugget 04-03'
    """)

    print("\n  ── Created formats ─────────────────────────────────")
    for name in ("NUGGET_CSV_FORMAT", "NUGGET_JSON_FORMAT", "NUGGET_PARQUET_FORMAT"):
        ftype = name.split("_")[1]   # CSV / JSON / PARQUET
        print(f"    [✓] {name:<25} ({ftype})")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. Inspect formats via INFORMATION_SCHEMA.FILE_FORMATS
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── INFORMATION_SCHEMA.FILE_FORMATS ─────────────────")
    cur.execute("""
        SELECT file_format_name,
               file_format_type,
               field_delimiter,
               skip_header,
               compression
        FROM   information_schema.file_formats
        WHERE  file_format_name LIKE 'NUGGET_%'
        ORDER  BY file_format_name
    """)
    rows = cur.fetchall()
    print(f"    {'FORMAT_NAME':<22}  {'TYPE':<8}  {'FIELD_DELIM':<12}  {'SKIP_HEADER':>11}  COMPRESSION")
    print(f"    {'─'*22}  {'─'*8}  {'─'*12}  {'─'*11}  {'─'*11}")
    for fname, ftype, delim, skip, comp in rows:
        print(
            f"    {fname:<22}  {str(ftype):<8}  {str(delim or ''):<12}  "
            f"{str(skip or ''):>11}  {comp or ''}"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # 5. Re-run COPY INTO using the named format (cleaner syntax)
    #    Compare this to the inline format in nugget 04-02 — same result,
    #    but now the format rules live in one reusable object.
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── Use named format in COPY INTO ───────────────────")
    cur.execute("SHOW STAGES LIKE 'NUGGET_INTERNAL_STAGE'")
    stage_exists = bool(cur.fetchone())
    cur.execute("SHOW TABLES LIKE 'NUGGET_ORDERS_STAGING'")
    table_exists = bool(cur.fetchone())

    if stage_exists and table_exists:
        cur.execute("""
            COPY INTO NUGGET_ORDERS_STAGING
            FROM        @NUGGET_INTERNAL_STAGE
            FILE_FORMAT = NUGGET_CSV_FORMAT
        """)
        copy_rows = cur.fetchall()
        copy_cols = [d[0] for d in cur.description]
        for row in copy_rows:
            row_dict = dict(zip(copy_cols, row))
            status   = row_dict.get("status", "UNKNOWN")
            print(f"    Re-loading with NUGGET_CSV_FORMAT ...")
            print(f"    Result: {status}  (same file — idempotent as expected)")
    else:
        print("    Skipped — run 04-01 and 04-02 first to have stage + table.")

    # ─────────────────────────────────────────────────────────────────────────
    # 6. DESCRIBE FILE FORMAT — see all properties of a format
    # ─────────────────────────────────────────────────────────────────────────
    print(f"\n  ── Describe NUGGET_CSV_FORMAT ───────────────────────")
    cur.execute("DESC FILE FORMAT NUGGET_CSV_FORMAT")
    desc_rows = cur.fetchall()
    desc_cols = [d[0] for d in cur.description]
    prop_idx  = desc_cols.index("property")
    val_idx   = desc_cols.index("property_value")

    # Show only the interesting subset
    show_props = {
        "TYPE", "FIELD_DELIMITER", "RECORD_DELIMITER", "SKIP_HEADER",
        "FIELD_OPTIONALLY_ENCLOSED_BY", "NULL_IF", "DATE_FORMAT", "COMPRESSION",
    }
    print(f"    {'Property':<30}  Value")
    print(f"    {'─'*30}  {'─'*30}")
    for row in desc_rows:
        prop = str(row[prop_idx])
        if prop in show_props:
            print(f"    {prop:<30}  {row[val_idx]}")

conn.close()
print()
