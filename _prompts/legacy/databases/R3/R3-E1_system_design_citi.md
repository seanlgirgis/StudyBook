SAVE AS: system_design_citi.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a system design walkthrough notebook.

TASK: Walk through a complete system design for "Citi's API Monitoring Data Platform" — covering ingestion, storage tier selection, query serving, alerting pipeline, and analytical layer — using the live Citi telemetry stack as the implementation reference throughout.

DATABASE STACK (all pre-configured via db_connections.py — used for live validation queries):
- PostgreSQL      localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Redis           localhost:6380  password=DeRedis2026!
- Cassandra       localhost:9042  no auth  keyspace=telemetry
- Elasticsearch  http://localhost:9200  elastic/DeElastic2026!
- InfluxDB        http://localhost:8086  de_admin/DeInflux2026!  org=de_org  bucket=telemetry
- DuckDB          in-memory, attaches Postgres as 'pg'

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- events: 50,000 rows | endpoint_id, event_type, description, performed_by, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys, time
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import (
    get_postgres_conn, get_redis_conn, get_cassandra_session,
    get_elasticsearch_client, get_influxdb_client, get_duckdb_conn
)
```

SECTIONS:
1. Title + Problem Statement — "System Design: Citi API Monitoring Data Platform"; state requirements: (a) ingest 10K metric events/second, (b) serve real-time endpoint status with <10ms latency, (c) full-text search across 1M+ alert messages, (d) time-series aggregations for dashboards, (e) daily analytical reports across all dimensions; scale: 6,000 active endpoints, 30-day hot data, 2-year cold data
2. Imports + connections (import pattern above; verify all 6; print "System design lab: all tiers connected")
3. Requirements → DB Mapping — markdown cell: structured requirements analysis table; for each requirement map to: DB choice → reason → consistency requirement → latency SLA; end with the full architecture decision record in one table
4. Ingestion Layer Design — code: simulate the ingest path: a Python function ingest_metric_event(endpoint_id, metric_name, value) that writes to: (a) Postgres (source of truth, async), (b) InfluxDB (time-series, async), (c) Redis sorted set update (sync, for real-time ranking); time a batch of 1,000 events through this function; print throughput: "X events/second"
5. Real-Time Query Tier — code: demonstrate the <10ms read path: (a) GET endpoint status from Redis hash (cache hit path); (b) MISS path: fall back to Postgres SELECT, write result back to Redis with TTL=300s; run 100 reads and measure cache hit rate and P95 latency; print "Cache hit rate: X% | P95: Yms"
6. Search Tier — code: demonstrate full-text alert search path: Elasticsearch match query on message field with highlight; show relevance scoring; run 5 different search queries (cpu, memory, network timeout, authentication, disk); print result counts and top hit per query; explain why this search tier replaces 5 different Postgres ILIKE queries
7. Time-Series Analytics Tier — code: InfluxDB Flux query: average cpu_percent per datacenter over last 7 days windowed by 1 hour; render as pandas DataFrame; then same query via DuckDB on Postgres data; compare latency; explain when InfluxDB's downsampling/retention policies save storage vs Postgres partitioning
8. Analytical Layer — DuckDB query over Postgres: complex multi-table JOIN (endpoints + metrics + alerts + events) with window functions: rank endpoints by alert frequency within datacenter; show EXPLAIN plan; explain why DuckDB vectorized engine outperforms Postgres for this cross-table analytical query; print "Analytical report: top 5 at-risk endpoints per datacenter"
9. Failure Mode Analysis — markdown table: for each tier, describe: (a) what fails, (b) impact on system, (c) mitigation; cover: Postgres down (Redis still serves cache, but writes queue), Redis down (fall-through to Postgres, latency spikes), Elasticsearch down (search unavailable, core monitoring continues), InfluxDB down (real-time dashboards degrade, Postgres still stores metrics), Cassandra not used here — explain why Postgres+InfluxDB was chosen over Cassandra for this design
10. What Just Happened — full architecture summary diagram (ASCII); build vs buy analysis (self-hosted stack vs fully managed cloud: Aurora + ElastiCache + OpenSearch + Timestream + Redshift); 6 interview Q&A; Citi framing: "This architecture handles Citi's monitoring requirements with each database doing exactly one job it excels at"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redis port is 6380 (not 6379)

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

