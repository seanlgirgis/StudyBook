# ChatGPT Prompt — PySpark Tutorial
# Paste everything between the === markers into ChatGPT

===

You are generating educational Python tutorial files for a Senior Data Engineer
personal study system. Each file must be production-quality, heavily commented,
and fully runnable.

TOPIC: PySpark for Data Engineers
SLUG: pyspark
PRIORITY: Toyota Interview Prep
INFRASTRUCTURE: Pure Python (PySpark local mode — no cluster needed)

===== CODING STANDARDS =====

FILE HEADER — every file starts with:
# ============================================================
# Topic   : PySpark for Data Engineers
# File    : NN_filename.py
# Covers  : one-line description
# Prereqs : pip install pyspark | Java 11+ installed
# Run     : python filename.py
# ============================================================

COMMENTS: Explain WHY, not WHAT. Every design decision gets a comment.
Explain Spark-specific concepts (lazy evaluation, DAG, shuffle) where they appear.

DOCSTRINGS — every function must have:
- One-line summary, WHY this approach, Args, Returns, Raises, Example

CODE: Python 3.11+, type hints, SparkSession created with local[*] mode,
synthetic data generated inside each file, cleanup SparkSession in main block.

===== FILES TO GENERATE =====

01_spark_session_and_rdds.py
  Purpose: SparkSession creation, RDDs vs DataFrames, lazy evaluation, DAG concepts
  Key concepts: SparkSession, lazy evaluation, actions vs transformations, RDD basics
  Functions:
    - create_spark_session(app_name, cores="*") — local mode session with explanation
    - demonstrate_lazy_evaluation(spark) — show nothing runs until action
    - rdd_word_count(spark, text) — classic word count on RDD
    - compare_rdd_vs_dataframe(spark) — same operation both ways, explain tradeoffs
    - show_dag_stages(spark) — use explain() to show physical plan
  Main block: create session, run all demos, show explain plan

02_dataframe_operations.py
  Purpose: Core DataFrame transformations — select, filter, groupBy, join, window functions
  Key concepts: Column expressions, aggregations, join types, window specs, null handling
  Functions:
    - create_sales_df(spark, n_rows=10000) — synthetic sales dataset
    - basic_transformations(df) — select, filter, withColumn, drop, rename
    - aggregations_and_groupby(df) — groupBy, agg, pivot, rollup
    - join_patterns(spark) — inner/left/broadcast join with explanation of when to use each
    - window_functions(df) — rank, lag, lead, running total with WindowSpec
    - null_handling(df) — fillna, dropna, coalesce, when/otherwise
  Main block: demo all operations on synthetic sales data

03_reading_and_writing.py
  Purpose: Read/write CSV, JSON, Parquet, Delta — formats, schemas, options, partitioning
  Key concepts: schema inference vs explicit schema, partitionBy, write modes, predicate pushdown
  Functions:
    - read_csv_with_schema(spark, path) — explicit schema vs inferred, options
    - read_json_nested(spark, path) — nested JSON, schema, explode arrays
    - write_parquet_partitioned(df, path, partition_cols) — partitioned write, explain pruning
    - read_with_predicate_pushdown(spark, path, filter_col, filter_val) — show pushdown in explain
    - compare_format_performance(spark) — read same data as CSV vs Parquet, show timing
  Main block: generate synthetic data, write/read all formats, show performance comparison

04_performance_tuning.py
  Purpose: Spark performance — partitioning, caching, broadcast joins, explain plan, skew
  Key concepts: shuffle partitions, broadcast threshold, caching vs persisting, data skew
  Functions:
    - demonstrate_shuffle_cost(spark) — show join without and with broadcast, compare timing
    - optimize_partitions(df) — repartition vs coalesce, when to use each
    - cache_vs_persist(spark, df) — show speedup from caching on repeated access
    - detect_data_skew(df, key_col) — count per key, flag if top key > 10x median
    - read_explain_plan(df) — parse and explain the physical plan in plain English comments
    - tune_shuffle_partitions(spark, df) — show impact of spark.sql.shuffle.partitions
  Main block: run tuning demos on 1M row synthetic dataset

05_spark_sql_and_catalog.py
  Purpose: Spark SQL interface — temp views, catalog, SQL queries, UDFs
  Key concepts: createOrReplaceTempView, catalog, SQL vs DataFrame API, UDF performance cost
  Functions:
    - register_temp_views(spark, dfs) — create temp views from DataFrames
    - run_analytical_sql(spark) — complex SQL with CTEs, window functions, subqueries
    - create_python_udf(spark) — register Python UDF, explain performance penalty vs built-ins
    - create_pandas_udf(spark) — vectorized UDF with pandas, show speedup vs Python UDF
    - catalog_operations(spark) — list databases, tables, columns via catalog API
  Main block: register views, run SQL analytics, compare UDF performance

===== CAPSTONE PROJECT =====

capstone/brief.md
  Title: Manufacturing Sales Analytics Pipeline
  Scenario: Toyota regional sales data (1M records across 5 regions, 50 models, 3 years)
    needs to be cleaned, aggregated, and written as analytics-ready Parquet for BI queries.
  What to build:
    - Generate synthetic sales dataset (1M rows: date, region, model, units, revenue)
    - Clean: handle nulls, standardize dates, remove duplicates, validate revenue > 0
    - Aggregate: monthly revenue by region and model, YoY growth rate using window functions
    - Rank top 5 models per region per quarter using window rank
    - Write partitioned Parquet by year/region with Snappy compression
    - Print performance report: total time, records processed, partition count, file sizes
  Acceptance criteria:
    - 1M rows generated and processed in under 60 seconds on local mode
    - Output partitioned correctly (year= / region= folder structure)
    - YoY growth calculated correctly for all region/model combos
    - Top 5 ranking correct, verified by SQL query on output

capstone/capstone.py — complete working solution
capstone/test_capstone.py — pytest with SparkSession fixture, test aggregations and ranking

===== INFRASTRUCTURE NOTES =====

Pure Python — PySpark local mode only. No cluster, no AWS, no Docker.
Generate all test data synthetically inside the scripts using Python random/faker.
SparkSession uses master("local[*]") — uses all CPU cores on the machine.
Java 11 must be installed. JAVA_HOME must be set.
All file I/O uses /tmp/studybook/ or a configurable OUTPUT_DIR env var.

===== START =====

Acknowledge these instructions, then wait for me to say "generate file 01".

===
