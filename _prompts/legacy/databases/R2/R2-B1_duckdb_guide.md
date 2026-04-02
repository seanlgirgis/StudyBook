SAVE AS: duckdb_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep DuckDB guide notebook.

TASK: Cover DuckDB columnar internals, vectorized execution, Parquet queries, and the OLAP vs OLTP comparison — all running live against the Citi telemetry data.

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "DuckDB — Columnar OLAP in a Python Process"; explain columnar vs row storage with ASCII diagram; vectorized execution; why DuckDB has no server
2. Imports + DuckDB setup (duckdb, psycopg2, no pip install); DuckDB version print
3. Direct Postgres Attach — duckdb.connect().execute("ATTACH 'host=localhost port=5432 dbname=de_telemetry user=de_admin password=DeAdmin2026!' AS pg (TYPE postgres)"); query endpoints directly from DuckDB; print row count
4. Aggregate Benchmark — same query on DuckDB (via Postgres attach) vs psycopg2 direct: GROUP BY region, compute AVG(value) from 500K metrics; time both; print "DuckDB: Xms | Postgres: Yms | Speedup: Z×"
5. Parquet Export and Query — export metrics to Parquet with duckdb: COPY (SELECT ...) TO 'metrics.parquet' (FORMAT PARQUET); then query Parquet directly: SELECT region, COUNT(*) FROM read_parquet('metrics.parquet') JOIN ...; show column pruning and predicate pushdown in EXPLAIN
6. Window Functions and Analytics — run 3 OLAP queries on DuckDB: (1) running total alerts per day, (2) endpoint rank by P95 latency within region, (3) lag/lead to detect alert spikes; compare syntax with Postgres equivalent
7. DuckDB vs Postgres — when each wins: markdown table (row count, query type, write pattern, latency, multi-user); code: run the 500K metrics GROUP BY on both and print the comparison; Citi framing: "DuckDB is Citi's go-to for analyst ad-hoc on extracted data — no cluster needed, no cost"
8. What Just Happened — summary + 3 interview Q&A embedded; Citi tie-in

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

