# 📦 Parquet for Data Engineers — Complete Study Guide

This project is a **hands-on, production-focused deep dive into Apache Parquet**, designed to make you interview-ready for data engineering roles.

It covers:

* Columnar storage internals
* Compression & encoding
* Partitioning & predicate pushdown
* Schema evolution
* Production patterns (file sizing, compaction, query engines)

---

# 📚 Project Structure

```
12_parquet/
│
├── 01_parquet_basics_and_internals.py
├── 02_compression_and_encoding.py
├── 03_partitioning_and_predicate_pushdown.py
├── 04_schema_evolution_and_compatibility.py
├── 05_parquet_in_production.py
```

---

# 🚀 Setup

```bash
pip install pyarrow pandas duckdb
```

Run files in order:

```bash
python 01_parquet_basics_and_internals.py
python 02_compression_and_encoding.py
python 03_partitioning_and_predicate_pushdown.py
python 04_schema_evolution_and_compatibility.py
python 05_parquet_in_production.py
```

---

# 🧠 What You Learn (File-by-File)

---

## 🔹 01 — Parquet Basics & Internals

**Concepts:**

* Columnar storage
* Row groups
* Metadata (min/max stats)
* CSV vs Parquet comparison

**Key insight:**

> Parquet reads only required columns and skips irrelevant data.

**Interview takeaway:**

* Column pruning
* Predicate pushdown
* Storage efficiency

---

## 🔹 02 — Compression & Encoding

**Concepts:**

* Compression codecs: SNAPPY, GZIP, ZSTD, BROTLI
* Dictionary encoding
* Cardinality impact

**Key insight:**

> Low-cardinality columns compress extremely well using dictionary encoding.

**Interview takeaway:**

* ZSTD → best analytics default
* SNAPPY → best for ingestion
* Dictionary encoding = massive savings

---

## 🔹 03 — Partitioning & Predicate Pushdown

**Concepts:**

* Hive partitioning (`col=value/`)
* Partition pruning
* Row group filtering

**Key insight:**

> Good partitioning skips entire files before reading data.

**Interview takeaway:**

* Partition on frequently filtered columns
* Avoid high cardinality
* Row groups enable intra-file skipping

---

## 🔹 04 — Schema Evolution

**Concepts:**

* Adding columns (safe)
* Type widening (safe)
* Breaking changes (type mismatch)
* Schema merging

**Key insight:**

> Parquet has no schema registry — it’s just files.

**Interview takeaway:**

* Use Delta Lake / Iceberg for real evolution
* Parquet alone cannot safely handle renames/drops

---

## 🔹 05 — Production Patterns

**Concepts:**

* File sizing (128MB–512MB)
* Small file problem
* Compaction
* DuckDB (Athena-style queries)
* Spark config tuning

**Key insight:**

> Query performance depends heavily on file size and layout.

**Interview takeaway:**

* Small files = bad
* Compaction is essential
* DuckDB is great for local analytics

---

# 🧩 Core Concepts Summary

## Columnar Storage

* Data stored by column, not row
* Enables selective reads and compression

## Predicate Pushdown

* Uses metadata (min/max) to skip data
* Works at:

  * Partition level (files)
  * Row group level (inside files)

## Compression Strategy

| Use case              | Best codec |
| --------------------- | ---------- |
| Streaming / ingestion | SNAPPY     |
| Analytics             | ZSTD       |
| Archive               | BROTLI     |

## Partitioning Strategy

Good partition column:

* Appears in WHERE clauses
* Low–medium cardinality (3–100)

Bad partition column:

* High cardinality (user_id, timestamps)

## Schema Evolution Rules

| Change              | Safe? |
| ------------------- | ----- |
| Add nullable column | ✅     |
| Widen type          | ✅     |
| Rename column       | ❌     |
| Drop column         | ❌     |
| Change type         | ❌     |

---

# ⚡ Real-World Patterns

### ✅ Good

* 128–512 MB files
* ZSTD compression
* Partition by frequently filtered columns
* Periodic compaction

### ❌ Bad

* Thousands of tiny files
* Partition by user_id
* Frequent schema changes without governance

---

# 🧪 Tools Used

* **PyArrow** → Parquet read/write + metadata
* **Pandas** → Data generation & manipulation
* **DuckDB** → SQL queries on Parquet (Athena-style)

---

# 🎯 Interview Cheat Sheet

### Why Parquet is faster than CSV?

> 1. Columnar storage (read fewer columns)
> 2. Compression (less I/O)
> 3. Metadata (skip data via predicate pushdown)

---

### What is predicate pushdown?

> Skipping data using metadata (min/max) without reading it.

---

### When to partition?

> When queries filter on a column frequently.

---

### Why are small files bad?

> Too many files → high metadata overhead + slow queries.

---

### When to use ZSTD vs SNAPPY?

* ZSTD → analytics
* SNAPPY → streaming

---

# 🏁 Final Outcome

After completing this project, you can confidently explain:

* How Parquet works internally
* Why it is faster than row-based formats
* How to design partitioning strategies
* How schema evolution works (and fails)
* How production systems optimize Parquet

---

# 💡 Next Steps

* Learn **Delta Lake** or **Apache Iceberg**
* Practice with **Spark + Parquet**
* Explore **query engines (Athena, BigQuery, Snowflake)**

---

**You now understand Parquet at a production + interview level.**
