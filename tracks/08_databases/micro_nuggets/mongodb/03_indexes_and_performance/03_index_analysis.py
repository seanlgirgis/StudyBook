"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-03 · Index Analysis & Stats                                       ║
║  Reading explain output like a DBA and spotting index problems.              ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Deep-dive into explain() output, detect slow queries, find unused indexes,
and understand the cost of index writes vs the benefit of read performance.

CONCEPTS
────────
explain() verbosity levels:
  "queryPlanner"    → just the winning plan (fastest, no execution).
  "executionStats"  → runs the query and records execution stats.
  "allPlansExecution" → runs all candidate plans (slowest, most info).

  Key fields in executionStats:
    nReturned          → documents returned to the application.
    docsExamined       → documents read from disk (want = nReturned).
    keysExamined       → index keys scanned.
    executionTimeMillis → wall clock time.
    totalKeysExamined  → total index key scans across all stages.

  "Examined / Returned" ratio:
    Ratio = 1    → perfect index (index exactly identifies result set).
    Ratio >> 1   → index scans more than needed (filter applied post-scan).
    ∞            → COLLSCAN or result is 0 documents.

Winning plan structure:
  The plan tree represents the execution pipeline (read bottom-up):
    COLLSCAN / IXSCAN → FETCH → SORT → PROJECTION → ...
  IXSCAN + FETCH: index locates the _id pointer, then FETCH reads the doc.
  IXSCAN alone (no FETCH): covered query — reads only from index.

Slow query indicators:
  - COLLSCAN on a large collection.
  - SORT (in-memory sort) — no index on the sort key.
  - executionTimeMillis >> expected (network, disk, lock contention).

$indexStats aggregation:
  Returns per-index usage stats: how many times each index was used since
  the last mongod restart (or Atlas rolling restart).
  Zero accesses = potentially unused index → increases write cost for no gain.
  Note: stats reset on mongod restart — needs days/weeks to be meaningful.

Index overhead on writes:
  - Every insert/update/delete must also update ALL indexes on that collection.
  - Fewer indexes → faster writes. More indexes → faster reads.
  - Rule of thumb: < 5 indexes per write-heavy collection.
  - Drop indexes that are never used or that are prefixes of wider indexes.

Index prefix subsumption:
  If you have (a, b, c), you do NOT also need (a) or (a, b) as separate indexes —
  the compound index already covers those prefix queries.

USAGE
─────
    python 03_index_analysis.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pymongo

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

# ── We reuse the 'articles' collection from the previous nugget ───────────────
db = get_lab_db()
col = db["articles"]

if col.count_documents({}) == 0:
    print("  [!] 'articles' collection is empty. Run 02_compound_and_text_index.py first.")
    sys.exit(1)

print("\n── Index Analysis ────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 1. List all indexes and their key patterns
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Indexes on 'articles' collection:")
for idx in col.list_indexes():
    key  = dict(idx["key"])
    opts = []
    if idx.get("unique"):       opts.append("unique")
    if idx.get("sparse"):       opts.append("sparse")
    if idx.get("textIndexVersion"): opts.append("text")
    if idx.get("expireAfterSeconds") is not None:
        opts.append(f"TTL={idx['expireAfterSeconds']}s")
    print(f"    {idx['name']:<35} {key}  {opts}")

# ─────────────────────────────────────────────────────────────────────────────
# 2. explain("executionStats") — analyse a query
# ─────────────────────────────────────────────────────────────────────────────
def _cmd_explain(filter_dict, sort_dict=None, verbosity="executionStats"):
    """Use db.command('explain') — Cursor.explain() takes no args in pymongo 4.x."""
    cmd = {"find": col.name, "filter": filter_dict}
    if sort_dict:
        cmd["sort"] = sort_dict
    return col.database.command("explain", cmd, verbosity=verbosity)


def analyse_query(label: str, filter_dict: dict, sort_dict: dict | None = None) -> None:
    plan  = _cmd_explain(filter_dict, sort_dict)
    stats = plan.get("executionStats", {})
    n_ret = stats.get("nReturned", 0)
    docs  = stats.get("totalDocsExamined", stats.get("docsExamined", 0))
    keys  = stats.get("totalKeysExamined", stats.get("keysExamined", 0))
    ms    = stats.get("executionTimeMillis", 0)
    ratio = docs / n_ret if n_ret > 0 else float("inf")

    # Walk the plan tree to find the deepest stage name
    def leaf_stage(node):
        while "inputStage" in node:
            node = node["inputStage"]
        return node.get("stage", "?")

    winning = plan["queryPlanner"]["winningPlan"]
    scan    = leaf_stage(winning)
    print(f"\n  [{label}]")
    print(f"    Leaf stage:       {scan}")
    print(f"    keysExamined:     {keys}")
    print(f"    docsExamined:     {docs}")
    print(f"    nReturned:        {n_ret}")
    print(f"    examined/returned ratio: {ratio:.1f}  (1.0 = perfect)")
    print(f"    executionTime:    {ms} ms")


# Good: uses compound index, ratio ≈ 1
analyse_query(
    "GOOD: compound index hit",
    {"status": "published", "category": "tech"},
    {"published_at": pymongo.DESCENDING},
)

# Bad: query on 'author' — no index
analyse_query(
    "BAD: no index on 'author' → COLLSCAN",
    {"author": "alice"},
)

# Add the missing index and re-check
col.create_index([("author", pymongo.ASCENDING)], name="idx_author")
analyse_query(
    "FIXED: added index on 'author'",
    {"author": "alice"},
)

# In-memory SORT — sort on a field not in the index
analyse_query(
    "SORT: no sort index → in-memory sort",
    {"author": "alice"},
    {"score": pymongo.DESCENDING},
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. $indexStats — find potentially unused indexes
#    Note: stats since last mongod restart only. New indexes start at 0.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  $indexStats (accesses since last restart):")
for stat in col.aggregate([{"$indexStats": {}}]):
    name    = stat.get("name", "?")
    ops     = stat.get("accesses", {}).get("ops", 0)
    since   = stat.get("accesses", {}).get("since", "?")
    warning = "  ← NEVER USED — candidate for removal" if ops == 0 else ""
    print(f"    {name:<35} ops={ops}{warning}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Index prefix subsumption — detect redundant indexes
#    If idx_status_cat_date covers (status, category, published_at),
#    a separate (status) index is redundant.
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n  Index prefix analysis:")
indexes  = {idx["name"]: list(idx["key"].keys()) for idx in col.list_indexes()
            if "text" not in str(idx.get("key"))}
compound = [(name, keys) for name, keys in indexes.items() if len(keys) > 1]
single   = [(name, keys) for name, keys in indexes.items() if len(keys) == 1]

for sname, skeys in single:
    for cname, ckeys in compound:
        if skeys[0] == ckeys[0]:   # single-field is leftmost prefix of compound
            print(f"    '{sname}' ({skeys}) is a PREFIX of '{cname}' ({ckeys}) "
                  f"→ potential redundancy")
print()
