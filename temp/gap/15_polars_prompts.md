# Polars — ChatGPT Project Prompts

Priority: 🟠 Important — fast-growing Pandas alternative, used in HorizonScale Phase 1

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Polars for Data Engineers
Slug: polars

Extra coverage required:
- What Polars is — a DataFrame library written in Rust using the Apache Arrow memory model; multi-threaded by default, no Python GIL overhead
- Why it's faster than Pandas — parallel execution across all cores out of the box, lazy evaluation with query optimization, SIMD vectorized ops, zero-copy Arrow memory
- Eager vs lazy API — DataFrame (eager, executes immediately) vs LazyFrame (lazy, builds a plan and optimizes before executing); always prefer lazy for pipelines
- The lazy pipeline — scan_parquet / scan_csv, then chain filter/select/groupby, then .collect() to execute; what gets optimized automatically
- Query optimization — predicate pushdown (filters applied before reading), projection pushdown (only requested columns read), slice pushdown; all automatic in lazy mode
- Expressions — pl.col(), pl.lit(), pl.when().then().otherwise(); the building block of all transformations; replaces .apply() entirely
- GroupBy and aggregations — group_by().agg(); over() for window expressions (like SQL window functions but without a separate window clause)
- Joins — inner/left/outer/cross; how to handle duplicate column names with suffix parameter; join performance vs Pandas at scale
- String and datetime namespaces — pl.col("x").str.contains(), .str.replace(), .dt.strftime(), .dt.truncate(); clean accessor syntax
- Polars and Arrow — to_arrow() for zero-copy to PyArrow; from_arrow() back to Polars; direct DuckDB interop via Arrow
- When Polars wins — single-machine workloads where Pandas is too slow; CSV/Parquet pipelines in the 1–50GB range
- When to stay with Pandas — library ecosystem compatibility (sklearn, statsmodels expect Pandas); team familiarity; Pandas 2.0 with Arrow backend is competitive

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug polars -ChunkSize 750
```

Upload final_polars.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_polars.mp3` is live on R2.

```
Topic: Polars for Data Engineers
Slug: polars
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_polars.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. What Polars Is & Why It's Faster Than Pandas
  2. Eager vs Lazy API
  3. Query Optimization — predicate, projection, slice pushdown
  4. Expressions — the core building block
  5. GroupBy, Aggregations & Window Functions
  6. Joins & String / Datetime Operations
  7. Arrow Integration & Interop
  8. Polars vs Pandas — when to switch and when not to
  9. Polars in a Data Pipeline
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs; include a code block where it adds value (20 lines max)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\polars.html
