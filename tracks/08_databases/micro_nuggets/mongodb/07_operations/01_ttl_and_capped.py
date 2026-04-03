"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-01 · TTL Indexes & Capped Collections                             ║
║  Automatic data expiry and fixed-size circular buffers.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Implement automatic data lifecycle management:
  - TTL (Time To Live) indexes: auto-delete expired documents.
  - Capped collections: fixed-size circular buffers for log/event data.

CONCEPTS
────────
TTL Index:
  - A special single-field index on a Date field with expireAfterSeconds.
  - A background thread (TTLMonitor) runs every 60 seconds on mongod and
    deletes documents where: field_value + expireAfterSeconds < current_time
  - The deletion is NOT instant — it happens within 60 seconds of expiry.
  - In Atlas, TTL deletions may be deferred during high load.

TTL index rules:
  - Must be on a field of type Date (not string, not ISODate string).
  - Works on arrays of dates: document expires when the EARLIEST date has expired.
  - Cannot be on a compound index (TTL is always single-field).
  - expireAfterSeconds=0: delete when the date value itself has passed.
    (i.e., the field value IS the expiry time — useful for explicit expiry.)

TTL vs manual deletion:
  - TTL: fully automatic, no application code needed after setup.
  - Manual: delete_many({"expired_at": {"$lt": now}}) — you control timing.
  - TTL is preferred for standard lifecycle. Manual is better for complex rules
    (e.g., "expire only inactive sessions", conditional expiry).

Capped Collection:
  - A fixed-size, insertion-order collection (a circular buffer).
  - When full, the OLDEST documents are automatically overwritten.
  - CANNOT delete individual documents. Can only insert and read.
  - CANNOT update documents in a way that changes their size (in older MongoDB).
  - Natural order == insertion order — always.
  - Use cases: system logs, audit trails, recent-N event buffers.

Capped collection properties:
  size:    maximum size in bytes (required).
  max:     optional maximum document count.
  Whichever limit is hit first causes eviction of the oldest document.

Capped vs TTL for logs:
  - Capped: bounded by size — old events evicted regardless of age.
    Good when you care about storage limit, not time window.
  - TTL: bounded by time — events expire after N seconds.
    Good when you care about keeping the last 30 days, not a size limit.
  - Many production systems use BOTH: TTL for business data, Capped for raw logs.

Tailable cursors (Capped only):
  - A special cursor type that BLOCKS and waits for new documents.
  - Only works on capped collections (because insertion order is preserved).
  - The MongoDB equivalent of `tail -f` on a log file.
  - Useful for real-time log streaming before Change Streams existed.

USAGE
─────
    python 01_ttl_and_capped.py
"""
from __future__ import annotations

import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pymongo

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
print("\n── TTL Indexes & Capped Collections ──────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. TTL Index — sessions that expire after 30 minutes
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("sessions")
sessions = db["sessions"]

# Create TTL index: expire documents 1800 seconds after 'expires_at'
sessions.create_index(
    [("expires_at", pymongo.ASCENDING)],
    expireAfterSeconds=0,   # 0 = delete when expires_at < now (field IS the expiry time)
    name="ttl_session_expiry",
)

now = datetime.now(tz=timezone.utc)
sessions.insert_many([
    {"_id": "S001", "user": "alice", "data": "cart:item1,item2",
     "expires_at": now + timedelta(minutes=30)},            # expires in 30 min
    {"_id": "S002", "user": "bob",   "data": "cart:item3",
     "expires_at": now - timedelta(minutes=5)},             # already expired!
    {"_id": "S003", "user": "carol", "data": "empty cart",
     "expires_at": now + timedelta(hours=2)},               # expires in 2 hours
    {"_id": "S004", "user": "dave",  "data": "wishlist:x",
     "expires_at": now - timedelta(seconds=1)},             # just expired
])

active = sessions.count_documents({"expires_at": {"$gt": now}})
expired = sessions.count_documents({"expires_at": {"$lte": now}})
print(f"\n  [TTL] Sessions collection:")
print(f"    Total: {sessions.count_documents({})}  Active: {active}  Expired: {expired}")
print(f"    NOTE: TTLMonitor runs every ~60s — expired docs may still be present.")
print(f"    Application-side query to exclude expired sessions:")
print(f"      sessions.find({{\"expires_at\": {{\"$gt\": now}}}})  → {active} docs")

# Show TTL index metadata
for idx in sessions.list_indexes():
    if idx.get("expireAfterSeconds") is not None:
        print(f"\n  TTL index: '{idx['name']}'")
        print(f"    expireAfterSeconds: {idx['expireAfterSeconds']}")
        print(f"    key: {dict(idx['key'])}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Capped Collection — circular buffer for the last 10 log entries
# ─────────────────────────────────────────────────────────────────────────────
db.drop_collection("app_logs")
db.create_collection(
    "app_logs",
    capped=True,
    size=1024 * 100,   # 100 KB max size
    max=10,            # max 10 documents (whichever limit is hit first)
)
logs = db["app_logs"]

# Confirm it's capped
col_info = db.command("listCollections", filter={"name": "app_logs"})
opts = col_info["cursor"]["firstBatch"][0].get("options", {})
print(f"\n  [Capped] app_logs created:")
print(f"    capped={opts.get('capped')}  size={opts.get('size')} bytes  max={opts.get('max')} docs")

# Insert 15 log entries — oldest 5 will be evicted (max=10)
for i in range(1, 16):
    logs.insert_one({
        "seq": i,
        "level": "INFO" if i % 3 != 0 else "WARN",
        "msg":   f"Log message #{i:02d}",
        "ts":    datetime.now(tz=timezone.utc),
    })

retained = list(logs.find({}, {"seq": 1, "level": 1, "msg": 1, "_id": 0}))
print(f"\n  After inserting 15 logs (max=10), retained {len(retained)} documents:")
print(f"  (Oldest evicted — circular buffer behavior)")
for doc in retained:
    print(f"    seq={doc['seq']:02d}  [{doc['level']}]  {doc['msg']}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Capped collection constraints demo
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  [Capped] Delete behavior on capped collections:")
try:
    result = logs.delete_one({"seq": 6})
    if result.deleted_count == 0:
        print(f"  [✓] delete_one matched nothing (doc already evicted by circular buffer).")
    else:
        # MongoDB 8.x relaxed the capped-no-delete restriction in some scenarios.
        # Older behavior: raises OperationFailure. Newer Atlas behavior: may succeed.
        print(f"  [note] delete_one deleted {result.deleted_count} doc (MongoDB 8.x changed"
              f" capped delete semantics — individual deletes may now succeed on Atlas).")
except Exception as e:
    print(f"  [✓] delete_one rejected as expected on capped: {type(e).__name__}")

print(f"\n  [Capped] Natural order is guaranteed (no sort needed for log-order reads).")
first = logs.find_one({})
last  = logs.find(sort=[("$natural", -1)]).next()
print(f"    First (oldest retained): seq={first['seq']}")
print(f"    Last (most recent):      seq={last['seq']}")

db.drop_collection("sessions")
db.drop_collection("app_logs")
print()
