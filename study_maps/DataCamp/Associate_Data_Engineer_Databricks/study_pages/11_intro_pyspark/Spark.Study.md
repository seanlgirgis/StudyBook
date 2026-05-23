Relationship note:
This file is the expanded Spark production study guide. It extends beyond Course 11 into runtime architecture, Delta Lake, medallion architecture, CDC/MERGE, optimization, catalog/governance, and streaming. The canonical Course 11 foundation QA remains QA_01_1000ft_pyspark_opening.md.

Source-of-truth note:
This file is canonical for expanded production Spark topics.
It should not duplicate the full Course 11 foundation QA except where a short bridge or reference is useful.

## Foundation Bridge (Canonical Owner: QA_01)

The following foundation topics are intentionally owned in full by `QA_01_1000ft_pyspark_opening.md`:
- Spark/PySpark basics
- driver/executors
- SparkSession/DataFrames
- transformations/actions/lazy evaluation
- schemas and core DataFrame operations
- joins/unions/UDF basics
- RDD basics
- Spark SQL/temp views
- aggregation basics
- explain/cache/persist/broadcast fundamentals

Use this bridge rule:
- Read full foundation answers in `QA_01_1000ft_pyspark_opening.md`.
- Use this file for expanded production architecture, Delta, performance maintenance, catalog/governance, and streaming.

Bridge reference:
`QA_01_1000ft_pyspark_opening.md` (Q01-Q69 foundation path).
## Q21 How is a PySpark job submitted to a Spark cluster, and who decides which machines run the work?

A PySpark job is usually submitted through a submission layer or platform, not
by hard-coding machine names inside the PySpark code.

For example, on Hadoop/YARN, a job can be submitted with spark-submit using
options such as --master yarn, deploy mode, executor count, executor memory,
and executor cores. YARN manages the available machines and allocates resources
for the Spark driver and executors.

In Databricks, EMR, Glue, Kubernetes, or other managed environments, the job or
cluster configuration defines where the Spark job runs and what resources it
gets.

The PySpark code defines the data-processing logic. The submission layer or
platform defines where and how it runs.

Punch line:
PySpark code says what to do. spark-submit, Airflow, Databricks, EMR, Glue, or
Kubernetes says where and with what resources.

## Q22 What is the difference between collect(), show(), and count() in PySpark, and why can collect() be risky?

collect(), show(), and count() are all actions, so they trigger Spark jobs.

show() displays a limited number of rows, usually for inspection or debugging.
It is useful for small previews.

count() counts the number of rows in the DataFrame. It is useful for validation
and production controls, but repeated count() calls can trigger repeated work
unless the data is cached or persisted appropriately.

collect() brings all distributed results back to the driver as local Python
objects. That is risky on large datasets because it can overload driver memory
and fail the job.

Punch line:
show() previews rows, count() counts rows, and collect() pulls all results to
the driver. Use collect() only when the result is small enough for driver
memory.

## Q23 What is the difference between Spark runtime and cluster/resource manager?

Spark runtime is the part that runs the Spark application. It includes the
driver, executors, tasks, partitions, stages, and execution plan.

The driver coordinates the job. Executors run distributed tasks on partitions
of data.

The cluster/resource manager is the layer that allocates compute resources such
as machines, CPU, and memory. Examples include YARN, Kubernetes, Spark
Standalone, Databricks clusters, EMR, and AWS Glue managed runtime.

Punch line:
Spark runtime runs the data work. The cluster/resource manager gives Spark the
resources to run that work.

## Q24 What is the difference between storage, catalog/metadata, and orchestration in a Spark production architecture?

Storage is where the data physically lives.

Examples include HDFS, S3, ADLS, GCS, Parquet files, Delta tables, databases,
or Kafka topics.

Catalog / metadata is the layer that describes the data. It tracks table names,
schemas, locations, and permissions. Examples include Hive Metastore, AWS Glue
Data Catalog, and Databricks Unity Catalog.

Orchestration is the layer that coordinates when jobs run and in what order.
It handles schedules, dependencies, parameters, retries, alerts, and operational
history. Examples include Airflow, Databricks Workflows, Control-M, Autosys,
or AWS Step Functions.

Punch line:
Storage holds the data. Catalog explains the data. Orchestration coordinates
the pipeline.

## Q25 What is the difference between Databricks, EMR, Glue, Kubernetes, and YARN in the Spark world?
Databricks:
A managed Spark/lakehouse platform with notebooks, jobs, clusters, Delta Lake,
and catalog/governance features. It hides much of the low-level Spark cluster
management behind a managed platform experience.

EMR:
Amazon’s managed Hadoop/Spark cluster platform. It gives more infrastructure
control than Glue and is commonly used for Spark/Hadoop workloads on AWS.

Glue:
AWS managed ETL service that can run Spark jobs and integrates with S3 and the
Glue Data Catalog. It is more managed/serverless-style than EMR.

Kubernetes:
A container orchestration/resource-management platform. In Spark on Kubernetes,
the driver and executors run as pods.

YARN:
The classic Hadoop resource manager. In Hadoop-style Spark deployments, YARN
allocates cluster resources for the Spark driver and executors.

Punch line:
YARN and Kubernetes are resource managers. Databricks, EMR, and Glue are
managed platforms that package Spark runtime and operations in different ways.

## Q26 What is the difference between Airflow and Spark?

Spark is the distributed data-processing engine. It runs ETL or analytics work
using a driver, executors, transformations, actions, partitions, and Spark jobs.

Airflow is an orchestrator. It does not do Spark’s distributed data processing
itself. Instead, Airflow schedules and coordinates workflows. It can start a
PySpark job, pass parameters, manage dependencies, retry failures, alert on
problems, and track job history.

For example, Airflow may say: run ingestion first, then run the PySpark
transformation job, then run validation, then publish the output. But once the
PySpark job starts, Spark handles the distributed execution.

Punch line:
Airflow decides when and in what order jobs run. Spark does the distributed
data-processing work.

## Q27 What is the difference between spark-submit, Databricks Jobs, EMR Steps, and Glue Jobs?

spark-submit is the standard Spark command-line way to launch a Spark
application. It is common in Hadoop/YARN, standalone Spark, or some Kubernetes
style deployments.

Databricks Jobs are Databricks-managed job definitions. They can run notebooks,
Python files, Spark tasks, workflows, or multiple dependent tasks on a
Databricks cluster.

EMR Steps are work units submitted to an Amazon EMR cluster. A step can run a
Spark job, Hive job, script, or other big-data task on that EMR cluster.

Glue Jobs are AWS Glue-managed ETL jobs. They run in AWS Glue’s managed Spark
runtime and commonly read/write data from S3 and use the Glue Data Catalog.

Punch line:
spark-submit is the generic Spark launcher. Databricks Jobs, EMR Steps, and
Glue Jobs are platform-specific ways to run Spark or ETL work in managed
environments.


## Q28 What is the difference between Hadoop/YARN and Spark?

Spark is the compute engine. It runs distributed data processing jobs.

Hadoop is a broader big-data ecosystem. In classic Hadoop environments, HDFS
is often used for distributed storage, and YARN is used as the resource manager.

YARN is not the same as Spark. YARN allocates cluster resources such as CPU,
memory, and containers. Spark can run on YARN, and YARN can provide resources
for the Spark driver and executors.

Spark can also run in other environments, such as Kubernetes, Databricks, EMR,
Glue, or Spark Standalone.

Punch line:
Spark is the distributed compute engine. Hadoop is the broader ecosystem, and
YARN is the Hadoop resource manager that Spark can run on.

## Q29 What is Delta Lake, and how is it different from Spark or PySpark?


Delta Lake is a reliable table/storage layer for data lakes. Spark and
PySpark are compute tools used to process data, while Delta Lake is about how
the data is stored, managed, and protected.

Spark is the distributed compute engine. PySpark is the Python API for Spark.
Together, they let me read, transform, join, aggregate, and write data using
DataFrames or Spark SQL.

Delta Lake is different. It adds reliability features on top of data lake
storage, commonly using Parquet files underneath. It provides ACID (Atomicity, Consistency, Isolation, Durability)
transactions, schema enforcement, version history, and time travel.

That means Delta helps protect data quality and consistency. For example, if
multiple jobs are reading and writing, Delta helps prevent corrupted or
partially written table states. Schema enforcement helps stop bad or unexpected
data structures from entering a table. Version history allows rollback or
time-travel queries to inspect earlier table states.

In practice, I may write normal PySpark DataFrame logic, but save the output as
a Delta table instead of a plain CSV or basic Parquet output when I need more
reliability and table-management features.

Safe way to say it:
Spark/PySpark does the processing. Delta Lake makes the lakehouse table more
reliable, consistent, and auditable.

Punch line:
Spark is the compute engine. PySpark is the Python interface. Delta Lake is the
reliable table/storage layer that adds transactions, schema control, and
version history.

## Q30. What is the difference between Parquet and Delta Lake, and why might a data engineer choose Delta for production tables?

Parquet is a columnar file format. It stores data efficiently for analytics,
especially when queries only need certain columns. Spark can read and write
Parquet very efficiently.

Delta Lake is a table/storage layer built on top of Parquet files. It does not
replace Parquet; it adds reliability and table-management features around
Parquet data.

A Delta table usually contains Parquet data files plus a `_delta_log` folder.
The transaction log tracks table changes and provides a reliable source of
truth for the table state.

A data engineer might choose Delta Lake for production tables because Delta
adds features that plain Parquet folders do not provide by themselves:

- ACID transactions:
  Reads and writes are managed safely, helping prevent partial or corrupted
  table states.

- Schema enforcement:
  Delta can reject data that does not match the expected table schema.

- Version history:
  Delta tracks commits over time.

- Time travel:
  Users can query or restore earlier versions of a table.

- Better production reliability:
  Delta is safer for pipelines where multiple jobs may read, write, update, or
  audit the same dataset.

In practice, I can still use PySpark DataFrame logic, but write the output as a
Delta table when I need stronger reliability, auditability, and table-management
features than plain Parquet files.

Punch line:
Parquet is an efficient file format. Delta Lake is a reliable table layer built
on Parquet that adds transactions, schema enforcement, version history, and time
travel for production lakehouse tables.


## Q31. How does Delta Lake use Parquet files and the transaction log to support versioning and medallion architecture?

Delta Lake stores table data as Parquet files and tracks table versions through
a transaction log called `_delta_log`.

Instead of treating a folder of Parquet files as the table, Delta uses the
transaction log to determine which files belong to each table version. The log
records commits over time, including files added, removed, or changed from the
table’s active snapshot.

This gives Delta Lake reliability, version history, time travel, rollback
options, and safer reprocessing.

That is why Delta fits medallion architecture well. In a Bronze, Silver, and
Gold design, each layer can be treated as a controlled table version. If bad
data enters Silver or Gold, we can trace what changed, time travel to an earlier
version, rollback when appropriate, or reprocess from a known good point.

Punch line:
Parquet stores the data files. Delta log tells Spark which files make up each
table version. That gives the lakehouse reliability, auditability, time travel,
and safer medallion reprocessing.

## Q32. What is medallion architecture, and how do Bronze, Silver, and Gold layers relate to Delta Lake?

Medallion architecture is a lakehouse data-design pattern that organizes data
into progressive quality layers: Bronze, Silver, and Gold.

Bronze is the raw or lightly processed layer. It keeps source data close to how
it arrived, often with ingestion metadata. The goal is to preserve the original
data so it can be audited or reprocessed later.

Silver is the cleaned and validated layer. This is where data is standardized,
deduplicated, type-corrected, joined, and made reliable for broader use.

Gold is the business-ready layer. This is where data is aggregated, modeled, or
prepared for reporting, dashboards, analytics, machine learning, or downstream
business consumption.

Delta Lake fits medallion architecture well because each Bronze, Silver, and
Gold table can have transaction history, schema enforcement, time travel, and
rollback or reprocessing options.

If something goes wrong in Silver or Gold, Delta history can help trace what
changed, return to a known-good version, or reprocess from a clean upstream
layer.

Punch line:
Bronze preserves raw data, Silver cleans and validates it, Gold serves business
use cases. Delta Lake makes each layer more reliable, auditable, and
reprocessable.

## Q33. What is schema enforcement in Delta Lake, and why is it useful in production?

Schema enforcement means Delta Lake checks incoming data against the expected
table schema before allowing the write.

If the incoming DataFrame has unexpected columns, missing required structure,
or incompatible data types, Delta can reject the write instead of silently
allowing bad data into the table.

This is useful in production because schema drift is a real pipeline risk. For
example, an upstream system might change a column from integer to string, rename
a field, or add a new column without warning. If that bad structure is written
into a production table, downstream reports, dashboards, models, or ETL jobs
may break later.

Delta Lake helps prevent that by validating the incoming data against the table
schema at write time. This protects downstream consumers and gives the data
engineering team a chance to fix the source or adjust the pipeline deliberately.

Punch line:
Schema enforcement protects Delta tables from unexpected structure changes by
rejecting bad writes before they corrupt downstream data.

## Q34. What is time travel in Delta Lake, and why is it useful for data engineering?

Time travel in Delta Lake means querying a table as it existed at a specific
version or point in time.

Delta Lake can do this because it tracks table changes in the Delta transaction
log. The log records commits over time, so Delta can reconstruct which data
files belonged to the table at a given version.

This is useful for auditing, debugging, rollback, reruns, and bad-data recovery.
If a pipeline writes bad data, I can inspect an earlier table version, compare
versions, or reprocess from a known good state.

Time travel is especially useful in medallion architecture because Bronze,
Silver, and Gold tables can each have controlled versions. If something goes
wrong in Silver or Gold, I can trace what changed and reprocess from a trusted
upstream point.

Punch line:
Time travel lets me query or recover earlier Delta table versions, which helps
with audit, debugging, rollback, and safer reprocessing.


## Q35. What is the difference between schema enforcement and schema evolution in Delta Lake?

Schema enforcement means Delta Lake rejects writes that do not match the
table’s current schema. It acts as a gatekeeper to protect the table from
unexpected columns, missing structure, or incompatible data types.

Schema evolution means the table schema is intentionally allowed to change,
usually when a new field is expected and approved. For example, options like
`mergeSchema` can allow Delta to add new columns to the table schema.

The difference is control.

Schema enforcement protects production tables from accidental schema drift.
Schema evolution allows planned schema changes when the pipeline or business
logic really needs to accept new fields.

This is useful in medallion architecture. In Bronze, I may allow more schema
flexibility because raw source systems can change. In Silver and Gold, I would
usually be stricter because downstream reports, dashboards, and consumers
depend on stable, trusted schemas.

Punch line:
Schema enforcement blocks unexpected structure changes. Schema evolution
allows intentional structure changes under control.


## Q36. What is MERGE / upsert in Delta Lake, and why is it useful for data pipelines?

MERGE, also called upsert, is a Delta Lake operation that can update existing
records and insert new records in one controlled transaction.

It works by comparing an incoming source DataFrame or table against an existing
Delta target table using a match condition, usually a business key or primary
key. If a matching record exists, Delta can update it. If no matching record
exists, Delta can insert it.

MERGE is useful for CDC, incremental loads, and pipelines where only changed
records arrive after the first full load. Instead of rebuilding a large table
from scratch, the pipeline can apply only the new and changed records.

In production, the biggest caution is key quality and idempotency. The incoming
source should be deduplicated so there is only one intended change per match
key. If the source has duplicate updates for the same key, the merge can fail
or produce unclear logic. A common pattern is to keep the latest record per key
before merging.

MERGE is also useful because Delta’s transaction log commits the change
atomically, so the table is not left in a partial state.

Punch line:
MERGE lets Delta pipelines insert new records and update existing records by
key, which makes CDC and incremental loads safer and more efficient than full
reloads.

## Q37. What is CDC, and how does Delta Lake MERGE support incremental data pipelines?

CDC stands for Change Data Capture. It is a pattern for capturing inserts,
updates, and deletes from upstream source systems.

Delta Lake MERGE supports CDC-style pipelines by applying those changes to a
target Delta table using a match key. If the incoming record matches an
existing target record, Delta can update it. If it does not match, Delta can
insert it. Depending on the design, MERGE logic can also handle deletes or
soft-delete/expire records.

This is useful because the pipeline can process only the records that changed
instead of fully reloading a large table every time. That saves compute,
reduces runtime, and supports more efficient incremental processing.

In production, the incoming CDC batch must be prepared carefully. A common risk
is duplicate changes for the same key in the same batch. The source should be
deduplicated or reduced to the latest intended record per key before the MERGE
runs. This helps avoid multiple-match errors and keeps the pipeline
idempotent.

Punch line:
CDC captures upstream inserts, updates, and deletes. Delta MERGE applies those
changes by key so pipelines can run incrementally instead of doing full reloads.


## Q38. What does idempotency mean in a data pipeline, and why does it matter for CDC/MERGE jobs?

Idempotency means that running the same pipeline more than once with the same
input should produce the same final result.

This matters in production because jobs can fail, retry, or be restarted. If a
pipeline is not idempotent, a retry might insert duplicate rows, double-count
data, or leave the target table in an incorrect state.

For CDC and Delta Lake MERGE jobs, idempotency usually depends on a reliable
match key. Instead of blindly appending every incoming row, MERGE checks whether
a record already exists in the target table. If it exists, the job can update
it. If it does not exist, the job can insert it.

The incoming CDC batch also needs to be prepared carefully. If there are
multiple changes for the same key in one batch, the source should be
deduplicated or reduced to the latest intended record per key before running
MERGE. This helps avoid multiple-match errors and keeps reruns safer.

Punch line:
Idempotency means safe reruns: the same input should produce the same final
table state. For CDC/MERGE jobs, that depends on match keys, deduplication, and
careful retry-safe design.

## Q39. What is the difference between full load, incremental load, and CDC?

A full load reloads the entire dataset from the source into the target.

This is simple to reason about, but it can be expensive for large tables
because every run processes all records again.

An incremental load processes only new or changed records since the last
successful run. It is more efficient than a full load, but it needs a reliable
way to know what changed, such as timestamps, batch IDs, watermarks, or source
change markers.

CDC stands for Change Data Capture. It captures inserts, updates, and deletes
from source systems as change events. CDC is a more specific form of
incremental processing because it tracks the actual data changes.

Delta Lake MERGE is often used with incremental or CDC pipelines because it can
match incoming records to the target table by key, update existing rows, insert
new rows, and sometimes delete or expire rows depending on the design.

In production, incremental and CDC pipelines need reliable keys, source-state
tracking, deduplication, and idempotency so retries do not create duplicate or
incorrect results.

Punch line:
Full load reloads everything. Incremental load processes only what changed.
CDC captures insert, update, and delete events so MERGE can apply those changes
safely by key.

## Q40. What is the difference between append, overwrite, and merge/upsert in a Delta or Spark pipeline?

Append adds new rows to an existing table or dataset.

Overwrite replaces existing target data. Depending on how it is used, it may
replace an entire table or only a scoped partition. This must be handled very
carefully.

Merge, also called upsert, updates existing records and inserts new records
based on a matching key.

These three write strategies affect how fresh data interacts with existing
data in a Spark or Delta Lake pipeline.

Append is simple, but it can create duplicates if a job is rerun after a
failure, because it does not automatically check whether the rows already
exist.

Overwrite can be useful for rebuilding a full target or a specific partition,
but it can destroy data if scoped incorrectly, such as overwriting an entire
table when only one date partition should be replaced.

Merge/upsert is often safer for incremental and CDC pipelines because it uses a
match key. Existing records can be updated, and missing records can be inserted.
This helps support idempotent reruns, but it requires clean keys and source
deduplication before the merge.

Punch line:
Append adds rows but can duplicate data on rerun. Overwrite replaces data but
can destroy records if scoped wrong. Merge/upsert updates and inserts by key,
which is usually safer for CDC and incremental pipelines when keys and
deduplication are handled correctly.

## Q41. What is a partition in Spark/Delta, and why does partitioning matter for performance and safe writes?

A partition is a way of splitting data into smaller pieces so Spark can process
or store the data more efficiently.

In Spark execution, partitions are chunks of data that tasks can process in
parallel across executors.

In Delta or Parquet tables, partitioning often also means organizing data on
storage by columns such as date, region, or customer type. For example, a table
may be partitioned by `business_date` so Spark can read only the relevant date
folder instead of scanning the entire table.

Partitioning matters for performance because it supports parallel processing
and partition pruning. If a query filters on a partition column, Spark can skip
irrelevant partitions and read less data.

Partitioning also matters for safe writes. Instead of overwriting an entire
table, a pipeline may overwrite only a specific partition, such as one business
date. That is safer for incremental refreshes.

But partition design must be careful. Too many tiny partitions can create a
small-file problem and increase metadata overhead. High-cardinality columns
such as user ID or exact timestamp are usually poor partition choices.

Punch line:
Partitions split data for parallel processing and efficient reads. In Delta
tables, good partitioning can improve pruning and safer scoped overwrites, but
too many small partitions can hurt performance.


## Q42. What is the small-file problem in Spark/Delta, and why does it hurt performance?

The small-file problem happens when a dataset is stored as many tiny files
instead of fewer, larger, more efficient files.

This can happen because of over-partitioning, frequent small writes, streaming
micro-batches, or writing data in very small batches.

Small files hurt performance because each file has metadata that Spark must
list, track, plan, open, read, and close. When there are thousands or millions
of tiny files, Spark may spend too much time on file and task overhead instead
of actual data processing.

This can put pressure on the driver during planning and can create too many
small tasks during execution. Reads become slower, jobs become harder to plan,
and the cluster wastes compute on coordination overhead.

In Delta Lake, this is often handled through compaction. In Databricks, the
common command is `OPTIMIZE`, which combines many small files into fewer,
larger files. Good partition design also helps prevent the issue.

Punch line:
The small-file problem means too many tiny files create metadata overhead,
driver planning pressure, and too many tasks. Fix it with better partition
design, batching, and compaction such as Delta `OPTIMIZE`.


## Q43. What is Z-ordering in Delta Lake, and how is it different from partitioning?

Z-ordering is a Delta Lake optimization that clusters related values together
inside data files so Spark can skip more irrelevant files during reads.

It is different from partitioning. Partitioning physically separates data into
folders or partitions, often using broad columns like date. Z-ordering organizes
data within files to improve data skipping for commonly filtered columns like
customer_id, account_id, or region.

I would not use Z-ordering as a replacement for partitioning. A common pattern
is to partition by a broad column like date and Z-order by high-value filter
columns that would be too high-cardinality to partition on directly.

Punch line:
Partitioning narrows the search area.
Z-ordering makes the remaining files easier to skip.

Memory hook:
Partitioning helps Spark skip folders.
Z-ordering helps Spark skip files.
Use partitioning for broad columns like date, and Z-ordering for common
high-cardinality filter columns.

## Q44 What is the difference between data skipping, partition pruning, and Z-ordering?

Partition pruning skips data at the partition or folder level.

For example, if a Delta table is partitioned by `business_date` and the query
filters for one date, Spark can skip unrelated date partitions instead of
scanning the whole table.

Data skipping skips data at the file level.

Delta Lake can use file-level statistics, such as minimum and maximum values,
to decide whether a file could contain rows needed by the query. If the filter
value falls outside a file’s recorded range, Spark can skip reading that file.

Z-ordering is an optimization that makes data skipping more effective.

It clusters related values together inside data files. When related values are
stored close together, file-level min/max ranges become more useful, and Spark
can skip more irrelevant files during reads.

These optimizations work at different levels:

- Partition pruning skips partitions or folders.
- Data skipping skips individual files using file statistics.
- Z-ordering organizes data inside files to improve data skipping.

Punch line:
Partition pruning skips folders. Data skipping skips files. Z-ordering clusters
data so file-level skipping becomes more effective.

## Q45. What is the difference between OPTIMIZE and VACUUM in Delta Lake?

OPTIMIZE and VACUUM solve two different Delta Lake maintenance problems.

OPTIMIZE improves performance by compacting many small data files into fewer,
larger files. This helps reduce metadata overhead, driver planning pressure,
and too many tiny read tasks. In Databricks, OPTIMIZE can also be used with
ZORDER to cluster data for better data skipping.

VACUUM cleans up old data files that are no longer referenced by the current
Delta table snapshot. These files may exist because Delta keeps version history
for time travel, rollback, and recovery.

The key difference is:

OPTIMIZE reorganizes active data files to improve read performance.

VACUUM deletes old unreferenced files to reduce storage usage.

VACUUM must be used carefully because deleting old files can reduce or remove
the ability to time travel back to older table versions. If the retention
window is too short, you may lose rollback or audit options that the team still
needs.

Safe way to say it:
I would use OPTIMIZE when a Delta table has many small files and query
performance is suffering. I would use VACUUM only after confirming the
retention policy and making sure old versions are no longer needed for time
travel, audit, rollback, or recovery.

## Q46. What is the risk of running VACUUM too aggressively in Delta Lake?

VACUUM removes old unreferenced files that are no longer part of the current
Delta table snapshot.

That can save storage, but it must be used carefully because Delta Lake uses
older files and the transaction log to support time travel, rollback, audit,
and recovery.

If VACUUM is run with too short a retention period, it can delete files needed
to reconstruct older table versions. That can break time travel and reduce the
team’s ability to recover from a bad write.

It can also be risky if long-running queries are still reading older files. If
VACUUM removes files that an active query still needs, that query may fail.

In production, I would confirm the retention policy, audit requirements,
rollback needs, and active workload behavior before running VACUUM. I would not
force a very short retention period casually.

Punch line:
VACUUM cleans up old unreferenced files, but if it is run too aggressively it
can break time travel, reduce rollback/audit options, and potentially disrupt
active reads.

## Q47. What is the difference between logical delete, physical delete, and VACUUM in Delta Lake?

A logical delete, or soft delete, does not physically remove the row from the
table. Instead, the pipeline marks the row with a flag such as `is_deleted =
true`, `active_flag = false`, or an expiration date. The data still exists, but
normal business queries can filter it out.

A physical delete removes rows from the current Delta table snapshot using a
command such as `DELETE FROM`. Delta updates the transaction log and may rewrite
affected data files so the deleted rows are no longer part of the active table
version.

However, the old files may still remain in storage for Delta history and time
travel until they become eligible for cleanup.

VACUUM is the cleanup operation that permanently removes old unreferenced files
from storage after the retention period. It helps reduce storage cost, but it
must be used carefully because it can limit time travel, rollback, audit, and
recovery options.

Punch line:
Logical delete hides or expires rows. Physical delete removes rows from the
current Delta table snapshot. VACUUM permanently cleans up old unreferenced
files after retention.

## Q48. What is the difference between a managed table and an external table in Databricks or Spark SQL?

A managed table is a table where the platform or metastore manages the table’s
storage location and lifecycle.

An external table is a table whose data lives at a specified external path,
such as S3, ADLS, or another cloud storage location. The catalog stores the
metadata, but the data files are managed outside the table definition.

This difference matters for ownership, governance, and storage lifecycle.

For a managed table, the platform controls the table location. In Databricks
Unity Catalog, dropping a managed table removes the table metadata and the
underlying data is handled by Databricks-managed deletion behavior.

For an external table, dropping the table removes the table metadata from the
catalog, but the underlying data files remain in the external storage path.
Databricks documentation states that dropping an external table removes
metadata but does not delete the underlying data files. :contentReference[oaicite:0]{index=0}

A data engineer needs to know the difference before dropping tables, designing
storage ownership, or deciding who controls the data lifecycle.

Punch line:
Managed tables are managed by the platform, including storage lifecycle.
External tables point to data in an external path; dropping them usually removes
metadata only and leaves the data files in place.


## Q49. What is the difference between Unity Catalog, Hive Metastore, and AWS Glue Data Catalog?

Unity Catalog, Hive Metastore, and AWS Glue Data Catalog are all catalog or
metadata layers. They track table names, schemas, data locations, and related
metadata. They are not the same as storage. Storage systems such as S3, ADLS,
GCS, HDFS, or Delta/Parquet files hold the actual data files.

Hive Metastore is the classic Spark/Hive metadata store. It maps database and
table names to schemas and storage locations. It is common in older Hadoop,
Hive, and Spark environments.

AWS Glue Data Catalog is an AWS-managed metadata catalog. It stores metadata
about datasets and is commonly used with AWS services such as Glue, Athena,
and EMR. AWS describes it as a central metadata repository for structural and
operational metadata about data sets. :contentReference[oaicite:0]{index=0}

Unity Catalog is Databricks’ unified governance/catalog layer. It manages
metadata and governance for data and AI assets in Databricks, including access
control, auditing, lineage, and discovery across workspaces. Databricks
describes Unity Catalog as the unified governance layer built into Databricks,
with access control, lineage, activity logging, and auditing capabilities.
:contentReference[oaicite:1]{index=1}

Punch line:
Hive Metastore is the classic Spark/Hive catalog. AWS Glue Data Catalog is the
AWS-managed catalog. Unity Catalog is the Databricks governance catalog with
stronger centralized security, lineage, auditing, and workspace-level
governance.

## Q50. What is the difference between Bronze, Silver, and Gold data quality responsibilities in a medallion architecture?

Medallion architecture organizes data into progressive quality layers:
Bronze, Silver, and Gold. As data moves forward, quality checks and structure
usually become stricter.

Bronze is the raw or lightly processed landing layer. Its main responsibility
is to preserve source data close to how it arrived, often with ingestion
metadata such as load timestamp, source file, or batch ID. The goal is
traceability and replayability.

Silver is the cleaned and validated layer. This is where data is standardized,
deduplicated, type-corrected, joined, conformed, and checked against stronger
quality rules. Silver is often where data becomes reliable enough for shared
enterprise use.

Gold is the business-ready layer. This is where clean Silver data is curated,
aggregated, modeled, or optimized for reporting, dashboards, analytics,
machine learning, or downstream business products.

Delta Lake supports this pattern by giving each layer transaction history,
schema enforcement, time travel, and rollback/reprocessing options. If bad
data reaches Silver or Gold, the team can trace what changed and reprocess
from a known good layer.

Punch line:
Bronze preserves source data, Silver cleans and validates it, and Gold turns
trusted data into business-ready products.

## Q51. What is the difference between data quality checks in Bronze, Silver, and Gold?

Data quality gets stricter as data moves from Bronze to Silver to Gold.

Bronze checks focus on ingestion completeness and traceability. At this layer,
I want to confirm that source files or records arrived, ingestion metadata was
captured, and the raw data can be audited or replayed if needed.

Silver checks focus on structural and relational quality. This is where I
validate schemas, data types, null behavior, duplicates, business keys, and
standardized values. Bad or suspicious records may be routed to a quarantine
or exception table instead of being trusted downstream.

Gold checks focus on business correctness. This includes validating business
rules, totals, aggregates, reconciliations, dashboard/report numbers, and
expected trends. Gold data should be ready for reporting, analytics, and
business consumption.

Across all layers, I would compare row counts and reconciliation metrics so I
can detect unexpected data loss, duplication, or drop-offs between Bronze,
Silver, and Gold.

Punch line:
Bronze checks that data arrived and is traceable. Silver checks that data is
clean and valid. Gold checks that business outputs are accurate and trusted.

## Q52. What is the difference between a quarantine table, an error table, and simply dropping bad records?

A quarantine table preserves rejected records so they can be audited, debugged,
repaired, or reprocessed later.

An error table records why records failed validation. It may include the failed
rule, bad column, error message, source file, batch ID, timestamp, and other
diagnostic metadata.

In some systems, the quarantine table and error table are separate. In other
systems, one exception table may store both the rejected row and the error
reason.

Simply dropping bad records removes them from the pipeline without preserving
evidence. That is risky in production because the team loses visibility into
upstream data issues and cannot easily audit, explain, or reprocess the
rejected records.

This is especially important in the Silver layer, where data is cleaned and
validated before becoming trusted downstream.

Punch line:
Quarantine keeps the rejected data. Error tables explain why it failed.
Dropping bad records silently loses evidence and should be avoided in
production.

## Q53. What is the difference between batch processing, streaming, and micro-batch processing in Spark?

Batch processing handles bounded data. It processes a fixed dataset on a
schedule, such as hourly, daily, or nightly. Batch jobs usually optimize for
throughput and reliability, but the data is only as fresh as the last run.

Streaming processing handles continuously arriving data. The goal is to process
events as they arrive or shortly after they arrive, which supports lower-latency
use cases.

Micro-batch processing is a middle ground. It treats a continuous stream as a
series of small repeated batches, such as every few seconds. Spark Structured
Streaming commonly uses this model, which lets developers write streaming logic
with a DataFrame-style API while Spark handles repeated execution, state, and
checkpointing.

The tradeoff is latency versus reliability and operational complexity. Batch is
simpler and high-throughput. Streaming is lower-latency but requires stronger
monitoring, checkpointing, and failure handling. Micro-batch gives a practical
balance for many production data pipelines.

Punch line:
Batch processes fixed data on a schedule. Streaming processes continuously
arriving data. Micro-batch processes a stream as many small repeated batches,
balancing latency, reliability, and Spark-style processing.

## Q54. What is a checkpoint in Spark Structured Streaming, and why is it important?

A checkpoint is a reliable storage location where Spark Structured Streaming
saves progress, metadata, and state for a running streaming query.

It tracks what data has already been processed, such as source file progress or
Kafka offsets. For stateful operations, it can also store state needed for
aggregations, windows, watermarks, and other logic that must remember data
across micro-batches.

Checkpoints are important for failure recovery. If the streaming job stops,
crashes, or restarts, Spark can use the checkpoint to resume from the last known
progress instead of starting from scratch.

The checkpoint location should be durable storage, such as S3, ADLS, HDFS, or
another reliable path — not temporary local disk.

In production, I should not casually delete checkpoint directories. Deleting a
checkpoint can reset the stream’s memory and may cause reprocessing, skipped
data, duplicate output, or broken state depending on the source, sink, and job
logic.

Punch line:
A checkpoint records streaming progress and state so Spark can recover safely
after failure instead of losing its place.

## Q55. What is a watermark in Spark Structured Streaming, and why is it useful?

A watermark in Spark Structured Streaming tells Spark how long to wait for
late-arriving data based on event time.

This is important because streaming data does not always arrive in perfect
order. Events can be delayed because of network issues, source-system delays,
device outages, or processing lag.

Watermarks are especially useful for windowed aggregations. For example, if I
am counting transactions in 10-minute windows, Spark needs to know how long to
keep old windows open for late records.

The watermark acts as a moving cutoff. Once Spark believes a window is older
than the allowed lateness, it can finalize that window and clean up the state
it was holding in memory or checkpoint storage.

This prevents unbounded state growth. Without a watermark, Spark might need to
keep old windows open forever in case very late data arrives.

There is a tradeoff. If the watermark is too short, valid late records may be
dropped. If it is too long, Spark keeps more state for longer, which increases
memory and storage pressure.

Punch line:
A watermark tells Spark how long to wait for late event-time data before
finalizing old windows and cleaning up state.

## Q56. What is the difference between event time and processing time in streaming?

Event time is when the event actually happened.

Processing time is when Spark receives or processes the event.

For example, a transaction may happen at 10:00 AM, but because of network delay
or source-system lag, Spark may not process it until 10:15 AM. In that case,
10:00 AM is the event time, and 10:15 AM is the processing time.

This difference matters for correct analytics. If I am calculating 10-minute
transaction windows, I usually want the event to count in the window when it
actually happened, not when Spark happened to receive it.

Watermarks use event time to decide how long Spark should wait for late-arriving
records before finalizing old windows and cleaning up state.

Punch line:
Event time is when the event happened. Processing time is when Spark processed
it. For accurate windowed analytics, event time is usually the important one.

## Q57. What is the difference between stateful and stateless streaming operations?

A stateless streaming operation processes each record or micro-batch
independently. It does not need to remember prior records.

Examples of stateless operations include `select()`, `filter()`, simple
column transformations, and adding calculated columns.

A stateful streaming operation must remember information across records,
micro-batches, or time windows.

Examples include windowed counts, streaming deduplication, rolling
aggregations, and joins that require keeping state over time.

Stateful operations need stronger production controls because Spark must store
and recover state. That means checkpointing is required for failure recovery,
and watermarks are often needed to clean up old state so memory and checkpoint
storage do not grow forever.

Punch line:
Stateless operations do not need memory of the past. Stateful operations must
remember prior data across time, so they require checkpointing and often
watermarks.

## Q58. What is the difference between Structured Streaming and old-style Spark Streaming?

Old-style Spark Streaming used DStreams, or Discretized Streams. DStreams were
built on lower-level RDD concepts and treated streaming data as a sequence of
small RDD batches.

Structured Streaming is the modern Spark streaming API. It is built on the
DataFrame and Spark SQL engine. It treats a stream like an unbounded table where
new rows continuously arrive over time.

This makes Structured Streaming easier to use with the same patterns used in
batch PySpark: select, filter, groupBy, joins, aggregations, and writes. It also
integrates better with Spark SQL, Catalyst optimization, and modern lakehouse
formats such as Delta Lake.

Structured Streaming commonly uses micro-batch execution, where Spark processes
the stream as many small repeated batches. This gives a practical balance
between batch-style reliability and near-real-time processing.

Punch line:
Old Spark Streaming used DStreams and lower-level RDD-style processing.
Structured Streaming uses the modern DataFrame/Spark SQL model and treats
streaming data like an unbounded table.

## Q59. What is the difference between a streaming source, streaming sink, and checkpoint location?

A streaming source defines where the input data originates, a streaming sink specifies where the processed results are written, and a checkpoint location dictates where Spark securely saves its operational progress and state.

These three components form the core architecture of any Spark Structured Streaming pipeline, and each must be configured correctly to guarantee data integrity:

Streaming Source: This is the ingestion origin where streaming data comes from. Common source examples include messaging queues like Kafka, cloud file directories monitoring new arrivals, or an upstream Delta table tracking incremental appends.

Streaming Sink: This is the output destination where streaming output is written after transformations are applied. Examples include writing the transformed data out to a target Delta table, a database connector, Kafka, or a cloud file path.

Checkpoint Location: This is a dedicated directory on durable storage where Spark tracks processing offsets, metadata, and state. If the stream stops or crashes, Spark uses this directory to recover its exact position, preventing duplicate processing or data loss.

Because it serves as the pipeline's memory, the checkpoint must be durable storage (such as AWS S3 or ADLS) rather than local cluster memory. As a critical production rule, you must not mix checkpoint folders between different queries. Each streaming query needs its own isolated checkpoint directory; sharing or overlapping them will cause metadata conflicts, corrupt the state tracking, and crash your pipelines.

Punch line:
The source is your data intake, the sink is your data output, and the checkpoint location is the durable storage folder that tracks the stream's progress to guarantee fault tolerance.


## Q70-Q73 Bridge Back to Foundation QA

These questions overlap the canonical Course 11 foundation QA and are intentionally summarized here:
- Q70 cluster targeting/submission ownership
- Q71 Python/C speed vs distributed Spark value
- Q72 Python/SQL analytics bridge to distributed Spark
- Q73 production architecture layer summary

Canonical full answers:
`QA_01_1000ft_pyspark_opening.md` Q70-Q73

Expanded production architecture detail remains in this file under Q21 onward.
