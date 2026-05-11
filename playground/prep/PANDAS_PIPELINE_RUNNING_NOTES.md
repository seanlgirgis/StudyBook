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
- [2. Clean Column Names and Normalize Text Fields](#pattern-02-clean-column-names-and-normalize-text-fields)
- [3. Convert Data Types Safely](#pattern-03-convert-data-types-safely)
- [4. Data Quality Summary](#pattern-04-data-quality-summary)
- [5. Deduplication With Survivor Selection](#pattern-05-deduplication-with-survivor-selection)
- [6. Group and Aggregate With groupby](#pattern-06-group-and-aggregate-with-groupby)
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

<a id="pattern-02-clean-column-names-and-normalize-text-fields"></a>
## 2. Clean Column Names and Normalize Text Fields

What it is:
This pattern standardizes messy column names and text values early in a Pandas pipeline.

When to use it:
Use it after reading a file and before joins, grouping, deduplication, or validation.

Mental model:
Clean columns make code easier.
Clean text values make matching and grouping reliable.

Basic column-cleaning template:

```python
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)
```

Production-friendlier column-cleaning template:

```python
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(r"[^a-z0-9]+", "_", regex=True)
      .str.strip("_")
)
```

Meaning:

- strip removes leading and trailing spaces.
- lower makes names consistent.
- regex replace turns punctuation and spaces into underscores.
- strip("_") removes extra underscores at the beginning or end.

Normalize text fields:

```python
df["service_name"] = (
    df["service_name"]
      .astype("string")
      .str.strip()
      .str.lower()
)

df["host_name"] = (
    df["host_name"]
      .astype("string")
      .str.strip()
      .str.lower()
)
```

Small example:

```python
import pandas as pd

df = pd.DataFrame({
    " Service Name ": [" Checkout ", "CHECKOUT", " Search "],
    " Host Name ": [" Server01 ", "SERVER01", " Server02 "],
    "CPU %": [72, 91, 45],
})

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(r"[^a-z0-9]+", "_", regex=True)
      .str.strip("_")
)

df["service_name"] = df["service_name"].astype("string").str.strip().str.lower()
df["host_name"] = df["host_name"].astype("string").str.strip().str.lower()

print(df)
```

Common mistakes:

- Cleaning values but forgetting to clean column names.
- Cleaning column names but not key text fields.
- Grouping or joining before normalizing casing and whitespace.
- Accidentally creating duplicate column names after cleaning.

Memorize:
Clean column names first so the rest of the pipeline is easier, then normalize text fields so grouping, joining, and deduplication work reliably.

Strong practical sentence:
In Pandas pipelines, I clean column names and normalize key text fields early because inconsistent casing, spaces, and punctuation can break joins, grouping, deduplication, and data quality checks.

[Back to TOC](#toc)

---

<a id="pattern-03-convert-data-types-safely"></a>
## 3. Convert Data Types Safely

What it is:
This pattern converts text columns into proper datetime and numeric types.

When to use it:
Use it after reading and cleaning data, before filtering, sorting,
aggregating, date bucketing, or calculations.

Mental model:
CSV data often starts as text.
Convert it into usable types before doing real analysis.

Core template:

```python
df["sampled_at"] = pd.to_datetime(df["sampled_at"], errors="coerce")
df["cpu_percent"] = pd.to_numeric(df["cpu_percent"], errors="coerce")
df["memory_percent"] = pd.to_numeric(df["memory_percent"], errors="coerce")
```

Meaning:

- pd.to_datetime converts values into datetime.
- pd.to_numeric converts values into numbers.
- errors="coerce" turns bad values into NaN or NaT instead of crashing.

Important follow-up check:

```python
bad_type_summary = {
    "bad_sampled_at": df["sampled_at"].isna().sum(),
    "bad_cpu_percent": df["cpu_percent"].isna().sum(),
    "bad_memory_percent": df["memory_percent"].isna().sum(),
}

print(bad_type_summary)
```

Small example:

```python
import pandas as pd

df = pd.DataFrame({
    "sampled_at": ["2026-05-01 10:00", "bad-date", "2026-05-01 10:10"],
    "cpu_percent": ["72", "N/A", "91"],
    "memory_percent": ["68", "bad-number", "88"],
})

df["sampled_at"] = pd.to_datetime(df["sampled_at"], errors="coerce")
df["cpu_percent"] = pd.to_numeric(df["cpu_percent"], errors="coerce")
df["memory_percent"] = pd.to_numeric(df["memory_percent"], errors="coerce")

print(df)
print(df.isna().sum())
```

Date buckets after conversion:

```python
df["sample_date"] = df["sampled_at"].dt.date
df["sample_hour"] = df["sampled_at"].dt.floor("h")
```

Filter usable rows:

```python
clean_df = df.dropna(
    subset=["sampled_at", "cpu_percent", "memory_percent"]
)
```

Common mistakes:

- Trusting inferred CSV data types without checking.
- Using errors="coerce" but never checking how many values became null.
- Aggregating before converting numeric fields.
- Sorting date strings instead of real datetime values.
- Dropping bad rows without recording how many were dropped.

Memorize:
Convert dates and numbers safely, then check how many values became null.

Strong practical sentence:
In Pandas pipelines, I convert date and numeric columns explicitly with errors="coerce", then validate null counts so bad input values become visible instead of silently corrupting calculations.

[Back to TOC](#toc)

---

<a id="pattern-04-data-quality-summary"></a>
## 4. Data Quality Summary

What it is:
A compact set of checks that tells you whether the DataFrame is safe to use.

When to use it:
Use it after cleaning and type conversion, before filtering, aggregating, or exporting.

Mental model:
Do not trust the data until you count what is missing, duplicated, or invalid.

Core template:

```python
quality_summary = {
    "total_rows": len(df),
    "missing_sampled_at": df["sampled_at"].isna().sum(),
    "missing_service_name": df["service_name"].isna().sum(),
    "missing_cpu": df["cpu_percent"].isna().sum(),
    "missing_memory": df["memory_percent"].isna().sum(),
    "duplicate_rows": df.duplicated().sum(),
    "negative_cpu": (df["cpu_percent"] < 0).sum(),
    "cpu_over_100": (df["cpu_percent"] > 100).sum(),
}

print(quality_summary)
```

Meaning:

- len(df) counts all rows.
- isna().sum() counts missing values.
- duplicated().sum() counts exact duplicate rows.
- Boolean checks like df["cpu_percent"] > 100 return True/False.
- .sum() counts how many True values exist.

Readable output:

```python
quality_df = pd.DataFrame(
    list(quality_summary.items()),
    columns=["check_name", "check_value"]
)

print(quality_df)
```

Pass/fail status example:

```python
quality_status = "PASS"

if quality_summary["missing_sampled_at"] > 0:
    quality_status = "FAIL"

if quality_summary["missing_service_name"] > 0:
    quality_status = "FAIL"

if quality_summary["missing_cpu"] > 0:
    quality_status = "WARNING"

print("quality_status:", quality_status)
```

Keep bad rows for review:

```python
bad_rows = df[
    df["sampled_at"].isna()
    | df["service_name"].isna()
    | df["cpu_percent"].isna()
    | (df["cpu_percent"] < 0)
    | (df["cpu_percent"] > 100)
]

clean_df = df.drop(bad_rows.index)

print("bad_rows:", len(bad_rows))
print("clean_rows:", len(clean_df))
```

Common mistakes:

- Dropping bad rows without counting them.
- Checking missing values but not duplicates.
- Checking values after aggregation instead of before.
- Forgetting business validity checks like CPU > 100 or negative amounts.
- Treating WARNING and FAIL conditions the same.

Memorize:
Before transforming or exporting, summarize row counts, missing keys, duplicates, and invalid values.

Strong practical sentence:
In Pandas pipelines, I create a small quality summary before publishing output, so missing fields, duplicates, invalid values, and dropped rows are visible instead of hidden inside the transformation logic.

[Back to TOC](#toc)

---

<a id="pattern-05-deduplication-with-survivor-selection"></a>
## 5. Deduplication With Survivor Selection

What it is:
A Pandas pattern for keeping one best row per duplicate business key.

When to use it:
Use it when multiple records exist for the same customer, order, event,
server sample, or business entity.

Mental model:
Do not deduplicate randomly.
Define the business key and survivor rule first.

Common survivor rule:
Keep the latest updated_at.
If tied, keep the highest record_id.

Core template:

```python
df_sorted = df.sort_values(
    ["customer_id", "updated_at", "record_id"],
    ascending=[True, True, True]
)

survivors = df_sorted.drop_duplicates(
    subset=["customer_id"],
    keep="last"
)
```

Meaning:

- sort_values puts records in survivor-rule order.
- subset defines the duplicate business key.
- keep="last" keeps the row that sorted last.

Find duplicate groups first:

```python
duplicate_counts = (
    df
      .groupby("customer_id", as_index=False)
      .size()
      .rename(columns={"size": "row_count"})
      .query("row_count > 1")
)

print(duplicate_counts)
```

Keep rejected duplicates for audit:

```python
df_sorted = df.sort_values(
    ["customer_id", "updated_at", "record_id"],
    ascending=[True, True, True]
)

survivors = df_sorted.drop_duplicates(
    subset=["customer_id"],
    keep="last"
)

rejected_duplicates = df_sorted[
    ~df_sorted.index.isin(survivors.index)
]
```

Telemetry example:

```python
df_sorted = df.sort_values(
    ["server_id", "sampled_at", "ingested_at", "sample_id"],
    ascending=[True, True, True, True]
)

deduped_samples = df_sorted.drop_duplicates(
    subset=["server_id", "sampled_at"],
    keep="last"
)
```

Meaning:
For each server and sampled_at timestamp, keep the latest ingested version.

Common mistakes:

- Using drop_duplicates without sorting first.
- Deduping on the wrong business key.
- Keeping first or last without knowing why.
- Deleting duplicates without saving rejected rows.
- Treating exact duplicate rows and business duplicates as the same thing.

Memorize:
Sort by the survivor rule first, then drop duplicates by the business key.

Strong practical sentence:
In Pandas, I do not deduplicate blindly. I define the business key, sort by the survivor rule, keep the winning row, and preserve rejected duplicates when audit or debugging matters.

[Back to TOC](#toc)

---

<a id="pattern-06-group-and-aggregate-with-groupby"></a>
## 6. Group and Aggregate With groupby

What it is:
A Pandas pattern for summarizing row-level data into grouped metrics.

When to use it:
Use it after cleaning and type conversion when you need summaries by service,
host, date, batch, customer, order, or other business entity.

Mental model:
Pandas groupby is the local DataFrame version of SQL GROUP BY.

Core template:

```python
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
```

Meaning:

- groupby defines the grouping columns.
- as_index=False keeps the result table-like.
- agg creates named output columns.
- Each named output uses: output_name=("source_column", "aggregation").

Small example:

```python
import pandas as pd

df = pd.DataFrame({
    "sample_date": ["2026-05-01", "2026-05-01", "2026-05-01", "2026-05-01"],
    "service_name": ["checkout", "checkout", "search", "search"],
    "cpu_percent": [72, 91, 45, 88],
    "memory_percent": [68, 80, 50, 90],
})

service_summary = (
    df
      .groupby(["sample_date", "service_name"], as_index=False)
      .agg(
          sample_count=("cpu_percent", "count"),
          avg_cpu=("cpu_percent", "mean"),
          max_cpu=("cpu_percent", "max"),
          avg_memory=("memory_percent", "mean"),
      )
)

print(service_summary)
```

Rounding example:

```python
service_summary["avg_cpu"] = service_summary["avg_cpu"].round(2)
service_summary["avg_memory"] = service_summary["avg_memory"].round(2)
```

Add status after aggregation:

```python
service_summary["cpu_status"] = service_summary["avg_cpu"].apply(
    lambda x: "HIGH" if x >= 85 else "WATCH" if x >= 70 else "NORMAL"
)
```

count vs size:

```python
summary = (
    df
      .groupby("service_name", as_index=False)
      .agg(
          non_null_cpu_count=("cpu_percent", "count"),
          total_rows=("cpu_percent", "size"),
      )
)
```

Meaning:

- count counts non-null values.
- size counts all rows in the group.

Common mistakes:

- Grouping before cleaning text values.
- Forgetting as_index=False.
- Aggregating numeric strings before conversion.
- Using count when size is needed.
- Not sorting the final summary.

Memorize:
Clean first, convert types, then group and aggregate with named outputs.

Strong practical sentence:
In Pandas, I use groupby with named aggregation to turn cleaned row-level data into service, batch, customer, or daily summaries that are easy to validate and export.

[Back to TOC](#toc)

---
