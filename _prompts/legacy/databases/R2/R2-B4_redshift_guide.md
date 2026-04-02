SAVE AS: redshift_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Redshift deep-dive notebook.

TASK: Cover Redshift distribution keys, sort keys, COPY from S3, Spectrum, and RA3 architecture — using the Citi telemetry dataset. Connection variables defined at top for fill-in after cluster creation.

CONNECTION VARIABLES (define as Python vars at top — user fills after cluster creation):
REDSHIFT_HOST = "default-workgroup.357811130281.us-east-1.redshift-serverless.amazonaws.com"
REDSHIFT_PORT = 5439
REDSHIFT_DB = "dev"
REDSHIFT_USER = "de_admin"
REDSHIFT_PASSWORD = "DeAdmin2026!"
REDSHIFT_IAM_ROLE = "arn:aws:iam::357811130281:role/RedshiftS3ReadRole"

AWS CONTEXT — do not deviate:
- AWS profile: study
- AWS region: us-east-1
- S3 bucket: citi-telemetry-data-lake-dev

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Redshift — MPP Column-Store Data Warehouse"; explain shared-nothing MPP: leader node + compute nodes; columnar storage + zone maps; RA3 architecture (compute/storage separated); how Redshift differs from Postgres
2. Imports + connection setup (psycopg2 or redshift-connector, using vars above, no pip install)
3. Distribution Key Design — CREATE TABLE metrics with DISTKEY(endpoint_id) SORTKEY(timestamp); CREATE TABLE endpoints with DISTSTYLE ALL; CREATE TABLE alerts with DISTKEY(endpoint_id) SORTKEY(created_at); explain why DISTKEY on join column minimizes data shuffling; insert 10K sample rows each
4. COPY from S3 — upload metrics CSV to S3 using boto3 (profile=study); COPY metrics FROM 's3://citi-telemetry-data-lake-dev/metrics.csv' IAM_ROLE '...' CSV; explain why COPY is 100× faster than INSERT for bulk loads; verify row count
5. Sort Key and Zone Maps — run range query on timestamp with and without VACUUM SORT ONLY; show STL_SCAN blocks_pre vs blocks_post; explain zone maps as block-level min/max statistics
6. Spectrum — CREATE EXTERNAL SCHEMA spectrum_citi FROM DATA CATALOG DATABASE 'de_telemetry' IAM_ROLE '...'; query Parquet files on S3 directly; compare scan cost vs loaded table; Citi use case: cold archive query
7. Query Optimization — SVL_QLOG to see actual vs estimated rows; STL_ALERT_EVENT_LOG to find redistribution events; fix a redistribute broadcast join; Citi framing: "Redshift distribution key design is the single most impactful architecture decision for query performance"
8. What Just Happened — Redshift vs BigQuery vs Snowflake decision table; 4 interview Q&A; cleanup: DROP TABLE statements

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Connection host defined as variable — clearly labeled for user to fill after cluster creation
- Every code cell must execute top-to-bottom without error once credentials are set

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

