SAVE AS: performance_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A on database indexing and query performance.

TASK: Generate 30 Q&A pairs covering index types, query planning, statistics, and performance tuning. Group into sections: Index Internals (Q1-8), Query Planner & Statistics (Q9-14), Join Strategies (Q15-20), Performance Tuning Patterns (Q21-26), Cross-DB Performance (Q27-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: B-tree index structure (balanced tree, O(log n) lookup, why it handles range queries), hash index vs B-tree (hash is O(1) equality but no range), GIN index for array and full-text (inverted posting lists), BRIN index for naturally ordered columns (min/max per page range, tiny size), partial index reducing bloat on filtered queries, composite index column order (most selective first vs leading column rule), index-only scan vs index scan vs bitmap index scan, when Postgres chooses SeqScan over index scan (low selectivity threshold ~5%), VACUUM and autovacuum impact on index bloat, pg_stat_statements for production query profiling, EXPLAIN ANALYZE cost units (not milliseconds — arbitrary planner units), actual rows vs estimated rows discrepancy causing bad plans, ANALYZE frequency and why stale statistics hurt at high insert rates, hash join vs merge join vs nested loop — when each wins, work_mem impact on sort and hash join (spill to disk), DuckDB vectorized execution vs Postgres volcano model for analytics, Redshift sort key zone maps (block-level min/max pruning), Elasticsearch inverted index vs Postgres full-text GIN, Cassandra partition key as the only efficient access path, connection pooling (PgBouncer) and why direct connections at scale exhaust shared_buffers.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

