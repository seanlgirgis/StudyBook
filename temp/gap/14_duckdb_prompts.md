# DuckDB — ChatGPT Project Prompts

Priority: 🔴 Critical — hot in modern data stack, used in HorizonScale Phase 1

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: DuckDB for Data Engineers
Slug: duckdb

Extra coverage required:
- What DuckDB is — an in-process OLAP database; no server, no installation beyond pip install duckdb; runs inside Python or CLI
- Why it's fast — columnar vectorized execution engine, SIMD instructions, parallel query within a single process, automatic predicate pushdown on Parquet
- DuckDB vs SQLite — both embedded, zero server; SQLite is row-store OLTP (writes, small lookups), DuckDB is columnar OLAP (analytical aggregations); completely different use cases
- DuckDB vs Pandas — DuckDB can query a Pandas DataFrame with SQL; avoids Python loops; zero-copy via Apache Arrow interchange
- DuckDB vs Spark — on a single machine with <100GB, DuckDB is often faster than a local Spark cluster and requires zero infrastructure
- Reading Parquet directly — SELECT * FROM read_parquet('path/*.parquet') with automatic schema detection and partition-aware filtering
- Querying S3 — INSTALL httpfs; LOAD httpfs; SET s3_region; then read_parquet('s3://bucket/prefix/*.parquet') directly without downloading
- Python API — duckdb.connect(), .execute(sql), .fetchdf() returns Pandas DataFrame, .arrow() returns PyArrow table, .relation() for lazy query building
- Window functions — LAG, LEAD, RANK, DENSE_RANK, ROW_NUMBER with PARTITION BY and ORDER BY; identical syntax to PostgreSQL
- Writing results — COPY (SELECT ...) TO 'output.parquet' (FORMAT PARQUET); INSERT INTO; EXPORT DATABASE for full database export
- In-memory vs persistent — duckdb.connect() is in-memory (lost on exit); duckdb.connect('file.db') persists to disk
- When DuckDB is the right tool — local development against S3 data, risk detection queries on forecast outputs, ad-hoc analytics on Parquet files
- Limitations — single node only, no distributed mode; not a replacement for Spark at multi-TB scale or for concurrent write workloads

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug duckdb -ChunkSize 750
```

Upload final_duckdb.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_duckdb.mp3` is live on R2.

```
Topic: DuckDB for Data Engineers
Slug: duckdb
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_duckdb.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What DuckDB Is & Why It's Fast
  2. DuckDB vs SQLite vs Pandas vs Spark
  3. Reading Parquet & CSV Directly
  4. Querying S3 with httpfs
  5. Python API — connect, execute, fetchdf, arrow
  6. Window Functions
  7. Writing Results & In-Memory vs Persistent
  8. When to Use DuckDB — and When Not To
  9. Real-World Pipeline Patterns
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\duckdb.html
