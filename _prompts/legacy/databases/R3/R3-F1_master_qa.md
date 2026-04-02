SAVE AS: master_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing a comprehensive Staff-level interview Q&A reference covering the entire Databases curriculum (R1 through R3).

TASK: Generate 80 Q&A pairs spanning all database types and concepts covered in this curriculum. This is the master review document — every question should be interview-ready and cover the most important and commonly tested concepts. Group into 10 sections of 8 questions each.

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS AND COVERAGE:

Section 1 — Relational & SQL (Q1-8): MVCC, WAL, B-tree index internals, EXPLAIN ANALYZE, window functions, CTE vs subquery, VACUUM, pg_stat_statements

Section 2 — OLAP & Columnar (Q9-16): DuckDB vectorized execution, Snowflake micro-partitions + Time Travel, BigQuery on-demand vs slots, Redshift DISTKEY/SORTKEY, columnar compression (RLE + dictionary), OLAP vs OLTP identification, zone maps, Parquet predicate pushdown

Section 3 — Document Stores (Q17-24): MongoDB document model, embedding vs referencing, MongoDB aggregation pipeline, DynamoDB partition key design, DynamoDB hot partition, single-table design, MongoDB Atlas search vs Elasticsearch, schema-less tradeoffs

Section 4 — Key-Value & Cache (Q25-32): Redis data structures (string/hash/list/set/zset), cache-aside vs write-through vs write-behind, TTL and eviction policies (LRU vs LFU), Redis sorted set for leaderboards, Redis persistence (RDB vs AOF), cache stampede and prevention, Redis Cluster sharding, when KV store beats relational

Section 5 — Wide-Column (Q33-40): Cassandra partition key design, clustering key ordering, compaction strategies (STCS vs LCS), consistency levels (ONE vs QUORUM vs ALL), hinted handoff, tombstone accumulation, Cassandra vs HBase, why Cassandra has no joins

Section 6 — Graph & Time-Series (Q41-48): Neo4j native graph storage (index-free adjacency), Cypher MATCH vs SQL recursive CTE, graph algorithms (PageRank, shortest path), InfluxDB measurement/tag/field model, TimescaleDB hypertable, downsampling and retention policies, time-series vs relational for sensor data, when graph DB beats relational for relationships

Section 7 — Vector & Search (Q49-56): embedding model output dimensionality, ANN vs exact nearest neighbor (HNSW vs brute force), cosine similarity vs dot product vs Euclidean, Elasticsearch inverted index structure, BM25 relevance scoring, Elasticsearch shard sizing, pgvector vs Pinecone vs Elasticsearch kNN, RAG retrieval pattern

Section 8 — CDC & Pipelines (Q57-64): WAL-based CDC vs trigger-based vs polling, Debezium architecture, outbox pattern vs dual-write, idempotency key pattern, ETL vs ELT in cloud DW context, watermark-based incremental load, schema evolution in pipelines (additive vs breaking), pipeline SLA monitoring

Section 9 — Consistency & Replication (Q65-72): ACID isolation levels and anomalies prevented by each, MVCC non-blocking reads, CAP theorem — partition tolerance is non-negotiable, Cassandra tunable consistency W+R>RF, synchronous vs asynchronous replication tradeoff, Postgres WAL durability guarantee, RPO vs RTO definitions, Redis Sentinel vs Redis Cluster

Section 10 — Architecture & System Design (Q73-80): polyglot persistence operational complexity, database-per-service microservice pattern, two-phase commit cost, saga pattern, event sourcing with append-only stores, GDPR deletion across a polyglot stack, Lambda vs Kappa architecture, "right tool for the right job" — 3 questions to ask before choosing a DB

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown with clear section headers

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

