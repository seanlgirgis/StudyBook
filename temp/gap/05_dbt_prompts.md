# dbt — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #5

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: dbt for Data Engineers
Slug: dbt
Extra coverage required: what dbt actually is — a transformation tool that runs SQL inside your warehouse, not an orchestrator,
models — SQL SELECT files that become tables or views, the ref() function for dependency tracking,
materializations — view, table, incremental, ephemeral — when to choose each,
incremental models — is_incremental() filter, unique_key for idempotent MERGE, strategies (append, merge, delete+insert),
seeds — loading small static CSV files into the warehouse for lookup tables,
sources — declaring upstream raw tables, freshness checks,
tests — not_null, unique, accepted_values, relationships — the data quality layer built into dbt,
custom generic tests and singular tests for business-rule validation,
macros — reusable Jinja SQL for DRY transformations,
dbt documentation — auto-generated lineage DAG and column-level descriptions,
dbt Core vs dbt Cloud — open source CLI vs managed platform, CI/CD integration,
dbt + Airflow — orchestrating dbt model runs as DAG tasks,
dbt for SCD Type 2 — snapshot models, dbt_updated_at, dbt_valid_from, dbt_valid_to,
dbt for data engineering — building the gold layer of a medallion architecture,
common mistakes — wide incremental models without partitioning, missing unique_key, overusing ephemeral.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
```
run_mission_audio.ps1 -Slug dbt -ChunkSize 750
```

Upload final_dbt.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_dbt.mp3` is live on R2.

```
Topic: dbt for Data Engineers
Slug: dbt
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_dbt.mp3
Today's date: 2026-04-25

Content sections — create exactly these, in this order:
What dbt Is | Models & ref() | Materializations | Incremental Models | Sources, Seeds & Tests | Macros & Jinja | dbt Docs & Lineage | SCD Snapshots | dbt + Airflow & CI
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\dbt.html
