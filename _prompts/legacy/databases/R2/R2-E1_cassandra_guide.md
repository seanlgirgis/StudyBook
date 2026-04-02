SAVE AS: cassandra_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep Cassandra guide notebook.

TASK: Cover Cassandra partition design, CQL query patterns, consistency levels, compaction strategies, and tombstones — all running live against the Citi telemetry Cassandra instance.

DATASET CONTEXT — do not deviate:
- Cassandra: localhost:9042, keyspace=telemetry
- metrics table: ~1M rows | PRIMARY KEY (endpoint_id UUID, recorded_at TIMESTAMP, metric_id UUID) CLUSTERING ORDER BY (recorded_at DESC) | fields: metric_name TEXT, value DOUBLE, unit TEXT
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026! (to cross-reference endpoint UUIDs)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Cassandra — Partition-First Design, Tunable Consistency, Write-Optimized"; explain the ring architecture, consistent hashing, vnodes; why writes are always O(1); why reads require partition key; CAP position (AP); ASCII diagram of data distribution across 3 nodes
2. Imports + setup (cassandra-driver with gevent reactor for Python 3.12, no pip install); cluster = Cluster(['localhost'], port=9042); session = cluster.connect('telemetry'); verify with SELECT COUNT(*) FROM metrics; print row count
3. Partition Key Design — SELECT metrics for one endpoint_id (fast path, partition key provided); explain why this is O(1); demonstrate what happens without partition key (ALLOW FILTERING — warning); design rule: partition key = query anchor; compute partition size for a busy endpoint (1M/10K endpoints = 100K rows/partition — discuss wide partition risk)
4. Clustering Key Patterns — SELECT latest 10 metrics for endpoint (ORDER BY recorded_at DESC LIMIT 10 — uses clustering order); SELECT metrics in time range (WHERE endpoint_id=? AND recorded_at >= ? AND recorded_at <= ?); explain why range queries on clustering key are efficient
5. Consistency Levels — run the same SELECT at ONE, QUORUM, ALL; time each; print latency table; explain what each level means with 3-replica RF=3; Citi framing: "Citi's telemetry reads use QUORUM — tolerates one node failure without stale data"
6. Compaction Strategies — explain SizeTieredCompactionStrategy (write-heavy) vs LeveledCompactionStrategy (read-heavy) vs TimeWindowCompactionStrategy (time-series); ALTER TABLE metrics WITH compaction = {'class': 'TimeWindowCompactionStrategy', 'compaction_window_size': '1', 'compaction_window_unit': 'DAYS'}; explain why TWCS is ideal for append-only time-series
7. Tombstones — DELETE 100 metric rows; explain tombstones accumulate until gc_grace_seconds (10 days default); SELECT tombstone_ratio from system.compaction_history conceptual demo; show how tombstone storms degrade read performance; fix: use TTL instead of DELETE for time-series data
8. What Just Happened — Cassandra vs DynamoDB vs HBase decision table; 4 interview Q&A; cleanup: no data deletion needed; print "Session closed"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use gevent reactor import pattern before Cluster import (required for Python 3.12)
- No ALLOW FILTERING except in the explicit warning demo cell
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

