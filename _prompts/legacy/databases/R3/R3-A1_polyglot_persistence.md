SAVE AS: polyglot_persistence.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a polyglot persistence architecture notebook.

TASK: Demonstrate how a real production architecture uses the right database for each workload — using the Citi telemetry dataset already seeded across all 8 databases. Show the same business question answered from multiple DBs, compare latency and tradeoffs, and build a routing decision table.

DATABASE STACK (all credentials pre-configured via db_connections.py — no manual setup):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Redis       localhost:6380  password=DeRedis2026!
- Cassandra   localhost:9042  no auth  keyspace=telemetry
- Neo4j       bolt://localhost:7687  neo4j/DeNeo4j2026!
- InfluxDB    http://localhost:8086  de_admin/DeInflux2026!  org=de_org  bucket=telemetry
- Elasticsearch http://localhost:9200  elastic/DeElastic2026!
- DuckDB      in-memory, attaches Postgres as 'pg'
- MongoDB Atlas MONGO_URI from env  db=de_telemetry

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- events: 50,000 rows | endpoint_id, event_type, description, performed_by, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (all cells use this — no inline connection code):
```python
import sys
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import (
    get_postgres_conn, get_redis_conn, get_cassandra_session,
    get_neo4j_driver, get_influxdb_client, get_elasticsearch_client,
    get_duckdb_conn, get_mongo_db
)
```

SECTIONS:
1. Title + Architecture Map — "Polyglot Persistence — Right Tool for Each Workload"; ASCII diagram showing Citi's monitoring stack and which DB handles which workload tier; table: DB → primary workload → why chosen
2. Imports + connections (import pattern above; verify all 8 with .ping() / COUNT(*); print "All 8 databases connected")
3. Query 1: "Top 10 endpoints by alert count" — run same query on Postgres (SQL GROUP BY), Redis (ZREVRANGE alert_counts), MongoDB (aggregation pipeline); time each; print latency comparison table; explain when each routing choice is correct
4. Query 2: "CPU metrics for NYC1 datacenter last 7 days" — run on Postgres (filtered SELECT), Cassandra (partition key scan), InfluxDB (Flux range query), DuckDB (columnar aggregation over pg); time each; comparison table
5. Query 3: "Find endpoints with 3+ hops of dependency from srv-00001" — Neo4j Cypher (MATCH path*1..3); explain why this query is impossible in relational without recursive CTE and 10× slower; show equivalent Postgres recursive CTE for comparison
6. Query 4: "Search alerts containing 'memory' in message" — Elasticsearch match query vs Postgres ILIKE; time both on 25K alerts; explain inverted index vs seq scan; relevance scoring bonus
7. Write Pattern Demo — simulate a new alert event: write to Postgres (source of truth) → Redis sorted set (cache update) → Elasticsearch (search index); show 3-step write fan-out; explain eventual consistency tradeoff
8. Polyglot Decision Table — markdown table: workload type → best DB → why → latency tier → consistency model; cover: OLTP, analytical aggregation, cache/hot lookup, time-series, graph traversal, full-text search, document store, bulk ETL
9. What Just Happened — 3 Citi architect statements: what each DB owner would say in a design review; 4 interview Q&A; anti-pattern: "using Postgres for everything at Citi's scale"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2; do not hardcode connection strings inline
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redis port is 6380 (not 6379) — always use 6380

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

