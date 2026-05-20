# QA 01 — 1000-Foot PySpark Opening

Purpose:
This file captures Sean's final polished learning/interview answers from the
Course 11 opening map and entrance pages. Keep answers short, safe, and useful
for Wipro PySpark interview rehearsal.

Only final accepted answers should be kept here. Draft thinking stays in chat.

# Spark and PySpark Big Picture

# QA 01 — 1000-Foot PySpark Opening

Purpose:
This file captures Sean's final polished learning/interview answers from the
Course 11 opening map and entrance pages. Keep answers short, safe, and useful
for Wipro PySpark interview rehearsal.

Only final accepted answers should be kept here. Draft thinking stays in chat.

# Spark and PySpark Big Picture

## Q01. What is Spark?

Spark is a distributed compute engine used for large-scale data processing.

The simple idea is that Spark does not have to process all data on one machine.
It can split data into partitions, distribute the work across executors, and
process many pieces in parallel.

In a Spark application, the driver coordinates the job, builds the execution
plan, and sends work to executors. The executors perform the actual tasks on
partitions of the data.

Spark is useful for ETL and analytics because it can process large datasets
using DataFrames, SQL, transformations, joins, aggregations, and writes to
downstream storage.

A key thing to remember is that Spark uses lazy evaluation. It does not run
every transformation immediately. It builds a plan first, then runs when an
action such as count, show, collect, or write is called.

Punch line:
Spark is the distributed engine that lets us process large data in parallel
instead of treating everything like a one-machine Python or SQL job.


## Q02. What is PySpark?

PySpark is the Python API for Apache Spark.

It lets me write Spark data-processing logic using Python, while Spark handles
the distributed execution underneath. In PySpark, I usually work with
SparkSession, DataFrames, transformations, actions, Spark SQL, joins,
aggregations, and read/write operations.

The important idea is that PySpark is not just normal Python running on one
machine. It is Python code that expresses work for the Spark engine. Spark then
plans and executes that work across the driver and executors.

PySpark is useful for ETL because I can read data from files or tables,
transform it, join it, aggregate it, validate it, and write the result to a
downstream target.

Punch line:
PySpark is Python for writing Spark jobs, but Spark is the distributed engine
doing the heavy execution work.



## Q03. Why does this job care about PySpark?
This job cares about PySpark because many production data engineering jobs
need to process data at a scale where single-machine Python scripts or manual
SQL work are not enough.

PySpark is useful for ETL work because it can read large datasets, apply
transformations, join data, aggregate results, run SQL-style logic, and write
outputs to downstream tables or files.

For this role, PySpark also connects naturally with SQL, UNIX shell scripting,
job scheduling, automation, and production support. A real PySpark job is not
just code. It has inputs, outputs, logs, row counts, schema checks, dependencies,
failure handling, and rerun behavior.

In a finance environment, that matters because data pipelines often need to be
reliable, repeatable, auditable, and supportable.

Punch line:
This job cares about PySpark because PySpark is the engine for scalable ETL,
and the role needs someone who can build and support those jobs in production.

# Spark Architecture

## Q04. What is the driver?

The driver is the main coordinating process for a Spark application.

It runs the main program, creates the SparkSession, builds the execution plan,
and coordinates work across the cluster. The driver does not do all the heavy
data processing itself. It plans the job, tracks progress, and sends tasks to
executors.

In PySpark, when I write DataFrame transformations, the driver helps build the
logical plan or DAG. When an action is called, Spark turns that plan into stages
and tasks that executors run on partitions of the data.

Punch line:
The driver is the coordinator of the Spark job. Executors do the distributed
worker-side processing.


## Q05. What are executors?

Executors are the distributed worker processes that run Spark tasks.

The driver coordinates the Spark application, but executors do the actual data
processing. Each executor works on partitions of the data and runs tasks in
parallel.

Executors also report status, results, and failures back to the driver. If a job
is slow or failing, executor logs, memory usage, failed tasks, and shuffle
behavior are important things to check.

Punch line:
Executors are the workers. They process partitions of data in parallel while
the driver coordinates the job. 


# DataFrame Work

## Q06. What is a SparkSession?

A SparkSession is the main entry point for PySpark work.

It gives my PySpark code access to Spark DataFrames, Spark SQL, configuration,
and read/write operations. In most modern PySpark jobs, I start from a
SparkSession and use it to read data, create DataFrames, run SQL-style logic,
apply transformations, and write results.

I think of SparkSession as the connection between my PySpark code and the Spark
engine.

Punch line:
SparkSession is the front door into Spark from PySpark.


## Q07. What is a DataFrame in PySpark?

A DataFrame in PySpark is a table-like distributed data structure.

It has rows and columns like a database table or spreadsheet, but the data can
be split into partitions and processed in parallel across Spark executors.

Most PySpark ETL work is done with DataFrames. For example, I can read data into
a DataFrame, select columns, filter rows, add derived columns, join datasets,
aggregate results, and write the output.

The important point is that a PySpark DataFrame is not the same as a local
Pandas DataFrame. A PySpark DataFrame represents distributed work that Spark
plans and executes across the cluster.

Punch line:
A PySpark DataFrame is the main table-like object used to express distributed
ETL work in Spark.


# Execution Model

## Q08. What is the difference between transformations and actions?

Transformations are the steps that define what Spark should do to the data.

Examples of transformations include select, filter, withColumn, groupBy, joins,
and aggregations. Transformations are lazy, which means Spark does not execute
them immediately. Instead, Spark uses them to build an execution plan.

Actions are the operations that trigger Spark to actually run the plan.

Examples of actions include show, count, collect, and write. When an action is
called, Spark takes the planned transformations, optimizes the work, and runs
the job across the driver and executors.

Punch line:
Transformations build the plan. Actions trigger the execution.


## Q09. What is lazy evaluation?

Lazy evaluation means Spark does not execute transformations immediately.

When I write transformations such as select, filter, withColumn, groupBy, or
join, Spark builds a plan instead of running each step right away. The actual
execution happens only when an action is called, such as count, show, collect,
or write.

This helps Spark optimize the full pipeline before running it. Spark can look
at the sequence of work, improve the plan, and avoid doing unnecessary
processing too early.

In production, lazy evaluation matters because an error may not appear at the
line where the transformation is written. The job may fail later when an action
finally triggers execution.

Punch line:
Lazy evaluation means Spark builds the plan first and runs it only when an
action triggers execution.

## Q10. What are partitions and shuffle?

Partitions are how Spark splits data so it can be processed in parallel.

Instead of one machine processing one large dataset from beginning to end,
Spark divides the data into partitions. Executors can then run tasks on those
partitions at the same time.

Shuffle is the movement of data across executors.

Shuffle often happens during operations such as joins, groupBy, repartitioning,
and aggregations. It can be expensive because data may need to move across the
network and sometimes spill to disk.

In production, shuffle is one of the first things I would think about when a
Spark job is slow, unstable, or using too much memory. Good partitioning,
careful joins, avoiding unnecessary wide transformations, and using broadcast
joins when appropriate can reduce shuffle pressure.

Punch line:
Partitions allow parallel processing. Shuffle is the expensive data movement
between executors.


# Production Support Mindset

## Q11. How do you support a PySpark job in production?

Supporting a PySpark job in production means checking both the technical
execution and the data quality of the pipeline.

First, I would confirm the operational basics: did the job start, what
parameters were used, what upstream data arrived, and what dependencies ran
before it. Then I would check logs, failed stages, executor errors, runtime,
and whether the job failed during read, transform, join, shuffle, or write.

I would also check data controls such as input counts, output counts, schema
expectations, nulls or bad records, duplicate behavior, and whether the output
looks reasonable compared to the baseline.

For reruns, I would make sure the job is safe to rerun and understand whether
it overwrites, appends, or creates duplicate output.

Punch line:
Production support is not just fixing code. It is checking logs, counts,
data quality, dependencies, and safe rerun behavior.

## Q12. What should you check when a PySpark job fails?

When a PySpark job fails, I would check the failure from both the job-execution
side and the data-pipeline side.

First, I would look at the scheduler or job-run status to confirm when it
started, what parameters were used, and which step failed. Then I would review
the Spark logs, failed stages, executor errors, and whether the failure happened
during read, transform, join, shuffle, or write.

I would also check the data side: whether the upstream file or table arrived,
whether the schema changed, whether input counts look normal, and whether any
bad records, nulls, duplicates, or data-quality issues caused the failure.

Before rerunning, I would confirm rerun safety. I need to know whether the job
overwrites, appends, checkpoints, or could create duplicate output.

Punch line:
When a PySpark job fails, check logs, failed stages, parameters, dependencies,
data quality, and rerun safety before simply restarting it.

# Orchestration and Internals Touchpoints

## Q13. What is a DAG in Spark?

A Spark DAG is the execution plan Spark builds from a chain of transformations.

When I write transformations such as select, filter, joins, or groupBy, Spark
does not run each step immediately. It builds a **directed acyclic graph**, or DAG,
that represents the work.

When an action such as count, show, write, or collect is called, Spark optimizes
the plan and executes it as stages and tasks. Expensive operations such as joins
or groupBy may create shuffle boundaries between stages.

Punch line:
A Spark DAG is Spark’s internal plan for how to execute the data work.


## Q14. What is the difference between a Spark DAG and an Airflow DAG?

A Spark DAG is about executing one Spark job. It describes how Spark will run
transformations across stages and tasks.

An Airflow DAG is about orchestrating a workflow. It describes which jobs run,
in what order, with scheduling, retries, parameters, and dependencies.

The key difference is scope. Spark DAGs are inside the Spark execution engine.
Airflow DAGs sit above jobs and coordinate the larger pipeline.

Punch line:
Spark DAG = data execution plan.
Airflow DAG = workflow orchestration plan.

## Q15. Where does Airflow fit with PySpark jobs?

Airflow can schedule and orchestrate PySpark jobs. It can decide when the job
runs, what parameters are passed, what runs before or after it, and what happens
if it fails.

But once the PySpark job starts, Spark handles the distributed execution using
the driver and executors.

In production, Airflow is useful because it gives visibility into job status,
dependencies, retries, failures, and operational history.

Punch line:
Airflow starts and monitors the pipeline. Spark runs the distributed data work.

## Q16. Is PySpark actually running only Python?

PySpark gives developers a Python API, but Spark’s core execution engine runs on
the JVM.

In normal DataFrame and Spark SQL work, I write Python code, Spark translates
the logic into an execution plan, and the Spark engine executes that plan across
the cluster.

This is why DataFrame and SQL-style PySpark code can be much more efficient
than writing everything as custom Python logic. If I use Python UDFs heavily,
there can be extra overhead because data may need to cross between the Spark/JVM
side and Python execution.

Punch line:
PySpark is Python for the developer, with Spark/JVM execution underneath.

### UDF
UDF stands for User-Defined Function.

In PySpark, a Python UDF is a custom, standard Python function that you write to perform an operation on your data when Spark's built-in functions can't handle your specific logic.

Think of it like writing a regular Python function and then telling Spark: "Hey, take this custom Python code and apply it to every row in my massive distributed DataFrame."

## Q17. What should I safely say about PySpark internals?

A safe answer is that I understand the practical Spark execution model: the
driver coordinates the job, executors process partitions, transformations are
lazy, actions trigger execution, and expensive operations like joins or groupBy
can cause shuffles.

I also understand that PySpark gives me a Python API, while Spark execution
runs underneath through the Spark engine/JVM layer.

I would avoid claiming deep Spark engine internals unless the role specifically
requires it. But I can discuss the practical internals needed to build,
troubleshoot, and support PySpark ETL jobs.

Punch line:
Know enough internals to write, troubleshoot, and support jobs safely.
