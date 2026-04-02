SAVE AS: timescaledb_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a TimescaleDB deep-dive notebook.

TASK: Cover TimescaleDB hypertables, chunk management, compression, continuous aggregates, and time-series SQL patterns — all running live against the Citi telemetry PostgreSQL instance with the TimescaleDB extension.

DATASET CONTEXT — do not deviate:
- PostgreSQL + TimescaleDB: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "TimescaleDB — PostgreSQL for Time-Series at Scale"; explain hypertables: Postgres table automatically partitioned by time into chunks; why this beats plain Postgres for time-series (chunk exclusion = partition pruning, per-chunk compression, parallel chunk scans); ASCII diagram of hypertable chunks
2. Imports + setup (psycopg2, no pip install); verify TimescaleDB extension: SELECT default_version FROM pg_available_extensions WHERE name='timescaledb'; if not installed, explain: CREATE EXTENSION IF NOT EXISTS timescaledb; connect and print version
3. Hypertable Creation — CREATE TABLE ts_metrics (LIKE metrics INCLUDING ALL); SELECT create_hypertable('ts_metrics', 'timestamp', chunk_time_interval => INTERVAL '1 day'); INSERT 100K rows from metrics; verify with SELECT show_chunks('ts_metrics'); print chunk count and time ranges
4. Chunk Management — SELECT * FROM timescaledb_information.chunks for ts_metrics; show how Postgres prunes chunks with time filter; compare EXPLAIN ANALYZE with time filter (chunk exclusion) vs without (all chunks scanned)
5. Compression — ALTER TABLE ts_metrics SET (timescaledb.compress, timescaledb.compress_segmentby = 'endpoint_id'); SELECT compress_chunk(c) FROM show_chunks('ts_metrics') c WHERE ...; show chunk_compression_stats; print compression ratio; explain why columnar compression fits time-series
6. Continuous Aggregates — CREATE MATERIALIZED VIEW hourly_metrics WITH (timescaledb.continuous) AS SELECT time_bucket('1 hour', timestamp), endpoint_id, AVG(value) as avg_value, MAX(value) as max_value FROM ts_metrics GROUP BY 1, 2; add refresh policy; query the view vs raw table; compare query times
7. Time-Series SQL Patterns — 5 queries using TimescaleDB functions: time_bucket, first(), last(), histogram(), time_bucket_gapfill() for missing interval detection; each on the Citi telemetry; print results
8. What Just Happened — TimescaleDB vs InfluxDB vs plain Postgres decision table; Citi framing: "TimescaleDB is Citi's choice when analysts need SQL JOINs on time-series data — the hypertable gives partition pruning without schema changes"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- If TimescaleDB extension is not installed, include a markdown cell explaining how to install it (docker exec de_postgres psql -U de_admin -d de_telemetry -c "CREATE EXTENSION timescaledb")
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

