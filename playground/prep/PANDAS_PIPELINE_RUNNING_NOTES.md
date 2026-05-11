# Pandas Pipeline Running Notes

This is a running side-note document for Pandas pipeline patterns.
Each section should answer:
- What it is
- When to use it
- Mental model
- Python template
- Common mistake
- One sentence to memorize

<a id="toc"></a>

## Table of Contents

- [1. Basic Pandas Pipeline Shape](#pattern-01-basic-pandas-pipeline-shape)

---

<a id="pattern-01-basic-pandas-pipeline-shape"></a>
## 1. Basic Pandas Pipeline Shape

What it is:
A basic Pandas pipeline is a clear sequence of steps:
read, inspect, clean, convert, derive, validate, aggregate, and export.

When to use it:
Use this pattern when working with CSV, Excel, small/medium datasets,
local data checks, quick reporting, or prototype logic before moving to Spark.

Mental model:
Pandas pipeline = small local ETL.

Pipeline stages:
1. Read data.
2. Inspect shape, rows, types, and missing values.
3. Clean column names.
4. Normalize text fields.
5. Convert dates and numeric columns.
6. Add derived fields.
7. Run data quality checks.
8. Filter or quarantine bad rows.
9. Aggregate results.
10. Export output.

Python template:

```python
import pandas as pd

# 1. Read data
df = pd.read_csv("telemetry_samples.csv")

# 2. Inspect
print(df.shape)
print(df.head())
print(df.info())
print(df.isna().sum())

# 3. Clean column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# 4. Normalize text fields
df["service_name"] = df["service_name"].str.strip().str.lower()
df["host_name"] = df["host_name"].str.strip().str.lower()

# 5. Convert data types
df["sampled_at"] = pd.to_datetime(df["sampled_at"], errors="coerce")
df["cpu_percent"] = pd.to_numeric(df["cpu_percent"], errors="coerce")
df["memory_percent"] = pd.to_numeric(df["memory_percent"], errors="coerce")

# 6. Add derived fields
df["sample_date"] = df["sampled_at"].dt.date

# 7. Data quality checks
quality_summary = {
    "total_rows": len(df),
    "missing_sampled_at": df["sampled_at"].isna().sum(),
    "missing_service_name": df["service_name"].isna().sum(),
    "missing_cpu": df["cpu_percent"].isna().sum(),
    "duplicate_rows": df.duplicated().sum(),
}

print(quality_summary)

# 8. Keep usable rows
clean_df = df.dropna(
    subset=["sampled_at", "service_name", "cpu_percent"]
)

# 9. Aggregate
service_summary = (
    clean_df
      .groupby(["sample_date", "service_name"], as_index=False)
      .agg(
          sample_count=("cpu_percent", "count"),
          avg_cpu=("cpu_percent", "mean"),
          max_cpu=("cpu_percent", "max"),
          avg_memory=("memory_percent", "mean"),
      )
)

# 10. Export
service_summary = service_summary.sort_values(
    ["sample_date", "service_name"]
)

service_summary.to_csv("service_summary.csv", index=False)
```

Common mistake:
Doing transformations before inspecting data quality.
Always inspect shape, types, missing values, and sample rows first.

Another common mistake:
Using errors="coerce" but never checking how many values became null.

Memorize:
In Pandas, I read, inspect, clean, convert, derive, validate, aggregate, and export.

Strong practical sentence:
I use Pandas for local pipeline prototyping and data quality checks,
then move the same pattern to Spark when data volume requires distributed processing.

[Back to TOC](#toc)

---
