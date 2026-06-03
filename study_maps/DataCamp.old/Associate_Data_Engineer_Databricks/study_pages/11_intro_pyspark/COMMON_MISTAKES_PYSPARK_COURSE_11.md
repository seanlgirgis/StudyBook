# Common Mistakes - PySpark Course 11

## 1) CSV second argument misuse
Mistake:
Passing a plain Python list as second argument to `spark.read.csv()`.

Why it happened:
Confusion between rename intent and schema argument position.

Correct pattern:
Use read first, then rename:
```python
spark.read.csv(...).toDF(...)
```

Punch line:
A list in that position is treated like schema metadata, not column rename list.

## 2) SparkSession exercise mismatch
Mistake:
Using a different builder pattern than exercise expectation.

Why it happened:
Multiple valid SparkSession styles exist.

Correct pattern:
```python
SparkSession.builder.appName("my_spark").getOrCreate()
```

Punch line:
Match expected exercise signature when assessment is strict.

## 3) Forgetting actions trigger execution
Mistake:
Assuming transformations execute immediately.

Why it happened:
Not internalizing lazy evaluation.

Correct pattern:
Remember `show()`, `count()`, `collect()`, and `write` trigger execution.

Punch line:
Transformations build plan; actions run plan.

## 4) Inner join data loss in enrichment
Mistake:
Defaulting to inner join for lookup enrichment.

Why it happened:
Inner joins are familiar defaults.

Correct pattern:
Use `leftouter` when preserving main records is required.

Punch line:
Enrichment often needs retention first, not strict key match filtering.

## 5) Blind null dropping
Mistake:
Calling `na.drop()` without row-count checks.

Why it happened:
Fast cleanup habit without impact validation.

Correct pattern:
Check counts before/after and verify business acceptability.

Punch line:
Null handling is a data decision, not just syntax.

## 6) Overusing UDFs
Mistake:
Using UDF first when built-ins exist.

Why it happened:
Python comfort bias.

Correct pattern:
Prefer built-in Spark functions first; use UDF when required.

Punch line:
Built-ins usually optimize better and run cleaner at scale.

## 7) UDF used when built-ins were enough
Mistake:
Using a UDF for simple logic that Spark can already do with built-in functions.

Why it happened:
Python-first habit instead of Spark optimization-first thinking.

Correct pattern:
Use built-ins first, then regular UDF or pandas UDF only when custom logic justifies the tradeoff.

Punch line:
Built-in Spark functions first. UDFs only when custom logic is worth the cost.

## 8) Using RDDs when DataFrames are better for structured ETL
Mistake:
Using RDDs for normal structured ETL when DataFrames would be simpler and schema-aware.

Why it happened:
Over-focusing on low-level Spark primitives instead of practical DataFrame workflows.

Correct pattern:
Use DataFrames by default for structured ETL and analytics; move to RDD only when low-level custom behavior is truly needed.

Punch line:
RDDs are foundational; DataFrames are usually the production-practical default.

## 9) Assuming temporary view is a permanent table
Mistake:
Thinking `createOrReplaceTempView()` creates a permanent table.

Why it happened:
SQL mental model drift between view registration and persisted table creation.

Correct pattern:
Treat temp views as SparkSession-scoped; persist outputs explicitly when needed.

Punch line:
Temp view is session-only context, not permanent storage.

## 10) spark.sql() return-type confusion
Mistake:
Thinking spark.sql() returns a SQL-only object.

Why it happened:
Separating SQL mindset from DataFrame API mindset.

Correct pattern:
Treat spark.sql() output as DataFrame and continue with describe/filter/select/withColumn/write as needed.

Punch line:
Spark SQL output is DataFrame output.

## 11) Aggregation on string-typed numeric columns
Mistake:
Running SUM or AVG on a salary/value column read as string.

Why it happened:
Schema not validated before aggregation.

Correct pattern:
Cast numeric columns to proper types, handle nulls, and check row counts before trusting aggregated output.

Punch line:
Type-check and clean before aggregate.

## 12) Repeated actions causing repeated jobs
Mistake:
Calling count(), show(), or collect() repeatedly on the same plan and triggering repeated work.

Why it happened:
Underestimating action-trigger behavior and recomputation cost.

Correct pattern:
Use actions intentionally, cache/persist only reused intermediates, and unpersist when finished.

Punch line:
At scale, repeated actions can silently multiply runtime cost.

## 13) Caching without reuse strategy
Mistake:
Caching many DataFrames by default without validating reuse or memory impact.

Why it happened:
Treating cache as universal speed-up.

Correct pattern:
Cache only reused intermediates and remove with unpersist once done.

Punch line:
Cache is strategic, not automatic.
