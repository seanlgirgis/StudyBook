SAVE AS: snowflake_architecture.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Snowflake architecture deep-dive notebook.

TASK: Cover Snowflake virtual warehouses, micro-partitions, Time Travel, zero-copy clone, and query optimization — using the Citi telemetry dataset. Connection variables are defined at the top for easy fill-in after Snowflake free trial setup.

CONNECTION VARIABLES (define as Python vars at top of first code cell — credentials confirmed):
SNOWFLAKE_ACCOUNT=<stored_in_studybook_encrypted_secret>
SNOWFLAKE_USER=<stored_in_studybook_encrypted_secret>
SNOWFLAKE_PASSWORD=<stored_in_studybook_encrypted_secret>
SNOWFLAKE_WAREHOUSE=<stored_in_studybook_encrypted_secret>
SNOWFLAKE_DATABASE=<stored_in_studybook_encrypted_secret>
SNOWFLAKE_SCHEMA=<stored_in_studybook_encrypted_secret>

DATASET CONTEXT — do not deviate:
- Source data to load: Citi telemetry (same schema as local Postgres)
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Snowflake — Shared Disk + Shared Nothing Architecture"; explain the three-layer architecture: cloud services → virtual warehouse compute → storage (S3/Azure Blob/GCS); ASCII diagram; micro-partition internals (16MB compressed, metadata-only pruning)
2. Imports + connection setup (snowflake-connector-python, connection using vars above, no pip install)
3. Virtual Warehouse Demo — SHOW WAREHOUSES; ALTER WAREHOUSE COMPUTE_WH SET WAREHOUSE_SIZE = 'XSMALL'; execute the same GROUP BY query on 500K metrics at XSMALL vs SMALL; time both; print "XSMALL: Xms | SMALL: Yms — linear scale-out confirmed"
4. Data Load — CREATE TABLE endpoints, metrics, alerts matching local schema; INSERT via Python connector (batched 1K rows); COUNT(*) verify; print "Loaded: 10K endpoints, 500K metrics, 25K alerts"
5. Micro-Partition Pruning — EXPLAIN query with date filter on timestamp; show PARTITIONS SCANNED vs PARTITIONS TOTAL in query profile; explain why partition elimination is metadata-only (no actual row scan)
6. Time Travel — DELETE 1000 alerts; SELECT COUNT(*) to confirm; AT(OFFSET => -60) to see count before delete; UNDROP TABLE demo; explain 1-day (free tier) vs 90-day (enterprise) retention
7. Zero-Copy Clone — CREATE TABLE alerts_backup CLONE alerts; INSERT 100 rows into alerts_backup; show original unaffected; explain no storage cost until divergence; Citi use case: branch development environments
8. Clustering Keys — ALTER TABLE metrics CLUSTER BY (region, timestamp); explain when clustering beats partitioning; SYSTEM$CLUSTERING_INFORMATION output; compare to Postgres partitioning
9. What Just Happened — summary table: Snowflake feature vs equivalent in Postgres; 4 interview Q&A; Citi framing: "Snowflake's separation of compute and storage lets Citi spin up 10 analyst warehouses simultaneously without copying data"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Connection variables defined as Python vars at top — clearly labeled for user to fill in
- Every code cell must execute top-to-bottom without error once credentials are set

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

