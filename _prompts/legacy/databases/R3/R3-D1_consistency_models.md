SAVE AS: consistency_models.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a consistency models and ACID isolation notebook.

TASK: Demonstrate ACID isolation levels in Postgres, eventual consistency in Cassandra, and Redis persistence modes — making the abstract concrete with live demos using the Citi telemetry dataset.

DATABASE STACK (all pre-configured via db_connections.py):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Cassandra   localhost:9042  no auth  keyspace=telemetry
- Redis       localhost:6380  password=DeRedis2026!

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys, time, threading
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_cassandra_session, get_redis_conn
```

SECTIONS:
1. Title + Mental Model — "Consistency Models — From ACID to BASE"; spectrum diagram: strict serializability → serializable → repeatable read → read committed → read uncommitted → eventual consistency; map each DB in the stack to its position; explain why most apps use READ COMMITTED (sweet spot)
2. Imports + connections (import pattern above; verify all 3; print "Consistency lab ready")
3. READ COMMITTED Demo — open two Postgres connections (conn1, conn2); conn1: BEGIN, UPDATE alert status to 'acknowledged' for 100 alerts, do not commit; conn2: SELECT COUNT(*) WHERE status='acknowledged' (should see original count — dirty reads blocked); conn1: COMMIT; conn2: re-query (now sees updated count); print "READ COMMITTED: dirty reads blocked ✓"
4. REPEATABLE READ Demo — conn1: SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; SELECT COUNT(*) FROM alerts WHERE severity='critical'; conn2 (separate): INSERT 5 new critical alerts and COMMIT; conn1: re-SELECT COUNT(*) (should return same count — phantom reads blocked in RR); conn1: COMMIT; print "REPEATABLE READ: phantom reads blocked ✓"
5. Serializable Demo — demonstrate a write skew scenario with two transactions both reading 'open' alerts and both deciding to close the last one; show the anomaly at REPEATABLE READ; re-run at SERIALIZABLE level (one transaction aborts with serialization failure); print "SERIALIZABLE: write skew prevented ✓ — at cost of serialization retry"
6. Cassandra Consistency Levels — write 5 alerts with CONSISTENCY ONE, QUORUM, ALL; time each; read back with matching levels; demonstrate tunable consistency: use CONSISTENCY ONE for write + CONSISTENCY ONE for read (fastest, possible stale read); use QUORUM+QUORUM (strong consistency, higher latency); print comparison table; explain Citi telemetry uses ONE for metrics (acceptable staleness) but QUORUM for alert status changes
7. Cassandra Read-Your-Writes — demonstrate the read-your-writes problem at CONSISTENCY ONE: write an alert update, immediately read it back (may return stale value from a different replica); fix with LOCAL_QUORUM; explain why Cassandra's eventual consistency is a feature for write-heavy telemetry but a bug for alert acknowledgement workflows
8. Redis Persistence Modes — show CONFIG GET save (RDB snapshots); show CONFIG GET appendonly (AOF); demonstrate: write 100 endpoint hashes to Redis; explain what is lost if Redis crashes between RDB snapshots vs with AOF every-second vs AOF always; trade-off table: RDB=fast restart, AOF=durable, AOF-always=slowest; Citi framing: Redis cache is acceptable with RDB, but Redis as session store needs AOF
9. What Just Happened — consistency model comparison table: DB → model → isolation level → when to use; 4 interview Q&A; Citi framing: "Citi's alert pipeline needs ACID for status transitions but accepts eventual consistency for metric aggregations — choosing the right model per workload is a core DE skill"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redis port is 6380 (not 6379)
- Clean up test data: reset any modified alert statuses at end

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

