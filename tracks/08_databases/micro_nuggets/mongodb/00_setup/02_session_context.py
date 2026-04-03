"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-02 · Session Context & Server Info                                ║
║  Understand what cluster you're connected to and how it's configured.        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Inspect the MongoDB server / Atlas cluster properties:
  - Server version and topology
  - Current database and collection inventory
  - Read/write concern defaults
  - Connection pool state

CONCEPTS
────────
server_info():
  - Returns a dict with MongoDB server build metadata.
  - Key fields: version, gitVersion, modules, openssl, sysInfo.
  - "version" tells you the MongoDB server version (e.g. "7.0.4").
  - Atlas typically runs the current long-term-support (LTS) release.

Topology types (how MongoDB nodes are organized):
  - Single:        standalone server (dev only — no replication).
  - ReplicaSet:    1 primary + N secondaries. All Atlas clusters are replica sets.
  - Sharded:       multiple replica sets + config servers + mongos routers.
                   Used for horizontal scale (Atlas M30+ tiers).

Read Concern (how fresh the data must be):
  - "local"        → reads from the primary, may see uncommitted writes.
  - "majority"     → reads only data confirmed by a majority of nodes.
                     Prevents reading rollback victims. Atlas default.
  - "linearizable" → strictly consistent, but slow (requires primary roundtrip).
  - "snapshot"     → used inside multi-document transactions only.

Write Concern (how many nodes must acknowledge a write):
  - w=1            → primary acknowledges. Fast, can lose data on failover.
  - w="majority"   → majority of nodes persist the write. Atlas default.
  - j=True         → also write to the on-disk journal before acknowledging.
                     Combined with w=majority this is the strongest guarantee.

codec_options:
  - Controls how Python types map to BSON types.
  - uuid_representation: how Python UUID objects are encoded.
  - tz_aware: whether datetime fields return timezone-aware objects.
  - Default in pymongo 4: tz_aware=False, uuid_representation=UNSPECIFIED.
  - Production recommendation: tz_aware=True, uuid_representation=STANDARD.

USAGE
─────
    python 02_session_context.py

EXPECTED OUTPUT
───────────────
    ── MongoDB Session Context ─────────────────────────

      Server version:   7.0.x
      Topology type:    ReplicaSet
      Replica set name: atlas-xxxxx-shard-0

      Databases & collection counts:
        admin           0 collections
        de_telemetry    5 collections
        local           1 collections
        nugget_lab      0 collections   ← empty until nuggets insert data
        sample_mflix    3 collections

      Lab database: nugget_lab
        Collections: []   ← empty until nuggets create them

      Write concern:  WriteConcern(w='majority')
      Read concern:   ReadConcern(level='majority')
      Codec options:  CodecOptions(tz_aware=False, uuid_representation=UNSPECIFIED, ...)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_client, LAB_DB

client = get_client()

print("\n── MongoDB Session Context ─────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Server info
#    server_info() issues a "buildInfo" admin command.
#    On Atlas this works for all authenticated users.
# ─────────────────────────────────────────────────────────────────────────────
info = client.server_info()
print(f"\n  Server version:   {info.get('version', 'unknown')}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Topology type
#    The topology_description tells you how the cluster is organized.
#    ReplicaSet is universal on Atlas — even a single-node M0 (free tier)
#    runs as a 3-node replica set behind the scenes.
# ─────────────────────────────────────────────────────────────────────────────
topology = client.topology_description
topo_type = getattr(topology.topology_type, "name", str(topology.topology_type))
print(f"  Topology type:    {topo_type}")

# Replica set name is embedded in the server hello response
try:
    hello = client.admin.command("hello")
    rs_name = hello.get("setName", "N/A")
    print(f"  Replica set name: {rs_name}")
except Exception:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# 3. Database and collection inventory
#    list_databases() returns richer info than list_database_names():
#    each entry has "name", "sizeOnDisk" (bytes), "empty" (bool).
# ─────────────────────────────────────────────────────────────────────────────
print("\n  Databases & collection counts:")
for db_info in sorted(client.list_databases(), key=lambda d: d["name"]):
    db_name = db_info["name"]
    cols = client[db_name].list_collection_names()
    print(f"    {db_name:<20} {len(cols)} collections")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Lab database detail
#    The lab db starts empty. Collections appear here after nuggets run.
# ─────────────────────────────────────────────────────────────────────────────
lab_db = client[LAB_DB]
lab_cols = lab_db.list_collection_names()
print(f"\n  Lab database: {LAB_DB}")
if lab_cols:
    for col_name in sorted(lab_cols):
        count = lab_db[col_name].count_documents({})
        print(f"    {col_name:<30} {count} documents")
else:
    print(f"    Collections: []   ← empty until nuggets create them")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Client-level codec and concern settings
#    These are the defaults that every collection inherits unless overridden.
#    In production you often override write_concern and read_concern per-op
#    rather than at the client level.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Write concern:  {client.write_concern!r}")
print(f"  Read concern:   {client.read_concern!r}")
print(f"  Codec options:  {client.codec_options!r}")

client.close()
print()
