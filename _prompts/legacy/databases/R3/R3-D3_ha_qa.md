SAVE AS: ha_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A on consistency, replication, and high availability.

TASK: Generate 30 Q&A pairs covering ACID isolation levels, consistency models, replication, and HA patterns. Group into sections: ACID & Isolation (Q1-8), Consistency Models (Q9-14), Replication Mechanics (Q15-22), High Availability & Recovery (Q23-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: the 4 ACID properties and which databases guarantee all 4, difference between READ COMMITTED and REPEATABLE READ (phantom reads), write skew anomaly and why SERIALIZABLE prevents it (serialization graph), why most production systems use READ COMMITTED not SERIALIZABLE (performance cost), MVCC (Multi-Version Concurrency Control) — how Postgres implements non-blocking reads, Cassandra tunable consistency — how W + R > RF guarantees strong consistency, eventual consistency definition — not "data is eventually wrong" but "replicas converge given no new writes", synchronous vs asynchronous replication — durability vs latency tradeoff, Postgres WAL (Write-Ahead Log) — why writing to WAL before data files guarantees durability, replication lag — how to measure and what happens to reads during lag, Postgres logical vs physical replication — what each replicates and when to choose each, Cassandra hinted handoff — how it handles temporary node failure, read-your-writes consistency and why it fails at Cassandra CONSISTENCY ONE, RPO vs RTO definitions and how they drive HA architecture choices, active-active vs active-passive failover tradeoffs, Redis Sentinel vs Redis Cluster — when to choose each, connection pooling necessity at scale (PgBouncer, why direct connections fail at 1000+ clients), Aurora global database and Spanner TrueTime as solutions to cross-region consistency.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

