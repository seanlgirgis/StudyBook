SAVE AS: sql_query_optimization_live.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a PostgreSQL query optimization lab notebook.

TASK: 10 live optimization drills on the Citi telemetry database — each shows the slow query, its EXPLAIN ANALYZE, the fix, and the after EXPLAIN ANALYZE. Every improvement must be measurable.

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Framework — "PostgreSQL Query Optimization — 10 Live Drills"; explain the optimization loop: measure → identify bottleneck → fix → measure again; how to read EXPLAIN ANALYZE (cost, actual time, rows, loops, buffers)
2. Setup — DROP INDEX IF EXISTS for any indexes created later; ANALYZE endpoints, metrics, alerts; confirm row counts
3. Drill 1 — Sequential scan on metrics: slow query (SELECT * FROM metrics WHERE metric_name = 'latency_ms'); EXPLAIN ANALYZE before; CREATE INDEX idx_metrics_name ON metrics(metric_name); EXPLAIN ANALYZE after; print speedup factor
4. Drill 2 — Missing join index: slow query (SELECT e.name, COUNT(a.*) FROM endpoints e JOIN alerts a ON e.endpoint_id = a.endpoint_id GROUP BY e.name); EXPLAIN ANALYZE before; CREATE INDEX idx_alerts_endpoint ON alerts(endpoint_id); EXPLAIN ANALYZE after
5. Drill 3 — Composite index vs single: slow query filtering on (region, status) together; single index first; composite index second; show composite wins on index-only scan
6. Drill 4 — Function on indexed column killing the index: WHERE UPPER(region) = 'APAC' vs WHERE region = 'APAC'; show index ignored vs used; fix with expression index CREATE INDEX ON endpoints(UPPER(region))
7. Drill 5 — LIKE prefix scan: WHERE name LIKE 'api-%' vs WHERE name LIKE '%api%'; show first uses index, second does seq scan; explain why
8. Drill 6 — N+1 query pattern: loop fetching alerts per endpoint (simulate 100 iterations); compare to single JOIN query; show query count and total time difference
9. Drill 7 — Aggregate pushdown: subquery vs window function for "rank endpoints by alert count within region"; show window function is faster; print actual times
10. Drill 8 — Partition pruning: create partitioned table metrics_partitioned by range(timestamp) with 4 partitions; INSERT 10K rows; show query with partition filter uses partition pruning vs full scan
11. Drill 9 — VACUUM and bloat: DELETE 10K metrics rows; check pg_stat_user_tables for n_dead_tup; VACUUM ANALYZE; show dead tuple count drop; explain AUTOVACUUM timing risk
12. Drill 10 — Connection pooling impact: run 50 sequential psycopg2 connections each doing 1 query; compare to 1 connection doing 50 queries; print total time difference; explain PgBouncer pattern
13. What Just Happened — summary table: drill, problem pattern, fix, speedup; Citi framing: "At 500K metrics/day, a missing index on endpoint_id costs Citi 40× query time — drill 1 is the most common production fix"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error
- Drop all created indexes in the final cleanup cell

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

