SAVE AS: spark_concepts.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

ROLE: You are a senior Data Engineer writing a reference guide for an engineer preparing
for Staff DE interviews at a financial institution. Precise, dense, no filler.

TASK: Generate spark_concepts.md — a concept reference covering 7 core Spark abstractions,
each in one tight paragraph, followed by a Citi narrative tie-in.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints, 500,000 metric rows processed in Spark batch jobs

STRUCTURE — produce exactly these sections in order:

# Apache Spark — Core Concepts

## 1. SparkSession
One paragraph. Cover: unified entry point (replaced SparkContext + SQLContext in Spark 2.x),
holds cluster configuration, creates DataFrames, the object you get from SparkSession.builder.
End with: "Every notebook starts with SparkSession.builder.appName('CityTelemetry').master('local[*]').getOrCreate()."

## 2. DAG (Directed Acyclic Graph)
One paragraph. Cover: Spark models computation as a DAG of stages, lazy evaluation means nothing
runs until an action is called, DAG is optimized by Catalyst before execution, stages separated by shuffles.
End with: "Calling regional_avg.show() triggers the DAG — Spark reads from Postgres, shuffles by region, aggregates, returns rows."

## 3. RDD vs DataFrame
One paragraph. Cover: RDD (Resilient Distributed Dataset) is low-level typed Java/Python objects,
DataFrame is structured with schema and SQL optimizer, Dataset adds compile-time type safety (Scala/Java only),
when each is appropriate, why DataFrame wins in 2024.
End with: "All telemetry jobs use DataFrames — Catalyst optimization alone gives 10x+ speedup over equivalent RDD code."

## 4. Partition (Spark)
One paragraph. Cover: fundamental unit of parallelism, each partition processed by one executor core,
default 200 shuffle partitions (spark.sql.shuffle.partitions), too few = underutilized cluster,
too many = task overhead, repartition vs coalesce.
End with: "Reading 500k metric rows: Spark creates ~10 partitions from JDBC fetchsize batches, then shuffles to 200 for aggregation."

## 5. Shuffle
One paragraph. Cover: most expensive operation — moves data across executors by key, triggered by
groupBy/join/orderBy, writes intermediate data to disk (shuffle files), network + disk I/O,
AQE (Adaptive Query Execution) can reduce shuffle partitions automatically.
End with: "The regional avg job shuffles all 500k rows by (region, metric_name) — AQE detects skew and adjusts partition sizes."

## 6. Lazy Evaluation
One paragraph. Cover: transformations (filter, select, groupBy, join) build the plan but do nothing,
actions (show, count, write, collect) trigger execution, benefits: Catalyst can reorder and prune,
predicate pushdown to JDBC happens at plan time not runtime.
End with: "Adding .filter(col('severity') == 'CRITICAL') before .count() pushes the WHERE clause to Postgres — Spark reads only matching rows."

## 7. Executor + Driver
One paragraph. Cover: Driver = JVM process that orchestrates the job (your notebook process),
Executors = JVM processes that run tasks on partitions, local[*] runs both in same JVM,
cluster mode separates them, executor memory/cores configuration, OOM typically in executor.
End with: "In local[*] mode, the notebook IS the driver — a 1g executor memory setting limits each partition's working memory."

---

## Quick Reference Table

| Concept | One-line definition | Citi telemetry example |
|---------|---------------------|------------------------|
| SparkSession | Entry point to all Spark APIs | .appName("CityTelemetry") |
| DAG | Lazy computation graph, triggered by actions | show() on regional_avg |
| DataFrame | Distributed table with schema + optimizer | metrics_df (500k rows) |
| Partition | Unit of parallelism, one core per partition | ~10 from JDBC, 200 after shuffle |
| Shuffle | Cross-executor data movement by key | groupBy("region", "metric_name") |
| Lazy Evaluation | Transforms build plan; actions execute it | .filter().groupBy().show() |
| Executor | JVM process running partition tasks | local[*] = same JVM as driver |

---

## Interview Flashcards

**Q: What triggers execution in Spark?**
A: Actions — show(), count(), collect(), write(). Transformations (filter, select, groupBy, join)
only build the logical plan. Spark executes nothing until an action is called.

**Q: What is a shuffle and why is it expensive?**
A: A shuffle redistributes data across executors by key. It involves serialization, disk writes
(shuffle files), and network transfer. Minimizing shuffles is the #1 Spark performance technique.

**Q: Why use local[*] instead of spark://localhost:7077 from a notebook?**
A: When submitting to a remote Spark master, executors inside Docker cannot route traffic back
to the host driver process. local[*] runs driver and executors in the same JVM — no networking issue.

**Q: What is AQE and when does it help?**
A: Adaptive Query Execution (Spark 3.0+) rewrites the plan at runtime using shuffle statistics.
It collapses small shuffle partitions, handles join skew, and switches join strategies.
Enable with spark.sql.adaptive.enabled=true — it's on by default in Spark 3.2+.

**Q: repartition(N) vs coalesce(N) — when do you use each?**
A: repartition triggers a full shuffle and can increase or decrease partition count — use when
you need balanced partitions before a wide transformation. coalesce only merges partitions without
a shuffle — use to reduce partition count before writing (avoids small file problem).

CONSTRAINTS:
- Each concept section: exactly one paragraph, 4-6 sentences
- Citi tie-in is the last sentence of each paragraph
- No bullet points inside paragraphs
- Table: valid GFM pipe table
- No filler phrases

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
