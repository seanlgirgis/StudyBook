"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-01 · Internal Stage & PUT                                         ║
║  How to get a local file into Snowflake's file storage.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Creates a Snowflake internal stage, writes a small CSV file locally,
uploads it with PUT, and verifies it landed. This is Step 1 of the
two-step load pattern: PUT (file → stage) then COPY INTO (stage → table).

CONCEPTS
────────
What is a Stage?
  A Stage is a named pointer to file storage — a holding area for data files
  before they are loaded into tables (or after they are unloaded from tables).

  Two kinds:
  ┌───────────────┬──────────────────────────────────────────────────────────┐
  │ Internal Stage│ Storage managed BY Snowflake, inside your account.       │
  │               │ Files are encrypted automatically.                        │
  │               │ No AWS/Azure/GCP account needed.                          │
  │               │ Subtypes: User (@~), Table (@%table), Named (@my_stage)  │
  ├───────────────┼──────────────────────────────────────────────────────────┤
  │ External Stage│ Pointer to YOUR cloud bucket (S3, Azure Blob, GCS).      │
  │               │ You manage the storage and credentials.                   │
  │               │ Covered in nugget 04-04.                                  │
  └───────────────┴──────────────────────────────────────────────────────────┘

Named internal stage (what we create here):
    CREATE STAGE my_stage;
  - Persists until dropped — not tied to a session or table.
  - Can be shared across multiple COPY INTO statements.
  - Best practice for production pipelines.

PUT command:
    PUT file://local/path/file.csv @my_stage;
  - Uploads the local file to the named stage.
  - Runs client-side: the Snowflake connector streams the file directly.
  - Automatically GZIP compresses the file unless AUTO_COMPRESS = FALSE.
  - Returns: source_file, destination_file, source_size, status.
  - Status values: UPLOADED | SKIPPED (file already exists with same checksum)

Stage path notation:
  @my_stage               — root of the stage
  @my_stage/subdir/       — subdirectory within the stage
  @my_stage/file.csv.gz   — a specific file

LIST command:
    LIST @my_stage;      — shows all files with size, md5, last_modified
    LIST @my_stage PATTERN = '.*orders.*';  — filtered by regex

REMOVE command:
    REMOVE @my_stage/file.csv.gz;   — delete a specific file from stage

Encryption:
  Internal stages use AES-256 server-side encryption automatically.
  Client-side encryption can also be enabled (extra key management overhead).
  For most DEs: default server-side is sufficient and zero-config.

USAGE
─────
    python 01_internal_stage_put.py

EXPECTED OUTPUT
───────────────
    ── Internal Stage & PUT ─────────────────────

      Created stage: NUGGET_INTERNAL_STAGE

      Writing local CSV: C:\\Users\\...\\nugget_orders_sample.csv (5 data rows)

      PUT result:
        source               destination                     size  status
        -------------------- ------------------------------- ----- --------
        nugget_orders_sa...  nugget_orders_sample.csv.gz      312  UPLOADED

      Files in @NUGGET_INTERNAL_STAGE:
        name                                size  md5                               last_modified
        ----------------------------------- ----- --------------------------------- -------------------------
        nugget_orders_sample.csv.gz          312  a1b2c3d4e5f6...                   2024-01-17 10:23:44.000

      Stage is ready for COPY INTO (nugget 04-02).
"""
from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── Internal Stage & PUT ─────────────────────")

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Create a named internal stage
    #    COPY_OPTIONS and FILE_FORMAT can be set here or overridden at COPY time.
    #    Keeping stage definition simple; FILE_FORMAT is set in nugget 04-03.
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE STAGE IF NOT EXISTS NUGGET_INTERNAL_STAGE
        COMMENT = 'Demo internal stage for micro-nuggets loading exercises'
    """)
    print("\n  Created stage: NUGGET_INTERNAL_STAGE")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. Write a small CSV file to a temp location
    #    In a real pipeline this file would come from an API, S3, or a local
    #    export.  Here we generate it so the nugget is self-contained.
    # ─────────────────────────────────────────────────────────────────────────
    sample_rows = [
        ("order_id", "customer_id", "product_id", "quantity", "unit_price", "order_date", "status"),
        (1001, 201, 10, 2, 29.99, "2024-01-10", "SHIPPED"),
        (1002, 202, 11, 1, 49.99, "2024-01-11", "PENDING"),
        (1003, 201, 12, 5,  9.99, "2024-01-12", "DELIVERED"),
        (1004, 203, 10, 3, 29.99, "2024-01-13", "SHIPPED"),
        (1005, 204, 13, 1, 99.99, "2024-01-14", "PENDING"),
    ]

    # Write to a temp file — tempfile gives us a guaranteed writable location
    tmp_dir  = Path(tempfile.gettempdir())
    csv_path = tmp_dir / "nugget_orders_sample.csv"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(sample_rows)

    data_rows = len(sample_rows) - 1   # exclude header
    print(f"\n  Writing local CSV: {csv_path} ({data_rows} data rows)")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. PUT — upload the local file to the stage
    #    file:// prefix is required on the local path.
    #    On Windows, backslashes must be forward-slashes inside the SQL string.
    #    AUTO_COMPRESS = TRUE (default) gzip-compresses the file during upload.
    #    OVERWRITE = TRUE replaces an existing file with the same name.
    # ─────────────────────────────────────────────────────────────────────────
    put_path = csv_path.as_posix()   # forward slashes for cross-platform SQL
    cur.execute(f"""
        PUT 'file://{put_path}'
            @NUGGET_INTERNAL_STAGE
            AUTO_COMPRESS = TRUE
            OVERWRITE     = TRUE
    """)
    put_rows = cur.fetchall()
    put_cols = [d[0] for d in cur.description]

    print(f"\n  PUT result:")
    src_idx  = put_cols.index("source")
    dst_idx  = put_cols.index("target")
    size_idx = put_cols.index("target_size")
    stat_idx = put_cols.index("status")
    print(f"    {'source':<20}  {'destination':<31}  {'size':>5}  status")
    print(f"    {'─'*20}  {'─'*31}  {'─'*5}  {'─'*8}")
    for row in put_rows:
        src  = str(row[src_idx])[-20:]
        dst  = str(row[dst_idx])[:31]
        size = row[size_idx]
        stat = row[stat_idx]
        print(f"    {src:<20}  {dst:<31}  {size:>5}  {stat}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. LIST — verify the file landed in the stage
    #    Returns: name, size, md5, last_modified
    # ─────────────────────────────────────────────────────────────────────────
    cur.execute("LIST @NUGGET_INTERNAL_STAGE")
    list_rows = cur.fetchall()
    list_cols = [d[0] for d in cur.description]

    print(f"\n  Files in @NUGGET_INTERNAL_STAGE:")
    n_idx   = list_cols.index("name")
    sz_idx  = list_cols.index("size")
    md5_idx = list_cols.index("md5")
    lm_idx  = list_cols.index("last_modified")
    print(f"    {'name':<35}  {'size':>5}  {'md5':<34}  last_modified")
    print(f"    {'─'*35}  {'─'*5}  {'─'*34}  {'─'*25}")
    for row in list_rows:
        name = str(row[n_idx]).split("/")[-1]   # just filename, not full path
        print(
            f"    {name:<35}  {row[sz_idx]:>5}  "
            f"{str(row[md5_idx]):<34}  {row[lm_idx]}"
        )

conn.close()
print("\n  Stage is ready. Run 02_copy_into_table.py to load it into a table.\n")
