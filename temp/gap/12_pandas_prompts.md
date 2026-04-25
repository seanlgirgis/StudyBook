# Pandas — ChatGPT Project Prompts

Priority: 🔴 Critical — core Python data engineering tool

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Pandas for Data Engineers
Slug: pandas
Extra coverage required: DataFrame and Series — the core data structures, index concept and why it matters,
reading data — read_csv, read_parquet, read_sql — key parameters and gotchas,
selection and filtering — loc vs iloc vs boolean masks — when to use each and the performance difference,
merge and join — merge vs join, how and on parameters, left/right/inner/outer, indicator column for debugging,
groupby — split-apply-combine pattern, agg vs transform vs apply — critical distinction,
apply vs vectorized operations — why apply is slow and when you truly can't avoid it,
dtypes — int64 vs Int64 (nullable), object vs StringDtype, category dtype for low-cardinality columns,
memory optimization — astype to downcast, category columns, chunked reading with chunksize,
method chaining — pipe, assign, query — writing readable pipeline-style transformations,
handling missing data — NaN vs None vs pd.NA, fillna, dropna, isnull strategies,
time series in Pandas — DatetimeIndex, resample, rolling, shift, date_range,
pivot_table and melt — reshaping data wide-to-long and long-to-wide,
string operations — str accessor, regex in Pandas, common cleaning patterns,
performance pitfalls — iterrows (never), copy vs view, SettingWithCopyWarning explained,
Pandas in ETL pipelines — reading from Oracle/SQL Server, transforming, writing to SQLite/Parquet,
when Pandas isn't enough — the scale threshold where you move to Polars, DuckDB, or PySpark.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

Content sections — create exactly these, in this order:
DataFrames & Series | Reading Data | Selection & Filtering | Merge & Join | GroupBy | dtypes & Memory Optimization | Method Chaining | Missing Data | Time Series | Performance Pitfalls
Then add: Interview Q&A (6 pairs) | Quick Reference (12-15 rows)
Size per section: 2-3 tight paragraphs, one code block max (20 lines). No tutorials.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\pandas.html
