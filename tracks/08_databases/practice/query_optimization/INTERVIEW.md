# Interview Questions — Query Optimization

> Topics covered: bad vs good queries · EXPLAIN plan reading
> Levels: Starter | Mid | Senior | Architect

---

## Level 1 — Starter

**Q1: In c050, what makes a query "bad" versus "good"?**
What a good answer covers:
- The bad query wraps the column in LOWER() which blocks index use
- The good query uses direct equality and can use the index
- The bad query takes longer in the timing output
Why this is asked: Checks basic understanding of the demo's contrast.

**Q2: In c051, what does EXPLAIN ANALYZE do?**
What a good answer covers:
- It shows the execution plan used by the database
- It includes estimated cost and row counts
- It includes actual rows and time for what really happened
- The demo prints plans for both bad and good queries
Why this is asked: Tests basic familiarity with query plan analysis.

**Q3: What is a sequential scan and when does it appear in c051?**
What a good answer covers:
- A sequential scan reads every row in the table
- It appears for the bad query because the index cannot be used
- It is more expensive than an index scan for selective queries
Why this is asked: Confirms understanding of the most common plan node.

**Q4: What is an index scan and when does it appear in c051?**
What a good answer covers:
- An index scan follows the index to find matching rows
- It appears for the good query that uses direct equality
- It is faster than a sequential scan for selective filters
Why this is asked: Pairs with Q3 to test the core plan contrast.

---

## Level 2 — Mid

**Q1: Why does wrapping a column in a function like LOWER() block index use?**
What a good answer covers:
- The index stores raw values, not transformed values
- LOWER(email) cannot match an index on email
- The planner falls back to a sequential scan
- The fix is to store data in the correct case or use a functional index
Why this is asked: Tests understanding of index sargability.

**Q2: How do you read cost and actual time in EXPLAIN ANALYZE output?**
What a good answer covers:
- Cost is the planner's estimate in arbitrary units
- Actual time is wall-clock milliseconds for that node
- Large gaps between estimated and actual rows signal stale stats
- The demo labels these fields explicitly
Why this is asked: Checks practical ability to interpret plan output.

**Q3: What does "rows" in EXPLAIN output tell you?**
What a good answer covers:
- Estimated rows is the planner's prediction before execution
- Actual rows is what the query really processed
- A large gap means statistics are stale or the filter is unusual
Why this is asked: Tests reading of the most diagnostic field in EXPLAIN.

**Q4: When should you run ANALYZE on a table?**
What a good answer covers:
- When stats are stale and planner estimates diverge from reality
- After large bulk loads or deletes
- Autovacuum handles this automatically but manual ANALYZE helps after large changes
Why this is asked: Tests operational awareness of planner dependency on stats.

---

## Level 3 — Senior

**Q1: How do you decide between adding an index versus rewriting the query?**
What a good answer covers:
- If the query pattern is fixed and the column is selective, add an index
- If the query can be restructured to avoid function wrapping, rewrite first
- Indexes have write overhead; rewriting is free
- The c050 demo shows rewriting is the simplest fix
Why this is asked: Probes judgment on the cheapest effective intervention.

**Q2: What are the risks of over-indexing based on c050/c051 patterns?**
What a good answer covers:
- Every index slows down writes (INSERT, UPDATE, DELETE)
- Indexes consume storage
- The planner may choose a wrong index if cardinality is low
- The demos show one targeted index is often enough
Why this is asked: Tests understanding of index cost beyond read benefit.

**Q3: How do you use EXPLAIN ANALYZE to confirm a fix worked?**
What a good answer covers:
- Run EXPLAIN ANALYZE before and after the change
- Compare plan nodes: Seq Scan vs Index Scan
- Compare actual time to confirm improvement
- c051 does this comparison explicitly
Why this is asked: Evaluates practical diagnostic process.

---

## Level 4 — Architect

**Q1: How do query optimization principles from c050/c051 scale to distributed query engines like Spark or Athena?**
What a good answer covers:
- Function wrapping on partition columns in Athena/Spark prevents partition pruning
- The same sargability rule applies: predicates must match stored form
- Distributed engines have their own EXPLAIN equivalents (EXPLAIN in Spark, query plans in Athena)
- The fix pattern is identical: push the transformation to the write side
Why this is asked: Tests cross-system application of the core concept.

**Q2: When would you escalate from query tuning to schema redesign?**
What a good answer covers:
- When the query pattern is too complex for indexing to solve
- When multiple queries suffer from the same structural mismatch
- When denormalization or pre-aggregation would eliminate the bottleneck
- Tuning buys time; redesign solves root cause
Why this is asked: Evaluates architectural judgment beyond single-query fixes.

---

## Topic - Bad vs Good Queries / EXPLAIN Plan Reading (Add-On)

### Level 1 - Starter

**Q1: In c050_query_optimization_bad_vs_good.py, what makes the bad query slower than the good query?**
What a good answer covers:
- The bad query wraps customer_email in LOWER()
- That blocks the index on customer_email
- The demo prints a longer time for the bad query
Why this is asked: Confirms basic mechanics of the bad vs good contrast.

**Q2: In c051_explain_plan_reading.py, what plan node should you see for the bad query?**
What a good answer covers:
- Seq Scan on customer_orders
- High rows read and higher actual time
- The plan label appears in EXPLAIN ANALYZE output
Why this is asked: Tests identification of the bad plan in the demo.

**Q3: In c051_explain_plan_reading.py, what plan node should you see for the good query?**
What a good answer covers:
- Index Scan on customer_orders_email_idx
- Low rows read and lower actual time
- The plan label appears in EXPLAIN ANALYZE output
Why this is asked: Checks recognition of the good plan in the demo.

**Q4: In d01_query_optimization_story.md, what is the core optimization goal?**
What a good answer covers:
- Help the database do less work
- Prefer targeted lookup over full table scans
- Give the planner a cheaper path
Why this is asked: Verifies the story-level mental model.

### Level 2 - Mid

**Q1: In c050_query_optimization_bad_vs_good.py, what is the practical fix besides rewriting the query?**
What a good answer covers:
- Use a functional index on LOWER(customer_email)
- Store normalized email values to keep equality sargable
- Ensure the predicate matches the index shape
Why this is asked: Tests application-level alternatives.

**Q2: In c051_explain_plan_reading.py, how do you tell if stats are off?**
What a good answer covers:
- Large gap between estimated rows and actual rows
- High actual time relative to estimated cost
- The demo notes stats gaps in the plan comments
Why this is asked: Checks plan interpretation skills.

**Q3: Using d01_query_optimization_story.md, when might the planner ignore an index even if it exists?**
What a good answer covers:
- Low selectivity means too many rows match
- Tiny tables can be cheaper to scan
- Cost-based planning chooses the cheapest path
Why this is asked: Tests understanding of cost-based decisions.

**Q4: In c050_query_optimization_bad_vs_good.py, what common mistake makes the demo comparison invalid?**
What a good answer covers:
- Not resetting data before timing comparisons
- Comparing results without consistent data size
- Ignoring that warm caches can skew results
Why this is asked: Probes experimental hygiene and common pitfalls.

### Level 3 - Senior

**Q1: In c051_explain_plan_reading.py, how would you validate that a rewrite really fixed performance?**
What a good answer covers:
- Run EXPLAIN ANALYZE before and after
- Confirm Seq Scan becomes Index Scan
- Compare actual time and rows processed
Why this is asked: Tests diagnostic rigor.

**Q2: Using d01_query_optimization_story.md, what failure mode happens when predicate shape blocks index use?**
What a good answer covers:
- The planner falls back to a sequential scan
- Cost balloons as table size grows
- The system feels fine in dev but broken in prod
Why this is asked: Evaluates scaling failure recognition.

**Q3: In c050_query_optimization_bad_vs_good.py, what design decision would you revisit if email matching needs to be case-insensitive?**
What a good answer covers:
- Store a normalized column and index it
- Use a functional index on LOWER(email)
- Avoid runtime transformations in predicates
Why this is asked: Tests design judgment around correctness vs performance.

### Level 4 - Architect

**Q1: Using c051_explain_plan_reading.py, how would you apply plan-reading habits to warehouse queries (analytics/modeling tracks)?**
What a good answer covers:
- Use EXPLAIN to detect full scans on large fact tables
- Add partitioning or indexes to reduce scanned data
- The same plan-reading discipline applies at warehouse scale
Why this is asked: Connects query optimization to analytics/modeling tracks.

**Q2: In d01_query_optimization_story.md, how do these lessons map to distributed engines in the Spark track?**
What a good answer covers:
- Predicate shape impacts partition pruning and scan size
- EXPLAIN equivalents reveal shuffle vs scan costs
- Pushing transformations to write time keeps predicates sargable
Why this is asked: Tests cross-track system design reasoning.

---

## Topic - Index Not Used Cases

### Level 1 - Starter

**Q1: In c052_index_not_used_cases.py, what does Case A demonstrate about LOWER(column)?**
What a good answer covers:
- Wrapping the column in LOWER() blocks the index
- The plan shows a Seq Scan instead of Index Scan
- The demo labels this as Case A
Why this is asked: Checks basic recognition of function-blocked indexes.

**Q2: In c052_index_not_used_cases.py, what is the key reason Case B uses a Seq Scan?**
What a good answer covers:
- Low selectivity: most rows match event_type = 'click'
- Scanning can be cheaper than using the index
- The plan still shows Seq Scan despite the index
Why this is asked: Verifies the low-selectivity case.

**Q3: In c052_index_not_used_cases.py, why does Case C still use a Seq Scan with an index present?**
What a good answer covers:
- The table is tiny
- Index overhead outweighs the benefit
- Planner chooses the cheaper full scan
Why this is asked: Confirms the tiny-table exception.

**Q4: In c052_index_not_used_cases.py, what is the main takeaway about indexes?**
What a good answer covers:
- Index exists does not mean index used
- Planner picks the cheapest path
- Always verify with EXPLAIN ANALYZE
Why this is asked: Tests the core lesson from the demo.

### Level 2 - Mid

**Q1: In c052_index_not_used_cases.py, how would you fix Case A if case-insensitive search is required?**
What a good answer covers:
- Add a functional index on LOWER(user_email)
- Store normalized emails and compare directly
- Ensure predicate shape matches the index
Why this is asked: Applies the demo to a real fix.

**Q2: In c052_index_not_used_cases.py, what mistake would cause Case B to stay slow even after indexing event_type?**
What a good answer covers:
- Using an index on a low-selectivity column
- Expecting the index to help when most rows match
- Ignoring the planner cost model
Why this is asked: Checks practical expectations of index utility.

**Q3: In c052_index_not_used_cases.py, when might you accept the Seq Scan in Case C?**
What a good answer covers:
- When the table is tiny and scans are cheap
- When the query is infrequent
- When index maintenance cost is not worth it
Why this is asked: Tests tradeoff judgment for small tables.

**Q4: In c052_index_not_used_cases.py, what is a common mistake when interpreting EXPLAIN for index use?**
What a good answer covers:
- Assuming index presence guarantees Index Scan
- Ignoring actual rows and actual time
- Not comparing plans across cases
Why this is asked: Validates plan-reading discipline.

### Level 3 - Senior

**Q1: In c052_index_not_used_cases.py, how would stale statistics distort the planner's decision?**
What a good answer covers:
- Planner may misestimate selectivity
- Could pick Seq Scan when Index Scan is cheaper (or vice versa)
- Leads to unpredictable performance
Why this is asked: Tests deeper understanding of planner dependencies.

**Q2: In c052_index_not_used_cases.py, what design decision would you revisit if most queries filter on event_type = 'click'?**
What a good answer covers:
- Consider partial indexes for rare values instead
- Consider redesigning queries to target selective predicates
- Recognize that indexing a dominant value may not help
Why this is asked: Probes advanced indexing strategy.

**Q3: In c052_index_not_used_cases.py, how do you validate that your fix changed the plan?**
What a good answer covers:
- Re-run EXPLAIN ANALYZE after the change
- Compare plan nodes and actual row counts
- Confirm total time improves for the target query
Why this is asked: Tests verification rigor.

### Level 4 - Architect

**Q1: Using c052_index_not_used_cases.py, how do these index-ignored cases influence data modeling choices (analytics/modeling tracks)?**
What a good answer covers:
- Low-selectivity filters may require denormalization or summary tables
- Modeling for query patterns can reduce scan volume
- Indexes alone may not solve systemic scan costs
Why this is asked: Connects query optimization to modeling decisions.

**Q2: In c052_index_not_used_cases.py, how would you apply these lessons to distributed query engines (Spark track)?**
What a good answer covers:
- Low-selectivity predicates still cause large scans
- Predicate shape affects partition pruning and scan cost
- Plan inspection is required even in distributed engines
Why this is asked: Tests cross-track system reasoning.

---

## Topic - Composite Index (Left-to-Right Rule)

### Level 1 - Starter

**Q1: In d02_composite_indexes_story.md, what is the left-to-right rule for composite indexes?**
What a good answer covers:
- Index on (col1, col2) can use col1
- Can use col1 + col2
- Cannot use col2 alone well
Why this is asked: Checks the core rule from the story.

**Q2: In c053_composite_index_left_to_right.py, what happens in Case A (last_name only)?**
What a good answer covers:
- Uses the leftmost column of the index
- Expect Index Scan for last_name = 'Smith'
- Demonstrates left-to-right effectiveness
Why this is asked: Verifies the leftmost column behavior.

**Q3: In c053_composite_index_left_to_right.py, what happens in Case C (first_name only)?**
What a good answer covers:
- Missing the leftmost column weakens the index
- Expect Seq Scan or poor index use
- Shows why column order matters
Why this is asked: Tests recognition of the weak-coverage case.

**Q4: In c054_composite_index_good_vs_bad_queries.py, which query is the "good" one and why?**
What a good answer covers:
- The query includes region (leftmost column)
- Region + shipped_at matches the index prefix
- Expect Index Scan in EXPLAIN output
Why this is asked: Confirms understanding of good composite index coverage.

### Level 2 - Mid

**Q1: Using d02_composite_indexes_story.md, what common mistake makes a composite index appear "unused"?**
What a good answer covers:
- Filtering only on the trailing column
- Ignoring the leftmost column in predicates
- Assuming index exists means it will be used
Why this is asked: Tests practical mistake recognition.

**Q2: In c054_composite_index_good_vs_bad_queries.py, why is the shipped_at-only query "bad"?**
What a good answer covers:
- It misses the leftmost column (region)
- Index prefix is not matched
- Planner falls back to Seq Scan
Why this is asked: Checks understanding of prefix requirements.

**Q3: In c053_composite_index_left_to_right.py, how would you change the index if most queries filter by first_name only?**
What a good answer covers:
- Put first_name as the leftmost column
- Consider a separate index on first_name
- Align index order with query shapes
Why this is asked: Tests index design reasoning.

**Q4: In d02_composite_indexes_story.md, why does column order matter more than people think?**
What a good answer covers:
- Indexes are sorted by the leftmost column first
- Missing the leftmost column prevents efficient lookups
- Query patterns should drive index order
Why this is asked: Reinforces the story's warning.

### Level 3 - Senior

**Q1: In c053_composite_index_left_to_right.py, what failure mode appears if most queries filter only on first_name?**
What a good answer covers:
- Composite index provides little benefit
- Planner chooses Seq Scan or weak index scan
- Performance degrades as data grows
Why this is asked: Tests scaling risk awareness.

**Q2: Using c054_composite_index_good_vs_bad_queries.py, how would you decide between a composite index and two single-column indexes?**
What a good answer covers:
- Composite index helps when filters match the prefix
- Single-column indexes help when queries are independent
- Evaluate actual query mix and selectivity
Why this is asked: Probes design tradeoffs.

**Q3: In d02_composite_indexes_story.md, how can functions on the leftmost column break the composite index?**
What a good answer covers:
- Function wrapping blocks index use on the leading column
- Index becomes ineffective for that query
- Similar to the left-to-right failure case
Why this is asked: Checks edge-case reasoning beyond simple predicates.

### Level 4 - Architect

**Q1: Using d02_composite_indexes_story.md, how does composite index design affect analytics warehouses (modeling/analytics tracks)?**
What a good answer covers:
- Composite keys can reduce scan cost on fact tables
- Index order should follow common filter dimensions
- Poor order forces full scans in large datasets
Why this is asked: Connects index design to warehouse modeling.

**Q2: In c054_composite_index_good_vs_bad_queries.py, how would you apply prefix-based indexing ideas to distributed engines (Spark track)?**
What a good answer covers:
- Partitioning order should match common filter prefixes
- Queries missing the leading partition keys scan more data
- Plan inspection still required to confirm pruning
Why this is asked: Tests cross-track system design reasoning.

---

## Topic - Covering Indexes + Index-Only Scan

### Level 1 - Starter

**Q1: In c055_covering_index_vs_normal_index.py, what is a covering index in plain language?**
What a good answer covers:
- An index that includes all columns needed by the query
- The database can satisfy the query from the index alone without touching the table
- The demo compares a normal index that requires a table fetch to one that does not
Why this is asked: Confirms the basic definition of a covering index from the demo.

**Q2: In c055_covering_index_vs_normal_index.py, why does a normal index still need to read the table?**
What a good answer covers:
- The normal index stores only the indexed column and a pointer to the row
- The query needs additional columns not present in the index
- Each matched row requires a separate heap (table) fetch
Why this is asked: Tests understanding of why index coverage matters.

**Q3: In c056_index_only_scan_demo.py, what does an Index Only Scan mean in a query plan?**
What a good answer covers:
- The engine reads all required data directly from the index
- No rows are fetched from the actual table (heap)
- The demo expects Index Only Scan when the visibility map allows it
Why this is asked: Checks recognition of the Index Only Scan plan node.

**Q4: In c056_index_only_scan_demo.py, what is the visibility map and why does it matter for Index Only Scan?**
What a good answer covers:
- It tracks which table pages have no dead tuples (are clean)
- The engine can skip the heap fetch only when visibility is confirmed
- If pages are not marked clean, the planner falls back to a heap fetch even with a covering index
Why this is asked: Surfaces the visibility map dependency shown in the demo.

### Level 2 - Mid

**Q1: In c055_covering_index_vs_normal_index.py, how do you decide which extra columns to include in a covering index?**
What a good answer covers:
- Include all columns referenced in SELECT and WHERE for the target query
- Avoid including wide or frequently updated columns to keep index size down
- Profile the query mix to choose columns that benefit multiple queries
Why this is asked: Tests practical column-selection judgment for covering indexes.

**Q2: In c056_index_only_scan_demo.py, what would cause the plan to show an Index Scan instead of an Index Only Scan?**
What a good answer covers:
- Pages that are not marked clean in the visibility map require heap fetches
- Running VACUUM marks pages clean and enables Index Only Scan
- High write rates keep pages dirty, preventing full coverage
Why this is asked: Probes awareness of when Index Only Scan can degrade.

**Q3: In c055_covering_index_vs_normal_index.py, what write-side cost does a covering index add compared to a normal index?**
What a good answer covers:
- Every INSERT, UPDATE, and DELETE must maintain the extra columns in the index
- Index size grows with the number of included columns
- High-churn columns are expensive to cover
Why this is asked: Checks understanding of the write overhead tradeoff.

**Q4: In c056_index_only_scan_demo.py, how would you confirm that an Index Only Scan is actually happening?**
What a good answer covers:
- Run EXPLAIN ANALYZE and look for the "Index Only Scan" node label
- Check the "Heap Fetches" count in the output; zero means no table reads
- Verify the visibility map is up to date by running VACUUM before testing
Why this is asked: Tests practical verification skills using plan output.

### Level 3 - Senior

**Q1: In c055_covering_index_vs_normal_index.py, when would you choose a covering index over query rewriting?**
What a good answer covers:
- When the query pattern is fixed and the column set is stable
- When the table is large and heap fetches dominate latency
- When rewriting is not possible because the query comes from an ORM or third-party tool
Why this is asked: Evaluates design judgment on when covering indexes are the right tool.

**Q2: In c056_index_only_scan_demo.py, how do high-write workloads affect the benefit of a covering index?**
What a good answer covers:
- Frequent writes keep pages dirty, blocking Index Only Scan
- VACUUM must run regularly to restore visibility and enable heap-free reads
- In write-heavy tables, the coverage benefit may rarely materialize
Why this is asked: Tests awareness of write workload impact on index effectiveness.

**Q3: In c055_covering_index_vs_normal_index.py, how would stale statistics affect the planner's choice between a normal index and a covering index?**
What a good answer covers:
- Stale stats can cause the planner to misestimate row counts and skip the better index
- Running ANALYZE updates stats so the planner sees accurate selectivity
- Both indexes must exist and be visible to the planner for it to choose correctly
Why this is asked: Probes understanding of planner dependency on current statistics.

### Level 4 - Architect

**Q1: Using c055_covering_index_vs_normal_index.py, how do covering index principles translate to columnar analytics stores or distributed query engines?**
What a good answer covers:
- Columnar stores (Parquet, Redshift, BigQuery) already store columns separately, achieving similar coverage by scanning only needed columns
- Partitioning and sort keys play the role of index coverage by limiting scanned data
- The same idea of avoiding unnecessary data reads applies at warehouse scale
Why this is asked: Connects covering index concepts to the analytics and distributed tracks.

**Q2: In c056_index_only_scan_demo.py, how would you factor covering index design into a schema that must support both high-write ingestion and low-latency read queries?**
What a good answer covers:
- Separate the write path from the read path using replication or materialized views
- Apply covering indexes on read replicas where writes are not happening
- Use table partitioning to isolate hot write partitions from read-optimized cold partitions
Why this is asked: Tests architectural thinking about reconciling write and read index needs across system layers.
