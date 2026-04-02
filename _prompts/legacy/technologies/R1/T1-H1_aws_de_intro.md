SAVE AS: aws_de_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
AWS data engineering services for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against real AWS.

TASK: Generate aws_de_intro.ipynb — a Jupyter notebook covering the AWS DE mental model,
S3 as a data lake, Glue catalog, and Athena querying — all using the Citi telemetry dataset.

NOTE: This notebook provisions real AWS resources using the free tier. Resources are cleaned up
at the end. Users need an AWS account with CLI configured (aws configure).

DATASET CONTEXT — do not deviate:
- Local Postgres: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: telemetry data moving to AWS — S3 as data lake, Glue catalog, Athena for SQL

TECH STACK CONTEXT — do not deviate:
- AWS CLI configured with aws configure (access key, secret key, region us-east-1)
- boto3 for programmatic access
- S3 bucket: created in this notebook, named citi-telemetry-lake-{account_id}
- Glue database: citi_telemetry_db
- Athena output bucket: citi-telemetry-athena-{account_id}

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "AWS Data Engineering — First Contact"
- 3-paragraph mental model: AWS DE stack overview (S3 → Glue → Athena → EMR → Redshift),
  serverless vs managed services, pay-per-query vs always-on
- Citi framing: "Citi's cloud DE stack: raw telemetry lands in S3, Glue catalogs the schema,
  Athena runs ad-hoc SQL, EMR runs batch Spark jobs — no servers to manage."
- ASCII diagram: [Postgres] → [Export CSV] → [S3 Data Lake] → [Glue Catalog] → [Athena SQL] → [Results]

SECTION 2 — Install + Setup (code cell)
- pip install boto3 psycopg2-binary pandas pyarrow
- imports: boto3, psycopg2, pandas, io, json, os
- Code: get AWS account ID via boto3:
  account_id = boto3.client('sts').get_caller_identity()['Account']
  region = boto3.session.Session().region_name
  print(f"AWS Account: {account_id}, Region: {region}")
  BUCKET_NAME = f"citi-telemetry-lake-{account_id}"
  ATHENA_BUCKET = f"citi-telemetry-athena-{account_id}"
  GLUE_DB = "citi_telemetry_db"

SECTION 3 — Create S3 Buckets (code cell + markdown)
- Markdown: "Create the data lake and Athena results buckets"
- Code: use boto3 s3 client to create both buckets (handle BucketAlreadyOwnedByYou)
  Enable versioning on data lake bucket
  Block all public access on both buckets
  Print: "Created: {BUCKET_NAME} and {ATHENA_BUCKET}"

SECTION 4 — Export Postgres to S3 as Parquet (code cell + markdown)
- Markdown: H2 "Export Telemetry Data to S3"
  - Explain: Parquet is the standard DE format for S3 data lakes (columnar, compressed, schema-embedded)
- Code:
  - Connect to Postgres, read endpoints and alerts into pandas DataFrames
  - Write to Parquet in memory using pyarrow: buffer = io.BytesIO(); df.to_parquet(buffer, index=False)
  - Upload to S3:
    - s3://BUCKET_NAME/telemetry/endpoints/endpoints.parquet
    - s3://BUCKET_NAME/telemetry/alerts/alerts.parquet
  - Print: f"Uploaded endpoints ({len(endpoints_df)} rows) and alerts ({len(alerts_df)} rows) to S3"

SECTION 5 — Glue Catalog (code cell + markdown)
- Markdown: H2 "AWS Glue — The Metadata Catalog"
  - Explain: Glue Data Catalog = Hive metastore in AWS, stores schema (database + table + columns),
    Athena, EMR, and Redshift Spectrum all read from it; Glue crawler auto-discovers schema
- Code: use boto3 glue client to:
  - Create database citi_telemetry_db (handle AlreadyExistsException)
  - Create table "endpoints" with exact schema:
    StorageDescriptor: S3 location, columns (endpoint_id:int, name:string, region:string, status:string, category:string),
    InputFormat: org.apache.hadoop.mapred.TextInputFormat,
    SerdeInfo: org.apache.hive.hcatalog.data.JsonSerDe (actually parquet:
    use org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat and
    org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe)
  - Create table "alerts" with schema:
    columns: alert_id:int, endpoint_id:int, severity:string, message:string, created_at:string
    Same Parquet serde
  - Print: "Glue catalog: {GLUE_DB}.endpoints and {GLUE_DB}.alerts created"

SECTION 6 — Athena Query (code cell + markdown)
- Markdown: H2 "Athena — Serverless SQL on S3"
  - Explain: Athena = Presto-based SQL engine, queries S3 directly via Glue catalog,
    pay per TB scanned, results saved to S3, no infrastructure to manage
- Code: define run_athena(sql, database, output_bucket) function:
  - boto3 athena client
  - start_query_execution with QueryString, QueryExecutionContext, ResultConfiguration
  - Poll status until SUCCEEDED or FAILED (max 30s, 2s sleep)
  - get_query_results → parse and return as list of dicts
- Run 3 queries:
  1. SELECT severity, COUNT(*) as cnt FROM alerts GROUP BY severity ORDER BY cnt DESC
  2. SELECT region, COUNT(DISTINCT endpoint_id) as endpoints FROM endpoints GROUP BY region ORDER BY endpoints DESC
  3. SELECT e.region, a.severity, COUNT(*) as alert_count
     FROM alerts a JOIN endpoints e ON a.endpoint_id = e.endpoint_id
     GROUP BY e.region, a.severity ORDER BY alert_count DESC LIMIT 20
- Print results of each query

SECTION 7 — Cost Awareness (markdown cell)
- H2: "Cost — What This Costs"
- Table:

| Service | How you're charged | This notebook |
|---------|-------------------|---------------|
| S3 | $0.023/GB/month + PUT requests | ~$0.01 for 25K rows in Parquet |
| Glue Catalog | First 1M objects free | Free |
| Athena | $5/TB scanned | ~$0.01 for 3 queries on 2 small files |
| Total this session | — | < $0.05 |

- Note: Parquet compression = 10x fewer bytes scanned vs CSV → 10x less cost

SECTION 8 — Clean Up (code cell + markdown)
- Markdown: "Delete all AWS resources created in this notebook to avoid ongoing charges"
- Code:
  - Delete all objects from both S3 buckets, then delete the buckets
  - Delete Glue tables (endpoints, alerts), then delete database citi_telemetry_db
  - Print: "Clean up complete — all AWS resources deleted"

SECTION 9 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: exported Postgres → Parquet, uploaded to S3, Glue catalog created, Athena SQL ran,
  cost < $0.05, cleaned up
- Citi tie-in: "This is the Citi AWS DE pattern: nightly Airflow DAG exports telemetry to S3,
  Glue crawler updates the catalog, Athena serves the risk team SQL access — no data warehouse needed."
- Next: "Run aws_de_concepts.md for Glue/EMR/Kinesis vocabulary."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All boto3 calls handle exceptions (print error, do not crash on duplicate resources)
- Athena poll loop terminates — max 15 iterations with 2s sleep
- Clean up (Section 8) is a mandatory final code cell
- No hardcoded account IDs

ACCEPTANCE: Every code cell executes. Section 6 prints Athena query results.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

