# dbt — ChatGPT Project Prompts

Priority: 🟠 Important — Toyota gap #5

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: dbt for Data Engineers
Slug: dbt

Extra coverage required:
- What dbt actually is — a SQL transformation tool that runs inside your warehouse, not an orchestrator or loader
- Models — SQL SELECT files that become tables or views; the ref() function for automatic dependency resolution
- Materializations — view (default, no storage), table (full rebuild), incremental (append/merge only new rows), ephemeral (CTE-only)
- Incremental models — is_incremental() filter pattern; unique_key for idempotent MERGE; strategies: append, merge, delete+insert
- Sources and seeds — declaring upstream raw tables with freshness checks; loading small static CSVs as lookup tables
- Built-in tests — not_null, unique, accepted_values, relationships; how they run as SQL assertions against your warehouse
- Custom tests — singular tests (one-off SQL files) and generic tests (reusable macros) for business-rule validation
- Macros — reusable Jinja SQL blocks for DRY transformations; packages from dbt Hub
- dbt docs — auto-generated lineage DAG and column-level descriptions; dbt docs serve for local browsing
- dbt Core vs dbt Cloud — open-source CLI vs managed platform; CI/CD integration differences
- SCD Type 2 snapshots — dbt snapshot command; dbt_valid_from, dbt_valid_to, dbt_updated_at columns
- dbt + Airflow — triggering dbt model runs as Airflow DAG tasks using BashOperator or the Cosmos package
- Common mistakes — incremental models without partitioning, missing unique_key causing duplicates, overusing ephemeral

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
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

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What dbt Is — and what it is not
  2. Models & ref() — dependency graph basics
  3. Materializations — view, table, incremental, ephemeral
  4. Incremental Models — strategies and unique_key
  5. Sources, Seeds & Built-in Tests
  6. Custom Tests & Macros
  7. dbt Docs & Lineage DAG
  8. SCD Type 2 Snapshots
  9. dbt + Airflow & CI/CD
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\dbt.html
