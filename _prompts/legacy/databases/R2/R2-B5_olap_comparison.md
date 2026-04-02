SAVE AS: olap_comparison.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an OLAP engine comparison notebook.

TASK: Run the same 3 analytical queries on DuckDB, BigQuery, and Postgres — record execution time and cost for each — and produce a decision matrix. This is the capstone for the columnar category.

GCP CONTEXT — do not deviate:
- GCP project: citi-de-learning
- GCP key file: D:/Workspace/Technologies/_setup/gcp_key.json

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Setup — "OLAP Comparison — DuckDB vs BigQuery vs Postgres"; explain the benchmark methodology: same 3 queries, same data, each engine measured 3 times, median taken
2. Imports + connections (duckdb, google-cloud-bigquery, psycopg2, timeit, no pip install); verify all 3 connections; print "All 3 engines ready"
3. Benchmark Query 1 — P95 latency per region: SELECT region, PERCENTILE_CONT(0.95) WITHIN GROUP(ORDER BY value) FROM metrics JOIN endpoints USING (endpoint_id) GROUP BY region; run on all 3 engines; record times; print results table
4. Benchmark Query 2 — Daily alert spike detection: count alerts per day, flag days where count > 2 standard deviations above mean; run on all 3 engines; record times
5. Benchmark Query 3 — Top 20 endpoints by anomaly score: JOIN metrics + alerts, rank by (alert_count / avg_value) within region; run on all 3 engines; record times
6. Results Table — markdown table: engine × query × median_ms × cost_estimate; color commentary on which engine won each query and why
7. Decision Matrix — when to use each: DuckDB (single analyst, <50GB, embedded, no server), BigQuery (multi-user, serverless, petabyte, cost-per-scan model), Postgres (OLTP + light analytics, existing infra), Snowflake (enterprise multi-cloud, governed, time travel); Citi scenario mapping per cell
8. What Just Happened — the 3 ready-to-deliver interview answers: "Compare DuckDB and BigQuery", "When would you choose Redshift over BigQuery?", "How does Citi decide which OLAP engine to use?"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error
- Use DuckDB Postgres attach for DuckDB queries (not in-memory copy)

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

