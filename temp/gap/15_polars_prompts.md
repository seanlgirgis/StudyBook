# Polars — ChatGPT Project Prompts

Priority: 🟠 Important — fast-growing Pandas alternative, used in HorizonScale Phase 1

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Polars for Data Engineers
Slug: polars
Extra coverage required: what Polars is — DataFrame library written in Rust, Apache Arrow memory model,
why Polars is faster than Pandas — multi-threaded by default, lazy evaluation, SIMD, no Python GIL overhead,
eager vs lazy API — DataFrame (eager, executes immediately) vs LazyFrame (lazy, builds a query plan),
the lazy API pipeline — scan_parquet / scan_csv, filter, select, groupby, collect — why this pattern exists,
query optimization — predicate pushdown, projection pushdown, slice pushdown — what Polars does automatically,
Polars vs Pandas API differences — no index concept, method chaining is idiomatic, expressions instead of apply,
expressions — pl.col(), pl.lit(), pl.when().then().otherwise() — the core building block,
groupby and aggregations — group_by, agg, over (window expressions without groupby),
joins — inner/left/outer, cross join, how to handle duplicate column names after join,
reading and writing Parquet, CSV, JSON — scan_parquet for lazy, read_parquet for eager,
string operations — the Polars str namespace, regex matching, splitting, replacing,
datetime handling — the dt namespace, date_range, truncate, strftime,
Polars and Arrow — to_arrow(), from_arrow(), zero-copy interop with DuckDB and PyArrow,
Polars in a pipeline — replacing Pandas in an ETL script, what to rewrite vs keep,
when Polars wins over Pandas — the scale and speed threshold,
when to still use Pandas — ecosystem compatibility, libraries that expect Pandas DataFrames.
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
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\polars.html
