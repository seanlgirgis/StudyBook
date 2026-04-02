SAVE AS: etl_s3_pipeline.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an ETL pipeline notebook.

TASK: Build a full batch ETL pipeline — extract from Postgres, stage to S3 as Parquet, and load into Redshift Serverless via COPY — using the Citi telemetry dataset.

CONNECTION VARIABLES:
REDSHIFT_HOST     = "default-workgroup.357811130281.us-east-1.redshift-serverless.amazonaws.com"
REDSHIFT_PORT     = 5439
REDSHIFT_DB       = "dev"
REDSHIFT_USER     = "de_admin"
REDSHIFT_PASSWORD = "DeAdmin2026!"
REDSHIFT_IAM_ROLE = "arn:aws:iam::357811130281:role/RedshiftS3ReadRole"
S3_BUCKET         = "citi-telemetry-data-lake-dev"
AWS_PROFILE       = "study"
AWS_REGION        = "us-east-1"

POSTGRES (source — pre-configured via db_connections.py):
- localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn
import boto3, pandas as pd, pyarrow as pa, pyarrow.parquet as pq, psycopg2, io, time
from datetime import datetime
```

SECTIONS:
1. Title + Mental Model — "Batch ETL — Postgres → S3 Parquet → Redshift"; ASCII pipeline diagram; explain why S3 staging is standard (atomic, resumable, auditable); COPY vs INSERT throughput at 500K rows; explain Parquet benefits for Redshift columnar ingestion
2. Imports + connection setup (import pattern above; test Postgres connection; test boto3 S3 access with profile=study; test Redshift connection via psycopg2; print "ETL pipeline ready: Postgres ✓ S3 ✓ Redshift ✓")
3. Extract — read all 3 tables from Postgres into pandas DataFrames using get_postgres_conn(); print shape and dtypes for each; note extraction time; print "Extracted: 10,000 endpoints | 500,000 metrics | 25,000 alerts"
4. Transform — apply transforms: (a) endpoints: add etl_loaded_at timestamp column, normalize datacenter to uppercase; (b) metrics: cast value to float32, drop unit column, add date partition column as recorded_at.dt.date; (c) alerts: map severity to int (critical=4, high=3, medium=2, low=1) and keep original, add is_open boolean; print "Transforms applied"
5. Stage to S3 — write each DataFrame to S3 as Parquet using partition by date for metrics; use boto3 with profile=study; paths: s3://citi-telemetry-data-lake-dev/etl/endpoints/endpoints.parquet, etl/metrics/date=YYYY-MM-DD/metrics.parquet (partitioned), etl/alerts/alerts.parquet; print S3 paths written; print "Staged to S3: 3 tables"
6. Load to Redshift — CREATE TABLE IF NOT EXISTS for endpoints_etl, metrics_etl, alerts_etl matching transformed schemas; run COPY for each table FROM S3 path IAM_ROLE; verify with SELECT COUNT(*); print "Loaded: endpoints_etl=10000 | metrics_etl=500000 | alerts_etl=25000"
7. Incremental Load Pattern — demonstrate watermark-based incremental extraction: SELECT * FROM telemetry.alerts WHERE created_at > %(last_watermark)s; insert 3 new alerts to Postgres; run incremental extract; stage to S3 incremental path; COPY with TRUNCATECOLUMNS to Redshift; update watermark; print "Incremental: 3 new alerts loaded"
8. Pipeline Observability — build a simple run_log dict: pipeline_run_id, start_time, end_time, rows_extracted, rows_loaded, s3_bytes_staged; write to Redshift pipeline_runs table; print run summary; explain why pipeline metadata is as important as the data itself
9. What Just Happened — ETL vs ELT decision table; COPY vs INSERT benchmark; Parquet vs CSV for staging; 4 interview Q&A; Citi framing: "This pattern is how Citi moves telemetry from operational Postgres into Redshift for next-day analytics without impacting prod query performance"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Connection variables defined at top of first code cell
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

