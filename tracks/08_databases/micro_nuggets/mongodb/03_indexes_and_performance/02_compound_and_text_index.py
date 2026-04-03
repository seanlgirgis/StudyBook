"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 03-02 · Compound & Text Indexes                                      ║
║  Multi-field indexes, ESR rule, and full-text search.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Master compound indexes (the workhorse of production MongoDB) and text indexes
for full-text search without Atlas Search or Elasticsearch.

CONCEPTS
────────
Compound Index:
  - An index on multiple fields: create_index([("a", 1), ("b", -1)])
  - Supports queries on: (a), (a, b) — but NOT (b) alone.
    The leftmost prefix rule: a compound index on (a, b, c) covers:
      a, ab, abc — but not b, c, bc.
  - The index can also sort results if the sort matches the index direction
    (or its exact reverse for all fields simultaneously).

ESR Rule — the golden rule for ordering compound index fields:
  E = Equality first      → fields you filter with exact match
  S = Sort next           → fields you ORDER BY
  R = Range last          → fields with $gt/$lt/$gte/$lte/$in

  Example: find users with status='active', sorted by created_at,
           with score in a range → index: (status, created_at, score)
  Deviating from ESR often results in in-memory sorts (expensive).

Covered Query:
  - A query is "covered" when ALL fields it needs (filter + projection) are
    in the index — no document reads required at all.
  - Check: executionStats.totalDocsExamined == 0 on a covered query.
  - To cover a projection: include all projected fields in the compound index.

Multikey Index:
  - Automatically created when you index an array field.
  - MongoDB creates one index entry per array element.
  - A compound index can have AT MOST ONE multikey field.
  - Cannot create a compound index on two array fields.

Text Index:
  - Enables full-text search with $text operator.
  - A collection can have only ONE text index (can span multiple fields).
  - Text index stores normalized word stems (not full substrings).
    → "running" and "runs" both match stem "run".
  - Supports language-specific stemming (default: English).
  - Score-based relevance: $meta: "textScore" sorts by relevance.
  - Limitation: no prefix matching, no regex-style — use Atlas Search for that.

USAGE
─────
    python 02_compound_and_text_index.py
"""
from __future__ import annotations

import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pymongo

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("articles")
col = db["articles"]

print("\n── Compound & Text Indexes ───────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed data — articles with author, category, published_at, score, body text
# ─────────────────────────────────────────────────────────────────────────────
random.seed(7)
categories = ["tech", "science", "gaming", "business"]
authors = ["alice", "bob", "carol", "dave"]
bodies = [
    "Python is a powerful programming language for data engineering and machine learning.",
    "MongoDB Atlas provides a fully managed cloud database with built-in search and analytics.",
    "Delta Lake enables ACID transactions on data lakes for reliable batch and streaming pipelines.",
    "Kubernetes orchestrates containerized workloads for scalable microservices architectures.",
    "Rust programming language offers memory safety without garbage collection overhead.",
    "PostgreSQL is the world's most advanced open source relational database system.",
    "Apache Kafka streams millions of events per second with durable distributed logs.",
    "Data engineering transforms raw data into analytics-ready assets for business intelligence.",
    "Machine learning models require clean, well-engineered feature pipelines to perform well.",
    "Cloud databases like MongoDB Atlas reduce operational overhead for development teams.",
]
docs = []
base = datetime.now(tz=timezone.utc)
for i in range(100):
    docs.append({
        "title":        f"Article {i+1:03d}: {random.choice(bodies[:3])[:40]}",
        "body":         random.choice(bodies),
        "author":       random.choice(authors),
        "category":     random.choice(categories),
        "status":       random.choice(["published", "draft", "archived"]),
        "score":        random.randint(0, 500),
        "published_at": base - timedelta(days=random.randint(0, 365)),
        "tags":         random.sample(["python", "mongodb", "kafka", "kubernetes", "rust"], k=random.randint(1,3)),
    })
col.insert_many(docs)
print(f"\n  Seeded {col.count_documents({})} articles.")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Compound index following ESR rule
#    Query: status=published AND category=tech ORDER BY published_at DESC
#    E: status (equality), E: category (equality), S: published_at (sort)
# ─────────────────────────────────────────────────────────────────────────────
col.create_index(
    [("status", pymongo.ASCENDING),
     ("category", pymongo.ASCENDING),
     ("published_at", pymongo.DESCENDING)],
    name="idx_status_cat_date",
)
print(f"\n  Created compound index: (status, category, published_at)")


def _explain(collection, filter_dict, sort_list=None, projection=None,
             verbosity="executionStats"):
    """Explain helper — Cursor.explain() takes no args in pymongo 4.x."""
    cmd = {"find": collection.name, "filter": filter_dict}
    if sort_list:
        cmd["sort"] = dict(sort_list)
    if projection:
        cmd["projection"] = projection
    return collection.database.command("explain", cmd, verbosity=verbosity)


plan = _explain(col,
    {"status": "published", "category": "tech"},
    sort_list=[("published_at", pymongo.DESCENDING)])
stats = plan.get("executionStats", {})
print(f"  Query status+category sort by date:")
print(f"    docsExamined: {stats.get('totalDocsExamined', stats.get('docsExamined', '?'))}  "
      f"nReturned: {stats.get('nReturned', '?')}  "
      f"executionTimeMillis: {stats.get('executionTimeMillis', '?')} ms")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Covered query — all fields in the projection are in the index
#    Add 'score' to index to cover a projection of {status, category, published_at, score}
# ─────────────────────────────────────────────────────────────────────────────
col.create_index(
    [("status", pymongo.ASCENDING),
     ("category", pymongo.ASCENDING),
     ("published_at", pymongo.DESCENDING),
     ("score", pymongo.ASCENDING)],
    name="idx_covered",
)
plan = _explain(col,
    {"status": "published", "category": "tech"},
    projection={"_id": 0, "status": 1, "category": 1, "published_at": 1, "score": 1})
stats = plan.get("executionStats", {})
print(f"\n  Covered query (all fields in index):")
print(f"    docsExamined: {stats.get('totalDocsExamined', stats.get('docsExamined', '?'))}  "
      f"(should be 0 — no doc fetch needed)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Multikey index — index on an array field
#    MongoDB creates one entry per tag per document.
# ─────────────────────────────────────────────────────────────────────────────
col.create_index([("tags", pymongo.ASCENDING)], name="idx_tags_multikey")
plan = _explain(col, {"tags": "mongodb"})
stats = plan.get("executionStats", {})
print(f"\n  Multikey index on 'tags':")
print(f"    Docs with tag 'mongodb': {stats.get('nReturned', '?')}  "
      f"(IXSCAN, not COLLSCAN)")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Text index — full-text search
#    A collection can have only ONE text index.
#    We index 'title' and 'body' with different weights.
#    weight=10 for title: title matches score 10x higher than body matches.
# ─────────────────────────────────────────────────────────────────────────────
col.create_index(
    [("title", pymongo.TEXT), ("body", pymongo.TEXT)],
    weights={"title": 10, "body": 1},
    default_language="english",
    name="idx_text_search",
)
print(f"\n  Created text index on (title, body) with title weight=10.")

# $text operator with $search — space-separated terms are OR by default.
# Phrase: "\"exact phrase\""  Negation: "-term"
results = list(col.find(
    {"$text": {"$search": "mongodb atlas"}},
    {"title": 1, "score": {"$meta": "textScore"}, "_id": 0},
).sort([("score", {"$meta": "textScore"})]).limit(3))

print(f"  Top 3 text matches for 'mongodb atlas':")
for r in results:
    print(f"    score={r['score']:.2f}  title={r['title'][:55]}")

# Phrase search — exact multi-word match
results = list(col.find(
    {"$text": {"$search": "\"data engineering\""}},
    {"title": 1, "_id": 0},
).limit(2))
print(f"  Phrase 'data engineering' matches: {len(results)}")

# Term negation — exclude Kafka articles
results = list(col.find(
    {"$text": {"$search": "data -kafka"}},
    {"title": 1, "_id": 0},
).limit(2))
print(f"  'data -kafka' matches: {len(results)}")
print()
