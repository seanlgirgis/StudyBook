"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-03 · Operational Checks & Server Stats                            ║
║  Monitoring, diagnostics, and health checks for production MongoDB.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Run operational diagnostics: server status, connection pool metrics,
database/collection stats, and current operation snapshots.
These are the commands used by DBAs, SREs, and monitoring systems.

CONCEPTS
────────
db.command("serverStatus"):
  - The most comprehensive server health command.
  - Returns: connections, opcounters, memory, wiredTiger, repl, metrics...
  - Requires the "serverStatus" privilege (all Atlas users have it).
  - Key sections:
      connections.current         → active connections right now
      connections.available       → remaining pool capacity
      opcounters.insert/query/... → operations since last restart
      mem.resident                → resident memory (MB)
      repl.setName                → replica set name
      wiredTiger.cache            → WiredTiger cache hit rate

db.command("dbStats"):
  - Database-level size and collection counts.
  - collections  → number of collections
  - dataSize     → logical data size (uncompressed, bytes)
  - storageSize  → actual disk usage (compressed)
  - indexes      → total indexes across all collections
  - indexSize    → total index size on disk

collection.stats() / db.command("collStats"):
  - Per-collection: document count, avg document size, index sizes.
  - totalIndexSize: sum of all index sizes.
  - Useful for understanding index overhead vs data size.

currentOp:
  - Shows currently running operations on the server.
  - db.command("currentOp") → all ops including idle connections.
  - db.command("currentOp", {"active": True}) → only active ops.
  - Key fields: opid, op (query/insert/update/...), ns, secs_running, client.
  - Production use: identify slow queries / locks.

killOp:
  - db.command("killOp", op=<opid>) → terminates a running operation.
  - Use with extreme care — only kill long-running queries you own.

Ping & ismaster / hello:
  - "ping"    → lightweight connectivity test (returns {ok: 1}).
  - "hello"   → returns topology info, election state, replica set members.
  - "isMaster" → legacy alias for "hello" (deprecated but still works).

Connection pool metrics (pymongo client):
  - client.nodes → set of (host, port) tuples the client is connected to.
  - The pool is managed by the MongoClient; you don't manually manage connections.

USAGE
─────
    python 03_operational_checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

client = get_client()
db = client[LAB_DB]

print("\n── Operational Checks ────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Ping — lightweight connectivity check
# ─────────────────────────────────────────────────────────────────────────────
ping = client.admin.command("ping")
print(f"\n  [ping] {ping}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. hello — topology and replica set state
# ─────────────────────────────────────────────────────────────────────────────
hello = client.admin.command("hello")
print(f"\n  [hello] Cluster topology:")
print(f"    isWritablePrimary: {hello.get('isWritablePrimary', hello.get('ismaster', '?'))}")
print(f"    setName:           {hello.get('setName', 'N/A')} (replica set name)")
print(f"    maxWireVersion:    {hello.get('maxWireVersion', '?')}  (feature level)")
print(f"    localTime:         {hello.get('localTime', '?')}")
hosts = hello.get("hosts", [])
if hosts:
    print(f"    hosts ({len(hosts)} members):")
    for h in hosts:
        print(f"      {h}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. serverStatus — key health metrics
# ─────────────────────────────────────────────────────────────────────────────
ss = client.admin.command("serverStatus")

conns    = ss.get("connections", {})
opcounts = ss.get("opcounters", {})
mem      = ss.get("mem", {})

print(f"\n  [serverStatus] Connection pool:")
print(f"    current:    {conns.get('current', '?')} (active connections now)")
print(f"    available:  {conns.get('available', '?')} (remaining capacity)")
print(f"    totalCreated: {conns.get('totalCreated', '?')} (total since restart)")

print(f"\n  [serverStatus] Operation counters (since last restart):")
for op in ("insert", "query", "update", "delete", "getmore", "command"):
    count = opcounts.get(op, 0)
    print(f"    {op:<10} {count:>12,}")

print(f"\n  [serverStatus] Memory (MB):")
print(f"    resident: {mem.get('resident', '?')} MB")
print(f"    virtual:  {mem.get('virtual',  '?')} MB")

# WiredTiger cache stats (storage engine internals)
wt = ss.get("wiredTiger", {}).get("cache", {})
if wt:
    dirty_mb     = wt.get("tracked dirty bytes in the cache", 0) / (1024**2)
    max_mb       = wt.get("maximum bytes configured", 0) / (1024**2)
    hits         = wt.get("pages read into cache", 1)
    lookups      = wt.get("pages requested from the cache", 1)
    hit_rate     = (1 - hits/lookups) * 100 if lookups > 0 else 0
    print(f"\n  [serverStatus] WiredTiger cache:")
    print(f"    max configured: {max_mb:.0f} MB")
    print(f"    dirty bytes:    {dirty_mb:.1f} MB")
    print(f"    hit rate:       ~{hit_rate:.1f}%  (higher = better; < 90% may need more RAM)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. dbStats — database-level sizes
# ─────────────────────────────────────────────────────────────────────────────
db_stats = db.command("dbStats")
print(f"\n  [dbStats] nugget_lab:")
print(f"    collections:  {db_stats.get('collections', 0)}")
print(f"    objects:      {db_stats.get('objects', 0):,} documents")
print(f"    dataSize:     {db_stats.get('dataSize', 0) / 1024:.1f} KB (uncompressed)")
print(f"    storageSize:  {db_stats.get('storageSize', 0) / 1024:.1f} KB (compressed on disk)")
print(f"    indexes:      {db_stats.get('indexes', 0)}")
print(f"    indexSize:    {db_stats.get('indexSize', 0) / 1024:.1f} KB")

# ─────────────────────────────────────────────────────────────────────────────
# 5. collStats — per-collection breakdown
# ─────────────────────────────────────────────────────────────────────────────
collections = db.list_collection_names()
if collections:
    print(f"\n  [collStats] Collection summary:")
    print(f"    {'Collection':<30} {'Docs':>8} {'DataKB':>8} {'IndexKB':>8}")
    print(f"    {'-'*30} {'-'*8} {'-'*8} {'-'*8}")
    for cname in sorted(collections)[:8]:  # show up to 8 collections
        try:
            cs = db.command("collStats", cname)
            data_kb  = cs.get("size", 0) / 1024
            index_kb = cs.get("totalIndexSize", 0) / 1024
            ndocs    = cs.get("count", 0)
            print(f"    {cname:<30} {ndocs:>8,} {data_kb:>7.1f}K {index_kb:>7.1f}K")
        except Exception:
            pass

# ─────────────────────────────────────────────────────────────────────────────
# 6. currentOp — see what's running right now
#    On Atlas, you typically only see your own operations.
# ─────────────────────────────────────────────────────────────────────────────
current_ops = client.admin.command("currentOp", {"active": True, "ownOps": True})
ops = current_ops.get("inprog", [])
print(f"\n  [currentOp] Active operations: {len(ops)}")
for op in ops[:5]:
    print(f"    opid={op.get('opid')}  op={op.get('op')}  "
          f"ns={op.get('ns')}  secs={op.get('secs_running', 0)}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. pymongo client topology view
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  [pymongo] Client-side topology:")
print(f"    Connected nodes: {client.nodes}")
print(f"    Primary:         {client.primary}")
print(f"    Secondaries:     {client.secondaries}")

client.close()
print()
