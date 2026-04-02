# Databases R1 — What Was Built (No Prompts)

Status: R1 notebooks were built directly by Claude + Sean, not through the ChatGPT/Gemini prompt system.
This file documents what exists so future sessions have full context.

## Deliverables

All 9 intro notebooks are complete. Concept .md files are not yet built.

| ID | File | Type | Status | Notes |
|----|------|------|--------|-------|
| R1-A1 | `sql_relational_intro.ipynb` | notebook | ✅ | 5 live queries on telemetry data, EXPLAIN shows seq scan on metrics |
| R1-A2 | `relational_concepts.md` | concepts | ⬜ | MVCC, WAL, B-tree index, query planner |
| R1-B1 | `columnar_intro.ipynb` | notebook | ✅ | DuckDB attached to Postgres, 4 queries timed, comparison table |
| R1-B2 | `columnar_concepts.md` | concepts | ⬜ | Columnar vs row storage, vectorized execution, compression |
| R1-C1 | `document_intro.ipynb` | notebook | ✅ | MongoDB document model, telemetry as JSON documents |
| R1-C2 | `document_concepts.md` | concepts | ⬜ | Schema-less tradeoffs, embedding vs referencing, index types |
| R1-D1 | `keyvalue_intro.ipynb` | notebook | ✅ | Redis data structures, cache the endpoint lookup |
| R1-D2 | `keyvalue_concepts.md` | concepts | ⬜ | When KV wins, TTL, eviction, Redis vs Memcached |
| R1-E1 | `widecolumn_intro.ipynb` | notebook | ✅ | Cassandra mental model, CQL, write telemetry metrics |
| R1-E2 | `widecolumn_concepts.md` | concepts | ⬜ | Partition key design, consistency levels, CAP position |
| R1-F1 | `graph_intro.ipynb` | notebook | ✅ | Neo4j, endpoint dependencies as graph, first Cypher |
| R1-F2 | `graph_concepts.md` | concepts | ⬜ | Nodes/edges/properties, when graph wins, Cypher vs SQL |
| R1-G1 | `timeseries_intro.ipynb` | notebook | ✅ | InfluxDB, write telemetry metrics with timestamps, first Flux query |
| R1-G2 | `timeseries_concepts.md` | concepts | ⬜ | Time-series data model, retention, downsampling, Citi narrative |
| R1-H1 | `vector_intro.ipynb` | notebook | ✅ | pgvector, embed alert text, first similarity search |
| R1-H2 | `vector_concepts.md` | concepts | ⬜ | Embeddings, ANN, cosine similarity, RAG connection |
| R1-I1 | `search_intro.ipynb` | notebook | ✅ | ES match, bool, aggs, fuzzy, multi_match + date range, 25K alerts |
| R1-I2 | `search_concepts.md` | concepts | ⬜ | Inverted index, relevance scoring, when search wins vs SQL LIKE |

## Note on concepts files (R1-x2)

The 9 concept .md files were planned but not built. They are simple reference documents.
If needed, say "Build Databases R1 concept files" and Claude will generate prompts for them.
The R2 QA and nuggets files cover the same material at greater depth — the concepts files are optional.

## Notebooks location

All 9 notebooks live in: `D:\Workspace\Basics\Databases\`

