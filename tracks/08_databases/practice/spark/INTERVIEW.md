# Interview Questions — Spark Basics

> Topics covered: DataFrames vs RDDs · lazy evaluation · partitioning and shuffling · joins at scale · broadcast joins
> Levels: Starter | Mid | Senior | Architect

---

## Topic 1: DataFrames vs RDDs

**Q1 (Starter): In c001_dataframes_vs_rdds_demo.py, `_rdd_filter` and `_dataframe_filter` do the same filtering. What is the key difference in how you write each style?**
What a good answer covers:
- RDD-style uses explicit Python loops and manual logic for every step
- DataFrame-style is declarative — you describe what you want, not how to do it
- Spark's Catalyst optimizer can only plan and optimize declarative DataFrame operations, not arbitrary Python code
Why this is asked: Tests whether the candidate understands the semantic difference before worrying about performance.

**Q2 (Starter): Looking at c001_dataframes_vs_rdds_demo.py, `_rdd_aggregate` loops through rows to sum amounts per customer. How would you express the same logic as a DataFrame operation?**
What a good answer covers:
- `groupBy("customer").agg(sum("amount"))` replaces the manual accumulator loop
- The engine decides the execution plan, including whether to use hash aggregation or sort-based aggregation
- Column expressions (`F.sum`, `F.col`) operate on the schema, not on Python objects
Why this is asked: Checks that the candidate can translate imperative RDD logic into declarative DataFrame expressions.

**Q3 (Starter): c001_dataframes_vs_rdds_demo.py shows RDD operations as ordinary Python functions. Why does this make optimization harder for Spark?**
What a good answer covers:
- Spark cannot inspect the inside of a Python lambda or function — it is a black box
- Without inspecting logic, it cannot reorder, prune columns, or push filters to the source
- DataFrames expose a logical plan that Catalyst can rewrite and optimize
Why this is asked: Establishes that optimization is the practical reason to prefer DataFrames, not just code style.

**Q4 (Starter): What is a schema in the context of DataFrames, and why does having one matter?**
What a good answer covers:
- A schema defines column names and data types, enforced at the DataFrame boundary
- Catalyst uses the schema to validate column references and infer output types at plan time, not at runtime
- Schema-aware operations allow columnar storage formats like Parquet to read only the needed columns
Why this is asked: Ensures the candidate connects DataFrames to typed, structured data rather than untyped rows.

---

**Q5 (Mid): c001_dataframes_vs_rdds_demo.py builds an RDD-style pipeline by chaining `_rdd_filter` → `_rdd_select` → `_rdd_aggregate`. What makes this pipeline more expensive than an equivalent DataFrame pipeline, even if both produce the same result?**
What a good answer covers:
- Each RDD function materializes an intermediate Python list — there is no fusion across steps
- DataFrame operations are composed into a single logical plan; Catalyst can fuse filter and projection into one pass over the data
- RDD Python UDF overhead: every row crosses the JVM-Python boundary; DataFrames apply native JVM or Photon-compiled code
Why this is asked: Probes understanding of whole-stage code generation and stage fusion.

**Q6 (Mid): When would you choose an RDD over a DataFrame in a real Spark job?**
What a good answer covers:
- When the transformation requires per-partition state or custom iterators that cannot be expressed as column operations
- When working with unstructured or semi-structured data that has no natural schema
- When you need fine-grained control over serialization (e.g., custom Kryo serializers)
- DataFrames should be the default; RDDs are the escape hatch
Why this is asked: Distinguishes candidates who know the trade-off from those who simply avoid RDDs without knowing why.

**Q7 (Mid): In c001_dataframes_vs_rdds_demo.py, `_rdd_filter` filters on both `amount` and `status`. If this were a DataFrame filter, how would Catalyst's predicate pushdown change the execution?**
What a good answer covers:
- Catalyst pushes the filter to the scan layer, so only matching rows are read from storage
- With Parquet or ORC, this also enables row-group skipping using column statistics
- The RDD version reads all rows into Python memory before filtering
Why this is asked: Tests predicate pushdown as a concrete optimization rather than an abstract concept.

**Q8 (Mid): What is the Catalyst optimizer, and at what stage does it transform a DataFrame query plan?**
What a good answer covers:
- Catalyst parses the query into an unresolved logical plan, resolves column references against the schema, then optimizes the logical plan, and finally generates physical execution strategies
- Key rules: predicate pushdown, constant folding, projection pruning, join reordering
- The optimized physical plan is compiled to JVM bytecode via whole-stage code generation
Why this is asked: Ensures the candidate can explain the full lifecycle of a DataFrame query.

---

**Q9 (Senior): A team migrates a large RDD pipeline from c001_dataframes_vs_rdds_demo.py style to DataFrames but sees no performance improvement. What would you investigate first?**
What a good answer covers:
- Check whether Python UDFs were carried over — they re-introduce the serialization bottleneck even inside a DataFrame plan
- Use `explain(True)` to compare logical vs physical plans and verify that filter pushdown and projection pruning are firing
- Look for schema inference on JSON/CSV, which can trigger full scans; replacing it with an explicit schema removes one planning bottleneck
- Check whether the bottleneck is actually IO or shuffle rather than CPU, which DataFrames alone will not fix
Why this is asked: Tests diagnostic depth — a candidate who only knows theory will suggest switching APIs; a senior knows to profile first.

**Q10 (Senior): How does Tungsten's off-heap binary format relate to the performance difference seen between DataFrame and RDD execution in c001_dataframes_vs_rdds_demo.py?**
What a good answer covers:
- Tungsten stores row data in compact binary off-heap memory, avoiding Java object overhead and GC pressure
- DataFrames operate on this binary format directly using generated code; RDDs deserialized to Java/Python objects on every operation
- The result is better cache utilization and fewer GC pauses at scale
Why this is asked: Probes low-level memory model knowledge that separates senior engineers from mid-level ones.

**Q11 (Senior): When a DataFrame schema is inferred at runtime (e.g., from JSON), what risks arise in a production pipeline, and how do you mitigate them?**
What a good answer covers:
- Schema inference requires a full or partial scan of the data, adding latency proportional to data size
- Inferred types can change between runs if source data changes, causing silent type coercions or failures in downstream models
- Mitigation: always define an explicit `StructType` schema; use schema registries in streaming contexts; version schemas alongside pipeline code
Why this is asked: Production relevance — schema drift is a common source of silent failures in data pipelines.

---

**Q12 (Architect): Your team builds an ELT pipeline that reads raw JSON from object storage into DataFrames, applies transformations similar to c001_dataframes_vs_rdds_demo.py, and writes to a Delta Lake table. Describe the schema enforcement and evolution strategy you would implement.**
What a good answer covers:
- Define an explicit `StructType` at the ingestion boundary and validate incoming data against it before writing
- Use Delta Lake's schema enforcement (`mergeSchema=false` by default) to reject writes that add or change columns unexpectedly
- For intentional schema changes, use `ALTER TABLE` or `mergeSchema=true` with a migration runbook and downstream model review
- Decouple raw landing zone (schema-on-read) from the curated layer (schema-on-write) so inference failures are contained
- Connect to dbt staging models (c001_models_demo.py) as the normalization boundary after Delta ingestion
Why this is asked: Tests whether the architect thinks about schema as a contract across the whole pipeline, not just a Spark detail.

**Q13 (Architect): An organization is debating whether to standardize on DataFrames (Spark SQL) or push transformation logic into dbt models on a warehouse. What factors drive that architectural decision?**
What a good answer covers:
- Spark DataFrames are appropriate when data volumes exceed warehouse scale, when ML feature pipelines need Python libraries, or when streaming is required
- dbt wins for SQL-native teams, warehouse-native compute (Snowflake, BigQuery), and layered model governance (staging/intermediate/marts as in c001_models_demo.py)
- Hybrid patterns are common: Spark handles heavy ingestion and feature engineering; dbt handles business-logic transformations on the warehouse layer
- Key governance factors: lineage tooling, cost model, team SQL vs Python fluency, and existing compute contracts
Why this is asked: Assesses system-level thinking and ability to frame technology choices in terms of organizational context.

---

## Topic 2: Lazy Evaluation

**Q1 (Starter): What does "lazy evaluation" mean in Spark?**
What a good answer covers:
- Transformations (e.g., `filter`, `select`, `groupBy`) do not execute immediately — they build a logical plan
- Execution is triggered only when an action is called (e.g., `show`, `count`, `write`)
- This defers work until Spark knows the full plan and can optimize it end-to-end
Why this is asked: Lazy evaluation is the most fundamental Spark concept; any Spark engineer must be able to state it clearly.

**Q2 (Starter): In c002_lazy_evaluation_demo.py, multiple transformations are chained before any result is printed. Why does nothing run until the action is called?**
What a good answer covers:
- Each transformation appends a node to the DAG (directed acyclic graph) of operations
- The driver builds the DAG in memory without touching any data
- The first action triggers the DAG Scheduler to break the plan into stages and submit tasks to executors
Why this is asked: Confirms the candidate understands the separation between the planning phase and the execution phase.

**Q3 (Starter): What is the difference between a transformation and an action in Spark?**
What a good answer covers:
- Transformations return a new DataFrame or RDD and are lazy (e.g., `filter`, `map`, `join`)
- Actions trigger execution and return a result to the driver or write to storage (e.g., `count`, `collect`, `save`)
- Every action causes Spark to re-evaluate the full plan from the source unless intermediate results are cached
Why this is asked: This distinction is the entry point to every discussion about Spark job planning and debugging.

**Q4 (Starter): Why is calling `collect()` on a large DataFrame dangerous?**
What a good answer covers:
- `collect()` pulls all partition data back to the driver JVM as a single list
- On a large dataset this causes an out-of-memory error on the driver
- Safe alternatives: `show(n)`, `limit(n).collect()`, writing to storage with `write`, or sampling with `sample()`
Why this is asked: Tests practical awareness — candidates who write `collect()` on large data in production cause incidents.

---

**Q5 (Mid): A colleague says the Spark job in c002_lazy_evaluation_demo.py is slow because "it runs the filter twice." Looking at the DAG, how would you determine whether that is true?**
What a good answer covers:
- Open the Spark UI and inspect the DAG visualization — identical upstream nodes that are not cached will appear as separate branches if triggered by two separate actions
- If the dataset is not persisted/cached between actions, Spark re-reads and re-executes from the source for each action
- Fix: call `.cache()` or `.persist()` after the shared transformation so the result is stored and reused
Why this is asked: Tests whether the candidate knows how to use the Spark UI and understands cache/persist semantics.

**Q6 (Mid): What is the DAG Scheduler's role in translating a lazy plan into executable stages?**
What a good answer covers:
- The DAG Scheduler receives the final optimized physical plan and identifies shuffle boundaries (wide dependencies)
- It splits the plan at each shuffle into stages; within a stage all tasks are narrow (no data movement between partitions)
- Stages are submitted to the Task Scheduler, which assigns tasks to executors based on data locality
Why this is asked: Probes understanding of the internal architecture beyond the user-facing API.

**Q7 (Mid): When should you call `.cache()` or `.persist()` in a lazy evaluation chain, and what are the trade-offs?**
What a good answer covers:
- Cache when a DataFrame is used by more than one downstream action or branch in the same job
- `.cache()` uses the default `MEMORY_AND_DISK` storage level; `.persist()` allows choosing level (e.g., memory-only, off-heap, serialized)
- Trade-offs: caching consumes executor memory and may evict other cached partitions; unnecessary caching slows GC
- Always call `.unpersist()` when the cached data is no longer needed in long-running sessions
Why this is asked: Cache misuse is among the most common causes of performance regressions in Spark pipelines.

**Q8 (Mid): How does lazy evaluation interact with Spark's fault tolerance model?**
What a good answer covers:
- Because Spark records the full lineage of transformations in the DAG, any lost partition can be recomputed from the original source without checkpointing
- Fault tolerance is a property of lazy evaluation — without the DAG there would be no lineage to replay
- With long lineage chains (deep iterative jobs), explicit checkpointing truncates the lineage and avoids stack overflows during recomputation
Why this is asked: Connects lazy evaluation to the broader resilience design of Spark.

---

**Q9 (Senior): A Spark job reads a table, applies ten chained transformations from c002_lazy_evaluation_demo.py style, then fans out into three separate `.write` calls. Explain the execution and how you would optimize it.**
What a good answer covers:
- Without caching, Spark re-reads the source and re-executes all ten transformations for each of the three write actions — three full passes over the data
- Inserting `.cache()` after the shared transformations and before the fan-out reduces this to one read and one set of transformations, then three fast write passes over the cached partitions
- Verify the cache is hitting by checking storage tab in the Spark UI; confirm partitions are not being evicted
- If the cached data is too large for memory, switch to `DISK_ONLY` persistence or consider writing to a temp Delta table and branching from there
Why this is asked: Real multi-output job optimization is a senior-level concern.

**Q10 (Senior): Explain why lazy evaluation is particularly valuable in a structured streaming context.**
What a good answer covers:
- In structured streaming, the query runs continuously; Spark incrementally plans each micro-batch by inspecting new data against the same lazy plan
- The optimizer can apply the same Catalyst rules (filter pushdown, projection pruning) per micro-batch without the user rewriting the query
- Watermarking and stateful aggregations are expressed as lazy plan nodes that the streaming engine evaluates incrementally
- Without laziness, each micro-batch would require explicit re-planning by the user
Why this is asked: Tests whether the candidate can generalize batch-oriented concepts to streaming.

**Q11 (Senior): A long-running Spark application experiences increasing GC pause times over several hours. Lazy evaluation and caching are suspected. How do you diagnose and address this?**
What a good answer covers:
- Check the Spark UI executor memory tab for rising on-heap usage; look at GC time per executor in the metrics
- Identify DataFrames that are cached but never unpersisted — they accumulate deserialized Java objects on the heap
- Switch cached DataFrames to `MEMORY_AND_DISK_SER` (Kryo serialized) to reduce object graph size, or to off-heap storage
- Add explicit `.unpersist()` calls after each branch completes; in structured streaming use `unpersist` on micro-batch completion callbacks
Why this is asked: Memory leak diagnosis in long-running Spark jobs is a senior operational skill.

---

**Q12 (Architect): Design a lazy evaluation strategy for a pipeline that ingests 50 TB per day, applies shared cleansing transformations, then branches into five domain-specific mart tables. How do you balance recomputation cost against memory pressure?**
What a good answer covers:
- Write the cleansing transformations once as a shared plan; materialize the result to a Delta Lake intermediate table after validation rather than relying on in-memory cache across 50 TB
- Each domain branch reads from the intermediate Delta table — this converts recomputation cost into a cheap Delta scan with partition pruning
- Use Delta's Z-ordering or partitioning on the intermediate table to align with the filters each domain applies, minimizing IO per branch
- This pattern mirrors the dbt staging/intermediate/marts layering in c001_models_demo.py but implemented in Spark
- Reserve in-memory caching only for small lookup tables and dimension data used across branches
Why this is asked: At architect scale, caching the whole dataset is not viable — the candidate must think in terms of materialization checkpoints.

**Q13 (Architect): How would you govern lazy evaluation in a platform used by hundreds of data scientists who write ad hoc Spark notebooks, to prevent runaway jobs and cluster instability?**
What a good answer covers:
- Enforce dynamic allocation with per-application executor caps so no single lazy plan can monopolize the cluster
- Use Spark fair scheduler pools with per-team queues; lazy plans that trigger large actions are queued rather than immediately consuming all resources
- Provide shared libraries that wrap common transformations with built-in `.explain()` logging and cost estimation before actions run
- Gate production promotions through CI that runs `explain()` on queries and flags full-table scans or missing predicates
- Connect to the ELT pipeline patterns track: standardize on notebook-to-dbt promotion workflows so ad hoc exploration stays exploratory, not operational
Why this is asked: Platform governance around lazy evaluation is an architect-level concern on multi-tenant clusters.

---

## Topic 3: Partitioning and Shuffling

**Q1 (Starter): In c003_partitioning_shuffling_demo.py, `_partition_rows` assigns each order to a partition using a hash of the order ID. What is the purpose of partitioning data this way?**
What a good answer covers:
- Distributes data across multiple workers so tasks can run in parallel without each task needing all the data
- Hash partitioning ensures rows with the same key land on the same partition, which is required for correct group-by and join operations
- The modulo of the hash determines which partition receives each row
Why this is asked: Partitioning is the foundation of parallel execution — a candidate must explain it without jargon.

**Q2 (Starter): What is a shuffle in Spark, and when does it occur?**
What a good answer covers:
- A shuffle is a full data redistribution across the network — every partition sends data to every other partition to regroup rows by a new key
- Shuffles occur on wide-dependency operations: `groupBy`, `join` (non-broadcast), `distinct`, `repartition`, `orderBy`
- In c003_partitioning_shuffling_demo.py this corresponds to the moment rows must be regrouped by customer after arriving partitioned by order ID
Why this is asked: Every Spark performance conversation eventually comes back to shuffles.

**Q3 (Starter): Why are shuffles expensive in Spark?**
What a good answer covers:
- Each executor serializes and writes shuffle output to local disk, then other executors fetch those files over the network
- Network IO and disk IO are the bottlenecks; memory pressure during the sort-and-spill phase adds further cost
- The shuffle introduces a stage boundary — no task in the next stage can start until all tasks in the prior stage have finished writing shuffle output
Why this is asked: Understanding the cost of shuffles motivates every partitioning and join optimization technique.

**Q4 (Starter): In c003_partitioning_shuffling_demo.py, the hash is computed over `order_id`. If you later need to group by `customer`, what happens?**
What a good answer covers:
- A shuffle is required because rows for the same customer may currently live on different partitions (partitioned by order ID hash)
- Spark redistributes all rows by hashing on `customer`, which causes network IO proportional to dataset size
- If the data were pre-partitioned on `customer` (e.g., bucketed by customer in Hive/Delta), the group-by could be computed without a shuffle
Why this is asked: Directly links the demo's partitioning scheme to the shuffle cost it creates.

---

**Q5 (Mid): What is the difference between `repartition` and `coalesce` in Spark, and when would you choose each?**
What a good answer covers:
- `repartition(n)` performs a full shuffle to create exactly n balanced partitions; use it when you need to increase partition count or rebalance skewed data
- `coalesce(n)` merges partitions without a shuffle by combining local partitions on the same executor; only use it to reduce partition count
- Choosing the wrong one: `coalesce` on skewed data creates uneven partitions; `repartition` when reducing count wastes shuffle cost
Why this is asked: This is one of the most commonly asked Spark optimization questions in interviews.

**Q6 (Mid): Looking at c003_partitioning_shuffling_demo.py's hash function, what happens if all orders have order IDs that hash to the same partition index?**
What a good answer covers:
- This is data skew — one partition holds all the rows while others are empty
- The single overloaded task becomes the stragglers that holds up the entire stage
- Skew manifests in the Spark UI as one task taking 10x longer than all others in the same stage
- Mitigations: salting the key, using `skewHint` in Spark 3, switching to a better hash function, or using AQE skew join optimization
Why this is asked: Skew is the most common real-world shuffle problem; the demo's hash function makes the scenario concrete.

**Q7 (Mid): What is Adaptive Query Execution (AQE), and how does it help with partitioning and shuffle problems seen in c003_partitioning_shuffling_demo.py?**
What a good answer covers:
- AQE re-plans the query at runtime using actual shuffle statistics rather than estimates
- It automatically coalesces small post-shuffle partitions (reducing task overhead from too many tiny partitions)
- It detects skewed partitions and splits them into smaller sub-tasks to balance the load
- It can switch a sort-merge join to a broadcast join if the build side turns out to be small after filtering
Why this is asked: AQE is the modern answer to many static partitioning problems; a mid-level engineer should know it exists and what it does.

**Q8 (Mid): How does the number of shuffle partitions (`spark.sql.shuffle.partitions`) affect job performance, and how do you choose a good value?**
What a good answer covers:
- Default is 200, which is too many for small datasets (creates tiny tasks with high scheduling overhead) and too few for very large datasets (creates large tasks that spill to disk)
- Rule of thumb: target 100–200 MB per partition after the shuffle; divide total shuffle data size by that target to get the count
- With AQE enabled, the runtime can coalesce small partitions automatically, reducing the need for manual tuning
- Setting it too low causes large tasks to spill; too high causes scheduler overhead and GC pressure from many small objects
Why this is asked: Partition count is a dial every Spark engineer touches in production.

---

**Q9 (Senior): A job running the kind of customer group-by shown in c003_partitioning_shuffling_demo.py consistently has one task that runs five times longer than all others. Walk through your full diagnosis and remediation.**
What a good answer covers:
- Confirm skew in the Spark UI: check task duration distribution in the stage detail view; look at shuffle read size per task
- Identify the skewed key: query the source data to find which customer values account for disproportionate row counts
- Remediation options ranked by invasiveness: (1) enable AQE with `spark.sql.adaptive.skewJoin.enabled=true`; (2) salt the key by appending a random suffix before aggregating, then reducing; (3) repartition on a composite key; (4) pre-aggregate at the source or use approximate aggregations
- Validate fix by comparing stage durations in the Spark UI before and after
Why this is asked: Skew diagnosis and remediation is a senior-level operational skill.

**Q10 (Senior): Explain how bucketing in Spark (or Delta Lake clustering) can eliminate shuffles for repeated joins and group-bys on the same key.**
What a good answer covers:
- Bucketing pre-partitions data by a column and writes it to a fixed number of bucket files; subsequent joins or group-bys on the same column find rows pre-aligned and skip the shuffle
- Both sides of a join must be bucketed on the join key with the same number of buckets for the shuffle to be eliminated
- Delta Lake's liquid clustering generalizes this with Z-ordering and automatic file layout; it achieves similar IO benefits without strict bucket matching requirements
- Bucketing trades write-time cost for read-time savings; it is most valuable for tables joined repeatedly in the same patterns
Why this is asked: Bucketing is an advanced optimization that distinguishes engineers who tune pipelines from those who only write them.

**Q11 (Senior): In a pipeline that processes c003_partitioning_shuffling_demo.py-style order data daily, how would you design the partition layout of the output Delta table to minimize shuffle costs in downstream analytics queries?**
What a good answer covers:
- Partition the output table by date (e.g., `order_date`) so incremental reads for daily reporting scan only the current day's files — no full shuffle needed
- Within each date partition, Z-order on `customer_id` if most queries filter on customer, allowing data-skipping at the file level
- Avoid over-partitioning (e.g., partitioning by `order_id`) which creates millions of tiny files and increases listing and planning overhead
- Align partition granularity with the batch cadence — daily partitions for daily jobs, hourly for hourly pipelines
Why this is asked: Partition design is a senior design decision with long-term pipeline performance implications.

---

**Q12 (Architect): You are designing a real-time order analytics platform. Orders arrive via Kafka, are processed in Spark Structured Streaming using logic similar to c003_partitioning_shuffling_demo.py, and land in a Delta Lake table queried by a BI tool. Design the partitioning strategy across the full pipeline.**
What a good answer covers:
- Kafka: partition by `customer_id` so related events for the same customer arrive on the same Spark streaming partition, enabling stateful aggregations without inter-partition shuffles
- Spark Structured Streaming: use `.groupBy(window("event_time", "1 hour"), "customer_id")` with watermarking; stateful operators maintain per-key state without re-shuffling on every micro-batch
- Delta Lake landing: partition by `event_date` and Z-order by `customer_id`; use `OPTIMIZE` and `VACUUM` on a schedule to compact small files generated by streaming micro-batches
- BI queries: push filter predicates on `event_date` and `customer_id` so Delta's data-skipping eliminates irrelevant files before they reach the query engine
- Connect to joins at scale track: dimension enrichment (customer name, region) should use broadcast joins so the stream-side shuffle is not compounded by a dimension join shuffle
Why this is asked: End-to-end streaming partition design is an architect-level deliverable.

**Q13 (Architect): Your organization runs hundreds of Spark jobs that all perform shuffles against the same shared object storage. Shuffle IO is saturating the network. What architectural changes would you recommend?**
What a good answer covers:
- Move shuffle storage to a dedicated shuffle service (e.g., Spark's External Shuffle Service or Uber's remote shuffle service) that decouples shuffle IO from executor lifecycle and reduces redundant reads
- Evaluate disaggregated shuffle services (e.g., Magnet, RSS) that colocate shuffle data with the reducers' preferred nodes, reducing cross-rack traffic
- Use AQE to reduce the number of shuffle partitions and coalesce small shuffles, directly reducing total shuffle bytes
- Identify jobs that shuffle the same data repeatedly and pre-materialize shared intermediate results to Delta tables — reusing a Delta scan is cheaper than re-shuffling from source
- Schedule shuffle-heavy jobs in staggered windows rather than concurrently to spread network pressure
Why this is asked: Infrastructure-level shuffle management is an architect and platform engineering concern.

---

## Topic 4: Joins at Scale

**Q1 (Starter): What are the two most common join strategies in Spark, and when does each apply?**
What a good answer covers:
- Sort-merge join: both sides are shuffled and sorted on the join key; used when both tables are large
- Broadcast join: one side is collected to the driver and broadcast to all executors; used when one side is small enough to fit in executor memory
- Spark chooses automatically based on table size estimates, or the user can force a strategy with a hint
Why this is asked: Every Spark engineer must know these two strategies by name and trigger condition.

**Q2 (Starter): In c004_joins_at_scale_demo.py, orders are joined with customers. What determines whether Spark uses a sort-merge join or a broadcast join for this query?**
What a good answer covers:
- Spark estimates the size of each side using table statistics or file metadata
- If the smaller side is below `spark.sql.autoBroadcastJoinThreshold` (default 10 MB), Spark automatically broadcasts it
- The customer table is typically much smaller than orders, so it is a natural broadcast candidate
Why this is asked: Anchors the abstract join strategy discussion to the specific demo context.

**Q3 (Starter): What is a cartesian product, and why is it dangerous in Spark?**
What a good answer covers:
- A cartesian product pairs every row in the left table with every row in the right table, producing M × N output rows
- It occurs when a join has no condition, or when the condition is always true
- At scale (e.g., 1 M × 1 M), the output is 1 trillion rows — this exhausts memory and disk on every executor
Why this is asked: Tests awareness of a common accidental mistake with severe consequences.

**Q4 (Starter): What does a shuffle hash join do differently from a sort-merge join?**
What a good answer covers:
- Shuffle hash join builds an in-memory hash table from the smaller shuffled side, then probes it with each row from the larger side — no sorting required
- Sort-merge join sorts both sides and then merges them in a single pass — more memory-efficient but adds sort cost
- Sort-merge join is preferred for very large tables where neither side fits in a hash table; shuffle hash join is faster when one side is moderately small
Why this is asked: Distinguishes candidates who know multiple join strategies from those who only know sort-merge and broadcast.

---

**Q5 (Mid): A join in c004_joins_at_scale_demo.py between orders and a small dimension table is taking longer than expected. `explain()` shows a sort-merge join. What is the most likely cause, and how do you fix it?**
What a good answer covers:
- The dimension table statistics are stale or missing, so Spark overestimates its size and disables the broadcast
- Fix: run `ANALYZE TABLE customers COMPUTE STATISTICS FOR ALL COLUMNS` to update statistics, or add a `broadcast()` hint explicitly
- Verify with `explain()` after the fix to confirm the plan switches to `BroadcastHashJoin`
Why this is asked: Missing statistics causing suboptimal join strategies is an extremely common production issue.

**Q6 (Mid): What is a skewed join, and how does Spark 3's AQE handle it automatically?**
What a good answer covers:
- A skewed join occurs when one join key value appears far more often than others, causing one task to process the majority of the data
- AQE detects skewed partitions after the shuffle by comparing partition sizes to a configurable threshold
- It splits the large skewed partition into smaller sub-partitions and replicates the corresponding partition from the other side to match, enabling parallel processing
- The user does not need to salt keys manually when AQE skew join is enabled
Why this is asked: AQE skew join handling is a key Spark 3 improvement that seniors and above should be able to describe.

**Q7 (Mid): What is a bucketed join, and when does it eliminate the shuffle in c004_joins_at_scale_demo.py?**
What a good answer covers:
- If both the orders and customers tables are bucketed on the join key with the same number of buckets, Spark can skip the shuffle entirely because matching keys already land in the same bucket files
- Both tables must be written with `bucketBy(n, "customer_id")` on the same `n` and the join key must match the bucket column
- When the shuffle is skipped, the join reduces to a local merge within each bucket, dramatically cutting IO and network traffic
Why this is asked: Bucketed joins are an advanced optimization for repeated high-volume join patterns.

**Q8 (Mid): How do you detect join skew in the Spark UI, and what metrics indicate it?**
What a good answer covers:
- In the stage detail view, look at the task duration distribution — skew appears as one or a few tasks with drastically higher duration and shuffle read size
- The "Max" vs "Median" task duration ratio in stage summary is a quick indicator; a ratio above 5x warrants investigation
- Shuffle read size per task shows which tasks are pulling disproportionate data
- Cross-reference with the data: query the source to count rows per join key value to confirm which key is skewed
Why this is asked: Spark UI proficiency is a practical mid-level skill.

---

**Q9 (Senior): A sort-merge join between two 500 GB tables in c004_joins_at_scale_demo.py style is causing excessive spill to disk. Walk through your diagnosis and the options you would consider.**
What a good answer covers:
- Check the Spark UI stages view for "Spill (Memory)" and "Spill (Disk)" metrics — high spill indicates executor memory is insufficient for the sort buffers
- Increase executor memory (`spark.executor.memory`) or reduce the number of concurrent tasks per executor to give each task more headroom
- Increase `spark.sql.shuffle.partitions` to create smaller partitions that fit in memory during the sort phase
- If one side of the join is significantly smaller, force a broadcast join with a hint even if it exceeds the auto-threshold
- Consider pre-sorting and bucketing both tables on the join key so the sort phase is skipped entirely in future runs
Why this is asked: Spill diagnosis and remediation is a senior-level operational competency.

**Q10 (Senior): Explain how range partitioning differs from hash partitioning for a join, and when range partitioning produces better outcomes.**
What a good answer covers:
- Hash partitioning distributes rows by hashing the key modulo the partition count — produces even distribution but destroys sort order
- Range partitioning samples the data to determine key boundaries, then assigns rows to partitions by range — preserves sort order within each partition
- Range partitioning is better for range-based joins (e.g., event joins within a time window), sort-merge joins where the sort step can be eliminated, and for writing data that will be queried with range predicates
- Cost: range partitioning requires a sampling pass over the data before the partition step
Why this is asked: Range vs hash partitioning is a nuanced topic that separates senior engineers from mid-level ones.

**Q11 (Senior): How would you join a 10 TB fact table with a 500 MB dimension table in c004_joins_at_scale_demo.py without triggering a full sort-merge join shuffle on the fact table?**
What a good answer covers:
- 500 MB exceeds the default broadcast threshold (10 MB) but may fit in executor memory if set appropriately; increase `spark.sql.autoBroadcastJoinThreshold` to 512m and test with `explain()`
- If broadcasting the full 500 MB dimension is too risky, filter the dimension to only the rows referenced by the fact table before the join, reducing its size to broadcastable range
- Use bucketing: if the fact table is pre-bucketed on the join key, only the dimension needs to be broadcast or co-bucketed — eliminating the fact-side shuffle
- If the join is repeated, materialize the joined result as a Delta table and serve downstream queries from it
Why this is asked: Joining a very large fact with a moderately sized dimension is a common real-world problem with no single correct answer.

---

**Q12 (Architect): Design the join strategy for an ELT pipeline that joins a 100 TB clickstream fact table with five dimension tables ranging from 1 MB to 2 GB. Describe how you would handle each dimension differently.**
What a good answer covers:
- 1 MB dimension: auto-broadcast — no configuration change needed; Spark handles this transparently
- Dimensions up to ~200 MB: raise `autoBroadcastJoinThreshold` to 256m or use explicit `broadcast()` hints after verifying executor memory headroom
- 2 GB dimension: bucket both the fact table and the dimension on the join key with the same bucket count; this eliminates the shuffle on both sides for all future runs
- For any dimension with skewed join keys (e.g., a "unknown customer" catch-all): pre-filter or replace with a CASE expression to avoid skew propagating into the fact join
- Materialize intermediate joined results to Delta intermediate tables aligned with the dbt intermediate layer (c001_models_demo.py), so downstream mart queries do not re-execute the join
Why this is asked: Multi-dimensional join strategy at 100 TB scale is an architect-level design problem.

**Q13 (Architect): Your data platform team wants to standardize join strategies across hundreds of Spark jobs written by different teams. What governance mechanisms and tooling would you put in place?**
What a good answer covers:
- Build a shared Spark utilities library with opinionated join functions that log `explain()` output, enforce broadcast hints for known small tables, and emit metrics to the observability platform
- Integrate a CI job that runs `explain()` on all registered queries and fails the build if a sort-merge join appears where a broadcast join is expected (based on a table size registry)
- Publish a table metadata catalog that includes size statistics, bucketing keys, and recommended join strategy for each table; Spark jobs query the catalog to auto-configure hints
- Connect to the ELT pipeline patterns track: require that all cross-domain joins happen in the intermediate layer (not in mart models or ad hoc notebooks) so join strategies are reviewed centrally
- Enforce AQE globally (`spark.sql.adaptive.enabled=true`) as the platform default so runtime optimizations apply even when static hints are suboptimal
Why this is asked: Join strategy governance at platform scale is an architect-level responsibility.

---

## Topic 5: Broadcast Joins

**Q1 (Starter): What is a broadcast join in Spark, and what makes it faster than a sort-merge join?**
What a good answer covers:
- The driver collects the smaller table (the "build side") and sends a copy to every executor
- Each executor probes the in-memory copy of the small table for every row in its local partition of the large table — no shuffle needed on the large side
- Eliminates the network IO of shuffling the large table, which is the dominant cost in sort-merge joins
Why this is asked: Broadcast joins are the single most impactful join optimization and the first thing an interviewer reaches for.

**Q2 (Starter): In c005_broadcast_joins_demo.py, a small customer lookup table is joined with a large orders table. How does Spark decide to broadcast the customer table automatically?**
What a good answer covers:
- Spark estimates the size of the customer table from file metadata or table statistics
- If the estimate is below `spark.sql.autoBroadcastJoinThreshold` (default 10 MB), Spark inserts a `BroadcastHashJoin` node in the physical plan automatically
- The threshold is configurable; setting it to -1 disables auto-broadcast entirely
Why this is asked: Ensures the candidate understands that broadcast is often automatic, not always explicit.

**Q3 (Starter): How do you force a broadcast join in Spark when Spark does not choose it automatically?**
What a good answer covers:
- Use the `broadcast()` hint: `orders.join(broadcast(customers), "customer_id")`
- Or use the SQL hint: `SELECT /*+ BROADCAST(customers) */ ...`
- This overrides the auto-threshold decision and forces the broadcast regardless of estimated size
Why this is asked: Knowing the hint syntax is a basic practical skill.

**Q4 (Starter): What happens if you broadcast a table that is too large to fit in executor memory?**
What a good answer covers:
- The executor runs out of heap memory during the broadcast collection phase, causing an OOM error or excessive GC
- The driver must also hold the full table in memory to serialize and send it — this can crash the driver first
- Best practice: verify the table size before using a `broadcast()` hint; do not broadcast tables larger than ~200–500 MB without careful memory sizing
Why this is asked: Indiscriminate broadcast hints are a common cause of OOM crashes in Spark production jobs.

---

**Q5 (Mid): A broadcast join in c005_broadcast_joins_demo.py is timing out during the broadcast phase. What are the likely causes and how do you fix them?**
What a good answer covers:
- `spark.sql.broadcastTimeout` (default 300 seconds) is exceeded — the build side is taking too long to collect and broadcast
- Likely causes: the table is larger than expected (statistics are stale), network bandwidth between driver and executors is saturated, or the driver is GC-paused
- Fix: increase `broadcastTimeout`, reduce the build side by pre-filtering, or switch to a sort-merge join with explicit hints to disable broadcast for this query
Why this is asked: Broadcast timeout is a frequent production error that a mid-level engineer must be able to handle.

**Q6 (Mid): Explain the difference between `BroadcastHashJoin` and `BroadcastNestedLoopJoin` in Spark's physical plan.**
What a good answer covers:
- `BroadcastHashJoin`: the broadcast side is stored in a hash table; each row from the stream side does a hash lookup — O(1) probe per row
- `BroadcastNestedLoopJoin`: each row from the stream side is compared against every row in the broadcast side — O(n × m); used when there is no equi-join condition
- `BroadcastNestedLoopJoin` appears for inequality joins and cross joins with a small broadcast side; it is much slower and should be avoided on large stream sides
Why this is asked: Distinguishes engineers who read physical plans from those who only write queries.

**Q7 (Mid): How does a broadcast join interact with Spark's data locality preference?**
What a good answer covers:
- Normally Spark prefers PROCESS_LOCAL or NODE_LOCAL task scheduling to avoid reading data over the network
- With a broadcast join, the stream side tasks still respect data locality for their local partitions
- The broadcast side is already in memory on every executor, so there is no locality preference for it — every task has equal access to the broadcast variable
- This means broadcast joins do not compromise data locality for the large (stream) side
Why this is asked: Connects broadcast joins to the scheduling model — a nuanced mid-level point.

**Q8 (Mid): When should you prefer a sort-merge join over a broadcast join even when one table is small enough to broadcast?**
What a good answer covers:
- When the driver is memory-constrained and collecting the build side would crash it
- When the cluster has many executors and broadcasting a large-ish table creates too much network fan-out overhead
- When the join is used in a streaming context where re-broadcasting on each micro-batch is too expensive (prefer static broadcast variables or Delta reads instead)
- When the query plan already has multiple broadcast joins and executor memory is under pressure from multiple simultaneous broadcast variables
Why this is asked: Tests nuanced judgment — broadcast is not always better, even when technically applicable.

---

**Q9 (Senior): In c005_broadcast_joins_demo.py, the customer lookup table is updated daily. How do you ensure the broadcast join always uses the current version of the table without restarting the Spark application?**
What a good answer covers:
- In batch jobs: re-read the table at the start of each job run; Spark creates a fresh broadcast variable for each action, so daily job restarts naturally refresh it
- In long-running Spark applications or structured streaming: unpersist the old broadcast variable and create a new one pointing to the refreshed table at the start of each processing window
- In streaming with Delta: use `.option("ignoreChanges", True)` or read the dimension as a separate batch source refreshed on a schedule; join with the latest snapshot per micro-batch
- Avoid caching the broadcast variable across sessions in a shared Spark context without an explicit invalidation mechanism
Why this is asked: Broadcast variable lifecycle management in long-running applications is a senior operational concern.

**Q10 (Senior): How does Spark's AQE convert a planned sort-merge join into a broadcast join at runtime, and what conditions must be met?**
What a good answer covers:
- During the shuffle read phase, AQE collects actual shuffle output size statistics for each side
- If one side's actual size falls below `spark.sql.adaptive.autoBroadcastJoinThreshold` (separate from the static threshold), AQE replaces the sort-merge join with a broadcast hash join in the updated physical plan
- Conditions: AQE must be enabled (`spark.sql.adaptive.enabled=true`), the join must be an equi-join, and the runtime size of the build side must fall below the threshold (often because a filter reduced the data more than the optimizer estimated)
- This is particularly valuable when the static optimizer overestimates table sizes from stale statistics
Why this is asked: AQE dynamic join conversion is a key Spark 3 feature that seniors must understand mechanistically.

**Q11 (Senior): You have a pipeline with ten broadcast joins in the same Spark job — each broadcasting a different dimension table of ~100 MB. What risks does this create, and how would you mitigate them?**
What a good answer covers:
- Each broadcast variable occupies executor memory simultaneously; ten × 100 MB = 1 GB of executor memory reserved for broadcast data alone, reducing memory available for shuffle buffers and task execution
- Risk of OOM on executors if total broadcast footprint plus task memory exceeds `spark.executor.memory`
- Mitigation: stage the joins so not all ten broadcasts are live at the same time; unpersist broadcast variables after their last use
- Consider pre-joining some dimension tables together offline (reducing ten broadcasts to fewer, smaller ones) or partitioning the fact table processing so each batch only needs a subset of dimensions
- Connect to the joins at scale track: evaluate whether any dimension can be replaced with a lookup via a Delta scan with partition pruning instead of a full broadcast
Why this is asked: Multi-broadcast memory management is a senior-level production concern.

---

**Q12 (Architect): Design a broadcast join strategy for a multi-tenant analytics platform where each tenant has its own dimension tables (varying sizes: 1 MB to 5 GB) and shares a cluster with other tenants.**
What a good answer covers:
- Catalog all dimension tables by size at ingestion time; store size metadata in a central catalog queried by the job framework at plan time
- Auto-apply `broadcast()` hints only for tables below a configurable per-tenant threshold (e.g., 200 MB), scaled by the executor memory allocation for that tenant's queue
- Large dimension tables (> 1 GB): bucket on join key and store in Delta; joins against them use bucketed sort-merge without shuffling the fact side
- Isolate tenant broadcast variables using separate Spark sessions per tenant — broadcast variables in one session do not consume memory in another session's executors when dynamic allocation is in use
- Govern total broadcast memory per tenant via executor memory caps in the fair scheduler; alert when a tenant's combined broadcast footprint exceeds 50% of their executor memory allocation
Why this is asked: Multi-tenant broadcast resource isolation is an architect-level platform design problem.

**Q13 (Architect): How would you integrate broadcast join optimization into a CI/CD pipeline for Spark jobs, ensuring that developers are warned before deploying joins that will fail or degrade at production data volumes?**
What a good answer covers:
- Add a CI step that runs `df.explain(True)` on all registered join queries against representative table statistics (not production data) and parses the plan output for `SortMergeJoin` nodes where a broadcast was expected
- Maintain a table size registry (updated nightly from production metadata) that CI uses to simulate Spark's cost-based optimizer decisions
- Fail the build if a broadcast hint is applied to a table currently larger than the configured threshold, with a warning message linking to the table's size trend
- Gate production deployments on a dry-run that logs the physical plan to the observability platform; on-call engineers review plan regressions before traffic is shifted
- Connect to the ELT pipeline patterns track: standardize all dimension table joins in the intermediate dbt/Spark layer so plan governance applies centrally rather than per-notebook
Why this is asked: CI/CD integration for query plan governance is an architect-level engineering practice.
