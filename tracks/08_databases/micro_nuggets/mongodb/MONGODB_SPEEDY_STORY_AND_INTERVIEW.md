# MongoDB Micro-Nuggets — Story & Interview Guide

## Why MongoDB, Not Just "A Document Database"

MongoDB is not just a JSON store. It is a fully ACID-capable, horizontally
scalable operational database that natively understands documents, arrays,
and nested objects — the shapes that modern applications actually produce.

Key differences you should internalize:
- **Document model**: data lives as BSON documents. No schema migration when
  your product shape changes — just start using new fields.
- **Flexible schema + optional validation**: start flexible, add JSON Schema
  validators as your data matures. Both extremes are possible.
- **Aggregation Pipeline**: server-side analytics without leaving the DB.
  $group, $lookup, $facet, $setWindowFields — it is a real analytics engine.
- **Change Streams**: built-in CDC from the oplog. Real-time event streams
  without Debezium or additional middleware.
- **Atlas**: the managed cloud offering adds Search (Lucene), Charts,
  Triggers, and App Services on top of the core database.

For DE learners, MongoDB teaches you: document modeling decisions (embed vs
reference), operational write patterns (upsert, bulk_write, TTL), and
real-time pipeline patterns (Change Streams → Kafka → MongoDB).

---

## Nugget Journey Map

Run in this order for fastest understanding:

### 0. Setup
```
00_setup/00_prereq_check.py    ← Python, pymongo, certifi, live ping
00_setup/01_connection.py      ← minimal connect/ping/close pattern
00_setup/02_session_context.py ← server info, topology, collection inventory
```

### 1. Collections & Documents
```
01_collections_and_documents/01_create_collection.py  ← BSON types, ObjectId, insert_one
01_collections_and_documents/02_insert_many.py        ← ordered vs unordered, BulkWriteError
01_collections_and_documents/03_schema_validation.py  ← JSON Schema, validationLevel/Action
```

### 2. CRUD
```
02_crud_operations/01_find_and_filter.py   ← $eq $gt $in $or $regex $exists, projection
02_crud_operations/02_update_operators.py  ← $set $inc $mul $push $addToSet $pull $slice
02_crud_operations/03_delete_and_replace.py ← delete_one/many, find_one_and_delete, soft-delete
```

### 3. Indexes
```
03_indexes_and_performance/01_single_field_index.py     ← COLLSCAN→IXSCAN, unique, partial, sparse
03_indexes_and_performance/02_compound_and_text_index.py ← ESR rule, covered query, multikey, text
03_indexes_and_performance/03_index_analysis.py          ← explain(), $indexStats, prefix redundancy
```

### 4. Aggregation Pipeline
```
04_aggregation_pipeline/01_basic_pipeline.py   ← $match $group $project $sort $addFields $count
04_aggregation_pipeline/02_lookup_and_unwind.py ← $lookup (basic + pipeline form), $unwind
04_aggregation_pipeline/03_advanced_pipeline.py ← $facet $bucket $merge $setWindowFields
```

### 5. Data Modeling
```
05_data_modeling/01_embedding_pattern.py  ← embed vs reference, Subset, Bucket patterns
05_data_modeling/02_change_streams.py     ← watch(), resume token, CDC, fault-tolerant consumers
```

### 6. Transactions
```
06_transactions/01_multi_doc_transaction.py ← with_transaction(), ACID, retry semantics
06_transactions/02_bulk_write_ops.py        ← mixed ops, ordered/unordered, CDC apply pattern
```

### 7. Operations
```
07_operations/01_ttl_and_capped.py       ← TTL index, expireAfterSeconds, capped collections
07_operations/02_atlas_search.py         ← $search, fuzzy, compound, range (requires search index)
07_operations/03_operational_checks.py   ← serverStatus, dbStats, collStats, currentOp
```

### 8. Mini Capstone (run in order)
```
08_mini_capstone/01_land_raw_events.py  ← Bronze: ingest 500 events, idempotent upsert
08_mini_capstone/02_aggregate_silver.py ← Silver: $merge daily metrics pipeline
08_mini_capstone/03_upsert_gold.py      ← Gold: bulk_write dashboard-ready KPIs
08_mini_capstone/04_reset_lab.py        ← Drop all nugget_lab collections
```

---

## 60-Minute Sprint

If you only have one hour, do this minimal path:
1. `00_setup/01_connection.py`
2. `01_collections_and_documents/01_create_collection.py`
3. `02_crud_operations/01_find_and_filter.py`
4. `02_crud_operations/02_update_operators.py`
5. `03_indexes_and_performance/01_single_field_index.py`
6. `04_aggregation_pipeline/01_basic_pipeline.py`
7. `08_mini_capstone/01_land_raw_events.py` → `02_aggregate_silver.py`

---

## What This Teaches in DE Terms

- **Data modeling**: embed vs reference, Bucket Pattern for time-series.
- **Idempotent ingestion**: bulk_write with upsert — safe to re-run.
- **Bronze/Silver/Gold**: implemented as raw_events → silver_metrics → gold_dashboard.
- **CDC**: Change Streams with resume tokens — fault-tolerant event consumers.
- **Schema governance**: JSON Schema validators, validationLevel/Action.
- **Performance**: indexes, ESR rule, covered queries, explain analysis.
- **Transactions**: multi-document ACID with with_transaction() retry loops.
- **Operations**: TTL lifecycle, Atlas Search, server diagnostics.

---

## Core Concepts Glossary

| Term | Definition |
|---|---|
| BSON | Binary JSON — MongoDB's wire format. Superset of JSON with extra types (ObjectId, Date, Decimal128, Binary). |
| ObjectId | 12-byte auto-generated unique identifier. Embeds creation timestamp in the first 4 bytes. |
| Collection | Analogous to a table. Contains documents. Created on first write. |
| Document | A BSON object. The basic unit of storage. Each document has a unique `_id`. |
| Flexible Schema | Collections do not enforce a schema by default. Each document can have different fields. |
| Aggregation Pipeline | A sequence of stages that transforms documents server-side ($match → $group → $project → ...). |
| $lookup | LEFT OUTER JOIN across collections. Embeds joined docs as an array. |
| $unwind | Deconstructs an array field into one document per element. |
| $merge | Writes pipeline output into a collection (upsert). Used for materialized views. |
| Index | B-tree (or Lucene for Atlas Search) structure that accelerates queries. |
| COLLSCAN | Collection scan — reads every document. O(n). Avoid on large collections. |
| IXSCAN | Index scan — reads the B-tree. O(log n + k). Always preferred. |
| ESR Rule | Equality-Sort-Range — the correct field order for compound indexes. |
| Covered Query | A query where ALL required fields are in the index — no document reads needed. |
| TTL Index | Single-field index on a Date field that auto-deletes expired documents after N seconds. |
| Capped Collection | Fixed-size circular buffer. Oldest docs auto-evicted when full. |
| Change Stream | Real-time stream of oplog events (insert/update/delete). MongoDB's built-in CDC. |
| Resume Token | A cursor position token for Change Streams. Save it to resume after a crash. |
| with_transaction() | pymongo API that automatically retries multi-doc transactions on transient errors. |
| Write Concern | How many nodes must acknowledge a write. `w=majority` = durable across failures. |
| Read Concern | How fresh the read must be. `snapshot` = consistent point-in-time view (used in transactions). |
| Atlas Search | Lucene-based full-text search on Atlas. $search aggregation stage. Supports fuzzy, facets, autocomplete. |
| Replica Set | A group of mongod nodes that replicate data. Required for Change Streams and transactions. Atlas always runs replica sets. |

---

## Interview Cheat Sheet

### "What is the difference between embedding and referencing?"

**Embedding**: store related data inside the parent document as a subdocument
or array. Optimal for One-to-Few relationships where data is always read
together. One document read = all data needed. Downside: 16 MB limit,
write amplification when updating embedded items at scale.

**Referencing**: store the `_id` of the related document; query separately or
use `$lookup`. Optimal for One-to-Many / One-to-Squillions, when the child
has an independent lifecycle, or when multiple parents share the same child.

**Decision rule**: "Will you ALWAYS read the child with the parent? Is the child
list bounded in size?" → embed. Otherwise → reference.

---

### "How do MongoDB transactions work?"

MongoDB has been ACID at the single-document level since its inception. A
single `update_one` that modifies an embedded array is atomic — partial
updates cannot happen.

Multi-document ACID transactions (added in 4.0) work via:
1. `client.start_session()` → creates a ClientSession.
2. `session.with_transaction(callback)` → wraps the callback in a transaction.
   - Automatically retries on `TransientTransactionError` (network blips, elections).
   - Automatically retries commit on `UnknownTransactionCommitResult`.
3. ALL operations inside the callback pass `session=session`.
4. The callback must be idempotent (may run multiple times on retry).

Cost: transactions add latency and use more oplog space. Use only when you
actually need cross-document atomicity. Single-document operations do not need them.

---

### "What is the aggregation pipeline? How does it compare to SQL?"

The aggregation pipeline is MongoDB's server-side analytics engine. Documents
flow through a sequence of transformation stages, like Unix pipes:

```
$match → $group → $project → $sort → $limit → $out/$merge
```

| SQL | MongoDB Aggregation |
|---|---|
| WHERE | $match (early stages) |
| GROUP BY | $group with `_id` |
| SELECT / computed columns | $project / $addFields |
| HAVING | $match (after $group) |
| JOIN | $lookup |
| ORDER BY | $sort |
| LIMIT / OFFSET | $limit / $skip |
| INSERT INTO ... SELECT | $out / $merge |
| Window functions | $setWindowFields (5.0+) |
| Pivot-style multi-GROUP | $facet |
| Histogram | $bucket / $bucketAuto |

Key performance rule: **put $match first** so indexes can be used. A $match
after a $group filters aggregated results, not raw documents.

---

### "How do Change Streams work? How do you make them fault-tolerant?"

Change Streams are a cursor that tails MongoDB's oplog (the replication log).
They fire an event for every insert, update, replace, delete, and collection/
database-level operation.

Fault tolerance via **resume tokens**:
- Every change event has a `_id` field that is the resume token.
- Save the token to durable storage (another MongoDB collection, Redis, disk).
- On restart: `col.watch(resume_after=saved_token)` resumes from exactly where you left off.
- Without a resume token, events that occurred during downtime are missed.

Production pattern:
```python
with col.watch(pipeline=filter_pipeline, full_document="updateLookup") as stream:
    while True:
        change = stream.try_next()
        if change is None:
            time.sleep(0.1)
            continue
        process(change)
        save_checkpoint(change["_id"])   # persist resume token
```

`full_document="updateLookup"`: for update events, performs an extra read
to return the full document. Adds latency. May return `None` if the document
was deleted between the event and the lookup.

---

### "When would you use a TTL index vs a capped collection?"

**TTL index** (`expireAfterSeconds`):
- Deletes documents based on a Date field value + TTL.
- Supports any collection. Documents can be queried, updated, indexed normally.
- Good when you want a time-based retention policy (e.g., keep last 30 days).
- Deletion runs in a background thread every ~60 seconds (not instant).

**Capped collection**:
- Fixed-size circular buffer. Oldest docs evicted when full.
- Cannot delete individual documents. Insertion order is guaranteed.
- Good when you care about storage bound, not time window (e.g., last 10K log lines).
- Enables tailable cursors (`tail -f` equivalent).

**Both together**: use a capped collection for raw high-frequency logs (storage bound),
and a TTL index on a separate normalized collection for business records (time bound).

---

### "What is the ESR rule for compound indexes?"

**E**quality → **S**ort → **R**ange

When creating a compound index, place fields in this order:
1. Fields you filter with exact equality first (`status = 'active'`).
2. Fields you sort on next (`ORDER BY created_at DESC`).
3. Fields you filter with range queries last (`score BETWEEN 100 AND 500`).

**Why**: MongoDB uses the index prefix for equality lookups, then walks it
in order for sorts (avoiding in-memory sort), then applies the range filter.
Deviating from ESR often forces MongoDB to do an in-memory `SORT` stage,
which is O(n log n) and can spill to disk.

**Example**: `find({status:'active'}).sort({date:-1}).filter({score:{$gt:100}})`
→ Index: `(status, date, score)` — Equality: status, Sort: date, Range: score.

---

### "How does MongoDB Atlas Search differ from $text?"

| Feature | $text (core MongoDB) | Atlas Search ($search) |
|---|---|---|
| Engine | MongoDB B-tree + stemmer | Apache Lucene |
| Fuzzy matching | ❌ | ✅ maxEdits |
| Autocomplete | ❌ | ✅ n-gram analyzer |
| Facets | ❌ | ✅ $searchMeta |
| Synonyms | ❌ | ✅ synonym mapping |
| Geo search | ❌ | ✅ |
| Relevance tuning | Basic | Full boost/score |
| Collection limit | 1 text index | Multiple search indexes |
| Availability | All MongoDB | Atlas clusters only |

Use `$text` for simple keyword search on self-hosted MongoDB or small collections.
Use Atlas Search for production-grade search features (autocomplete, fuzzy, facets).

---

## Troubleshooting Quick Reference

| Problem | Check |
|---|---|
| ServerSelectionTimeoutError | IP not whitelisted in Atlas Network Access |
| Authentication failed | Wrong username/password or wrong auth database |
| No $search index | Create "default" dynamic search index in Atlas UI |
| TTL not deleting | TTLMonitor runs every ~60s; Atlas may defer under load |
| Slow query (COLLSCAN) | Add index; check `explain("executionStats")` |
| Transaction aborted | Wrap in `with_transaction()` for auto-retry |
| BulkWriteError | Use `ordered=False` + inspect `exc.details["writeErrors"]` |
| 16 MB document limit | Refactor: reference instead of embed; use Bucket Pattern |
