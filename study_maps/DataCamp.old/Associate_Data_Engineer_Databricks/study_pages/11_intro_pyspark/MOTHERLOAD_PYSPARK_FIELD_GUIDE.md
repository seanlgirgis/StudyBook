# Course 11 PySpark Motherload Field Guide

Purpose:
Explain that this guide captures durable PySpark learning from DataCamp Course
11 plus Wipro/interview production framing.

# 1. The PySpark Mental Model
Spark = distributed engine.
PySpark = Python API.
Driver coordinates.
Executors process partitions.
DataFrames express work.
Actions trigger execution.

# 2. SparkSession
Plain English:
SparkSession is the entry point for DataFrame and Spark SQL operations.

Code pattern:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("my_spark").getOrCreate()
```

Common mistake:
Using an inconsistent builder pattern when the exercise expects `appName("my_spark")`.

Production/interview angle:
SparkSession context controls app identity and runtime behavior.

# 3. DataFrame Basics
PySpark DataFrame is distributed; Pandas DataFrame is local process memory.
Use `show()` to inspect rows, `printSchema()` to confirm column types, and `count()` for row volume.

# 4. Reading Data
```python
spark.read.csv("file.csv", header=True, inferSchema=True)
spark.read.json("file.json")
spark.read.parquet("file.parquet")
```
CSV is text/tabular and often needs options.
JSON handles nested/semi-structured data.
Parquet is columnar and generally efficient for analytics.

# 5. Schemas
`inferSchema=True` is quick for exploration; manual schema is safer for stable pipelines.

```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

schema = StructType([
    StructField("age", IntegerType(), True),
    StructField("education_num", IntegerType(), True),
    StructField("marital_status", StringType(), True),
    StructField("occupation", StringType(), True),
    StructField("income", StringType(), True)
])

df = spark.read.csv(
    "adult_reduced_100.csv",
    sep=",",
    header=False,
    schema=schema
)

df.printSchema()
```

# 6. Core DataFrame Operations
Use `select`, `filter`, `where`, `groupBy`, `agg`, `sort`, and `orderBy` for core ETL shaping.

# 7. Missing Data
```python
df.na.drop()
df.where(col("columnName").isNotNull())
df.na.fill({"age": 0})
```
Production warning:
Dropping/filling nulls changes the data, so validate row counts and business meaning.

# 8. Column Operations
```python
df = df.withColumn("weekly_salary", df.income / 52)
df = df.withColumnRenamed("age", "years")
df = df.drop("department")
```

# 9. Row Operations and Aggregations
Use row filters and grouped metrics together:
`filter` + `groupBy` + `agg(avg/sum/count)`.

# 10. Joins
Join types: `inner`, `left`, `right`, `outer`.

Enrichment join pattern:
```python
airports = airports.withColumnRenamed("faa", "dest")

flights_with_airports = flights.join(
    airports,
    on="dest",
    how="leftouter"
)
```
Why `leftouter` preserved flights:
All records from the main flights DataFrame stay, even if lookup fields are missing.

# 11. Union
Union stacks DataFrames vertically.
Ensure compatible schema, column order, and types before union.

# 12. Complex Types
Arrays: ordered lists in one column.
Maps: key-value structures.
Structs: nested field groups.
Use for practical semi-structured modeling.

# 13. UDFs and pandas UDFs
UDF = custom function when built-ins are not enough.
pandas UDF can improve vectorized performance for some patterns.
Built-ins are preferred first.

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

age_category_udf = udf(age_category, StringType())

age_category_df_2 = age_category_df.withColumn(
    "category",
    age_category_udf(age_category_df["age"])
)
```


## UDF Decision Ladder: Built-ins First, UDFs Carefully
UDFs allow custom logic in PySpark, but they can add performance and support cost. In production PySpark, the default choice should be built-in Spark DataFrame or SQL functions whenever possible. Spark can optimize built-ins better than opaque custom Python logic.

Decision ladder:
1. Use built-in Spark DataFrame or SQL functions first.
2. Use DataFrame expressions for simple arithmetic, string, date, null, and conditional logic.
3. Use a regular PySpark UDF only when the logic is custom and not easy to express with built-ins.
4. Use a pandas UDF when custom logic is needed and vectorized/batch-style execution is a better fit than a regular Python UDF.
5. Treat external/JVM/platform-specific UDFs as environment-specific choices, not the default beginner pattern.

Built-in expression example:
```python
df = df.withColumn("10_plus", df["value"] + 10)
```

pandas UDF syntax example:
```python
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType

@pandas_udf(DoubleType())
def add_ten_pandas(column):
    return column + 10

df = df.withColumn(
    "10_plus",
    add_ten_pandas(df["value"])
)

df.show()
```

Plain English:
The pandas UDF example teaches syntax and vectorized custom logic. But for a simple operation like adding 10, the built-in Spark expression is better.

Production angle:
If a job uses UDFs or pandas UDFs, validate null handling, return type, performance impact, row counts, and whether a built-in Spark function could replace the UDF.

Common mistake:
Using a UDF for simple logic that Spark can already do with built-in functions.

Interview-safe answer:
I know UDFs are available for custom logic, but I would not use them casually. I would first check whether Spark built-in functions or SQL expressions can do the work. If custom logic is required, I would choose between a regular PySpark UDF and a pandas UDF based on data size, performance, maintainability, and runtime support.

Punch line:
Built-in Spark functions first. UDFs only when custom logic is worth the performance and support cost.


Transformations build the plan.
Actions trigger execution.
`show()`, `count()`, `collect()`, and `write` are actions.

# 15. Production Support Checklist
- input counts
- output counts
- schema checks
- null checks
- duplicate checks
- join row-count checks
- logs
- failed stages
- executor errors
- parameters
- upstream/downstream dependencies
- safe rerun behavior
- overwrite vs append risk

# 16. Common Mistakes From This Course
- Passing a plain Python list as second argument to `spark.read.csv()` is wrong because Spark treats it as schema.
Correct rename pattern: `spark.read.csv(...).toDF(...)`.
- SparkSession exercise expected: `SparkSession.builder.appName("my_spark").getOrCreate()`.
- `show()`, `count()`, `collect()`, and `write` are actions.
- `leftouter` often safer than inner for enrichment joins.
- `na.drop()` can remove many rows; validate before/after counts.
- Prefer built-in Spark functions before UDFs.

# 17. Interview-Safe PySpark Language
What is PySpark?
PySpark is the Python API for Spark distributed processing.

How do you support a PySpark job?
I check logs, stage failures, data quality, dependencies, parameters, and rerun safety.

How do you think about joins?
I choose join types based on business retention needs and validate row-count effects.

How do you think about UDFs?
I use built-ins first; I use UDFs when necessary and watch performance impact.

# 18. Mini Cookbook
- Start app: `SparkSession.builder.appName("my_spark").getOrCreate()`
- Read CSV with schema inference: `spark.read.csv(..., header=True, inferSchema=True)`
- Inspect: `printSchema()`, `show()`, `count()`
- Clean nulls: `na.drop()`, `na.fill(...)`
- Enrich: `join(..., how="leftouter")`
- Aggregate: `groupBy(...).agg(...)`
- Add/rename/drop columns: `withColumn`, `withColumnRenamed`, `drop`
- Custom transform fallback: UDF / pandas UDF


## RDDs vs DataFrames
RDD stands for Resilient Distributed Dataset. It is Spark's lower-level distributed data abstraction. An RDD represents a collection of data split across the cluster. RDDs are immutable, so transformations create new RDDs instead of changing the original one in place.

Plain English:
RDDs are closer to the raw Spark engine. DataFrames are higher-level, table-like, schema-aware objects that are usually easier and better for structured ETL and analytics.

Key terms:
- parallelization: splitting data and computation across workers
- RDD: lower-level distributed collection
- immutable: cannot be changed in place
- map(): apply a function to each element
- filter(): keep matching elements
- collect(): bring distributed results back to the driver

Code patterns:
```python
# Convert a DataFrame to an RDD
rdd = df.rdd

# Apply map to an RDD
mapped_rdd = rdd.map(lambda row: row)

# Filter an RDD
filtered_rdd = rdd.filter(lambda row: row["age"] > 40)

# Collect tiny results only
small_result = filtered_rdd.collect()
```

RDD vs DataFrame:
RDD:
- lower-level
- more flexible
- more manual code
- less schema-aware
- useful for Spark fundamentals and special custom processing

DataFrame:
- higher-level
- rows and columns
- schema-aware
- SQL-like
- usually preferred for structured ETL, analytics, and production PySpark jobs

Production warning:
Be careful with collect(). collect() brings distributed data back to the driver. It is fine for tiny examples but risky for large datasets because it can overload driver memory.

Common mistake:
Using RDDs for normal structured ETL when DataFrames would be simpler, schema-aware, and easier for Spark to optimize.

Interview-safe answer:
RDDs are Spark's lower-level distributed data abstraction. They are useful for understanding Spark fundamentals and for some custom low-level processing, but for most structured PySpark ETL work I would prefer DataFrames because they are schema-aware, SQL-friendly, and easier for Spark to optimize.

Punch line:
RDDs teach how Spark thinks. DataFrames are usually how I would build practical structured PySpark ETL.

## Spark SQL and Temporary Views
Spark SQL lets PySpark users query structured and semi-structured data using SQL syntax inside a Spark application. It connects SQL-style logic with DataFrame-based PySpark workflows.

Plain English:
A DataFrame can be registered as a temporary SQL view. Then spark.sql() can run SQL against that view. The result of spark.sql() is another DataFrame, so the workflow can continue with DataFrame operations.

Core pattern:
```python
# Load data into a DataFrame
employees_df = spark.read.csv(
    "employees.csv",
    header=True,
    inferSchema=True
)

# Register as a temporary SQL view
employees_df.createOrReplaceTempView("employees")

# Query with Spark SQL
high_earners = spark.sql("""
    SELECT name, salary
    FROM employees
    WHERE salary > 100000
""")

# SQL result is still a DataFrame
high_earners.show()
```

Key points:
- createOrReplaceTempView("view_name") registers a DataFrame as a session-scoped SQL view.
- spark.sql("SQL query") runs SQL and returns a DataFrame.
- Temporary views exist only for the current SparkSession.
- SQL and DataFrame operations can be blended in the same pipeline.

Common mistake:
Thinking createOrReplaceTempView() creates a permanent table. It does not. It creates a temporary view scoped to the active SparkSession.

Production angle:
Temp views are useful for session-based transformations, but production output should be clearly persisted when needed. Validate row counts before and after SQL filters, joins, and aggregations. Use clear view names so SQL and DataFrame steps are easy to support.

Interview-safe answer:
Spark SQL lets me use SQL inside a PySpark workflow. I can load data into a DataFrame, register it as a temporary view, run SQL with spark.sql(), and then continue processing the SQL result as another DataFrame. This is useful because it connects SQL skills with scalable Spark execution.

Punch line:
Spark SQL lets SQL and PySpark DataFrames work together in one distributed pipeline.

## Spark SQL result can continue as a DataFrame
Concept:
spark.sql() returns a DataFrame. After querying a temporary view with SQL, the result can still use DataFrame methods such as show(), describe(), filter(), select(), withColumn(), or write.

Code pattern:
```python
salaries_df.createOrReplaceTempView("salaries_table")

query = """
    SELECT job_title, salary_in_usd
    FROM salaries_table
    WHERE company_location = 'CA'
"""

canada_titles = spark.sql(query)

canada_titles.describe().show()
```

Plain English:
The SQL query filters and selects data from the temporary view. The result is stored as canada_titles, which is a DataFrame. Because it is a DataFrame, we can call describe() to get summary statistics.

Common mistake:
Thinking spark.sql() returns a separate SQL-only object. It returns a DataFrame.

SQL style note:
Prefer standard SQL equality with = inside SQL strings, even if Spark may accept == in some contexts.

Production angle:
Before trusting describe(), confirm numeric columns were read with the right types, check filtered row counts, and validate that filter values such as company_location = 'CA' are standardized.

Punch line:
spark.sql() returns a DataFrame, so SQL and DataFrame methods can be chained in the same PySpark workflow.

## PySpark Aggregations Best Practices
Concept:
PySpark supports aggregations through both Spark SQL and the DataFrame API. Common aggregations include SUM, COUNT, AVG, MAX, and MIN. Aggregations summarize data by groups, such as total salary by department or average salary by job title.

Plain English:
Aggregations are how we summarize many rows into useful business metrics. But the result is only trustworthy if the input data is filtered, typed, cleaned, and validated first.

Spark SQL pattern:
```python
df.createOrReplaceTempView("employees")

result = spark.sql("""
    SELECT department,
           SUM(salary) AS total_salary,
           AVG(salary) AS avg_salary,
           COUNT(*) AS employee_count
    FROM employees
    GROUP BY department
    ORDER BY total_salary DESC
""")

result.show()
```

DataFrame API pattern:
```python
from pyspark.sql.functions import sum, avg, count, max, min

result = (
    df
    .groupBy("department")
    .agg(
        sum("salary").alias("total_salary"),
        avg("salary").alias("avg_salary"),
        count("*").alias("employee_count"),
        max("salary").alias("max_salary"),
        min("salary").alias("min_salary")
    )
)

result.show()
```

Cast-before-aggregation pattern:
```python
from pyspark.sql.functions import col

df_clean = df.withColumn(
    "salary",
    col("salary").cast("double")
)
```

Best practices:
- Filter early to reduce data volume before aggregation.
- Confirm numeric columns are actually numeric.
- Cast string numbers before SUM or AVG.
- Handle nulls before aggregation.
- Check row counts before and after filters.
- Validate grouping values such as department, job title, region, or date.
- Prefer DataFrames or Spark SQL for structured aggregations.
- Avoid RDDs for normal analytics unless low-level custom control is required.
- Use explain() when performance needs investigation.

RDD note:
RDDs can do aggregations with map() and reduceByKey(), but for normal structured analytics they are more verbose and less convenient than DataFrames or Spark SQL.

Production angle:
Aggregation failures or bad results often come from wrong data types, nulls, unexpected grouping values, duplicate rows, or filters that remove too much data. Production support should verify schema, counts, nulls, duplicate behavior, and output totals before trusting aggregated results.

Common mistake:
Running SUM or AVG on a column that was read as a string, or trusting an aggregation without checking row counts and data types.

Interview-safe answer:
For PySpark aggregations, I can use either Spark SQL or the DataFrame API. Before aggregating, I would make sure the data is filtered, cleaned, and correctly typed. For example, if salary was read as a string, I would cast it to a numeric type before using SUM or AVG. In production, I would also check row counts, nulls, grouping values, and use explain() if performance is a concern.

Punch line:
Aggregate only after the data is filtered, typed, cleaned, and validated.

## PySpark at Scale: explain(), cache(), persist(), broadcast(), and repeated actions
Concept:
At scale, PySpark performance is not just about correct syntax. It depends on how Spark plans and executes the job across the cluster. Important tools include explain(), cache(), persist(), unpersist(), broadcast joins, and avoiding unnecessary repeated actions.

Plain English:
Spark builds an execution plan before running work. explain() lets us inspect that plan. cache() and persist() help avoid recomputing reused intermediate DataFrames. broadcast() can reduce shuffle cost when joining a large DataFrame to a small lookup DataFrame. Actions like count(), show(), collect(), and write trigger Spark jobs, so repeated actions can cause repeated work.

Execution plan pattern:
```python
df.explain()
```

Cache pattern:
```python
filtered_df = df.filter(df["company_location"] == "US")
filtered_df.cache()

filtered_df.count()
filtered_df.groupBy("job_title").avg("salary_in_usd").show()

filtered_df.unpersist()
```

Persist pattern:
```python
from pyspark import StorageLevel

df.persist(StorageLevel.MEMORY_AND_DISK)

df.unpersist()
```

Broadcast join pattern:
```python
from pyspark.sql.functions import broadcast

joined_df = large_df.join(
    broadcast(small_lookup_df),
    on="key",
    how="left"
)
```

Best practices:
- Use explain() to inspect logical and physical plans.
- Watch for expensive shuffles.
- Filter early to reduce data volume.
- Cache or persist only when an intermediate DataFrame is reused.
- Unpersist cached/persisted DataFrames when finished.
- Avoid repeated actions such as repeated count() or show() calls.
- Consider broadcast joins when joining a large DataFrame to a small lookup.
- Use DataFrames and Spark SQL for optimized structured processing.

Common mistakes:
- Calling count(), show(), or collect() repeatedly and triggering repeated jobs.
- Caching everything without checking reuse or memory pressure.
- Forgetting to unpersist cached data.
- Ignoring shuffles in joins and aggregations.
- Using collect() on large data and overloading the driver.
- Assuming correct code is automatically efficient at scale.

Production angle:
For production PySpark jobs, I would check the execution plan, look for shuffles, validate row counts, avoid repeated actions, use caching only when justified, and unpersist when done. For joins, I would consider broadcast joins when one side is small enough. Performance tuning should be tied to logs, stages, executor behavior, memory pressure, and the physical plan.

Interview-safe answer:
For PySpark at scale, I would inspect the execution plan with explain(), watch for expensive shuffles, filter early, avoid repeated actions, and use cache or persist only when an intermediate DataFrame is reused. For joins, if one side is small enough, I would consider a broadcast join to reduce shuffle. I would also unpersist cached data when it is no longer needed.

Punch line:
At scale, do not just ask whether PySpark code works. Ask how Spark will execute it, whether it shuffles, whether it recomputes, and whether resources are being used safely.


## Course 11 Final Summary - Introduction to PySpark
This course introduced foundational PySpark skills for large-scale data processing. It covered Spark architecture, distributed processing, RDDs, transformations, actions, DataFrames, Spark SQL, filtering, aggregations, joins, UDFs, caching, execution plans, broadcast joins, and basic production support thinking.

### What Sean can safely say
I completed a foundational PySpark course covering Spark architecture, DataFrames, Spark SQL, RDD basics, transformations and actions, joins, aggregations, UDFs, caching, execution plans, and broadcast concepts. I would describe this as foundational PySpark readiness, not deep Spark platform administration. My strongest connection is using PySpark for structured ETL-style work, SQL/DataFrame transformations, basic production support thinking, and scalable data-processing patterns.

### What was covered
- Apache Spark and PySpark overview
- SparkSession
- driver and executors
- DataFrames
- reading CSV, JSON, and Parquet
- schema inference and manual schemas
- StructType and StructField
- select, filter, where, sort, orderBy
- null handling with na.drop and na.fill
- withColumn, withColumnRenamed, drop
- joins and leftouter enrichment joins
- union
- arrays, maps, structs
- regular PySpark UDFs and pandas UDFs
- RDD basics
- transformations, actions, lazy evaluation
- Spark SQL and temporary views
- aggregations with Spark SQL and DataFrame API
- explain()
- cache(), persist(), unpersist()
- broadcast joins
- repeated action risk
- production row-count, schema, log, and rerun thinking

### What was not deeply covered yet
- advanced cluster configuration
- deep Spark performance tuning
- streaming data processing
- advanced machine learning pipelines
- cloud-managed Spark platforms
- advanced Databricks production workflows
- Spark administration
- full production CI/CD deployment of PySpark jobs

### Course punch line
Course 11 gives Sean a practical PySpark foundation: enough to read, inspect, transform, join, aggregate, query, and reason about PySpark jobs, while staying honest about deeper Spark platform topics that require future practice.

### Recommended next StudyBook work
1. Finish any remaining DataCamp exercises and capture mistakes.
2. Run a final Course 11 architecture/content audit.
3. Create a Course 11 final review page.
4. Later, when environment is ready, create small runnable PySpark drills under tutorials only.
5. Use Motherload + QA + code snippets as the future interview/practice base.

# Spark Runtime Architecture Quest

Purpose:
This section points to the deeper architecture quest that explains how PySpark
jobs run in production platforms.

Link:
SPARK_RUNTIME_ARCHITECTURE_QUEST.html

Key idea:
PySpark code defines the data work; the submission layer starts the job; Spark
runs it with a driver and executors; the cluster/resource manager allocates
resources; storage holds the data; catalog describes the tables; orchestration
coordinates the pipeline.

# Spark Review Lanes

This Course 11 package now has two related QA/study files:
- QA_01_1000ft_pyspark_opening.md for the Course 11 foundation.
- Spark.Study.md for expanded production Spark, Delta, architecture, and streaming.

Use SPARK_REVIEW_LANES.md to choose the correct study lane.
