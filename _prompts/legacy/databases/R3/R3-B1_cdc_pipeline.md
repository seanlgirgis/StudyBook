SAVE AS: cdc_pipeline.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a Change Data Capture (CDC) patterns notebook.

TASK: Demonstrate CDC concepts and patterns using Postgres logical replication output — simulating a real pipeline that propagates changes from Postgres (source of truth) to downstream stores (Redis cache, Elasticsearch search index) — using the Citi telemetry dataset.

DATABASE STACK (all pre-configured via db_connections.py):
- PostgreSQL  localhost:5432  de_admin/DeAdmin2026!  db=de_telemetry  schema=telemetry
- Redis       localhost:6380  password=DeRedis2026!
- Elasticsearch http://localhost:9200  elastic/DeElastic2026!

DATASET CONTEXT — do not deviate:
- endpoints: 10,000 rows | endpoint_id, hostname, datacenter, environment, service_type, ip_address, os, status, created_at
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, category, status, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

IMPORT PATTERN (use in cell 2):
```python
import sys
sys.path.insert(0, r"D:\Workspace\Basics\Databases\_setup")
from db_connections import get_postgres_conn, get_redis_conn, get_elasticsearch_client
```

SECTIONS:
1. Title + Mental Model — "CDC — Capturing Every Change Without Polling"; ASCII diagram: Postgres WAL → CDC reader → fan-out to Redis + Elasticsearch + S3; explain WAL-based vs trigger-based vs polling CDC; Debezium architecture overview (conceptual — no install required)
2. Imports + connection setup (import pattern above; connect all 3; print "CDC demo ready")
3. WAL Configuration — psycopg2 query: show wal_level; show max_replication_slots; show max_wal_senders; explain why wal_level=logical is required for Debezium; show how to check current setting and what to expect; explain that the Docker container may be at replica level (print actual value)
4. Simulating CDC Events — insert 5 new alerts into Postgres with explicit alert_ids (cdc_test_001 through cdc_test_005); update 3 existing endpoints (change status='inactive'); delete 2 alerts; query pg_stat_activity to show the changes; print "Source changes written: 5 inserts, 3 updates, 2 deletes"
5. CDC Consumer Simulation — write a Python class CitiCDCConsumer with methods on_insert(row), on_update(old_row, new_row), on_delete(row_id); implement each method to: on_insert → write to Elasticsearch index; on_update → update Redis hash; on_delete → remove from Redis; replay the 10 change events through the consumer; verify downstream state
6. Polling CDC Anti-Pattern — show a naive polling loop (SELECT * WHERE updated_at > last_checked); explain why it misses deletes, is slow on 500K rows, and creates load spikes at Citi scale; show pg_stat_user_tables.n_live_tup drift as evidence; contrast with WAL-based CDC
7. Outbox Pattern — create a telemetry.outbox table (event_id, table_name, operation, payload JSONB, processed BOOL, created_at); modify the alert insert to also write to outbox atomically in the same transaction; show the outbox being read and fanned out; explain why this guarantees at-least-once delivery
8. Idempotency — demonstrate the problem: replay the same 5 alert inserts through the consumer; show duplicate Elasticsearch docs; fix with doc_id=alert_id in ES index and upsert instead of index; re-replay; confirm no duplicates; explain idempotency key pattern
9. What Just Happened — CDC patterns comparison table: WAL vs trigger vs polling vs outbox; Debezium in production: what it adds beyond this demo; 4 interview Q&A; Citi framing: "CDC is how Citi keeps Redis and Elasticsearch in sync with Postgres without sacrificing write performance"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- Use import pattern above in cell 2
- Every code cell must execute top-to-bottom without error with the Docker stack running
- Redis port is 6380 (not 6379)
- Clean up test data at the end (DELETE from telemetry.outbox; DELETE alert_ids starting with 'cdc_test')

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

