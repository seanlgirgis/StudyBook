# Delta Lake — ChatGPT Project Prompts

Priority: 🟡 Good to have — Toyota gap #9

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Delta Lake
Slug: delta-lake

Extra coverage required:
- What Delta Lake is — an open table format layered on Parquet files that adds ACID transactions to S3 or ADLS object storage
- The transaction log — _delta_log directory of JSON commit files; every write appends a new entry; how this enables snapshot isolation
- ACID on object storage — atomicity via atomic log commits, isolation via snapshot reads, durability via S3; what each means practically
- Time travel — VERSION AS OF and TIMESTAMP AS OF; querying the table as it existed at any past commit; use cases: audit, rollback, debugging
- Schema enforcement — Delta rejects writes that don't match the declared schema by default; prevents silent data corruption
- Schema evolution — mergeSchema option to safely add new columns; column renaming and type changes and what's safe vs breaking
- MERGE INTO — the primary pattern for CDC (change data capture) upserts; matched vs not-matched clauses; why idempotency matters here
- OPTIMIZE — compacting many small Parquet files into fewer large ones; when to run it and how often
- Z-ORDER clustering — co-locating rows with similar values on the same files; improves filter pushdown on high-cardinality columns; pick 1-2 columns max
- VACUUM — removing old snapshot files beyond the retention threshold; why retention must be >= your time travel window; default 7 days
- Delta vs Iceberg vs Hudi — ecosystem support, AWS native integration, Databricks vs open community; when each wins
- Delta on AWS — using Delta with EMR, Glue 4.0 (native support), and Athena (via manifest files or native Delta support)
- Databricks and Delta — Delta Live Tables for declarative pipeline authoring; Auto Loader for incremental S3 ingestion

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug delta-lake -ChunkSize 750
```

Upload final_delta-lake.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_delta-lake.mp3` is live on R2.

```
Topic: Delta Lake
Slug: delta-lake
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_delta-lake.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Delta Lake Is — open table format on Parquet
  2. The Transaction Log & ACID on Object Storage
  3. Time Travel — VERSION AS OF, TIMESTAMP AS OF
  4. Schema Enforcement & Evolution
  5. MERGE INTO — CDC upsert pattern
  6. OPTIMIZE & Z-ORDER
  7. VACUUM — retention and time travel window
  8. Delta vs Iceberg vs Hudi
  9. Delta on AWS & Databricks
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\delta-lake.html
