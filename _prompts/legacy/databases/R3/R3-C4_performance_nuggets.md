SAVE AS: performance_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets on database indexing and query performance.

TASK: Generate 12 performance gotcha nuggets covering index misuse, query planner traps, and tuning anti-patterns. Cover: composite index created as (metric_name, endpoint_id) but all queries filter on endpoint_id first making the index unusable, EXPLAIN cost of 1000 means nothing in milliseconds — engineers interpret it as 1 second and set wrong optimization targets, adding an index to a 500K-row table without CONCURRENTLY causing an 8-minute exclusive lock during business hours, stale table statistics after a bulk load causing the planner to estimate 100 rows when actual is 500K and choose nested loop join that runs for 20 minutes, work_mem set globally to 256MB × 200 connections = 51GB memory allocation causing OOM, autovacuum not keeping up with Citi's 10K metrics/second insert rate causing table bloat and dead tuple accumulation, NOT IN with a subquery returning NULLs silently returning zero rows instead of the expected filtered set, OR condition on two separately indexed columns causing both indexes to be ignored in favor of a SeqScan, LIKE '%cpu%' with leading wildcard bypassing the B-tree index entirely (only trailing wildcards use B-tree), pg_stat_statements not enabled in prod so there is no way to identify the query causing the CPU spike, Cassandra secondary index on low-cardinality column (severity has 4 values) causing full cluster scan on every read, Elasticsearch query on a text field for exact match aggregation returning incorrect counts because analyzed tokens differ from raw values.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

