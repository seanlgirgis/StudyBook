# Pandas — ChatGPT Project Prompts

Priority: 🔴 Critical — core Python data engineering tool

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Pandas for Data Engineers
Slug: pandas

Extra coverage required:
- DataFrame and Series — the two core structures; the index concept and why it matters for alignment and joins
- Reading data — read_csv (sep, dtype, parse_dates, chunksize), read_parquet (columns, filters for pushdown), read_sql_query with a SQLAlchemy engine
- Selection and filtering — loc (label-based), iloc (position-based), boolean masks; why chaining conditions requires parentheses
- Merge and join — pd.merge vs DataFrame.join; how, on, left_on/right_on parameters; left/right/inner/outer; indicator=True for debugging unmatched rows
- GroupBy — split-apply-combine; agg (multiple functions at once), transform (returns same-shape output), apply (escape hatch, use sparingly)
- dtypes and memory — object vs StringDtype, int64 vs Int64 (nullable), category for low-cardinality columns; astype() for downcasting; why dtypes matter at 65K rows
- Method chaining — pipe(), assign(), query() — writing readable transformation sequences without intermediate variables
- Handling missing data — NaN vs None vs pd.NA; fillna, dropna, isnull; why NaN propagates silently through arithmetic
- Time series — DatetimeIndex, resample() for downsampling, rolling() for moving averages, shift() for lag features, date_range()
- Pivot and melt — pivot_table for wide aggregations, melt for wide-to-long reshaping; common ETL pattern when normalizing source data
- String operations — str accessor for vectorized string methods; str.contains, str.replace with regex; cleaning hostname and department fields
- Performance pitfalls — iterrows is 100x slower than vectorized ops; SettingWithCopyWarning explained; copy vs view distinction; when to use .values vs .to_numpy()
- When Pandas isn't enough — the scale threshold (roughly 10M+ rows or >4GB); when to move to Polars, DuckDB, or PySpark

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug pandas -ChunkSize 750
```

Upload final_pandas.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_pandas.mp3` is live on R2.

```
Topic: Pandas for Data Engineers
Slug: pandas
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_pandas.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. DataFrames & Series — structure and index
  2. Reading Data — CSV, Parquet, SQL
  3. Selection & Filtering — loc, iloc, boolean masks
  4. Merge & Join — parameters and gotchas
  5. GroupBy — agg vs transform vs apply
  6. dtypes & Memory Optimization
  7. Method Chaining & Missing Data
  8. Time Series Operations
  9. Performance Pitfalls & Scale Limits
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pandas.html
