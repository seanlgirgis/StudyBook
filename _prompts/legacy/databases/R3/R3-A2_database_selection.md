SAVE AS: database_selection.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a database selection framework notebook.

TASK: Build an interactive decision framework for choosing the right database — covering CAP theorem applied, ACID vs BASE tradeoffs, read/write pattern analysis, and cost modeling — using the Citi telemetry stack as the running example throughout.

DATABASE STACK (for live demos — no manual setup needed):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- DuckDB      in-memory, attaches Postgres as 'pg'
- Elasticsearch http://localhost:9200  elastic/DeElastic2026!

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_duckdb_conn, get_elasticsearch_client
```

SECTIONS:
1. Title + Mental Model — "Database Selection — Choosing the Right Tool"; why the wrong choice costs 10× at Citi scale; one-page visual: 9 DB types on axes of consistency vs availability vs partition tolerance
2. Imports + connection setup (import pattern above; connect to Postgres, DuckDB, Elasticsearch; print "Selection framework ready")
3. CAP Theorem Applied — code cell builds a pandas DataFrame of all 9 DBs × CAP positioning; print styled table; markdown explaining: CA (Postgres, MySQL), AP (Cassandra, CouchDB), CP (HBase, Zookeeper, MongoDB); Citi scenario: "Which CAP position suits our alert ingestion pipeline?"
4. ACID vs BASE Deep Dive — Postgres transaction demo: BEGIN → INSERT alert → UPDATE endpoint status → COMMIT; then simulate a failure mid-transaction and ROLLBACK; compare to Cassandra's eventual consistency for metrics (explain why it's acceptable for telemetry but not for financial records at Citi)
5. Read/Write Pattern Analysis — code: query pg_stat_user_tables for seq_scan vs idx_scan ratios on endpoints, metrics, alerts; build workload profile (read-heavy vs write-heavy vs mixed); print "Citi telemetry workload profile: metrics=write-heavy, alerts=read-heavy, endpoints=mixed"
6. Latency Tier Model — run the same aggregation (COUNT alerts by severity) on: Postgres, DuckDB, Elasticsearch; time all three; build a latency tier table (sub-1ms / 1-10ms / 10-100ms / 100ms+); map DB types to tiers; explain when each tier is acceptable in Citi's SLA context
7. Cost Model Framework — markdown + code: build a simple cost estimator Python function cost_model(db_type, rows, queries_per_day) that returns estimated monthly cost; compare Postgres self-hosted vs Snowflake on-demand vs BigQuery on-demand for 500K metric rows at 10K queries/day; print comparison table
8. Decision Tree — code renders a text-based decision tree: start → "Need ACID?" → yes: Postgres/Aurora; no → "Need full-text search?" → yes: Elasticsearch; no → "Time-series?" → yes: InfluxDB/TimescaleDB; etc.; covers all 9 DB types in the tree
9. Anti-Patterns Catalogue — markdown table: 8 common wrong choices (e.g., "Using Redis as primary store", "Using Postgres for 10B-row time-series", "Using Cassandra for joins") with symptom, root cause, correct fix; all framed around Citi telemetry
10. What Just Happened — "The 3 questions every DE asks before choosing a DB: (1) What's the access pattern? (2) What's the consistency requirement? (3) What's the scale ceiling?"; 4 interview Q&A; Citi framing

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

