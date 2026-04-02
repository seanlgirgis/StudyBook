# Interview Questions - Analytics

> Topics covered: row vs column storage
> Levels: Starter | Mid | Senior | Architect

---

## Topic - Row vs Column Storage

### Level 1 - Starter

**Q1: In c060_row_vs_column_demo.py, what is the difference between the row-style and column-style queries?**
What a good answer covers:
- Row-style uses SELECT * to read full rows
- Column-style selects only user_id and value
- Column-style reads less data and should be faster
Why this is asked: Checks basic mechanics of row vs column access.

**Q2: In c060_row_vs_column_demo.py, what does the buffer count or runtime tell you?**
What a good answer covers:
- More buffers/time mean more data was read
- Column-style should show fewer buffers and lower time
- Demonstrates why narrow reads help analytics
Why this is asked: Verifies how to interpret the demo output.

**Q3: In c061_parquet_demo.py, what is the key advantage of Parquet over CSV for analytics reads?**
What a good answer covers:
- Parquet is columnar and smaller on disk
- Narrow column reads are faster in Parquet
- The demo compares full vs narrow reads for CSV and Parquet
Why this is asked: Tests understanding of columnar file benefits.

**Q4: In c062_partition_pruning_demo.py, what does partition pruning do?**
What a good answer covers:
- Skips entire partitions before scanning rows
- Requires filtering on the partition key
- The demo shows fewer partitions touched in Scenario A
Why this is asked: Confirms basic partition pruning behavior.

### Level 2 - Mid

**Q1: In c060_row_vs_column_demo.py, why does selecting fewer columns matter even in a row-store engine?**
What a good answer covers:
- It reduces data read from disk or memory
- It can enable index-only access via a covering index
- The demo simulates column benefits by narrowing projection
Why this is asked: Tests application of projection-based optimization.

**Q2: In c061_parquet_demo.py, what common mistake makes Parquet look slower than CSV?**
What a good answer covers:
- Reading all columns when you only need a few
- Ignoring compression and column pruning benefits
- Comparing cold vs warm cache runs inconsistently
Why this is asked: Checks for practical benchmarking pitfalls.

**Q3: In c062_partition_pruning_demo.py, why does Scenario C reduce pruning?**
What a good answer covers:
- The partition key is wrapped in a function
- The planner cannot use it to prune partitions
- More partitions are scanned as a result
Why this is asked: Tests understanding of predicate shape impact.

**Q4: In c061_parquet_demo.py, when would you still choose CSV despite Parquet being faster?**
What a good answer covers:
- Simpler interoperability or tooling constraints
- Small datasets where simplicity beats performance
- Write path simplicity over read optimization
Why this is asked: Probes tradeoffs in storage format choices.

### Level 3 - Senior

**Q1: In c060_row_vs_column_demo.py, how would you decide between adding a covering index and switching to columnar storage?**
What a good answer covers:
- Covering index helps selective queries on a row store
- Columnar storage is better for wide analytics scans
- The demo shows index-only style benefits but still within a row engine
Why this is asked: Tests performance and storage decision making.

**Q2: Using c061_parquet_demo.py and c062_partition_pruning_demo.py, how do columnar files and partitioning work together?**
What a good answer covers:
- Partitioning reduces files scanned
- Columnar format reduces columns read within files
- Combined, they minimize I/O for analytics workloads
Why this is asked: Evaluates real-world scenario reasoning.

**Q3: In c062_partition_pruning_demo.py, what failure mode happens if most queries filter on non-partition keys?**
What a good answer covers:
- Pruning rarely triggers
- Most partitions are scanned anyway
- Partitioning choice does not match query patterns
Why this is asked: Tests ability to spot misaligned partitioning.

### Level 4 - Architect

**Q1: Using c061_parquet_demo.py, how would you choose between Parquet files in a lakehouse and row-store tables in an OLTP system?**
What a good answer covers:
- Parquet is optimized for analytics and narrow reads
- OLTP favors row-store for fast single-row lookups
- The demo shows Parquet wins for columnar analytics reads
Why this is asked: Connects file format choice to system design.

**Q2: Using c062_partition_pruning_demo.py, how would you align partitioning with query optimization practices?**
What a good answer covers:
- Partition keys should match common filters to enable pruning
- Avoid wrapping partition keys in functions
- Plan-reading habits ensure pruning is actually happening
Why this is asked: Links partitioning to query optimization decisions.

---

## Topic - Partition Pruning

### Level 1 - Starter

**Q1: In d03_partition_pruning_story.md, what is partition pruning in plain language?**
What a good answer covers:
- Partitioning splits data into labeled chunks
- Pruning skips irrelevant chunks before reading rows
- The label/box analogy from the story
Why this is asked: Confirms the core concept in simple terms.

**Q2: In c062_partition_pruning_demo.py, which scenario shows pruning working and why?**
What a good answer covers:
- Scenario A filters on the partition key (ts)
- Fewer partitions are touched
- The plan output lists only the March partition
Why this is asked: Tests recognition of pruning success in the demo.

**Q3: In c062_partition_pruning_demo.py, what happens in Scenario B with no partition filter?**
What a good answer covers:
- All partitions are scanned
- No pruning occurs
- The plan shows many partitions touched
Why this is asked: Verifies the no-pruning case.

**Q4: In c062_partition_pruning_demo.py, why does Scenario C often prevent pruning?**
What a good answer covers:
- The partition key is hidden inside a function
- The planner cannot match the filter to partition labels
- More partitions are scanned
Why this is asked: Checks understanding of function-wrapped filters.

### Level 2 - Mid

**Q1: Using d03_partition_pruning_story.md, what is a common mistake that breaks pruning?**
What a good answer covers:
- Not filtering on the partition key at all
- Wrapping the key in a function or expression
- Assuming the engine will prune anyway
Why this is asked: Tests practical pitfalls from the story.

**Q2: In c062_partition_pruning_demo.py, how would you rewrite Scenario C to enable pruning?**
What a good answer covers:
- Use a direct ts range filter
- Avoid to_char(ts, ...) in the predicate
- Match the partition boundaries explicitly
Why this is asked: Applies the demo to a concrete fix.

**Q3: In c061_parquet_demo.py, how does partition pruning complement columnar reads?**
What a good answer covers:
- Pruning reduces files scanned
- Parquet reduces columns read within files
- Together they minimize I/O for analytics queries
Why this is asked: Connects pruning to columnar file performance.

**Q4: In c060_row_vs_column_demo.py, why is pruning still valuable even when you select few columns?**
What a good answer covers:
- Fewer columns helps per-row cost
- Pruning reduces the number of rows scanned at all
- Both together drive faster analytics reads
Why this is asked: Tests combined optimization reasoning.

### Level 3 - Senior

**Q1: In c062_partition_pruning_demo.py, what failure mode appears if partition boundaries don’t match query patterns?**
What a good answer covers:
- Filters hit many partitions anyway
- Pruning benefit disappears
- Query cost grows even with partitioning
Why this is asked: Evaluates partition design judgment.

**Q2: Using d03_partition_pruning_story.md, how would you choose a partition key for an analytics table?**
What a good answer covers:
- Pick a column frequently used in filters (often time)
- Align boundaries with common query windows
- Avoid keys that are rarely filtered
Why this is asked: Tests real-world design reasoning.

**Q3: In c062_partition_pruning_demo.py, what edge case can still prevent pruning even with a partition key filter?**
What a good answer covers:
- Predicates that are not sargable (functions, casts)
- Filters that don’t align with partition ranges
- Planner cannot map filter to partition bounds
Why this is asked: Probes deeper query-shape issues.

### Level 4 - Architect

**Q1: Using c062_partition_pruning_demo.py, how would you combine pruning with query optimization practices from other tracks?**
What a good answer covers:
- Use plan reading to verify pruning
- Align predicates to avoid function-wrapped keys
- Combine with index or join optimization when needed
Why this is asked: Tests cross-track integration with query optimization.

**Q2: Using c061_parquet_demo.py, how does partition pruning influence lakehouse file layout decisions?**
What a good answer covers:
- Partition folders should align with query filters
- Pruning reduces file reads in Parquet
- Poor partitioning increases scan costs at scale
Why this is asked: Connects pruning to file format and lakehouse design.
