SAVE AS: relational_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for relational databases.

TASK: Generate 40 Q&A pairs covering PostgreSQL internals, indexing, transactions, query optimization, and replication. Group into sections: MVCC and Storage (Q1-8), Indexes (Q9-16), Transactions and Isolation (Q17-24), Query Planning and Optimization (Q25-32), Replication and Partitioning (Q33-40).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: MVCC xmin/xmax mechanics, WAL purpose and crash recovery, VACUUM vs autovacuum timing, B-tree vs GIN vs BRIN index selection, partial indexes, index-only scans, covering indexes, isolation level anomalies (dirty read, non-repeatable read, phantom), deadlock detection and prevention, EXPLAIN ANALYZE output interpretation, query planner cost model, sequential scan vs index scan decision, parallel query, table partitioning strategies (range vs hash vs list), logical vs streaming replication, read replicas for analytics offload.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

