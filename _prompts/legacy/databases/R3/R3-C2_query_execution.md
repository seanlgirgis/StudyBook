SAVE AS: query_execution.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a query execution and performance tuning notebook.

TASK: Deep dive into query planning, EXPLAIN ANALYZE, statistics, and optimizer behavior in Postgres — then contrast with DuckDB vectorized execution — using the Citi telemetry dataset.

DATABASE STACK (all pre-configured via db_connections.py):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- DuckDB      in-memory, attaches Postgres as 'pg'

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id UUID PK, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id UUID FK, metric_name, value, unit, recorded_at
- alerts: 25,000 rows | alert_id UUID PK, endpoint_id UUID FK, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys, time, json
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_duckdb_conn
```

SECTIONS:
1. Title + Mental Model — "Query Execution — From SQL to Bytes"; Postgres query lifecycle: parse → rewrite → plan → execute; volcano model (iterator tree, pull-based); DuckDB vectorized model (push-based, SIMD batches); ASCII diagrams for both; why vectorized wins for analytics
2. Imports + connections (import pattern above; verify both; print "Query execution lab ready")
3. EXPLAIN ANALYZE Anatomy — run a complex query: SELECT e.datacenter, m.metric_name, AVG(m.value) FROM telemetry.endpoints e JOIN telemetry.metrics m ON e.endpoint_id = m.endpoint_id WHERE e.status = 'active' GROUP BY e.datacenter, m.metric_name ORDER BY AVG(m.value) DESC; capture EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON); parse and pretty-print key nodes: SeqScan, HashJoin, Aggregate; explain each cost component (startup vs total, rows, width, actual vs estimated)
4. Statistics & Row Estimation — run ANALYZE on metrics; query pg_stats for metric_name column (n_distinct, most_common_vals, histogram_bounds); show how planner uses n_distinct to estimate GROUP BY output size; demonstrate estimation error: a query where actual rows >> estimated rows; explain how stale statistics cause bad plans at Citi's insertion rate
5. Join Strategy Comparison — force each join type via SET enable_hashjoin/enable_mergejoin/enable_nestloop; run endpoints JOIN metrics (10K × 500K) with each; time and EXPLAIN each; print "Hash join: Xms | Merge join: Yms | Nested loop: Zms"; explain when each wins
6. Index vs SeqScan Crossover — show that for low-selectivity queries (e.g., WHERE datacenter = 'NYC1' returning 25% of rows), Postgres correctly chooses SeqScan over index scan; set enable_seqscan=off to force index scan; time both; explain why the planner's cost model is right; show the crossover selectivity threshold (~5-10%)
7. pg_stat_statements — enable pg_stat_statements (CREATE EXTENSION IF NOT EXISTS); run 10 different queries on the telemetry schema; query pg_stat_statements for top 5 by total_time; show mean_exec_time, calls, rows; explain how this is the #1 tool for identifying slow queries in production at Citi
8. DuckDB Vectorized vs Postgres Volcano — run the same aggregation (GROUP BY datacenter, metric_name with AVG, COUNT on 500K rows) on Postgres and DuckDB (via pg attach); time both 3 times; print comparison table; explain SIMD batch processing; explain why DuckDB wins for analytics but Postgres wins for OLTP
9. Query Rewrite Patterns — show 4 common slow query patterns and their rewrites: (a) SELECT * in subquery → SELECT only needed columns; (b) NOT IN with NULLs → NOT EXISTS; (c) correlated subquery → JOIN; (d) OR on indexed columns → UNION ALL; show EXPLAIN improvement for each; Citi framing
10. What Just Happened — query execution summary: volcano vs vectorized; the 5 EXPLAIN nodes every DE must recognize; 4 interview Q&A; Citi framing: "Understanding query execution lets Citi DE teams cut P95 query latency without buying more hardware"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

