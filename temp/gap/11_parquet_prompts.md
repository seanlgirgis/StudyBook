# Parquet — ChatGPT Project Prompts

Priority: 🔴 Critical — every data engineer must explain why Parquet

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Apache Parquet for Data Engineers
Slug: parquet
Extra coverage required: why columnar storage — row-based vs column-based layout and what changes at the I/O level,
predicate pushdown — how the query engine skips row groups it doesn't need without reading them,
column pruning — reading only the columns a query touches, why this matters at scale,
row groups, pages, and the Parquet file structure — what each level is and why the layout exists,
compression — Snappy vs Gzip vs Zstd — trade-offs between CPU cost and compression ratio,
encoding schemes — dictionary encoding, run-length encoding, delta encoding — when each applies,
statistics — min/max per row group and why they enable pushdown,
schema evolution — adding columns, removing columns, renaming — what's safe and what breaks,
Parquet vs CSV — why you'd never use CSV at scale, the specific costs of text parsing,
Parquet vs Avro vs ORC — when each format wins and the ecosystems they belong to,
partitioning strategy — hive-style partitioning on S3, partition pruning, cardinality trade-offs,
small file problem — what it is, why it degrades performance, compaction strategies,
reading and writing Parquet in Python — pyarrow vs fastparquet, pandas read_parquet, PySpark,
Parquet in the lakehouse — how Delta Lake and Iceberg build on Parquet,
real scenario: designing the storage layer for a 65,000-endpoint telemetry pipeline.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug parquet -ChunkSize 750
```

Upload final_parquet.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_parquet.mp3` is live on R2.

```
Topic: Apache Parquet for Data Engineers
Slug: parquet
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_parquet.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
Why Columnar Storage | File Structure (Row Groups & Pages) | Compression | Encoding Schemes | Predicate & Column Pushdown | Schema Evolution | Parquet vs CSV vs Avro vs ORC | Partitioning Strategy | Small Files & Lakehouse Integration
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\parquet.html
