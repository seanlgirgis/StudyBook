# Interview Questions — Data Lakehouse

> Topics covered: object storage · Delta Lake ACID · Iceberg table formats · time travel · compaction and optimization
> Levels: Starter | Mid | Senior | Architect

---

## Topic 1 — Object Storage

*Reference file: `c001_object_storage_demo.py`*

---

**Q1: What is object storage and how does it differ from a traditional file system?**
What a good answer covers:
- Object storage (S3, GCS, ADLS) stores data as flat objects identified by a key (path-like string), with no true directory hierarchy — the slash-delimited prefix is a naming convention, not a real filesystem tree
- There is no in-place update: objects are immutable; modifying a file means writing a new object and optionally deleting the old one
- Object storage scales horizontally to exabytes and is orders of magnitude cheaper than block storage, making it the preferred foundation for data lakehouses
Why this is asked: Understanding the constraints of object storage (no in-place updates, eventual consistency) is foundational to understanding why lakehouses need transaction logs.

**Q2: Why does object storage's immutability create challenges for ACID operations, and what mechanism do lakehouses use to address this?**
What a good answer covers:
- Because objects cannot be updated in place, you cannot atomically modify a row the way a relational database can update a page in a B-tree
- Lakehouses address this with a transaction log (Delta Lake's `_delta_log`, Iceberg's metadata files) that records which objects belong to each logical table version
- A "write" creates new Parquet files and a new transaction log entry; the old files remain until they are vacuumed, enabling readers to see a consistent snapshot
Why this is asked: The transaction log is the core innovation of lakehouse formats; this question checks whether the candidate understands why it exists.

**Q3: What is a partition in object storage and how does it improve query performance?**
What a good answer covers:
- Partitioning organizes objects under a key prefix that encodes a column value (e.g., `s3://bucket/orders/date=2026-03-27/part-000.parquet`)
- Query engines use the partition prefix to prune files: a query for `date = '2026-03-27'` only reads files under that prefix, skipping all other dates
- Over-partitioning (too many small partitions) creates a "small files problem" where metadata overhead dominates query time; under-partitioning (one huge partition) eliminates pruning benefits
Why this is asked: Partitioning is the most important query optimization lever in object-storage-based lakehouses.

**Q4: What is the small files problem in object storage and why does it degrade performance?**
What a good answer covers:
- Many small Parquet files (under 128MB) cause high per-file overhead: each file requires a separate HTTP request to open, read the footer, and fetch row groups
- Query planners must list and filter thousands of small files even for narrow queries, increasing plan time and network round trips
- Small files accumulate when streaming pipelines write micro-batches or when partitions are over-granular (e.g., partitioned by minute instead of hour)
- Compaction (Topic 5) is the standard remedy
Why this is asked: The small files problem is one of the most commonly encountered production performance issues in lakehouses.

---

**Q5: An object storage bucket contains 3 years of Parquet files written by a legacy pipeline without a transaction log. How would you migrate this to a Delta Lake table without downtime?**
What a good answer covers:
- Use `CONVERT TO DELTA` (in Delta Lake) or register the existing files as an external table with schema inference, then convert in place
- The conversion registers all existing Parquet files in a new `_delta_log` as version 0 of the table; no data is moved or rewritten
- Validate the converted table by comparing row counts and key aggregates against the legacy pipeline's output before switching consumer queries
- After conversion, new writes use the Delta protocol; old files remain as-is until vacuumed by the compaction process
Why this is asked: Brownfield lakehouse migrations are common; candidates must know the conversion path.

**Q6: How do you control costs when storing terabytes of Parquet data in object storage, given that both storage and API request costs scale with usage?**
What a good answer covers:
- Use lifecycle policies to transition old partitions to cheaper storage tiers (S3 Glacier, GCS Nearline) after a defined retention window
- Compaction reduces file count, lowering per-request API costs on read-heavy workloads
- Partition pruning reduces the number of files read per query, cutting both compute and egress costs
- Vacuum old Delta Lake snapshot files (files no longer referenced by any transaction log entry) to reclaim storage; balance retention window against time travel requirements
Why this is asked: Cost management at scale is an architect-level operational concern candidates in senior roles are expected to own.

**Q7: A query reads a single column from a 200-column Parquet file. How does the columnar storage format interact with object storage to minimize data read?**
What a good answer covers:
- Parquet stores data column by column in row groups; the file footer contains column chunk offsets so readers can issue a range request for only the target column's bytes
- Object storage supports HTTP range requests (byte-range GET), so the query engine fetches only the column chunk bytes needed, not the entire file
- Column-level statistics (min, max, null count) in the footer allow the reader to skip entire row groups that cannot satisfy the predicate, further reducing bytes read
Why this is asked: Columnar pushdown is the primary reason Parquet + object storage outperforms row-oriented formats for analytics.

**Q8: Two pipelines write Parquet files to the same object storage prefix concurrently without a transaction log. What consistency problems can occur?**
What a good answer covers:
- Both pipelines may write files with the same name, causing one to silently overwrite the other (last-writer-wins semantics in most object stores)
- A reader listing the prefix mid-write may see files from both pipelines in an inconsistent intermediate state
- Object stores are eventually consistent for LIST operations in some configurations (older S3 regions); a file written seconds ago may not appear in a LIST immediately
- This is exactly why transaction logs are necessary: Delta Lake and Iceberg coordinate concurrent writers through the transaction log, preventing these races
Why this is asked: Motivates the transaction log by describing what happens without it.

---

**Q9: Design an object storage layout for a multi-tenant data lakehouse where 20 tenant organizations share the same cloud account but must have complete data isolation.**
What a good answer covers:
- Use a top-level prefix per tenant: `s3://lakehouse/tenant=acme/`, `s3://lakehouse/tenant=globex/`; assign each tenant an IAM role or service account with access only to their prefix
- Alternatively, use separate buckets per tenant for stronger isolation and to enable per-tenant lifecycle policies, encryption keys, and access logging
- Delta Lake tables within each tenant prefix are governed by the tenant's own transaction log; cross-tenant queries are prevented at the IAM layer
- Cost allocation uses per-prefix or per-bucket cost reporting tags; tenants can be charged back based on storage and request usage
Why this is asked: Multi-tenant storage design is an architect-level platform concern.

**Q10: Explain how object storage's eventual consistency model has changed across AWS S3 over time and what implications this has for lakehouse pipeline design today.**
What a good answer covers:
- Prior to December 2020, S3 had eventual consistency for overwrite PUTs and DELETEs; a file written and immediately listed might not appear in the LIST result
- Since December 2020, S3 provides strong read-after-write consistency for all operations, eliminating the need for consistency workarounds in most pipelines
- GCS and ADLS also provide strong consistency; the lakehouse ecosystem largely assumes strong consistency in their transaction log protocols
- Legacy pipelines may still contain `sleep` delays or retry loops designed for the old eventual consistency model; these can be removed but should be tested first
Why this is asked: Tests awareness of a historically important operational constraint that has changed, and whether candidates understand the current state.

**Q11: A data lakehouse table's Parquet files are stored unencrypted. Describe an encryption strategy that protects data at rest without impacting query performance.**
What a good answer covers:
- Use server-side encryption (SSE) with customer-managed keys (SSE-KMS): the object store handles encryption/decryption transparently at the API level, with no change to the query engine
- For column-level encryption of sensitive fields, Parquet native encryption encrypts individual column chunks with per-column keys; query engines must be configured with the key provider
- Key rotation policies and access logging on the KMS key provide auditable control over who can decrypt the data
- Performance impact of SSE-KMS is minimal for large sequential reads; column-level encryption has a measurable CPU overhead on the decrypting client that must be benchmarked
Why this is asked: Data security at rest is an architect-level concern that lakehouse practitioners must address.

---

**Q12: You are designing a global data lakehouse for a company with regions in the US, EU, and APAC, each subject to different data residency regulations. How do you architect object storage to comply with data sovereignty requirements while enabling cross-region analytics?**
What a good answer covers:
- Store data in region-specific buckets that never replicate regulated data outside the jurisdiction (EU data stays in an EU bucket, governed by GDPR)
- For cross-region analytics, publish anonymized or aggregated views that do not contain regulated PII; these can replicate globally
- Use a federated query layer (Trino/Presto federation, BigQuery Omni, or Athena cross-account queries) that queries in-region data without moving it
- Data contracts specify the residency region for each table; the pipeline routing layer enforces that regulated data is never written to an out-of-jurisdiction bucket
- Connect to data contracts and schema evolution: cross-region view schemas must be versioned and governed centrally even though the underlying data is region-isolated
Why this is asked: Data sovereignty is a dominant architectural constraint for global enterprises; tests whether the candidate can design for regulatory reality.

**Q13: A catastrophic misconfiguration causes a pipeline to delete 6 months of Parquet files from object storage. The Delta Lake transaction log still exists. Design the recovery procedure and the controls to prevent recurrence.**
What a good answer covers:
- If object versioning is enabled on the bucket, restore the deleted objects from their prior versions using the S3/GCS versioning API; the Delta transaction log already references the correct file names
- If versioning is not enabled, attempt recovery from S3 Glacier or a cross-region replication copy if one exists; this is why replication is non-optional for production data
- After file restoration, validate the Delta transaction log's file references against the restored objects; a `DESCRIBE HISTORY` and `CHECK CONSTRAINTS` run confirms table integrity
- Prevention: enable object versioning and MFA Delete on all production buckets; implement IAM deny policies that require an approval workflow for bulk deletes; run regular recovery drills
- Connect to the ACID topic (`c002_delta_lake_acid_demo.py`): the transaction log survives the file deletion and is the recovery anchor; without it, restoration would be guesswork
Why this is asked: Disaster recovery design and post-incident prevention are architect-level operational responsibilities.

---

## Topic 2 — Delta Lake ACID

*Reference file: `c002_delta_lake_acid_demo.py`*

---

**Q1: What does ACID stand for and why does it matter for a data lakehouse?**
What a good answer covers:
- Atomicity: a write either fully succeeds or fully fails; no partial writes are visible to readers
- Consistency: the table moves from one valid state to another; every commit produces a well-formed snapshot
- Isolation: concurrent readers and writers see consistent snapshots and do not interfere with each other
- Durability: once committed, data survives failures
- Without ACID, concurrent writers in `c002_delta_lake_acid_demo.py` could produce a table state that mixes partial writes from two transactions
Why this is asked: ACID is the foundational guarantee that lakehouses provide on top of object storage; candidates must understand each property and its practical meaning.

**Q2: How does Delta Lake achieve atomicity on object storage, which does not support atomic multi-object writes?**
What a good answer covers:
- Delta Lake writes new Parquet files to the object storage prefix and then atomically commits a new JSON entry to the `_delta_log` directory
- The transaction log entry lists all files added and removed in the transaction; the commit of the log entry is the atomic moment
- Readers look only at committed log entries; files that have been written but not yet committed are invisible to readers, as demonstrated in `c002_delta_lake_acid_demo.py`
- If the writer crashes after writing data files but before committing the log entry, the data files are orphaned and later cleaned up by `VACUUM`; the table is unaffected
Why this is asked: Understanding the commit protocol is essential for debugging race conditions and recovery scenarios.

**Q3: In `c002_delta_lake_acid_demo.py`, a reader takes a snapshot before Writer B commits. Does the reader see Writer B's files? Why or why not?**
What a good answer covers:
- No. The reader's snapshot is pinned to the transaction log version at the time `_snapshot()` was called; it lists only the files committed up to that version
- Writer B's commit adds a new log version after the reader's snapshot was taken; the reader's snapshot is immutable and does not reflect subsequent commits
- This is snapshot isolation: each reader sees a consistent point-in-time view regardless of concurrent writes, which is the I in ACID
Why this is asked: Directly tests reading and reasoning about the demo code's snapshot behavior.

**Q4: What is optimistic concurrency control and how does Delta Lake use it?**
What a good answer covers:
- Optimistic concurrency assumes that conflicts between concurrent writers are rare; each writer proceeds without locking, then checks for conflicts at commit time
- Delta Lake implements this by having each writer read the latest transaction log version, perform its write, then attempt to append a new log entry; if another writer has committed in the meantime, the commit is retried or rejected based on conflict analysis
- Conflict detection checks whether the concurrent transactions modified overlapping data (same partition, same file); non-overlapping transactions can both commit
Why this is asked: Distinguishes optimistic from pessimistic (locking) concurrency, which is the traditional RDBMS approach.

---

**Q5: A Spark job writes 10 partitions of data to a Delta table concurrently from 10 executors. How does Delta Lake ensure this multi-part write is atomic?**
What a good answer covers:
- Each Spark executor writes its Parquet files independently to the table prefix; the files exist in object storage but are not yet part of any committed transaction
- The Spark driver collects the list of all written files and issues a single transaction log commit entry that lists all 10 file additions atomically
- Readers cannot see any of the 10 files until the single commit is written; the entire 10-partition write is atomic from the reader's perspective
- If the driver crashes after writing some but not all files, the uncommitted files are orphans and do not affect table state
Why this is asked: Multi-executor atomic writes are the most common Spark + Delta Lake production scenario.

**Q6: How does Delta Lake handle a write conflict when two concurrent jobs both try to append data to the same partition?**
What a good answer covers:
- Delta Lake reads both jobs' conflict analysis: if both jobs are pure appends (INSERT) to the same partition, they do not conflict because neither modifies existing files
- If one job is an UPDATE or DELETE that affects files the other job is also reading, Delta Lake detects the conflict and retries the later-committing job by re-reading the updated snapshot and re-applying its transformation
- Maximum retry attempts are configurable; exceeding retries raises a `ConcurrentModificationException` that the pipeline must handle
Why this is asked: Concurrent write conflict handling is a mid/senior production concern for shared Delta tables.

**Q7: Explain the difference between Delta Lake's `MERGE` and `OVERWRITE` operations and when you would choose each.**
What a good answer covers:
- `MERGE` (upsert): matches rows by a key column; updates existing matched rows, inserts new unmatched rows, optionally deletes matched rows with a condition — used for incremental CDC or SCD Type 2
- `OVERWRITE`: replaces all data in the table (or a partition) with the new data; used for full reloads or partition replacement
- `OVERWRITE` is simpler and faster but destroys existing data in scope; `MERGE` is more complex but preserves non-matching rows
- In `c002_delta_lake_acid_demo.py`, the commit pattern is an additive append; a `MERGE` would be needed for upsert semantics
Why this is asked: Candidates must know which write operation matches each data loading pattern.

**Q8: A Delta Lake table's transaction log has grown to 50,000 entries over two years. What are the performance consequences and how do you address them?**
What a good answer covers:
- Reading the transaction log requires listing and parsing thousands of JSON files; plan time for queries increases as log size grows
- Delta Lake automatically creates checkpoint files (Parquet snapshots of the log) every 10 commits by default; queries start from the latest checkpoint rather than replaying the full log history
- `OPTIMIZE` and `VACUUM` commands also trigger checkpoint creation
- For very large logs, increase checkpoint frequency or run `DELTA TABLE CHECKPOINT()` manually; ensure the Spark driver has sufficient memory to load the checkpoint
Why this is asked: Transaction log management is a production operational concern that senior engineers must know.

---

**Q9: A financial pipeline requires that a batch of 50,000 order updates either all succeed or all fail, with no intermediate state visible to concurrent readers. Design the write protocol using Delta Lake ACID guarantees.**
What a good answer covers:
- Write all 50,000 updated Parquet files as a single Delta transaction; the commit log entry lists all file additions and deletions atomically
- While the write is in progress, concurrent readers see the previous committed version; the new version becomes visible only after the single commit log entry is written
- If the write fails mid-way (executor crash), uncommitted files are orphaned and cleaned by VACUUM; the table remains at the previous version — full atomicity is preserved
- Add a post-commit validation step that reads the committed version and asserts row counts and key aggregates before notifying downstream consumers
Why this is asked: Applies the ACID guarantee to a concrete financial use case, testing whether the candidate can map the abstract property to an implementation plan.

**Q10: Delta Lake's ACID guarantees apply within a single table. How do you achieve cross-table transactional consistency when a pipeline must update both `fact_orders` and `dim_customers` atomically?**
What a good answer covers:
- Delta Lake does not provide native cross-table transactions (as of current versions); each table has its own transaction log and commit boundary
- Workarounds: use a two-phase commit pattern (write to both tables, then write a "commit marker" record that consumers check before reading) — this is complex and error-prone
- Better: design the pipeline so that the two tables can be updated sequentially with idempotent logic; if the second update fails, re-running from the beginning is safe
- Alternatively, use a single Delta table with a denormalized schema that combines fact and dimension data, eliminating the cross-table problem
- Connect to streaming: Apache Iceberg's cross-table transaction support (via catalog-level commits) is emerging as a solution for multi-table atomicity
Why this is asked: Cross-table transactions are a known gap in current lakehouse ACID support; senior candidates must know the workarounds.

**Q11: A data engineer suggests disabling Delta Lake's transaction log for a high-throughput write path to improve write performance. Evaluate this proposal.**
What a good answer covers:
- Disabling the transaction log removes ACID guarantees entirely: concurrent writers will produce file-level races, and readers will see inconsistent intermediate states
- The performance cost of the transaction log is primarily in the commit step (one small JSON write per transaction), which is negligible compared to the cost of writing Parquet files
- If write performance is the actual bottleneck, address it by tuning partition size, increasing Spark parallelism, or using auto-optimize features — not by removing ACID
- The proposal trades correctness for performance, which is acceptable only in append-only, single-writer scenarios with no concurrent readers, and even then is rarely necessary
Why this is asked: Tests critical evaluation of a plausible but incorrect optimization proposal.

---

**Q12: Design a lakehouse write protocol for a real-time fraud detection system that must write flagged transactions to a Delta table within 500ms of detection, while also ensuring that downstream risk analysts always see a consistent view of the table.**
What a good answer covers:
- Use Spark Structured Streaming with micro-batch intervals of 100–200ms; each micro-batch writes a small Parquet file and commits a transaction log entry within the 500ms window
- Risk analysts query the table using snapshot reads (consistent view at a specific log version); their queries are not affected by the concurrent streaming writer's micro-batches
- Compaction must run asynchronously (not blocking the streaming path) to merge small files without holding a write lock during the compaction commit
- Connect to the small files problem (Topic 1) and compaction (Topic 5): a streaming writer with 200ms micro-batches generates ~18,000 small files per hour without compaction
- The ACID guarantee ensures analysts see either the pre-write or post-write state, never a torn write, even at sub-second commit frequency
Why this is asked: Real-time ACID writing at sub-second latency is an architect-level design problem that spans streaming, ACID, and compaction topics.

**Q13: Describe how Delta Lake's ACID model would need to evolve to support multi-cloud, multi-region writes where the same table is written by pipelines in two different cloud regions simultaneously.**
What a good answer covers:
- The current Delta Lake transaction log is a single-region, single-bucket construct; two regional writers cannot atomically commit to a shared log without a distributed consensus protocol
- A multi-region solution requires a globally consistent metadata store (e.g., DynamoDB Global Tables, Spanner) to coordinate transaction log commits across regions
- Alternatively, use a hub-and-spoke model: each region writes to its own regional Delta table; a global aggregation pipeline merges regional tables into a single global table on a defined schedule
- Apache Iceberg's pluggable catalog (Nessie, Hive Metastore) provides a path to multi-region coordination through catalog-level versioning
- Eventual consistency across regions is the practical trade-off; "last writer wins" with conflict detection based on row-level version vectors is one proposed resolution strategy
Why this is asked: Multi-region distributed ACID is a frontier problem in lakehouse architecture; architects must understand both current limitations and emerging solutions.

---

## Topic 3 — Iceberg Table Formats

*Reference file: `c003_iceberg_table_format_demo.py`*

---

**Q1: What is Apache Iceberg and how does it differ from raw Parquet files on object storage?**
What a good answer covers:
- Iceberg is an open table format that adds a metadata layer on top of Parquet (or ORC/Avro) files in object storage, providing table semantics: schema, partitioning, snapshots, and ACID commits
- Raw Parquet files have no awareness of each other; Iceberg's metadata files track which Parquet files belong to each table version
- Iceberg supports hidden partitioning, schema evolution, and time travel — none of which are possible with raw Parquet files alone
Why this is asked: Establishes the foundational distinction between a file format and a table format.

**Q2: What is the Iceberg metadata hierarchy and how does it track table versions?**
What a good answer covers:
- Iceberg maintains three layers: the catalog (points to the current metadata file), the metadata file (describes the current table schema and snapshot list), and manifest lists/manifest files (list which data files belong to each snapshot)
- A new write creates new manifest files and a new metadata file; the catalog is updated atomically to point to the new metadata file — this is the commit point
- Readers follow the chain: catalog → metadata file → manifest list → manifest files → data files, using the snapshot version they need
Why this is asked: Understanding the metadata hierarchy is necessary to reason about Iceberg's ACID and time travel behavior.

**Q3: What is hidden partitioning in Iceberg and why is it an improvement over Hive-style partitioning?**
What a good answer covers:
- Hive-style partitioning requires the query to explicitly filter on the partition column name (e.g., `WHERE date_partition = '2026-03-27'`); if the user queries by `event_time`, they get a full scan even if the data is partitioned by date
- Iceberg's hidden partitioning applies a partition transform (e.g., `days(event_time)`) internally; queries on `event_time` automatically benefit from partition pruning without requiring a separate partition column
- This decouples the physical partition layout from the logical table schema, allowing partition strategies to change without breaking existing queries
Why this is asked: Hidden partitioning is one of Iceberg's most significant practical improvements over Hive; candidates must understand why it exists.

**Q4: How does Iceberg compare to Delta Lake for schema evolution support?**
What a good answer covers:
- Both support adding and dropping columns, renaming columns, and widening types; the mechanisms differ in implementation details
- Iceberg tracks schema evolution using schema IDs in the metadata file; historical snapshots reference the schema ID in effect at the time of the write, so old data files are always read with the correct schema
- Delta Lake tracks schema changes in the transaction log; both formats handle backward-compatible changes transparently
- Iceberg's schema evolution is considered more rigorous for column renaming (uses column IDs, not names, as the stable identifier) which prevents data corruption when columns are renamed
Why this is asked: Candidates working in multi-engine environments must understand where the formats differ.

---

**Q5: You need to choose between Delta Lake and Apache Iceberg for a new lakehouse project. The team uses Spark for ETL, Trino for SQL analytics, and Flink for streaming. Which format do you recommend and why?**
What a good answer covers:
- Iceberg has broader multi-engine support: Trino, Flink, Spark, Hive, Impala, and Snowflake External Tables all natively support Iceberg
- Delta Lake has excellent Spark support and strong Databricks integration; Trino and Flink support is available but historically lagged Spark
- If multi-engine access without a single vendor's ecosystem is a requirement, Iceberg is the safer choice
- Consider the team's existing tooling: if the team already uses Databricks heavily, Delta Lake's tighter integration may outweigh Iceberg's broader compatibility
Why this is asked: Format selection is a real architectural decision; candidates must weigh trade-offs, not just recite feature lists.

**Q6: How does Iceberg handle concurrent writes from Spark and Flink simultaneously?**
What a good answer covers:
- Iceberg uses optimistic concurrency control at the catalog level; each writer reads the current metadata pointer, performs its write, and attempts to atomically update the catalog pointer to a new metadata file
- If two writers commit simultaneously, one succeeds and the other's commit is rejected (catalog pointer has changed); the failing writer retries using the updated metadata
- The catalog must support atomic compare-and-swap (CAS) operations; REST catalog, Nessie, Hive Metastore with DynamoDB locking, and AWS Glue all provide this
Why this is asked: Multi-engine concurrency requires understanding the catalog's role in Iceberg's commit protocol.

**Q7: What is partition evolution in Iceberg and why is it valuable?**
What a good answer covers:
- Partition evolution allows changing the partition strategy for new writes without rewriting historical data: old data remains in the old partition layout, new data uses the new layout
- Example: a table originally partitioned by month can evolve to daily partitioning for new data; Iceberg's metadata tracks both partition specs and applies the correct pruning for each
- This is impossible with Hive-style partitioning, which requires a full table rewrite to change the partition column
- Reduces migration cost dramatically: a partition strategy change that would require days of reprocessing with Hive takes seconds with Iceberg
Why this is asked: Partition evolution is a distinctive Iceberg capability with major operational implications.

**Q8: A team migrates from a Hive-partitioned table to Iceberg. They have 5 years of historical data in Hive partition format. What is the migration path?**
What a good answer covers:
- Use Iceberg's `ADD FILES` procedure or `REGISTER TABLE` to register existing Hive partition files as an Iceberg snapshot without rewriting data
- Generate Iceberg manifest files from the existing Hive partition metadata; the data files themselves do not move
- Validate the Iceberg table's row counts and aggregates against the Hive table before switching consumer queries
- After migration, new writes use the Iceberg protocol; historical data is read through Iceberg's metadata layer pointing to the original Hive partition files
Why this is asked: Migration from Hive to Iceberg is a common production task; candidates must know the in-place conversion path.

---

**Q9: Design an Iceberg catalog strategy for an organization that uses Spark on AWS EMR, Trino on a separate cluster, and Flink on a third cluster, all sharing the same Iceberg tables.**
What a good answer covers:
- Use a shared REST catalog (e.g., Tabular, AWS Glue, or a self-hosted Iceberg REST catalog) that all three engines connect to; the catalog provides the atomic commit point and the table namespace
- Each engine is configured with the catalog endpoint and credentials; they all see the same table metadata and can read/write with concurrent safety
- Use AWS Glue Data Catalog as the backend if the organization is already AWS-native; it supports Iceberg natively and integrates with Lake Formation for access control
- Nessie (Project Nessie) is an alternative that adds Git-like branching for table versions — useful for isolated testing environments
Why this is asked: Multi-engine catalog design is an architect-level platform decision with significant operational consequences.

**Q10: How does Iceberg's metadata layer affect query planning performance for a table with 10 years of history and millions of manifest entries?**
What a good answer covers:
- The manifest list for the current snapshot may reference thousands of manifest files, each listing thousands of data files; a full scan of all manifests for query planning is prohibitively slow
- Iceberg mitigates this with manifest file pruning: each manifest records the min/max of partition columns for all its data files; the planner skips manifests that cannot contain matching rows
- For very large tables, run `REWRITE MANIFESTS` to consolidate and sort manifest files, improving planning performance
- Snapshot expiration (`expire_snapshots`) removes old snapshot metadata and orphaned manifest files, reducing the manifest footprint
Why this is asked: Metadata scalability is a production concern for long-lived Iceberg tables.

**Q11: Compare Iceberg's approach to deletes with Delta Lake's approach. In what scenarios does each perform better?**
What a good answer covers:
- Delta Lake deletes: mark files containing deleted rows as removed in the transaction log; optionally rewrite those files without the deleted rows (using `OPTIMIZE` + `VACUUM`)
- Iceberg supports two delete modes: copy-on-write (rewrite files containing deleted rows immediately, same as Delta Lake) and merge-on-read (write a delete file recording deleted row positions; apply deletions at read time by merging the delete file with the data file)
- Merge-on-read is faster for write-heavy workloads with many small deletes (e.g., GDPR erasure); copy-on-write is faster for read-heavy workloads where the extra read-time merge overhead is too costly
- Delta Lake is moving toward merge-on-read (Deletion Vectors); Iceberg has supported it longer
Why this is asked: Delete implementation is a key format-level trade-off that influences workload suitability.

---

**Q12: An organization wants to use Iceberg branching (via Nessie) to allow data engineers to test transformations on a production table without affecting production consumers. Design the workflow.**
What a good answer covers:
- Nessie provides Git-like branches for Iceberg table metadata; a `dev` branch is created from the `main` branch at a specific snapshot
- Engineers run their transformations against the `dev` branch; the production `main` branch continues to receive live writes without interference
- After validation, changes from `dev` are merged back to `main` using Nessie's merge operation; conflicts (if `main` has advanced) are detected and resolved
- CI/CD runs automated data quality checks on the `dev` branch output before the merge is approved; this mirrors the pull request review workflow for code
- Connect to schema evolution: schema changes can also be tested on a `dev` branch before merging to `main`, reducing the risk of breaking production consumers
Why this is asked: Iceberg branching via Nessie is an emerging best practice for production-safe lakehouse development; architect-level candidates should know it.

**Q13: The organization is evaluating Iceberg vs Delta Lake vs Apache Hudi for a unified lakehouse platform that must support streaming ingest, batch analytics, ML training, and regulatory compliance. Provide a framework for making this decision.**
What a good answer covers:
- Streaming ingest: Hudi has the most mature streaming write support (MOR tables); Iceberg and Delta Lake both support streaming but require compaction to manage small files
- Batch analytics: all three support Spark, but Iceberg's multi-engine support (Trino, Flink, Hive, Snowflake) is the widest; Delta Lake is tightest with Databricks/Spark
- ML training: all three integrate with MLflow for data versioning; Iceberg's snapshot isolation and time travel make reproducible training dataset creation straightforward
- Regulatory compliance: all three support time travel for audit; Iceberg's column IDs (stable column identifiers) make schema lineage tracing more reliable across renames
- Decision framework: if the organization is Databricks-first, Delta Lake; if multi-engine and cloud-agnostic, Iceberg; if streaming-first with upsert-heavy workloads, Hudi
- Connect across tracks: the chosen format directly affects how watermarks, compaction, time travel, and schema evolution are implemented
Why this is asked: Format selection at the platform level is the most consequential lakehouse architecture decision; architects must be able to structure the evaluation.

---

## Topic 4 — Time Travel

*Reference file: `c004_time_travel_demo.py`*

---

**Q1: What is time travel in a data lakehouse and how is it implemented?**
What a good answer covers:
- Time travel allows querying a table as it existed at a previous point in time or at a specific version number
- In `c004_time_travel_demo.py`, `SNAPSHOTS` stores multiple versions of the table; `read_snapshot(version)` returns the data as it existed at that version
- Delta Lake implements this via the transaction log: each log entry is a version; `SELECT * FROM table VERSION AS OF 1` replays the log to reconstruct that version's file list
Why this is asked: Time travel is a foundational lakehouse capability; candidates must understand both what it is and how it is technically achieved.

**Q2: What use cases make time travel essential in a production data pipeline?**
What a good answer covers:
- Audit and compliance: reproduce the exact data used to generate a published report at any historical date
- Error recovery: if a pipeline bug corrupts data, time travel to the pre-bug version and restore, rather than reprocessing from raw
- Debugging: compare the current table state to a previous version to understand what changed and when
- ML reproducibility: training a model requires a dataset snapshot frozen at the training date; time travel provides this without copying data
Why this is asked: Tests whether the candidate sees time travel as a feature with concrete operational applications, not just an interesting capability.

**Q3: In `c004_time_travel_demo.py`, snapshot v1 shows `o101.amount = 85.0` and snapshot v2 shows `o101.amount = 90.0`. How does Delta Lake store both versions without duplicating all data?**
What a good answer covers:
- Delta Lake does not duplicate unchanged rows; it stores the new Parquet file containing the updated `o101` row alongside the old file
- Snapshot v1's transaction log entry points to the original file; snapshot v2's entry points to the new file (and marks the original as removed from the current view)
- The original file is not deleted until `VACUUM` runs with a retention threshold; until then, both versions of the row are accessible by reading the appropriate file
Why this is asked: Tests understanding of the append-only file model and how old snapshots remain accessible without data duplication at the snapshot level.

**Q4: What is the difference between time travel by version number and time travel by timestamp in Delta Lake?**
What a good answer covers:
- Version number (`VERSION AS OF N`) selects the exact transaction log entry N; deterministic and reproducible
- Timestamp (`TIMESTAMP AS OF 'YYYY-MM-DD HH:MM:SS'`) selects the latest transaction log version committed at or before that timestamp; non-deterministic if multiple commits occur within the same second
- For audit and ML reproducibility, version number is preferred because it is unambiguous; timestamp is more convenient for human-driven queries
Why this is asked: The distinction matters for reproducibility — an important property for audit and ML use cases.

---

**Q5: A pipeline bug corrupted the `amount` column in `fact_orders` for orders loaded on a specific date. Using time travel, design the recovery procedure.**
What a good answer covers:
- Identify the last clean transaction log version before the corrupt load using `DESCRIBE HISTORY fact_orders`
- Use `INSERT OVERWRITE` with the time-travel version to restore the affected partition: `INSERT OVERWRITE TABLE fact_orders PARTITION(date='2026-03-25') SELECT * FROM fact_orders VERSION AS OF 42 WHERE date='2026-03-25'`
- Validate the restored partition's row counts and aggregates against the source system before notifying downstream consumers
- Root-cause the bug, fix the transformation logic, re-run the corrected pipeline for the affected date, and validate again
Why this is asked: Time travel recovery is one of the most practical and commonly cited uses of the feature.

**Q6: How long should time travel history be retained for a production table, and what controls the retention period?**
What a good answer covers:
- Retention is controlled by the `VACUUM` command's retention threshold (default 7 days in Delta Lake); files older than the threshold and no longer referenced by any current transaction log entry are deleted
- Compliance requirements may mandate longer retention: financial tables may need 7 years of history for audit
- For long-term compliance, time travel in the live table is expensive to maintain (all old files must be kept); a better approach is to archive periodic snapshots to cheaper storage and use those for audit rather than live time travel
- Connect to object storage (Topic 1): longer retention directly increases storage costs; balance retention against compliance requirements and cost
Why this is asked: Retention policy is an operational decision with cost and compliance dimensions.

**Q7: A data analyst runs a time-travel query against a table and gets an error: "version 15 is not available." What has happened and how do you prevent future occurrences?**
What a good answer covers:
- The VACUUM command deleted the data files referenced by version 15 because they were older than the retention threshold; the transaction log entry may still exist but the underlying files are gone
- Prevention: increase the `delta.deletedFileRetentionDuration` table property to match the longest expected time-travel lookback window
- If analysts routinely query versions older than 7 days, the default retention is insufficient; set a longer retention aligned with the compliance or operational lookback requirement
- Alternatively, create a named snapshot (Iceberg) or a table clone (Delta Lake) at a regular interval to provide stable historical reference points without retaining all intermediate versions
Why this is asked: The gap between what analysts expect and what VACUUM deletes is a common production support issue.

**Q8: How would you use Delta Lake time travel to implement reproducible ML training datasets that do not change when the underlying table is updated?**
What a good answer covers:
- Record the Delta Lake table version at the time training begins and store it as model metadata (e.g., an MLflow tag: `training_data_version = 42`)
- To reproduce training, re-run the training job with `df = spark.read.format("delta").option("versionAsOf", 42).load(table_path)` — identical data guaranteed
- Wrap the training dataset creation in a Delta Lake snapshot clone so the dataset version is protected from VACUUM even if the source table is vacuumed beyond version 42
- Connect to data quality: before freezing the training version, run the anomaly detection checks (`c005_anomaly_detection_demo.py`) against that snapshot to verify data quality before training
Why this is asked: ML reproducibility is a cross-track design concern that time travel directly enables.

---

**Q9: An audit team asks you to prove that the revenue figure in a quarterly financial report filed 18 months ago was calculated correctly from the data available at that time. Design the audit evidence trail.**
What a good answer covers:
- Ensure the reporting pipeline stores the exact Delta Lake version or Iceberg snapshot ID used to generate each report alongside the report output in an audit metadata table
- Run `SELECT * FROM fact_revenue VERSION AS OF [stored_version]` to reconstruct the exact dataset the report was based on; compare the reconstruction to the filed figure
- If the table has been VACUUM'd beyond 18 months, fall back to the archived snapshot copy (see retention policy answer above) stored in a compliance archive
- The pipeline's git commit hash (transformation code version) + the data version together constitute the full audit evidence
Why this is asked: Financial audit reconstruction is a concrete regulatory scenario that time travel is built to support.

**Q10: How does Iceberg's time travel differ from Delta Lake's in terms of implementation and operational behavior?**
What a good answer covers:
- Iceberg time travel is based on snapshot IDs (immutable integers) and snapshot timestamps; `SELECT * FROM table FOR SYSTEM_TIME AS OF '...'` or `FOR SYSTEM_VERSION AS OF snapshot_id`
- Iceberg's snapshot expiration is managed by the `expire_snapshots` procedure, which removes old snapshot metadata and orphaned data files; functionally similar to Delta VACUUM
- Iceberg's metadata hierarchy (manifest files) makes it possible to expire snapshots without touching the transaction log root, whereas Delta Lake must retain all log entries up to the oldest retained version
- Iceberg supports named snapshots ("tags" in Iceberg 1.2+) that are protected from expiration — directly analogous to saving a specific version permanently
Why this is asked: Multi-format environment candidates must know where the formats behave differently.

**Q11: You need to implement a "time-windowed feature store" where each ML feature record is associated with the exact lakehouse snapshot valid at the time a prediction was made, enabling offline evaluation months later. Design this system.**
What a good answer covers:
- At prediction time, record the current Delta Lake version or Iceberg snapshot ID alongside each prediction in a prediction log table
- At evaluation time, join the prediction log to the feature store using the stored snapshot ID: `SELECT * FROM feature_store VERSION AS OF prediction_log.snapshot_id`
- Because evaluation may happen months later, snapshot retention must be managed: either extend retention indefinitely (expensive) or clone the snapshot at prediction time to a protected archive
- The clone is a shallow copy: it references the same Parquet files without duplicating data, and is pinned so VACUUM cannot delete its referenced files
- Connect to the ACID topic: the snapshot ID is only meaningful if the Delta/Iceberg ACID commit produced a consistent snapshot — a partially committed write would produce a snapshot with corrupt features
Why this is asked: Feature store time travel is an architect-level ML infrastructure design problem.

---

**Q12: Regulatory requirements mandate that data deleted under GDPR right-to-erasure requests must be unrecoverable from time-travel snapshots within 30 days of the deletion request. How do you reconcile this with a time-travel retention policy that keeps 90 days of history?**
What a good answer covers:
- Standard time travel retains old data files where deleted rows still exist; GDPR erasure requires those files to be unreachable
- Solution: when a GDPR delete is executed, immediately run a targeted VACUUM-style operation that rewrites and deletes only the files containing the erased rows, across all historical snapshots within the retention window
- This is called "selective snapshot rewriting" or "tombstone-aware vacuum"; Delta Lake 2.x's `REORG TABLE ... APPLY (PURGE)` and Iceberg's `delete_orphan_files` plus position deletes address this
- After the rewrite, time travel queries for versions containing the erased rows will return the redacted data, satisfying GDPR while retaining the rest of the historical record
- Document the erasure event with a timestamp in a compliance audit log; the audit log proves the request was fulfilled within the 30-day window
Why this is asked: GDPR vs time travel is a real compliance conflict that architects in European-market organizations must resolve.

**Q13: Design a multi-version testing framework for a data lakehouse where data engineers can validate transformation logic changes against the exact production data from any point in the past two years, without impacting production pipeline performance.**
What a good answer covers:
- Create a catalog branch (Nessie) or Delta Lake shallow clone for each test run, pointing to the target historical snapshot; engineers run their transformations against the branch without touching production
- Branches are read-only for historical data; test output is written to a separate namespace (`dev/engineer_name/test_run_id`) and automatically cleaned up after 7 days
- The CI pipeline automatically provisions a test branch pointing to the most recent production snapshot for every pull request; data quality checks run against the test output
- Historical snapshots older than the live retention window are stored as archived clones in cold storage; the test framework retrieves them on demand with a latency SLA (e.g., available within 10 minutes)
- Connect to the schema evolution track: the test framework validates that transformation changes do not break the published data contract for any consumer
Why this is asked: Isolated, reproducible testing against historical production data is an architect-level platform feature that requires combining time travel, branching, and storage management.

---

## Topic 5 — Compaction and Optimization

*Reference file: `c005_compaction_demo.py`*

---

**Q1: What is compaction in a data lakehouse and why is it necessary?**
What a good answer covers:
- Compaction merges many small Parquet files into fewer larger files, reducing the per-file overhead for query planning and execution
- Small files accumulate from streaming micro-batch writes, over-partitioned incremental loads, or frequent small appends
- `c005_compaction_demo.py` demonstrates reading multiple small files and writing them as a single larger file, making subsequent reads significantly faster
- Without compaction, a table with millions of small files degrades query performance progressively over time
Why this is asked: Compaction is a standard operational task in every production lakehouse; candidates must understand why it is needed and what it does.

**Q2: What is the `OPTIMIZE` command in Delta Lake and what does it do?**
What a good answer covers:
- `OPTIMIZE table_name` reads all small files in the table (or a specific partition) and rewrites them into fewer, larger Parquet files, typically targeting 1GB per output file
- It commits the new large files and marks the old small files as removed in the transaction log; old files become eligible for VACUUM after the retention window
- `OPTIMIZE ZORDER BY (column)` additionally co-locates rows with similar values in the same file, improving data skipping for range queries on that column
- Running OPTIMIZE does not affect the table's current data; it is a pure physical reorganization
Why this is asked: `OPTIMIZE` is the most frequently run maintenance command in Delta Lake; candidates must know its purpose and behavior.

**Q3: What is Z-ordering and how does it improve query performance?**
What a good answer covers:
- Z-ordering (Z-order curve) is a space-filling curve that maps multi-dimensional values to a single dimension while preserving locality — nearby values in the multi-dimensional space map to nearby positions in the sorted file
- When applied with `OPTIMIZE ZORDER BY (customer_id, date)`, rows with similar customer_id and date values are co-located in the same Parquet row groups
- Queries filtering on `customer_id` and/or `date` can skip entire row groups using Parquet min/max statistics, dramatically reducing bytes read
- Z-ordering is most effective on columns with high cardinality that are frequently used in query filters; it does not help partition pruning — that requires partitioning
Why this is asked: Z-ordering is a key performance optimization in Delta Lake; candidates must distinguish it from partitioning.

**Q4: What is VACUUM in Delta Lake and how does it relate to compaction?**
What a good answer covers:
- VACUUM deletes Parquet files that are no longer referenced by any transaction log entry and are older than the retention threshold (default 7 days)
- OPTIMIZE creates new large files and marks old small files as removed; VACUUM is what physically deletes the old small files from object storage
- Without VACUUM, compacted tables accumulate orphaned old files indefinitely, increasing storage cost without any query benefit
- VACUUM also affects time travel: it permanently deletes the old files that historical snapshots reference, setting the time travel boundary
Why this is asked: The OPTIMIZE + VACUUM pairing is the complete compaction workflow; candidates must understand both halves.

---

**Q5: A streaming pipeline writes 200 micro-batches per hour to a Delta Lake table. After one week, query performance has degraded severely. Diagnose and design a compaction strategy.**
What a good answer covers:
- One week at 200 batches/hour = 33,600 small files; each query must open and scan thousands of files, causing the performance degradation
- Run `OPTIMIZE` on a schedule (e.g., every hour or every 4 hours depending on query volume) to compact small files from recent micro-batches
- Partition the table by hour or day so OPTIMIZE can compact only the most recent partition, reducing the scope of each compaction run
- Delta Lake's auto-optimize feature (`delta.autoOptimize.optimizeWrite = true`) can merge small writes automatically at commit time, reducing the frequency of manual OPTIMIZE runs
Why this is asked: Streaming + Delta Lake compaction scheduling is a standard production operational scenario.

**Q6: How does compaction interact with time travel? Specifically, what happens to a snapshot that references small files that have since been compacted?**
What a good answer covers:
- OPTIMIZE creates new large files and marks old small files as removed, but does not delete them; the old files remain in object storage
- A time-travel query for a snapshot that predates the OPTIMIZE commit will use the old small files (still present, just not referenced by the current snapshot)
- After VACUUM deletes the old small files, time-travel queries for snapshots older than the retention threshold will fail because the referenced files no longer exist
- This is the same mechanism as described in Topic 4 (time travel retention); OPTIMIZE accelerates the accumulation of "removable" files, potentially shortening effective time-travel range
Why this is asked: The interaction between compaction and time travel is a subtle but important operational consideration.

**Q7: What is auto-optimize in Delta Lake and when should you enable or disable it?**
What a good answer covers:
- `autoOptimize.optimizeWrite`: Delta Lake bins small writes together before committing, producing larger output files without a separate OPTIMIZE run
- `autoOptimize.autoCompact`: after a write, Delta Lake automatically runs a background OPTIMIZE on recently written files
- Enable for streaming and frequent small-batch workloads where small files would otherwise accumulate quickly
- Disable for large batch workloads that already write large files: auto-optimize adds overhead without benefit; also disable when write latency is critical and background compaction interferes
Why this is asked: Auto-optimize configuration is a common production tuning decision.

**Q8: A table is partitioned by `date` and has 3 years of history. An `OPTIMIZE` command takes 6 hours because it scans all partitions. How do you reduce compaction time?**
What a good answer covers:
- Scope OPTIMIZE to only recently written partitions: `OPTIMIZE table WHERE date >= current_date - 7` — only recent partitions accumulate new small files; historical partitions are already compacted
- Schedule OPTIMIZE immediately after each daily load to compact only the new partition before the next day's load adds more files
- For historical partitions that are never updated, run a one-time full OPTIMIZE once, then exclude them from future runs using the date filter
- Use partition statistics to identify which partitions have the most small files and target those specifically
Why this is asked: Scoping compaction to recently active partitions is the standard production optimization for large partitioned tables.

---

**Q9: Design a compaction schedule for a lakehouse table that receives both high-frequency streaming writes (real-time) and daily batch corrections (historical partition updates).**
What a good answer covers:
- For streaming writes: run OPTIMIZE on the current partition every 30–60 minutes using a background job; use `autoOptimize.optimizeWrite` to reduce file count per micro-batch
- For historical partition corrections: run OPTIMIZE on the corrected partition immediately after each correction batch completes; historical partitions accumulate corrections infrequently so a triggered rather than scheduled compaction is more efficient
- Schedule full VACUUM weekly with a 7-day retention; the VACUUM run follows the OPTIMIZE run to reclaim storage from compacted old files
- Monitor file count and average file size per partition in a quality metadata table; alert if any partition exceeds a file count threshold (e.g., >1000 files) to trigger an unscheduled OPTIMIZE
Why this is asked: Mixed streaming and batch write patterns require a layered compaction strategy.

**Q10: How does Iceberg's rewrite manifests and rewrite data files operation compare to Delta Lake's OPTIMIZE command?**
What a good answer covers:
- Iceberg's `rewrite_data_files` procedure is the equivalent of Delta's `OPTIMIZE`: it merges small files into larger ones based on configurable target file size
- Iceberg's `rewrite_manifests` reorganizes the metadata layer (manifest files) to improve planning performance; this has no Delta Lake equivalent because Delta's transaction log has a different structure
- Iceberg's rewrite operations are more configurable: you can specify target file size, partial progress (bin-pack only N files per run), and filter to specific partitions using Iceberg's partition spec
- Both produce a new snapshot after the rewrite; old files are eligible for cleanup by `expire_snapshots` (Iceberg) or `VACUUM` (Delta)
Why this is asked: Format-specific compaction differences matter for teams managing multi-format lakehouses.

**Q11: A GDPR erasure request requires deleting a specific customer's records from 3 years of historical data across a 5TB table. How does this interact with compaction, and how do you execute it efficiently?**
What a good answer covers:
- A targeted DELETE statement removes the customer's rows from the current snapshot, but old Parquet files containing those rows remain on disk for the VACUUM retention period
- To fully erase the customer from all historical snapshots within the retention window, rewrite all affected files using `REORG TABLE ... APPLY (PURGE)` (Delta Lake) or Iceberg's position delete + `rewrite_data_files` with the delete applied
- Compaction helps here: if the customer's rows are spread across many small files, compact those files first to minimize the number of files that must be rewritten for the erasure
- After rewriting, run VACUUM immediately with a 0-day retention for the affected files (requires `spark.databricks.delta.retentionDurationCheck.enabled = false` in Databricks) to physically delete the erased data
- Document the erasure with a compliance audit record per the data contract requirements
Why this is asked: GDPR erasure + compaction interaction is a real architect-level operational scenario.

---

**Q12: Design an automated lakehouse optimization service for a platform with 500 tables of varying sizes, write frequencies, and query patterns, where a one-size-fits-all compaction schedule is insufficient.**
What a good answer covers:
- Collect per-table metrics after each write: file count, average file size, partition count, query frequency, and time since last OPTIMIZE
- Build a scoring model that ranks tables by "compaction urgency" (high file count + high query frequency = high priority; low file count + low query frequency = low priority)
- Run an optimization dispatcher that picks the top-N urgent tables and runs OPTIMIZE on them within a fixed maintenance window
- Tables with real-time SLAs trigger OPTIMIZE automatically after each streaming batch via a post-write hook; batch tables are scored and scheduled by the dispatcher
- VACUUM is run separately on a weekly schedule for all tables; retention period is read from the table's data contract metadata
Why this is asked: Autonomous lakehouse maintenance at scale requires a data-driven scheduling system — an architect-level platform engineering design.

**Q13: A business requires that query performance on a critical dashboard never exceed 10 seconds even as the table grows from 1TB to 100TB over five years. Design the full optimization strategy spanning partitioning, compaction, Z-ordering, and caching.**
What a good answer covers:
- Partitioning: choose a partition column that the dashboard's primary filters always use (e.g., `region` + `month`); this eliminates 99% of files from the scan for typical queries
- Compaction: compact each partition to 1GB files on a post-load schedule; at 100TB with monthly partitions, each partition is manageable in size
- Z-ordering: apply Z-order on the most selective filter columns within each partition (e.g., `customer_segment`, `product_category`) to enable row-group skipping within files
- Result caching: the query engine (Databricks, Trino) can cache the results of common dashboard queries; schedule a cache warm job after each compaction run so the cache is populated before business hours
- Data skipping statistics: run `ANALYZE TABLE` or equivalent to keep column statistics current; these statistics power the Z-order skipping
- Monitoring: track query P95 latency continuously; if it approaches the 10-second SLA, alert and trigger an unscheduled OPTIMIZE+ZORDER run on the hot partitions
- Connect across topics: this answer spans object storage layout (Topic 1), ACID commits (compaction writes are ACID, Topic 2), time travel retention (affects VACUUM frequency, Topic 4), and data freshness monitoring (quality track)
Why this is asked: End-to-end performance engineering under a long-horizon growth constraint is the most comprehensive architect-level question in this track.
