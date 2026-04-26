# 🚀 PySpark Learning Journey — StudyBook

## 📌 Overview

This repository documents a **hands-on PySpark learning journey** focused on:

* Core Spark concepts
* Performance tuning
* SQL + Window functions
* Production ETL pipeline design
* Real-world debugging (Windows + Java + PySpark)

This is not just theory — every concept was **executed, debugged, and validated** locally.

---

## ⚙️ Environment Challenges (Critical Learning)

### 🚨 Java Issues

* Multiple Java versions conflicted
* Windows used:

  ```
  C:\Program Files (x86)\Common Files\Oracle\Java\java8path
  ```
* Ignored `JAVA_HOME`

### ✅ Fix

* Forced JDK 17 at top of PATH
* Removed Oracle shim paths

### 💡 Key Insight

> PATH precedence matters more than JAVA_HOME in Spark environments.

---

### 🚨 Python Worker Crashes

Errors:

```
Python worker exited unexpectedly (EOFException)
```

### Root Cause

* Windows multiprocessing + PySpark instability
* Python interpreter mismatch

### ✅ Fix

```python
.config("spark.pyspark.python", sys.executable)
.config("spark.pyspark.driver.python", sys.executable)
```

### 💡 Key Insight

> Spark = JVM + Python workers → mismatch causes crashes.

---

### 🚨 winutils.exe Warning

```
Did not find winutils.exe
```

### Status

* ❌ Not fixed
* ✅ Safely bypassed

### 💡 Key Insight

> Spark on Windows requires Hadoop binaries for filesystem operations.

---

## 🧠 Core Concepts Learned

### 1. Lazy Evaluation

* Transformations are not executed until an action is called

### 2. Catalyst Optimizer

* Spark rewrites queries automatically
* Logical → Optimized → Physical plan

---

### 3. RDD vs DataFrame

| Feature      | RDD    | DataFrame |
| ------------ | ------ | --------- |
| Execution    | Python | JVM       |
| Performance  | Slower | Faster    |
| Optimization | None   | Catalyst  |

> DataFrames are preferred in production.

---

### 4. Joins

* Shuffle join (expensive)
* Broadcast join (fast)

```python
df.join(F.broadcast(dim), "key")
```

> Broadcast avoids shuffle.

---

### 5. Partitioning

* `repartition()` → full shuffle
* `coalesce()` → reduce partitions

> Partition count must be tuned.

---

### 6. Caching

```python
df.cache()
df.persist()
```

> Prevents recomputation.

---

### 7. Data Skew

* Uneven key distribution
* Causes slow jobs

Fixes:

* Salting
* Broadcast joins
* AQE

---

### 8. Window Functions

* `RANK()`
* `LAG()`
* Running totals

> Used for row-level analytics without aggregation.

---

### 9. File Formats

| Format  | Use                |
| ------- | ------------------ |
| CSV     | Simple             |
| JSON    | Nested             |
| Parquet | Best for analytics |

> Parquet is columnar + optimized.

---

## 🏗️ ETL Pipeline Design

### Bronze

* Raw data
* Contains duplicates & nulls

### Silver

* Cleaned
* Deduplicated
* Validated

### Gold

* Aggregated
* Business-ready

---

### Example Results

* Bronze: 100,000 rows
* Silver: 99,000 rows
* Gold: 244 rows

---

### Data Quality Metrics

* Duplicate detection
* Null handling
* Schema enforcement

---

### Incremental Processing

```text
Process only data where event_date > last_watermark
```

> Core production pattern.

---

## 📊 Execution Plan Awareness

Look for:

* `Filter`
* `HashAggregate`
* `Exchange` (shuffle)
* `Sort`

---

## 🧠 Key Takeaways

* Spark is JVM-first
* Python is a wrapper layer
* Performance depends on:

  * partitions
  * joins
  * data distribution
* Windows is NOT ideal for Spark

---

## 🎯 Skill Level Achieved

This project demonstrates:

* Intermediate → Advanced PySpark knowledge
* Real debugging ability
* Production pipeline thinking

---

# 🚀 Next Steps

* Distributed cluster (Databricks / EMR)
* Streaming (Structured Streaming)
* Delta Lake / Iceberg
* Airflow orchestration

---

# 💬 Interview Positioning

You can confidently say:

> “I’ve built an end-to-end Spark ETL pipeline, debugged JVM/Python integration issues, optimized joins and partitions, and analyzed execution plans.”

---

# 🔥 Status

✅ Job-ready foundation
🚀 Ready for real-world Spark work
