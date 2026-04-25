# DuckDB — ChatGPT Project Prompts

Priority: 🔴 Critical — hot in modern data stack, used in HorizonScale Phase 1

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: DuckDB for Data Engineers
Slug: duckdb
Extra coverage required: what DuckDB is — in-process OLAP database, no server, runs inside Python or CLI,
why DuckDB is fast — columnar execution, vectorized query engine, SIMD, parallel query within a process,
DuckDB vs SQLite — both embedded, but SQLite is row-store OLTP, DuckDB is columnar OLAP — completely different use cases,
DuckDB vs Pandas — SQL over DataFrames, reading Parquet directly from S3, zero-copy integration with Arrow,
DuckDB vs Spark — when DuckDB on a single machine outperforms Spark on a cluster (sub-100GB datasets),
reading Parquet files directly — SELECT * FROM read_parquet('path/*.parquet') with partition awareness,
reading CSV and JSON — auto schema detection, handling malformed files,
querying S3 directly — httpfs extension, AWS credential configuration, s3:// paths,
Python API — duckdb.connect(), .execute(), .fetchdf(), .arrow(), .relation() API,
window functions in DuckDB — LAG, LEAD, RANK, DENSE_RANK, ROW_NUMBER — the syntax and common patterns,
writing results — COPY TO parquet, EXPORT DATABASE, writing to Pandas,
in-memory vs persistent database — when to use each,
DuckDB for data pipeline development — local development against S3 data, replacing a Spark dev environment,
DuckDB in production — appropriate scale, limitations (single node, no distributed mode),
real scenario: using DuckDB for risk detection queries across 8,000+ forecast series in HorizonScale.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\duckdb.html
