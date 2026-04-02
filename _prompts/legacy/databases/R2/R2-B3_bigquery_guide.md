SAVE AS: bigquery_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a BigQuery deep-dive notebook.

TASK: Cover BigQuery slots, partitioning, clustering, cost control, and query optimization — using the Citi telemetry dataset loaded into BigQuery.

GCP CONTEXT — do not deviate:
- GCP project: citi-de-learning
- GCP key file: D:/Workspace/Technologies/_setup/gcp_key.json
- BigQuery dataset to create: citi_telemetry
- BigQuery location: US

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "BigQuery — Serverless Columnar OLAP at Petabyte Scale"; explain Dremel architecture (colossus storage, Borg compute, Jupiter network); slot = unit of compute; on-demand vs flat-rate pricing; why BigQuery has no indexes
2. Imports + setup (google-cloud-bigquery, service account key, no pip install); client = bigquery.Client.from_service_account_json("D:/Workspace/Technologies/_setup/gcp_key.json"); verify project
3. Create Dataset and Load — client.create_dataset("citi_telemetry"); define schemas for endpoints, metrics, alerts; load from Python lists (10K endpoints, 10K metrics sample, 10K alerts sample for cost control); verify row counts
4. Partitioning — CREATE TABLE metrics_partitioned PARTITION BY DATE(timestamp) AS SELECT ...; run query WITH and WITHOUT partition filter; check bytes_processed in job stats; print "With partition filter: X MB scanned | Without: Y MB scanned"
5. Clustering — CREATE TABLE alerts_clustered PARTITION BY DATE(created_at) CLUSTER BY severity, region AS SELECT ...; run query filtering on severity='critical' and region='APAC'; show bytes scanned reduction vs unordered table
6. Cost Control — use dry_run=True to estimate bytes before running; show cost calculation ($5/TB); set query_config maximum_bytes_billed=1_000_000_000; show what happens when query exceeds budget (BillingTierLimitExceeded)
7. Query Optimization — 3 optimization drills: (1) avoid SELECT *, use column pruning; (2) filter partition column before JOIN; (3) use APPROX_COUNT_DISTINCT instead of COUNT(DISTINCT) for cardinality estimates; show bytes_processed before and after each
8. What Just Happened — BigQuery vs Snowflake vs Redshift comparison table; Citi framing: "BigQuery's per-query pricing makes it Citi's preferred choice for analyst exploratory workloads — pay only for what you scan"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real GCP values from context above
- Every code cell must execute top-to-bottom without error
- Keep data loaded small (10K rows per table) to control BigQuery scan costs

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

