# Parquet — ChatGPT Project Prompts

Priority: 🔴 Critical — every data engineer must explain why Parquet

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Apache Parquet for Data Engineers
Slug: parquet

Extra coverage required:
- Why columnar storage — row-based formats read every column to return one; columnar reads only the columns the query touches; the I/O savings at scale
- File structure — row groups (horizontal slices), column chunks, pages; why this three-level layout enables both column pruning and predicate pushdown
- Compression — Snappy (fast, moderate ratio, default), Gzip (slow, high ratio), Zstd (best balance, preferred for cold storage); applied per column chunk
- Encoding schemes — dictionary encoding (replaces repeated values with integer IDs), run-length encoding (repeated runs), delta encoding (sequential integers); chosen automatically per column
- Statistics — min/max and null count stored per row group per column; how the query engine uses these to skip entire row groups without reading them
- Predicate pushdown — filter applied before data leaves storage; "WHERE region = 'US'" skips all row groups whose max(region) < 'US'
- Column pruning — SELECT id, value reads only two column chunks from disk, not the entire file; critical for wide tables
- Schema evolution — adding nullable columns is safe; removing or renaming columns breaks readers; the rules every DE must know
- Parquet vs CSV — CSV has no types, no compression, no pushdown, requires full scan for every query; never use CSV at scale
- Parquet vs Avro vs ORC — Parquet: columnar, analytics; Avro: row-based, schema evolution in Kafka; ORC: columnar, Hive ecosystem; know when each appears
- Partitioning strategy — hive-style partition folders on S3 (year=2024/month=01/); partition pruning eliminates entire folders; low-cardinality columns only
- Small file problem — thousands of small Parquet files degrade S3 list performance and Spark parallelism; OPTIMIZE or compaction jobs required
- Parquet in Python — pyarrow (faster, more features), fastparquet (lighter); pandas read_parquet / to_parquet; PySpark native support

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. Why Columnar Storage — the I/O argument
  2. File Structure — row groups, column chunks, pages
  3. Compression — Snappy vs Gzip vs Zstd
  4. Encoding Schemes — dictionary, RLE, delta
  5. Predicate Pushdown & Column Pruning
  6. Schema Evolution — what's safe, what breaks
  7. Parquet vs CSV vs Avro vs ORC
  8. Partitioning Strategy on S3
  9. Small Files & Parquet in Python
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\parquet.html
