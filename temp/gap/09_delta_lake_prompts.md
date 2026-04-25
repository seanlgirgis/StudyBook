# Delta Lake — ChatGPT Project Prompts

Priority: 🟡 Good to have — Toyota gap #9

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Delta Lake
Slug: delta-lake
Extra coverage required: what Delta Lake is — an open table format that adds ACID transactions to files on S3 or ADLS,
the transaction log — _delta_log directory, JSON commit files, how it enables ACID on object storage,
ACID on object storage — atomicity via log commits, isolation via snapshot reads, durability via S3,
time travel — VERSION AS OF, TIMESTAMP AS OF — querying historical snapshots for audit and recovery,
schema enforcement — Delta rejects writes that don't match the declared schema by default,
schema evolution — mergeSchema option, column addition and renaming, evolving production tables safely,
MERGE INTO — upsert pattern for CDC loads, matched vs not-matched clauses,
OPTIMIZE — compacting small files into larger Parquet files for faster reads,
Z-ORDER clustering — co-locating related data to improve filter pushdown on high-cardinality columns,
VACUUM — removing old snapshot files, retention period, why you must keep retention >= time travel window,
Delta vs Iceberg vs Hudi — the open table format comparison — ecosystem, features, AWS support,
Delta Lake on AWS — using Delta with EMR, Glue, and Athena (via manifest or native support),
Databricks and Delta — Delta Live Tables, Auto Loader for incremental S3 ingestion,
Delta for manufacturing data — append-only sensor streams, merge for device state tables,
cost and performance tradeoffs — small file problem, OPTIMIZE cadence, Z-ORDER column selection.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

Content sections — create exactly these, in this order:
What Delta Lake Is | Transaction Log & ACID | Time Travel | Schema Enforcement & Evolution | MERGE INTO & CDC | OPTIMIZE & Z-ORDER | VACUUM | Delta vs Iceberg vs Hudi | Delta on AWS & Databricks
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\delta-lake.html
