"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 07-02 · Atlas Search                                                 ║
║  Full-text search and relevance ranking on Atlas clusters.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Use Atlas Search ($search aggregation stage) for full-text, fuzzy, autocomplete,
and range-aware search — powered by Apache Lucene under the hood.

CONCEPTS
────────
Atlas Search vs Text Index:
  - Text index ($text):  Built into MongoDB core. Basic stemming, no fuzzy.
    Good for simple keyword search on small collections.
  - Atlas Search ($search): Powered by Apache Lucene. Available on Atlas M0+.
    Supports: fuzzy matching, autocomplete, synonyms, facets, geo, highlighting,
              compound queries, language analyzers, relevance tuning.
  - For production search features, always use Atlas Search over $text.

Search Index:
  - A separate index type managed by Atlas (not a B-tree).
  - Created in Atlas UI: Search → Create Search Index, OR via API/CLI.
  - Multiple search indexes per collection, each with its own mapping.
  - Mapping: "dynamic" (index all string fields automatically) or
             "static" (explicitly define which fields and analyzers).
  - Index builds asynchronously — may take minutes on large collections.

$search aggregation stage:
  Always the FIRST stage in the pipeline. Cannot be preceded by $match.
  Use $searchMeta for metadata-only (facet counts) without document results.

Common search operators:
  text:       { "text": { "query": "...", "path": "field" } }
              Full-text search with stemming and stop word removal.

  fuzzy:      { "text": { "query": "mongdb", "path": "title",
                           "fuzzy": { "maxEdits": 1 } } }
              Handles typos — matches within edit distance N.

  autocomplete: { "autocomplete": { "query": "mon", "path": "title" } }
              Prefix/n-gram matching. Requires a special search index mapping
              with "autocomplete" analyzer on the field.

  range:      { "range": { "path": "price", "gte": 100, "lte": 500 } }
              Numeric/date range inside search (unlike $match, range is
              Lucene-based and can be combined with text in relevance scoring).

  compound:   { "compound": { "must": [...], "should": [...], "mustNot": [...] } }
              Boolean logic combining multiple operators.
              "must" = AND, "should" = OR (boosts score), "mustNot" = NOT.

Relevance score:
  $search adds a "score" metadata field. Retrieve with:
    {"$meta": "searchScore"}
  Sort by: {"$sort": {"score": {"$meta": "searchScore"}}}

$searchMeta + facets:
  Returns category counts without returning documents.
  Useful for sidebar filters: "Electronics (12)  Clothing (8)  ..."

NOTE ON THIS NUGGET:
  Atlas Search requires a search index to be created in the Atlas UI or via
  the Atlas Data API. This nugget attempts $search and gracefully handles
  OperationFailure if no search index exists, falling back to a diagnostic message.
  To fully run this nugget: create a dynamic search index named "default" on
  the "search_demo" collection in the Atlas UI.

USAGE
─────
    python 02_atlas_search.py
"""
from __future__ import annotations

import sys
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

from pymongo.errors import OperationFailure

sys.path.insert(0, str(Path(__file__).parent.parent))
from _mg_connect import get_lab_db

db = get_lab_db()
db.drop_collection("search_demo")
col = db["search_demo"]

print("\n── Atlas Search ──────────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# Seed — product catalog for search demo
# ─────────────────────────────────────────────────────────────────────────────
random.seed(12)
products = [
    {"name": "Sony WH-1000XM5 Wireless Headphones",   "category": "audio",     "price": 349.99, "brand": "Sony",     "description": "Industry-leading noise cancelling wireless headphones with premium sound quality.", "rating": 4.8},
    {"name": "Apple AirPods Pro 2nd Gen",              "category": "audio",     "price": 249.00, "brand": "Apple",    "description": "Active noise cancellation and Transparency mode for wireless earbuds.", "rating": 4.7},
    {"name": "Jabra Evolve2 85 Business Headset",      "category": "audio",     "price": 449.00, "brand": "Jabra",    "description": "Professional wireless business headset with advanced ANC for office use.", "rating": 4.5},
    {"name": "MacBook Pro 16-inch M3 Pro",             "category": "computers", "price": 2499.0, "brand": "Apple",    "description": "Powerful laptop with M3 Pro chip for professional video editing and development.", "rating": 4.9},
    {"name": "Dell XPS 15 Laptop",                     "category": "computers", "price": 1799.0, "brand": "Dell",     "description": "Premium Windows laptop with OLED display for developers and creators.", "rating": 4.6},
    {"name": "Logitech MX Master 3S Mouse",            "category": "peripherals","price": 99.99,  "brand": "Logitech","description": "Ergonomic wireless mouse with MagSpeed scroll wheel and precision tracking.", "rating": 4.7},
    {"name": "Keychron K2 Pro Mechanical Keyboard",    "category": "peripherals","price": 109.00, "brand": "Keychron","description": "Compact wireless mechanical keyboard with hot-swap switches for productivity.", "rating": 4.6},
    {"name": "Samsung 32\" 4K Monitor",                "category": "displays",  "price": 699.0,  "brand": "Samsung",  "description": "Ultra HD 4K monitor with HDR support for professional color-accurate work.", "rating": 4.4},
    {"name": "LG 27\" UltraGear Gaming Monitor",       "category": "displays",  "price": 399.0,  "brand": "LG",       "description": "Fast 165Hz gaming monitor with 1ms response time and G-Sync compatible.", "rating": 4.5},
    {"name": "Elgato Stream Deck MK.2",                "category": "streaming", "price": 149.99, "brand": "Elgato",   "description": "Live streaming controller with customizable LCD keys for content creators.", "rating": 4.7},
]
col.insert_many(products)
print(f"\n  Seeded {col.count_documents({})} products for Atlas Search demo.")

# ─────────────────────────────────────────────────────────────────────────────
# Helper: run a $search pipeline and return results or show error
# ─────────────────────────────────────────────────────────────────────────────
def run_search(label: str, pipeline: list, project: dict | None = None) -> list:
    """Run an Atlas $search pipeline. Returns results or [] on index-not-found."""
    if project:
        pipeline = pipeline + [{"$project": project}]
    try:
        results = list(col.aggregate(pipeline))
        print(f"\n  [{label}] → {len(results)} result(s):")
        for r in results[:5]:
            score = r.get("score", "N/A")
            name  = r.get("name", "?")[:50]
            price = r.get("price", "?")
            cat   = r.get("category", "?")
            print(f"    score={score:<6}  ${price:<8}  [{cat}]  {name}")
        return results
    except OperationFailure as e:
        if "Search index" in str(e) or "AtlasSearch" in str(e) or "no search" in str(e).lower():
            print(f"\n  [{label}] SKIPPED — No Atlas Search index found.")
            print(f"    To enable: Atlas UI → Search → Create Index → Index Name: 'default'")
            print(f"               Collection: nugget_lab.search_demo  → Dynamic Mapping")
        else:
            print(f"\n  [{label}] ERROR: {e}")
        return []

# ─────────────────────────────────────────────────────────────────────────────
# 1. Basic text search — query across all indexed fields (dynamic mapping)
# ─────────────────────────────────────────────────────────────────────────────
run_search("text: wireless headphones", [
    {"$search": {
        "index": "default",
        "text": {
            "query": "wireless headphones",
            "path": {"wildcard": "*"},   # search all indexed fields
        },
    }},
    {"$addFields": {"score": {"$meta": "searchScore"}}},
    {"$sort": {"score": -1}},
], {"_id": 0, "name": 1, "price": 1, "category": 1, "score": 1})

# ─────────────────────────────────────────────────────────────────────────────
# 2. Fuzzy search — handles typos ("wireles" → "wireless")
# ─────────────────────────────────────────────────────────────────────────────
run_search("fuzzy: 'wireles keyborad'", [
    {"$search": {
        "index": "default",
        "text": {
            "query": "wireles keyborad",
            "path": {"wildcard": "*"},
            "fuzzy": {"maxEdits": 1, "prefixLength": 2},
        },
    }},
    {"$addFields": {"score": {"$meta": "searchScore"}}},
    {"$sort": {"score": -1}},
    {"$limit": 3},
], {"_id": 0, "name": 1, "score": 1, "category": 1, "price": 1})

# ─────────────────────────────────────────────────────────────────────────────
# 3. Compound search — must match "Apple" AND should prefer "laptop"
#    compound.must: all must match (AND).
#    compound.should: optional boosters — not required, but boost score if matched.
# ─────────────────────────────────────────────────────────────────────────────
run_search("compound: brand=Apple + should:laptop", [
    {"$search": {
        "index": "default",
        "compound": {
            "must": [
                {"text": {"query": "Apple", "path": "brand"}},
            ],
            "should": [
                {"text": {"query": "laptop", "path": {"wildcard": "*"}}},
            ],
        },
    }},
    {"$addFields": {"score": {"$meta": "searchScore"}}},
    {"$sort": {"score": -1}},
], {"_id": 0, "name": 1, "score": 1, "price": 1, "brand": 1})

# ─────────────────────────────────────────────────────────────────────────────
# 4. Range filter within search — price between $100 and $500
#    Combining text search + numeric range in a compound query.
# ─────────────────────────────────────────────────────────────────────────────
run_search("compound: text=monitor + range price $100-$500", [
    {"$search": {
        "index": "default",
        "compound": {
            "must": [
                {"text": {"query": "monitor", "path": {"wildcard": "*"}}},
                {"range": {"path": "price", "gte": 100, "lte": 500}},
            ],
        },
    }},
    {"$addFields": {"score": {"$meta": "searchScore"}}},
    {"$sort": {"score": -1}},
], {"_id": 0, "name": 1, "price": 1, "score": 1})

db.drop_collection("search_demo")
print()
