SAVE AS: master_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing a comprehensive gotcha nuggets master reference covering the entire Databases curriculum (R1 through R3).

TASK: Generate 60 gotcha nuggets — the most dangerous, interview-critical, and production-incident-causing traps across all database types and concepts. This is the master gotcha reference. Group into 10 sections of 6 nuggets each.

Every nugget must be Citi-framed.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:

Section 1 — Relational & SQL (6 nuggets): NOT IN with NULLs returning zero rows, LIKE with leading wildcard bypassing index, adding NOT NULL column without default locks the table, EXPLAIN cost is not milliseconds, autovacuum not keeping up with high insert rate causing table bloat, SELECT * in a JOIN pulling all 500K metric columns when only 2 are needed

Section 2 — OLAP & Columnar (6 nuggets): Snowflake warehouse left running burning credits, BigQuery unpartitioned table full scan on every query, Redshift DISTKEY mismatch causing broadcast join, DuckDB in-memory losing data on process exit, Snowflake Time Travel on large table doubling storage cost, Redshift VACUUM not running automatically degrading sort order

Section 3 — Document Stores (6 nuggets): MongoDB document growing beyond 16MB limit, DynamoDB hot partition from sequential endpoint_id as partition key, MongoDB missing index on a nested field causing full collection scan, DynamoDB on-demand pricing spike from a query with no partition key filter (full table scan), embedding unbounded arrays in MongoDB documents causing document growth beyond the 16MB cap, MongoDB aggregation $lookup joining two large collections behaving like a nested loop join

Section 4 — Key-Value & Cache (6 nuggets): Redis used as primary store with no TTL causing memory exhaustion, cache stampede on Redis TTL expiry of a hot endpoint key, Redis port 6379 conflict with native Windows service (use 6380), Redis KEYS * command blocking the server on a 10K-key dataset, cache-aside with no TTL serving stale endpoint status 3 hours after decommission, Redis Cluster MOVED error not handled by application causing 2% of requests to fail silently

Section 5 — Wide-Column (6 nuggets): Cassandra tombstone accumulation causing read timeouts on deleted alert history, querying Cassandra without partition key triggering a full cluster scan, Cassandra RF=1 in production losing data permanently when the one node fails, Cassandra secondary index on low-cardinality severity column causing cluster-wide fan-out reads, Cassandra light-weight transactions (IF NOT EXISTS) bypassing the async write path and causing latency spikes, gevent reactor not initialized before Cassandra driver import causing "already started" error on Python 3.12

Section 6 — Graph & Time-Series (6 nuggets): Neo4j unbounded variable-length path query (MATCH p=()-[*]->()) causing OOM on 10K-node graph, InfluxDB retention policy set to infinite causing disk exhaustion after 6 months, TimescaleDB hypertable chunk_time_interval too small creating thousands of tiny chunks degrading performance, Neo4j Cypher MATCH without WHERE clause returning all 10K nodes as a Cartesian product, InfluxDB tag with high cardinality (using endpoint_id as a tag instead of field) causing series explosion, time-series data stored in Postgres without partitioning causing seq scan across 500K rows for every dashboard query

Section 7 — Vector & Search (6 nuggets): Elasticsearch text field used for exact-match aggregation returning wrong counts due to tokenization, Elasticsearch shard count set too high (1 shard per document) causing overhead exceeding query time, pgvector cosine similarity without normalization returning misleading results for variable-length text embeddings, Elasticsearch index with no replica in production — single shard failure makes index unavailable, HNSW index ef_construction set too low causing poor recall (fast build, low accuracy), vector search returning semantically similar but contextually wrong results because the embedding model was trained on a different domain

Section 8 — CDC & Pipelines (6 nuggets): Debezium replication slot growing unbounded filling Postgres disk, dual-write to Postgres and Elasticsearch with no transaction causing divergence on failure, pipeline watermark stored in memory resetting on restart causing full re-extract, Parquet written without explicit schema causing UUID to be inferred as string breaking downstream joins, pipeline success measured by exit code not row count masking zero-row loads, incremental load using updated_at missing hard deletes so deleted rows persist in the warehouse forever

Section 9 — Consistency & Replication (6 nuggets): Postgres replica promoted to primary while old primary recovers causing split-brain and duplicate alert inserts, replication slot left unmonitored accumulating 50GB of WAL and halting Postgres writes, Redis AOF disabled meaning a crash loses the last hour of cache writes, Cassandra CONSISTENCY ALL causing every read to fail when any replica is temporarily unavailable, PITR WAL archive job silently failing for 3 weeks not discovered until a real recovery attempt, write skew at REPEATABLE READ allowing two transactions to both resolve the last open critical alert

Section 10 — Architecture & Selection (6 nuggets): choosing Cassandra for a use case requiring multi-row transactions leading to silent partial writes, using Postgres for everything until 500M rows causes full table scans that kill the prod API, Elasticsearch used as primary store losing data on index corruption with no durable source, two-phase commit blocking all participants when one slow node causes cascading timeout in the alert pipeline, polyglot stack with 6 databases where no engineer understands all 6 causing blind spots in incident response, cache-aside pattern with no TTL serving stale Citi endpoint registry data for hours after a topology change

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into every nugget
- Valid GitHub Flavored Markdown with clear section headers

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

