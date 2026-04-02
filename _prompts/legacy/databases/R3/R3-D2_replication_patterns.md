SAVE AS: replication_patterns.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a replication and high availability patterns notebook.

TASK: Cover Postgres WAL/streaming replication concepts, Cassandra replication factor, and Redis persistence/HA modes — using system catalog queries and configuration inspection on the live Citi telemetry stack. No second database instance is needed — demonstrate via system views, configuration, and simulation.

DATABASE STACK (all pre-configured via db_connections.py):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Cassandra   localhost:9042  no auth  keyspace=telemetry
- Redis       localhost:6380  password=DeRedis2026!

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- metrics: 500,000 rows | endpoint_id, metric_name, value, unit, recorded_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys, time
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_cassandra_session, get_redis_conn
```

SECTIONS:
1. Title + Mental Model — "Replication — How Databases Survive Node Failures"; comparison diagram: Postgres primary/replica (WAL streaming), Cassandra peer-to-peer (RF=3), Redis primary/replica + Sentinel; explain synchronous vs asynchronous replication and the durability vs latency tradeoff
2. Imports + connections (import pattern above; verify all 3; print "Replication lab ready")
3. Postgres WAL Inspection — query pg_stat_replication (show no replicas in single-node Docker — explain what the output looks like with replicas); show wal_level, archive_mode, archive_command settings; query pg_current_wal_lsn() and pg_walfile_name(); calculate WAL generation rate: call pg_current_wal_lsn() before and after inserting 10K metrics rows; print "WAL generated: X MB for 10K metric inserts"
4. Postgres Replication Slots — CREATE REPLICATION SLOT demo_slot LOGICAL; query pg_replication_slots; explain what accumulates in a slot when consumer falls behind (WAL retention risk — disk fill); DROP REPLICATION SLOT demo_slot; explain why monitoring replication lag is critical in a CDC setup like Citi's telemetry pipeline
5. Postgres Point-in-Time Recovery Concept — explain PITR with WAL archiving: base backup + WAL segments = ability to restore to any second; show pg_backup_start/stop API; explain why RPO (recovery point objective) = WAL archive frequency and RTO (recovery time objective) = restore time; Citi scenario: "How much alert data can we afford to lose?"
6. Cassandra Replication Factor — query system_schema.keyspaces for the telemetry keyspace replication settings; show NetworkTopologyStrategy vs SimpleStrategy; explain RF=3: write goes to 3 nodes, read quorum requires 2 nodes; run DESCRIBE KEYSPACE telemetry via cassandra-driver; explain why RF < 3 in production is an anti-pattern; show how to calculate consistency window: W + R > RF
7. Cassandra Hinted Handoff & Repair — explain hinted handoff: when a replica is down, the coordinator holds the write hint and delivers it on recovery; show nodetool status equivalent via Python (cassandra-driver cluster metadata); explain anti-entropy repair (nodetool repair) for long-term consistency; Citi framing: metrics that missed a node during a brief outage are recovered automatically
8. Redis HA Patterns — compare 3 Redis HA modes: (a) standalone (current Docker setup — single point of failure); (b) Sentinel (automatic failover, no sharding); (c) Cluster (sharded, HA, complex); check current Redis server INFO replication section via r.info('replication'); show role, connected_slaves; explain that Citi's cache tier would use Sentinel and session store would use Cluster
9. What Just Happened — HA comparison table: DB → replication model → failover mechanism → RPO → RTO; 4 interview Q&A; Citi framing: "Citi's telemetry stack needs sub-60-second RTO for alerts — that requirement drives the HA architecture choice for each database tier"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redis port is 6380 (not 6379)

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

