SAVE AS: relational_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for PostgreSQL.

TASK: Generate 12 PostgreSQL gotcha nuggets. Cover: NULL values not stored in B-tree indexes (IS NULL query ignores index), LIKE '%prefix' not using index (leading wildcard), autovacuum not running during long transactions (table bloat accumulates), SERIAL vs IDENTITY (SERIAL leaves orphaned sequence on table drop), ILIKE forces seq scan (use citext extension or functional index), UPDATE causing table bloat (dead tuples not reclaimed until VACUUM), index on timestamp column not used when cast to date in WHERE clause, max_connections exhausted by idle connections (use PgBouncer), EXPLAIN ANALYZE materializes CTEs by default in Postgres <12, parallel query disabled on small tables by default (min_parallel_table_scan_size), foreign key without index causes seq scan on child table, partition pruning requires literal value (not function result).

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know Postgres
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

