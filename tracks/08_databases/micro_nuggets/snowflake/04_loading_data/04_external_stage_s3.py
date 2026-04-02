"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 04-04 · External Stage (S3)                                          ║
║  Connect Snowflake to your cloud storage — the production data lake pattern. ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Reads from a real public S3 bucket to demonstrate external stage concepts
without needing your own AWS credentials. Shows stage creation, listing,
and COPY INTO from external storage — the pattern every cloud DE uses.

CONCEPTS
────────
External Stage vs Internal Stage:
  Internal stage: Snowflake manages the storage (nugget 04-01).
  External stage: YOU own the cloud bucket. Snowflake reads/writes it.
    - AWS S3      → s3://bucket/path/
    - Azure Blob  → azure://account.blob.core.windows.net/container/
    - GCS         → gcs://bucket/path/

Why external stages?
  1. Your data lake already lives in S3/Azure/GCS — don't copy it into
     Snowflake's internal storage, just point Snowflake at it.
  2. Multiple services (Spark, Athena, Snowflake) can read the same files.
  3. You control data lifecycle (retention, archiving) independently.
  4. Cheaper: Snowflake doesn't bill for storage you manage yourself.

Authentication options for external S3 stages:
  Option A — AWS Keys (simple, less secure):
    CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_KEY_ID='AKIA...' AWS_SECRET_KEY='...');

  Option B — Storage Integration (recommended for production):
    1. CREATE STORAGE INTEGRATION (admin creates once per account)
    2. Snowflake generates an IAM role ARN + external ID
    3. You configure an S3 bucket policy granting that ARN read/write
    4. CREATE STAGE ... STORAGE_INTEGRATION = my_integration;
    No secrets stored in Snowflake — credentials rotate automatically.

  Option C — Public bucket (this nugget — no credentials needed):
    CREATE STAGE my_public_stage URL = 's3://public-bucket/';

Public Snowflake sample data bucket:
  Snowflake maintains a public S3 bucket with sample datasets:
    s3://snowflake-workshop-lab/   — Citibike, orders, TPC-H data etc.
  We use this so the nugget runs on any trial account without AWS setup.

SELECT from stage (without COPY INTO):
  You can query files directly without loading them into a table:
    SELECT $1, $2, $3 FROM @my_stage/file.csv (FILE_FORMAT => my_fmt);
  $1, $2, $3 are positional column references for CSV.
  For JSON: SELECT $1:key FROM @my_stage/file.json (FILE_FORMAT => my_json_fmt);
  Useful for previewing data or transforming during load.

INFER_SCHEMA():
  For Parquet/ORC/Avro, Snowflake can infer the schema automatically:
    SELECT * FROM TABLE(INFER_SCHEMA(
        LOCATION => '@my_stage',
        FILE_FORMAT => 'my_parquet_fmt'
    ));
  Returns column names and types — use to auto-generate CREATE TABLE DDL.

Snowpipe (mention only — covered in a future nugget):
  Snowpipe = serverless continuous COPY INTO triggered by S3 event
  notifications (SQS).  Files land in S3 → event triggers Snowpipe →
  data is in your table within seconds.  No warehouse needed.

USAGE
─────
    python 04_external_stage_s3.py

EXPECTED OUTPUT
───────────────
    ── External Stage (S3) ───────────────────────

      ── Creating public external stage ───────────────────
        [✓] NUGGET_EXTERNAL_STAGE_PUBLIC created

      ── Files in public stage (sample) ───────────────────
        name                                    size
        --------------------------------------- --------
        citibike-trips/trips_2013_1.csv.gz     12345678
        citibike-trips/trips_2013_2.csv.gz      9876543
        ... (truncated to first 5)

      ── Preview first 3 rows without loading ─────────────
        COL1            COL2        COL3         COL4
        --------------- ----------- ------------ -----------
        tripduration    starttime   stoptime     bikeid
        381             2013-06-01  2013-06-01   536
        1372            2013-06-01  2013-06-01   344

      ── External stage DDL reference ─────────────────────
        (prints the authenticated CREATE STAGE template for your own S3 bucket)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _sf_connect import get_connection

conn = get_connection()

print("\n── External Stage (S3) ───────────────────────")

# Public S3 bucket maintained by Snowflake for training purposes.
# No credentials required — accessible from any Snowflake account.
PUBLIC_S3_URL = "s3://snowflake-workshop-lab/citibike-trips-csv/"

with conn.cursor() as cur:

    # ─────────────────────────────────────────────────────────────────────────
    # 1. Create an external stage pointing to a PUBLIC S3 bucket
    #    No CREDENTIALS clause = anonymous read (public bucket only).
    #    For your own bucket, add CREDENTIALS or STORAGE_INTEGRATION.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Creating public external stage ───────────────────")
    try:
        cur.execute(f"""
            CREATE OR REPLACE STAGE NUGGET_EXTERNAL_STAGE_PUBLIC
                URL         = '{PUBLIC_S3_URL}'
                FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 COMPRESSION = 'AUTO')
                COMMENT     = 'Points to Snowflake public Citibike training data — nugget 04-04'
        """)
        print("    [✓] NUGGET_EXTERNAL_STAGE_PUBLIC created")
    except Exception as exc:
        print(f"    [✗] Could not create external stage: {exc}")
        print("        (Network access to S3 may be restricted on this account)")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. LIST the external stage — shows files in the S3 path
    #    This makes a lightweight S3 ListObjects API call.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Files in public stage (first 5) ──────────────────")
    try:
        cur.execute("LIST @NUGGET_EXTERNAL_STAGE_PUBLIC LIMIT 5")
        list_rows = cur.fetchall()
        list_cols = [d[0] for d in cur.description]
        n_idx  = list_cols.index("name")
        sz_idx = list_cols.index("size")
        print(f"    {'name':<40}  {'size':>10}")
        print(f"    {'─'*40}  {'─'*10}")
        for row in list_rows[:5]:
            name = str(row[n_idx]).split("/")[-1][:40]
            print(f"    {name:<40}  {row[sz_idx]:>10,}")
        if not list_rows:
            print("    (no files returned — check network access to S3)")
    except Exception as exc:
        print(f"    LIST failed: {exc}")
        list_rows = []

    # ─────────────────────────────────────────────────────────────────────────
    # 3. SELECT from stage — preview rows WITHOUT loading into a table
    #    $1, $2, $3 … are positional column references for CSV files.
    #    This is a powerful pattern: validate the data shape before committing
    #    to a table schema.
    # ─────────────────────────────────────────────────────────────────────────
    print("\n  ── Preview first 3 rows without loading ─────────────")
    if list_rows:
        try:
            cur.execute("""
                SELECT $1, $2, $3, $4, $5
                FROM   @NUGGET_EXTERNAL_STAGE_PUBLIC
                (FILE_FORMAT => 'NUGGET_CSV_FORMAT')
                LIMIT 3
            """)
            preview_rows = cur.fetchall()
            cols = [f"$COL{i+1}" for i in range(5)]
            print(f"    {cols[0]:<16}  {cols[1]:<12}  {cols[2]:<12}  {cols[3]:<12}  {cols[4]}")
            print(f"    {'─'*16}  {'─'*12}  {'─'*12}  {'─'*12}  {'─'*12}")
            for row in preview_rows:
                print("    " + "  ".join(f"{str(v or ''):<12}" for v in row))
        except Exception as exc:
            print(f"    Preview query failed: {exc}")
            print("    (Run 04-03 first to create NUGGET_CSV_FORMAT)")
    else:
        print("    Skipped — no files available from LIST.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Reference DDL — template for YOUR own private S3 bucket
#    Printed as a comment block — not executed. Study this for real DE work.
# ─────────────────────────────────────────────────────────────────────────────
print("""
  ── DDL reference: authenticated S3 stage ────────────

  Option A — AWS Keys (quick, less secure):
  ─────────────────────────────────────────
    CREATE STAGE my_private_stage
        URL         = 's3://my-company-datalake/raw/orders/'
        CREDENTIALS = (
            AWS_KEY_ID     = 'AKIAIOSFODNN7EXAMPLE'
            AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        )
        FILE_FORMAT = (TYPE = PARQUET USE_LOGICAL_TYPE = TRUE)
        COMMENT     = 'Orders raw zone — production';

  Option B — Storage Integration (recommended, no secrets in Snowflake):
  ───────────────────────────────────────────────────────────────────────
    -- Step 1: Admin creates the integration (once per account)
    CREATE STORAGE INTEGRATION s3_int
        TYPE                      = EXTERNAL_STAGE
        STORAGE_PROVIDER          = 'S3'
        ENABLED                   = TRUE
        STORAGE_ALLOWED_LOCATIONS = ('s3://my-company-datalake/');

    -- Step 2: Get Snowflake's IAM role ARN and external ID
    DESC INTEGRATION s3_int;
    -- Copy STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID
    -- Then grant that ARN access in your S3 bucket policy (AWS console/Terraform)

    -- Step 3: Create the stage using the integration
    CREATE STAGE my_integrated_stage
        URL                = 's3://my-company-datalake/raw/'
        STORAGE_INTEGRATION = s3_int
        FILE_FORMAT        = (TYPE = PARQUET);
""")

conn.close()
