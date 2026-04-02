SAVE AS: indexing_master.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a master indexing strategy notebook.

TASK: Cover every major index type across the full database stack — B-tree, Hash, GIN, BRIN, partial, composite (Postgres), Cassandra partition/clustering keys, Elasticsearch mapping, vector HNSW, Redshift sort/dist keys — benchmarking each on the Citi telemetry dataset.

DATABASE STACK (all pre-configured via db_connections.py):
- PostgreSQL      localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Cassandra       localhost:9042  no auth  keyspace=telemetry
- Elasticsearch  http://localhost:9200  elastic/DeElastic2026!
- Redshift        default-workgroup.357811130281.us-east-1.redshift-serverless.amazonaws.com:5439  de_admin/DeAdmin2026!  db=dev

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id UUID PK, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id UUID FK, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id UUID PK, endpoint_id UUID FK, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys, time
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_cassandra_session, get_elasticsearch_client
import psycopg2
```

SECTIONS:
1. Title + Index Taxonomy — "Indexing Master — Every Index Type on the Citi Stack"; table: index type → DB → data structure → best for → worst for; explain why the wrong index is worse than no index (bloat, write overhead, planner confusion)
2. Imports + connections (import pattern above; verify 3 connections; print "Indexing lab ready")
3. Postgres B-tree — DROP all non-PK indexes on metrics; time query: SELECT * FROM telemetry.metrics WHERE endpoint_id = %s AND recorded_at > NOW()-INTERVAL '30 days'; CREATE INDEX idx_metrics_endpoint_date ON telemetry.metrics(endpoint_id, recorded_at DESC); time same query; EXPLAIN ANALYZE both; print "B-tree speedup: Xms → Yms"
4. Postgres GIN — CREATE GIN index on alerts.message using to_tsvector; run full-text search: WHERE to_tsvector('english', message) @@ to_tsquery('memory & critical'); compare vs ILIKE '%memory%' on same 25K alerts; time both; explain why GIN is inverted index and ILIKE is seq scan
5. Postgres BRIN — create BRIN index on metrics.recorded_at (natural time-ordered insert order makes BRIN ideal); EXPLAIN ANALYZE time range query with BRIN vs B-tree; explain BRIN pages_per_range tradeoff; when BRIN beats B-tree (append-only, naturally ordered, large table)
6. Postgres Partial Index — CREATE INDEX idx_open_alerts ON telemetry.alerts(endpoint_id) WHERE status = 'open'; query: SELECT COUNT(*) FROM telemetry.alerts WHERE status = 'open' AND endpoint_id = %s; show index size vs full index (partial index covers only ~33% of rows); explain when partial indexes dramatically reduce write overhead
7. Cassandra Partition Key as Index — query metrics for a known endpoint_id (uses partition key — efficient); then attempt SELECT * FROM metrics WHERE metric_name = 'cpu_percent' (no partition key — full scan, should warn or error); CREATE INDEX on metric_name (secondary index); re-run; explain why Cassandra secondary indexes are anti-pattern at scale and SAI (Storage-Attached Indexes) is the modern alternative
8. Elasticsearch Mapping Optimization — show current telemetry_alerts mapping; explain keyword vs text field tradeoff (keyword=exact match/agg, text=full-text); create a new index telemetry_alerts_v2 with optimized mapping (severity as keyword, message as text with keyword sub-field); reindex 25K docs; run aggregation on severity (keyword) and show it's 3× faster than on text field
9. Redshift Sort + Distribution Keys — connect to Redshift; show table definition for metrics_etl; run GROUP BY query on endpoint_id without any sort key; run same query on a table with SORTKEY(recorded_at) DISTKEY(endpoint_id); explain how zone maps work with sort keys; print "Sort key speedup: Xms → Yms"
10. Index Maintenance — Postgres: show pg_stat_user_indexes for bloat (idx_scan vs idx_tup_read ratio); REINDEX CONCURRENTLY; explain VACUUM and why autovacuum may not keep up at Citi's insert rate; brief note on Cassandra compaction and Elasticsearch force merge
11. What Just Happened — master index selection table: query type → recommended index → DB → rationale; 4 interview Q&A; Citi framing: "At Citi's telemetry scale, choosing the wrong index costs as much as choosing the wrong database"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redshift connection via psycopg2 directly (not db_connections.py)

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

