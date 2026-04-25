# SQL Patterns for Data Engineers — ChatGPT Project Prompts

Priority: 🔴 Critical — Toyota gap #3

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: SQL Patterns for Data Engineers
Slug: sql-patterns
Extra coverage required: window functions — ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE — real use cases not just syntax,
partitioned window frames — ROWS BETWEEN, RANGE BETWEEN — when each matters,
running totals and moving averages using window functions,
CTEs vs subqueries vs temp tables — readability, performance, and when each is the right tool,
recursive CTEs — hierarchical data, bill-of-materials, org charts,
Slowly Changing Dimensions — Type 1 overwrite, Type 2 history rows with effective dates, Type 3 current and previous,
SCD Type 2 in SQL — the full MERGE pattern with surrogate keys and row versioning,
incremental loads with MERGE and UPSERT — INSERT ... ON CONFLICT, MERGE INTO,
deduplication — ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) pattern,
anti-joins — finding rows in A not in B using LEFT JOIN IS NULL vs NOT EXISTS,
set operations — UNION vs UNION ALL, INTERSECT, EXCEPT — when each is correct,
EXPLAIN plan reading — understanding sequential scan vs index scan, hash join vs nested loop,
analytical functions for data engineering — percentiles, histograms, cohort analysis,
SQL for data quality — reconciliation queries, null counts, duplicate detection,
common SQL interview traps — NULLs in aggregations, COUNT(*) vs COUNT(col), GROUP BY pitfalls.
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug sql-patterns -ChunkSize 750
```

Upload final_sql-patterns.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_sql-patterns.mp3` is live on R2.

```
Topic: SQL Patterns for Data Engineers
Slug: sql-patterns
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_sql-patterns.mp3
Today's date: 2026-04-25
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\sql-patterns.html
