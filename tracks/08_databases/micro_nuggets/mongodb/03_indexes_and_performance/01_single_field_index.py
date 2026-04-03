"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-01 · Single-Field Indexes                                         ║
║  The single biggest performance lever in MongoDB — indexes.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Create indexes, understand COLLSCAN vs IXSCAN, and read the explain() output.
Without indexes, MongoDB scans EVERY document for every query — O(n) always.

CONCEPTS
────────
Index internals:
  - A MongoDB index is a B-tree (like most databases) on one or more fields.
  - The B-tree stores field values in sorted order with pointers to documents.
  - An IXSCAN scans the B-tree (O(log n + k) where k = result count).
  - A COLLSCAN reads every document in the collection (O(n)).
  - At 10M documents, IXSCAN returns a record in microseconds; COLLSCAN ~seconds.

Index types (single-field variants):
  pymongo.ASCENDING  (1)  → sorted ascending. Supports sort asc and desc.
  pymongo.DESCENDING (-1) → same as ASCENDING for a single-field index (B-tree
                            traversal is symmetric). Matters for compound indexes.
  pymongo.TEXT       → full-text search index (covered in next nugget).
  pymongo.HASHED     → hash of the field value. Used for sharding hash keys.
                       Cannot support range queries — equality only.
  pymongo.GEO2DSPHERE → geospatial index for lon/lat coordinates.

Index options:
  unique=True        → DuplicateKeyError on insert/update if value repeats.
                       The _id index is unique by default.
  sparse=True        → index skips documents where the field is absent.
                       Without sparse, absent = null → all NULLs share one key.
  background=True    → (pre-4.4) build without blocking reads. Deprecated in 4.4+.
  expireAfterSeconds → TTL index: automatically deletes docs after N seconds.
  partialFilterExpression → index only documents matching a filter.
                            e.g. only index "active" users.

create_index vs create_indexes:
  create_index("field")                      → one index
  create_indexes([IndexModel([...]), ...])   → multiple, one round-trip

explain() — reading the query plan:
  col.find(filter).explain() returns a detailed plan dict.
  Key path: explain["queryPlanner"]["winningPlan"]
  Look for: "stage": "IXSCAN" (good) vs "COLLSCAN" (expensive)

USAGE
─────
    python 01_single_field_index.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pymongo
from pymongo import IndexModel

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("users")
col = db["users"]

print("\n── Single-Field Indexes ───────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed 500 user documents
# ─────────────────────────────────────────────────────────────────────────────
import random
random.seed(42)
statuses = ["active", "inactive", "pending"]
users = []
for i in range(1, 501):
    users.append({
        "_id":      f"user-{i:04d}",
        "email":    f"user{i}@example.com",
        "username": f"user_{i}",
        "status":   random.choice(statuses),
        "age":      random.randint(18, 70),
        "score":    random.randint(0, 1000),
        "created_at": datetime.now(tz=timezone.utc),
        "referral_code": f"REF{i:04d}" if i % 5 == 0 else None,
    })
col.insert_many(users)
print(f"\n  Inserted {col.count_documents({})} users.")


def _explain(collection, filter_dict: dict, verbosity: str = "executionStats") -> dict:
    """Wrapper: db.command('explain') since Cursor.explain() takes no args in pymongo 4."""
    return collection.database.command(
        "explain",
        {"find": collection.name, "filter": filter_dict},
        verbosity=verbosity,
    )

# ─────────────────────────────────────────────────────────────────────────────
# 1. COLLSCAN — no index on 'email' yet
#    "executionStats.docsExamined" = 500 (every doc scanned)
# ─────────────────────────────────────────────────────────────────────────────
plan = _explain(col, {"email": "user42@example.com"})
winning = plan["queryPlanner"]["winningPlan"]

# Walk nested plan to find COLLSCAN/IXSCAN stage
def find_stage(node: dict, target: str) -> bool:
    if node.get("stage") == target:
        return True
    for child_key in ("inputStage", "inputStages"):
        child = node.get(child_key)
        if isinstance(child, dict) and find_stage(child, target):
            return True
        if isinstance(child, list):
            for c in child:
                if find_stage(c, target):
                    return True
    return False

docs_examined = plan.get("executionStats", {}).get("totalDocsExamined",
               plan.get("executionStats", {}).get("docsExamined", "?"))
stage = "COLLSCAN" if find_stage(winning, "COLLSCAN") else "IXSCAN"
print(f"\n  Before index on 'email':")
print(f"    Stage: {stage}  — docs examined: {docs_examined}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Create a unique index on email
# ─────────────────────────────────────────────────────────────────────────────
col.create_index([("email", pymongo.ASCENDING)], unique=True, name="idx_email_unique")
print(f"\n  Created unique index on 'email'.")

plan = _explain(col, {"email": "user42@example.com"})
winning = plan["queryPlanner"]["winningPlan"]
docs_examined = plan.get("executionStats", {}).get("totalDocsExamined",
               plan.get("executionStats", {}).get("docsExamined", "?"))
stage = "IXSCAN" if find_stage(winning, "IXSCAN") else "COLLSCAN"
print(f"  After index on 'email':")
print(f"    Stage: {stage}  — docs examined: {docs_examined}  (should be 1)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Partial index — only index documents where status = 'active'
#    Smaller index, faster builds, less memory footprint.
#    Queries MUST include the partial filter or MongoDB won't use this index.
# ─────────────────────────────────────────────────────────────────────────────
col.create_index(
    [("score", pymongo.DESCENDING)],
    partialFilterExpression={"status": "active"},
    name="idx_score_active_only",
)
print(f"\n  Created partial index on 'score' (active users only).")

# This query uses the partial index (includes the partition condition):
plan = col.find({"status": "active", "score": {"$gt": 800}}).explain()
winning = plan["queryPlanner"]["winningPlan"]
stage = "IXSCAN" if find_stage(winning, "IXSCAN") else "COLLSCAN"
print(f"    Query {{status:active, score>800}} → {stage}")

# This query does NOT use the partial index (missing status filter):
plan = col.find({"score": {"$gt": 800}}).explain()
winning = plan["queryPlanner"]["winningPlan"]
stage = "IXSCAN" if find_stage(winning, "IXSCAN") else "COLLSCAN"
print(f"    Query {{score>800}} (no status filter) → {stage}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Partial index replacing sparse+unique — index only non-null referral_codes.
#
#    WHY NOT sparse=True + unique=True:
#      MongoDB 8.x changed behavior: a sparse+unique index still treats null as
#      a key and refuses multiple nulls with DuplicateKeyError.
#      The correct modern pattern is partialFilterExpression, which completely
#      excludes null/absent documents from the index — no key generated at all.
#
#    partialFilterExpression + unique:
#      - Only indexes documents where referral_code is a string (not null/absent).
#      - Unique constraint applies only within that subset.
#      - Same result as the old sparse=True behaviour, but explicit and reliable.
# ─────────────────────────────────────────────────────────────────────────────
col.create_index(
    [("referral_code", pymongo.ASCENDING)],
    unique=True,
    partialFilterExpression={"referral_code": {"$type": "string"}},
    name="idx_referral_partial_unique",
)
print(f"\n  Created partial+unique index on 'referral_code' (non-null only).")
n_with_code = col.count_documents({"referral_code": {"$ne": None}})
print(f"    Docs with referral_code (indexed): {n_with_code} of {col.count_documents({})}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. List all indexes on the collection
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  All indexes on 'users':")
for idx in col.list_indexes():
    print(f"    {idx['name']:<30} key={dict(idx['key'])}  "
          f"unique={idx.get('unique', False)}  sparse={idx.get('sparse', False)}")
print()
