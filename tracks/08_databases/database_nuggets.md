# database_nuggets.md
# Database Mastery — Field Manual
# Sean Girgis | Dallas, TX | Senior Data Engineer / AI Architect
# Maintained by Claude Code

> **Simplicity and clarity is Gold.**
> Things the docs buried. One tight insight per entry.
> Append-only. Never delete. Date-stamped.

---

## HOW TO ADD A NUGGET

Open Claude Code and say:
> *"Read prompts/agent_rules.md. Append this nugget to Basics/Databases/database_nuggets.md. Update the TOC."*

Then describe the nugget. Claude Code handles the rest.

---

## TABLE OF CONTENTS

### Cassandra
<a id="toc-cassandra--python-312--windows--cassandra-driver-connection-fix"></a>
- [Cassandra — Python 3.12 / Windows — cassandra-driver connection fix](#cassandra--python-312--windows--cassandra-driver-connection-fix)
<a id="toc-cassandra--allow-filtering--single-partition-vs-full-cluster-scan"></a>
- [Cassandra — ALLOW FILTERING — Single-Partition vs Full-Cluster Scan](#cassandra--allow-filtering--single-partition-vs-full-cluster-scan)

### DuckDB
<a id="toc-duckdb--attached-postgres--wire-protocol-caveat"></a>
- [DuckDB — Attached Postgres — Wire Protocol Caveat](#duckdb--attached-postgres--wire-protocol-caveat)

### PostgreSQL
*(none yet)*

### Redis
<a id="toc-redis--lpush--ltrim--bounded-queue-pattern"></a>
- [Redis — LPUSH + LTRIM — Bounded Queue Pattern](#redis--lpush--ltrim--bounded-queue-pattern)

### Neo4j
<a id="toc-neo4j--variable-length-paths--cypher-1-2-vs-sql-recursive-cte"></a>
- [Neo4j — Variable-Length Paths — Cypher `*1..2` vs SQL Recursive CTE](#neo4j--variable-length-paths--cypher-12-vs-sql-recursive-cte)

### InfluxDB
<a id="toc-influxdb--flux-sort-limit-is-per-series-not-global"></a>
- [InfluxDB — Flux sort()+limit() is per-series, not global](#influxdb--flux-sortlimit-is-per-series-not-global)
<a id="toc-influxdb--tag-cardinality-explosion"></a>
- [InfluxDB — Tag Cardinality Explosion](#influxdb--tag-cardinality-explosion)

### Elasticsearch
*(none yet)*

### MongoDB
*(none yet)*

### General / Architecture
*(none yet)*

---
---

<!-- ============================================================ -->
<!--                        NUGGETS START                         -->
<!-- ============================================================ -->

---

## Cassandra — Python 3.12 / Windows — cassandra-driver connection fix
**Date added:** 2026-03-23
**Tags:** `cassandra` `python-3.12` `windows` `asyncio` `gevent` `driver` `jupyter` `pyasyncore` `asyncore`

### The Story
Python 3.12 removed the `asyncore` module entirely. `cassandra-driver` uses it as the default
connection class — so on 3.12, importing the driver silently breaks. The driver then falls
back to libev (not installed on Windows) and dies. Even if you patch that, the asyncio reactor
on Windows uses `IocpProactor` which immediately closes Cassandra connections with no error message.
Raw TCP to port 9042 works fine (Cassandra is up) — the problem is entirely inside the driver.

### Root Cause Chain
```
Python 3.12 removes asyncore
  → cassandra-driver module-level init fails to detect default connection class
  → falls back to asyncio reactor
  → Windows asyncio uses IocpProactor
  → IocpProactor closes the connection immediately after STARTUP frame
  → connect_timeout fires → NoHostAvailable
```

### The Fix
```python
# pip install gevent  ← do this once
import gevent.monkey
gevent.monkey.patch_all()

from cassandra.io.geventreactor import GeventConnection
from cassandra.cluster import Cluster

cluster = Cluster(
    ["127.0.0.1"],
    port=9042,
    connection_class=GeventConnection,   # ← bypass asyncio reactor entirely
    connect_timeout=30,
    control_connection_timeout=30,
)
session = cluster.connect()
```

### What Does NOT Work
```python
# ❌ asyncio reactor — IocpProactor kills the connection silently
# ❌ WindowsSelectorEventLoopPolicy() — still fails, different symptom
# ❌ shim cassandra.io.asyncorereactor → AsyncioConnection — still hits IocpProactor
# ✅ gevent reactor — bypasses asyncio entirely, works cleanly
```

### Quick Verification
```python
# Verify Cassandra is actually up before blaming the driver:
import socket, struct
s = socket.create_connection(("127.0.0.1", 9042), timeout=5)
# CQL v4 OPTIONS frame: version=4, flags=0, stream=0, opcode=5, length=0
s.sendall(b"\x04\x00\x00\x00\x05\x00\x00\x00\x00")
resp = s.recv(9)
# opcode byte is at index 4; 0x06 = SUPPORTED → Cassandra is alive
print("opcode:", hex(resp[4]))  # expect 0x6
s.close()
```

### Real-World Hook
Any Python 3.12+ project on Windows hitting Cassandra needs this fix.
In a Citi DE stack, Cassandra holds 500K+ time-series metrics rows — you can't skip it.
Add `pip install gevent` to requirements and set `connection_class=GeventConnection`
in every `Cluster()` call.

### Cleaner Fix (Jupyter-compatible)

The gevent fix works from scripts but breaks Jupyter kernels — `gevent.monkey.patch_all()` replaces Python threading internals and trips Jupyter's thread assertions on connect (`AssertionError: current_thread().name == SHELL_CHANNEL_THREAD_NAME`).

The cleaner solution: `pip install pyasyncore` — this restores the `asyncore` module that Python 3.12 removed. The cassandra-driver finds `AsyncoreConnection` through its normal fallback chain. No monkey-patching, no Jupyter conflict, works in both scripts and notebooks.

```python
# pyasyncore installs itself as the 'asyncore' module — import asyncore, not pyasyncore
import asyncore  # pip install pyasyncore restores this; cassandra-driver finds AsyncoreConnection
from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"], port=9042)
session = cluster.connect()
```

| Approach | Scripts | Jupyter | Notes |
|---|---|---|---|
| `gevent` + `GeventConnection` | ✓ | ✗ | Breaks `SHELL_CHANNEL_THREAD_NAME` assertion |
| `import pyasyncore` | ✓ | ✓ | Restores asyncore; driver uses normal fallback |

[↑ Back to TOC](#toc-cassandra--python-312--windows--cassandra-driver-connection-fix)

---

## DuckDB — Attached Postgres — Wire Protocol Caveat
**Date added:** 2026-03-23
**Tags:** `duckdb` `postgres` `attach` `performance` `columnar` `wire-protocol` `parquet`

### The Story
DuckDB can attach to a live Postgres instance and query it with SQL — impressive party trick.
But when you run `ATTACH '...' AS pg (TYPE postgres)`, DuckDB fetches data through the
**Postgres wire protocol**. It doesn't read Postgres's on-disk columnar pages directly.
For analytical queries that scan millions of rows, DuckDB still has to pull all that data
over the socket before it can do its vectorized magic. The speedup (if any) comes from
DuckDB's execution engine, not from reading less data.

### Pattern
```python
# ── WHAT HAPPENS UNDER THE HOOD ──────────────────────────────
# 1. DuckDB issues a SQL query to Postgres over a libpq connection
# 2. Postgres executes it (with its own planner, indexes, row storage)
# 3. Postgres returns rows in wire format
# 4. DuckDB receives them, runs its aggregation layer
#
# You get DuckDB's executor on top of Postgres's I/O — not columnar I/O.
```

### Quick Examples
```python
import duckdb, os

duck = duckdb.connect(":memory:")
duck.execute("INSTALL postgres; LOAD postgres;")

pg_dsn = (
    f"host=localhost port={os.getenv('POSTGRES_PORT', 5432)} "
    f"dbname={os.getenv('POSTGRES_DB')} "
    f"user={os.getenv('POSTGRES_USER')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)
duck.execute(f"ATTACH '{pg_dsn}' AS pg (TYPE postgres, READ_ONLY);")

# This runs on Postgres's row storage, not DuckDB's columnar engine:
duck.execute("SELECT COUNT(*) FROM pg.telemetry.metrics").fetchone()

# THIS is where DuckDB shines — local Parquet, zero network, pure columnar:
duck.execute("SELECT COUNT(*) FROM 'metrics.parquet'").fetchone()
```

### The Real Benchmark (Round 2)
```
Attached Postgres query (500K rows, GROUP BY):   ~800ms   ← Postgres did the work
Local Parquet query   (500K rows, GROUP BY):     ~40ms    ← DuckDB columnar I/O
```
DuckDB over attached Postgres ≈ Postgres speed + slight overhead.
DuckDB over local Parquet = 10–20× faster than Postgres on aggregations.

### When Attached Postgres IS Useful
- Ad-hoc cross-source joins: `FROM pg.telemetry.endpoints JOIN 'local.parquet' USING (id)`
- Exporting Postgres tables to Parquet: `COPY (SELECT * FROM pg.telemetry.metrics) TO 'metrics.parquet'`
- One-time migrations without writing a Python ETL script

### Real-World Hook
At Citi, DE pipelines land data in S3 as Parquet. DuckDB querying S3 Parquet directly
(via `httpfs` extension) is the right tool — not DuckDB-over-RDS. Know the difference
before you benchmark and wonder why it's not faster.

[↑ Back to TOC](#toc-duckdb--attached-postgres--wire-protocol-caveat)

---

## Redis — LPUSH + LTRIM — Bounded Queue Pattern
**Date added:** 2026-03-23
**Tags:** `redis` `list` `lpush` `ltrim` `queue` `bounded` `pattern` `cache`

### The Story
Redis has no built-in "keep only last N items" operation — but two commands together give you exactly that, atomically. `LPUSH` adds the new item to the head of the list. `LTRIM` immediately cuts the list to indices `0..N-1`, dropping anything beyond N. Both commands on every write. No separate cleanup job, no cron, no size check.

### Pattern
```python
# ── PATTERN ──────────────────────────────────────────
r.lpush("recent:critical_alerts", new_item)
r.ltrim("recent:critical_alerts", 0, 9)   # keep last 10, drop the rest
# LLEN will now always return ≤ 10
```

### Quick Examples
```python
import redis, json

r = redis.Redis(host="localhost", decode_responses=True)
r.delete("recent:critical_alerts")

for i in range(15):
    item = json.dumps({"id": f"alert_{i:03d}", "host": f"srv-{i:05d}.citi.internal"})
    r.lpush("recent:critical_alerts", item)
    r.ltrim("recent:critical_alerts", 0, 9)   # cap at 10

print(r.llen("recent:critical_alerts"))   # 10 — never more
items = r.lrange("recent:critical_alerts", 0, -1)
for it in items:
    print(json.loads(it))

# Simplicity and clarity is Gold
```

### Real-World Hook
Three places this shows up in DE work:

1. **Recent-events log** — last 10 alerts per endpoint, always fresh, zero cleanup overhead.
2. **Sliding window rate limiter** — store timestamps of last N requests; `LTRIM` keeps only the window; `LLEN` tells you instantly whether the limit is hit.
3. **Activity feed** — last 50 actions per user; `LPUSH + LTRIM` on every write; no background GC needed.

[↑ Back to TOC](#toc-redis--lpush--ltrim--bounded-queue-pattern)

---

## Cassandra — ALLOW FILTERING — Single-Partition vs Full-Cluster Scan
**Date added:** 2026-03-23
**Tags:** `cassandra` `cql` `allow-filtering` `partition-key` `performance` `scan`

### The Story
Cassandra refuses queries that would fan out to every node unless you explicitly add `ALLOW FILTERING`. The error message is the same whether your query would hit 1 partition or 10,000 nodes — Cassandra doesn't tell you which case you're in. That makes it easy to cargo-cult "never use ALLOW FILTERING" and over-restrict yourself, or to misread the message and accidentally trigger a full-cluster scan.

The actual cost depends entirely on whether the partition key is in the `WHERE` clause:

| WHERE clause | What Cassandra does | Cost |
|---|---|---|
| No partition key | Fans out to every node, scans everything | Expensive — avoid in prod |
| Partition key present | Scans only that one partition on one node | Cheap — fine to use |

### Pattern
```python
# ── EXPENSIVE — no partition key, full cluster scan ──────────
session.execute(
    "SELECT * FROM telemetry.metrics WHERE metric_name = 'cpu_percent' ALLOW FILTERING"
)
# Cassandra asks every node for matching rows. Cost grows with cluster size.

# ── CHEAP — partition key present, single-partition scan ─────
session.execute(
    "SELECT * FROM telemetry.metrics "
    "WHERE endpoint_id = %s AND metric_name = 'cpu_percent' ALLOW FILTERING",
    (endpoint_id,)
)
# Cassandra routes to exactly one node. ALLOW FILTERING only scans that partition.
```

### Quick Examples
```python
# Simulating the two cases
import uuid

# Bad: no partition key — remove ALLOW FILTERING from prod, add a secondary index
session.execute(
    "SELECT COUNT(*) FROM telemetry.metrics "
    "WHERE metric_name = 'cpu_percent' ALLOW FILTERING"
)

# Fine: partition key scopes the scan to one endpoint's data
endpoint_id = "some-uuid-here"
session.execute(
    "SELECT metric_name, value, recorded_at "
    "FROM telemetry.metrics "
    "WHERE endpoint_id = %s AND metric_name = 'cpu_percent' ALLOW FILTERING",
    (endpoint_id,)
)

# Simplicity and clarity is Gold
```

### Real-World Hook
In a Citi metrics pipeline, filtering `cpu_percent` rows for one endpoint with `ALLOW FILTERING` is fine — it scans 50–100 rows on one node. Filtering `cpu_percent` across all endpoints with no partition key scans 1M+ rows across every Cassandra node in the ring. Same error message before you add `ALLOW FILTERING`. Know which one you're writing.

[↑ Back to TOC](#toc-cassandra--allow-filtering--single-partition-vs-full-cluster-scan)

---

## Neo4j — Variable-Length Paths — Cypher `*1..2` vs SQL Recursive CTE
**Date added:** 2026-03-23
**Tags:** `neo4j` `cypher` `graph` `variable-length` `path` `recursive-cte` `sql` `system-design`

### The Story
Cypher `*1..2` on a relationship means "follow this edge between 1 and 2 hops." SQL needs a recursive CTE for each hop level, with an explicit anti-cycle guard, and a depth limit baked into the anchor/recursive terms. `*1..10` in Cypher is one token. In SQL it's 30 lines and a prayer. Know the difference before a system design interview asks "how would you find all downstream dependencies?"

### Pattern
```cypher
// ── CYPHER — any depth, one line ─────────────────────────────
MATCH (e:Endpoint {endpoint_id: $eid})-[:DEPENDS_ON*1..10]->(dep:Endpoint)
RETURN DISTINCT dep.hostname AS dependency

// Change *1..10 to *1..2 for 2 hops, *1.. for unbounded (careful — may not terminate on cycles)
```

### SQL Equivalent (the 30-line prayer)
```sql
-- ── SQL — recursive CTE for the same 2-hop query ─────────────
WITH RECURSIVE deps AS (
    -- anchor: direct dependencies
    SELECT to_endpoint_id AS dep_id, 1 AS depth
    FROM endpoint_dependencies
    WHERE from_endpoint_id = $eid

    UNION ALL

    -- recursive: one more hop
    SELECT d.to_endpoint_id, deps.depth + 1
    FROM endpoint_dependencies d
    JOIN deps ON deps.dep_id = d.from_endpoint_id
    WHERE deps.depth < 2           -- depth limit (baked in, not a parameter)
      AND d.to_endpoint_id != $eid -- anti-cycle guard (incomplete — only catches self-loops)
)
SELECT DISTINCT dep_id FROM deps;
-- Anti-cycle guard above is wrong for general cycles — full fix needs a visited array,
-- which PostgreSQL supports with arrays but it's another 10 lines.
```

### Quick Examples
```cypher
// 1 hop (direct deps only)
MATCH (e:Endpoint {endpoint_id: $eid})-[:DEPENDS_ON*1..1]->(dep) RETURN dep.hostname

// Up to 3 hops
MATCH (e:Endpoint {endpoint_id: $eid})-[:DEPENDS_ON*1..3]->(dep) RETURN DISTINCT dep.hostname

// Unbounded — finds ALL reachable nodes (Neo4j handles cycles internally)
MATCH (e:Endpoint {endpoint_id: $eid})-[:DEPENDS_ON*]->(dep) RETURN DISTINCT dep.hostname

// Simplicity and clarity is Gold
```

### Real-World Hook
System design interview question: *"Service A depends on B and C. B depends on D. If D goes down, which services are affected?"*
Cypher answer: `MATCH (d {name:'D'})<-[:DEPENDS_ON*]-(affected) RETURN affected.name`
SQL answer: recursive CTE with visited-array anti-cycle guard, depth limit, and a 10-minute whiteboard session.
Use the right tool. If your data is a graph, model it as a graph.

[↑ Back to TOC](#toc-neo4j--variable-length-paths--cypher-12-vs-sql-recursive-cte)

---

## InfluxDB — Flux sort()+limit() is per-series, not global
**Date added:** 2026-03-23
**Tags:** `influxdb` `flux` `sort` `limit` `per-series` `gotcha`

### The Story
In SQL, `ORDER BY col DESC LIMIT 10` gives you the global top 10 rows across the entire result set. In Flux, `sort()` and `limit()` operate *per table* (per series). If your data has 5 `metric_name` series, `limit(n: 2)` returns 2 rows from each series — up to 10 rows total, not the global top 2. The query runs without error; it just silently returns wrong results. To get a true global top-N you must `group()` all series into one table first, then sort and limit.

### Pattern
```flux
// ── PATTERN ──────────────────────────────────────────

// ❌ Wrong — per-series limit, not global top 5
from(bucket: "telemetry")
  |> range(start: -1d)
  |> filter(fn: (r) => r._measurement == "metrics")
  |> sort(columns: ["_value"], desc: true)
  |> limit(n: 5)
  // Returns up to 5 rows from EACH series — could be 25 rows total

// ✅ Correct — merge all series first, then global top 5
from(bucket: "telemetry")
  |> range(start: -1d)
  |> filter(fn: (r) => r._measurement == "metrics")
  |> group()                                  // ← collapses all series into one table
  |> sort(columns: ["_value"], desc: true)
  |> limit(n: 5)
  // Returns exactly 5 rows across all series combined
```

### Quick Examples
```python
# In Python — detect the problem by checking row count
tables = query_api.query(wrong_query, org=org)
rows = [r for t in tables for r in t.records]
print(len(rows))   # if > 5, your limit(n:5) is per-series, not global

# Fix: add |> group() before |> sort() in your Flux query

# Simplicity and clarity is Gold
```

### Real-World Hook
Dashboards showing "top 5 highest CPU endpoints" will silently return wrong results if `group()` is missing — one result per metric type instead of the global top 5. At Citi, an ops dashboard built on this pattern would show the wrong "most loaded server" during an incident. The query looks correct and completes fast; the data is just wrong.

[↑ Back to TOC](#toc-influxdb--flux-sortlimit-is-per-series-not-global)

---

## InfluxDB — Tag Cardinality Explosion
**Date added:** 2026-03-23
**Tags:** `influxdb` `tags` `cardinality` `performance` `schema-design`

### The Story
Tags in InfluxDB are indexed. Every unique combination of tag values creates a new *series* in the time-series index. If you tag with a UUID field that has 10 million distinct values, you get 10 million index entries — InfluxDB's memory usage grows linearly with series cardinality, not data volume. This is called *cardinality explosion* and it is the most common InfluxDB production incident. The rule: tags should have LOW cardinality (datacenter = 4 values, metric_name = 5 values). Fields hold HIGH cardinality values (the raw UUID, the raw measurement).

### Pattern
```python
# ── PATTERN ──────────────────────────────────────────
from influxdb_client import Point

# ❌ Wrong — UUID as tag = new series per request = OOM
write_api.write(bucket="telemetry", record=Point("metrics")
    .tag("request_id", str(uuid.uuid4()))   # millions of distinct values
    .field("latency_ms", 42.5))

# ✅ Correct — UUID as field, low-cardinality identifiers as tags
write_api.write(bucket="telemetry", record=Point("metrics")
    .tag("endpoint_id", endpoint_id)        # ~10K distinct values, stable
    .tag("metric_name", "cpu_percent")      # ~5 distinct values
    .field("value", 72.5)
    .field("request_id", str(uuid.uuid4()))) # high-cardinality → field, not tag
```

### Quick Examples
```python
# Check series cardinality in a bucket (InfluxDB 2.x)
# High number = investigate your tag schema
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
query_api = client.query_api()
result = query_api.query('import "influxdata/influxdb" influxdb.cardinality(bucket: "telemetry")', org=org)
for t in result:
    for r in t.records:
        print("Series cardinality:", r.get_value())
# < 100K = healthy. > 1M = investigate. > 10M = incident waiting to happen.

# Simplicity and clarity is Gold
```

### Real-World Hook
At Citi, `endpoint_id` (10K values) is safe as a tag. `alert_id` (25K unique UUIDs, one per alert) must be a field. Getting this wrong at 3K writes/second will exhaust InfluxDB memory within hours and trigger a `too many series` error that requires a full database rebuild to fix. Design the tag schema before writing the first point — it cannot be changed without dropping the measurement.

[↑ Back to TOC](#toc-influxdb--tag-cardinality-explosion)

---
