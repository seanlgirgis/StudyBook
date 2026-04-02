# Interview Questions — Joins

> Topics covered: nested loop vs hash join · index impact on join strategy
> Levels: Starter | Mid | Senior | Architect

---

## Level 1 — Starter

**Q1: In c057, what is a nested loop join?**
What a good answer covers:
- The database iterates outer rows and probes the inner table for each row
- With an index, each probe can be fast
- The demo expects Nested Loop for a small outer set with an index
- EXPLAIN output shows a Nested Loop node in Scenario A
Why this is asked: Confirms basic understanding tied to the demo.

**Q2: In c057, what is a hash join?**
What a good answer covers:
- The database builds a hash table of one side and probes it with the other
- It is efficient for large scans without useful indexes
- Scenario B in c057 expects Hash Join without an index
- EXPLAIN output shows a Hash Join node
Why this is asked: Checks the core mechanics grounded in the script.

**Q3: What is the basic difference between nested loop and hash join in the demos?**
What a good answer covers:
- Nested loop uses repeated index lookups per outer row
- Hash join builds a hash table once and scans the other side
- The planner flips strategy based on index presence and join size
Why this is asked: Tests the core contrast with demo evidence.

**Q4: Give a simple intuition from c057 for small vs large tables.**
What a good answer covers:
- Small outer set with index favors nested loop
- Large join without index favors hash join
- The US subset is tiny so nested loop is plausible
- The full join is large so hash join wins
Why this is asked: Ensures the candidate can reason about scale.

---

## Level 2 — Mid

**Q1: In c058, when is a nested loop fast?**
What a good answer covers:
- When there is an index on the join key (orders.customer_id)
- When the outer set is small (region = 'US')
- EXPLAIN shows faster total time with the index
Why this is asked: Tests application of the index-driven fast path.

**Q2: In c057, when is a hash join better?**
What a good answer covers:
- When join scans are large and no index is usable
- Scenario B drops the index and joins the full tables
- Hash join avoids many random lookups
Why this is asked: Verifies understanding of the planner's choice.

**Q3: How does a missing index affect join choice in c057 and c058?**
What a good answer covers:
- Dropping the index shifts the plan to Hash Join
- The join becomes slower due to larger scans
- EXPLAIN ANALYZE shows higher total time without the index
Why this is asked: Tests reading of plan behavior tied to index presence.

**Q4: How do you identify join type in EXPLAIN output from these demos?**
What a good answer covers:
- Look for plan nodes labeled Nested Loop or Hash Join
- Compare Scenario A vs B to see the switch
- The join type is explicit in the plan text
Why this is asked: Checks that the candidate can read real plan output.

---

## Level 3 — Senior

**Q1: What are the memory vs CPU tradeoffs between hash join and nested loop?**
What a good answer covers:
- Hash join spends memory to build a hash table upfront
- Nested loop spends CPU on repeated lookups but can be efficient with an index
- Large scans without indexes favor hash join despite memory cost
Why this is asked: Probes tradeoff reasoning beyond basic definitions.

**Q2: How does join order impact performance in the c057/c058 setup?**
What a good answer covers:
- Choosing the smaller outer table reduces probes in nested loop
- The US subset is the natural outer side
- Bad join order can increase work and push planner to a hash join
Why this is asked: Tests understanding of join order as a performance lever.

**Q3: How can skewed data affect hash joins and planner decisions?**
What a good answer covers:
- The US region is a small skewed subset
- Hash join may be overkill for skewed selective filters
- Planner estimates can be wrong if stats are off
Why this is asked: Probes edge cases and planner misestimation risk.

---

## Level 4 — Architect

**Q1: How do join strategies in Postgres map to distributed systems like Spark?**
What a good answer covers:
- Nested loop with small outer set is similar to broadcast join
- Hash join parallels shuffle-based joins on large datasets
- Strategy choice affects network, memory, and runtime cost
- The same small-vs-large intuition from c057 applies at scale
Why this is asked: Tests system-level translation of join concepts.

**Q2: When would you redesign schema versus optimizing join queries?**
What a good answer covers:
- If joins are persistently heavy, consider denormalization for analytics
- If the issue is missing indexes, add or adjust indexes first
- The demos show how an index can flip the plan and reduce cost
- Schema changes trade write complexity for read speed
Why this is asked: Evaluates architectural judgment on performance and modeling.

---

## Topic - Nested Loop vs Hash Join (Joins Track Add-On)

### Level 1 - Starter

**Q1: In d01_joins_story.md, what is the mental model of a nested loop join?**
What a good answer covers:
- "For each outer row, look up matching inner rows"
- Works well when the outer set is small
- Fits the story definition in d01_joins_story.md
Why this is asked: Checks basic join mechanics tied to the story.

**Q2: In d01_joins_story.md, what is the mental model of a hash join?**
What a good answer covers:
- "Build a hash table, then match"
- Suited for large sets without useful indexes
- Matches the story description in d01_joins_story.md
Why this is asked: Verifies foundational hash join understanding.

**Q3: In c057_nested_loop_vs_hash_join.py, what does Scenario A demonstrate?**
What a good answer covers:
- Index on orders.customer_id is present
- Small outer set (US region) is used
- Planner chooses Nested Loop in EXPLAIN
Why this is asked: Confirms the candidate can read the demo outcome.

**Q4: In c057_nested_loop_vs_hash_join.py, what does Scenario B demonstrate?**
What a good answer covers:
- Index is dropped before the broad join
- Planner shifts to Hash Join for the large scan
- EXPLAIN shows Hash Join for the full dataset
Why this is asked: Tests recognition of the hash join case.

### Level 2 - Mid

**Q1: Using d01_joins_story.md, when does an index still not guarantee a nested loop join?**
What a good answer covers:
- Planner selects by cost, not by index existence alone
- Large outer sets can make nested loop too expensive
- Story notes join shape and selectivity matter
Why this is asked: Checks for common misconceptions about indexes.

**Q2: In c057_nested_loop_vs_hash_join.py, why does the small US filter matter for join strategy?**
What a good answer covers:
- It shrinks the outer set dramatically
- Fewer probes make nested loop cheaper
- It aligns with Scenario A's plan choice
Why this is asked: Evaluates understanding of selectivity impact.

**Q3: In c057_nested_loop_vs_hash_join.py, what tradeoff is being made by dropping the index before Scenario B?**
What a good answer covers:
- Removes random index lookups in favor of a full scan
- Enables hash join to be cheaper for large datasets
- Demonstrates planner shifting strategies based on cost
Why this is asked: Tests application and tradeoff reasoning.

**Q4: Using d01_joins_story.md, what is a common mistake when diagnosing join slowness?**
What a good answer covers:
- Assuming the same plan will hold as data grows
- Ignoring selectivity and join order effects
- Failing to verify the actual plan with EXPLAIN
Why this is asked: Probes practical debugging awareness.

### Level 3 - Senior

**Q1: In c057_nested_loop_vs_hash_join.py, what failure mode appears if statistics are stale?**
What a good answer covers:
- Planner may misestimate selectivity
- Could choose nested loop when hash join is cheaper (or vice versa)
- Leads to slow performance despite the same query
Why this is asked: Tests understanding of planner dependencies.

**Q2: Using d01_joins_story.md, how would you decide the outer vs inner table in a nested loop?**
What a good answer covers:
- Choose the smaller, more selective outer table
- Reduce the number of index probes
- Aligns with the story's "tiny outer set" guidance
Why this is asked: Evaluates join order design decisions.

**Q3: In c057_nested_loop_vs_hash_join.py, what edge case makes nested loop unexpectedly slow even with an index?**
What a good answer covers:
- Outer set is larger than expected
- Index lookups become too many random reads
- Hash join becomes cheaper for the broad join
Why this is asked: Checks performance reasoning in edge conditions.

### Level 4 - Architect

**Q1: Using d01_joins_story.md, how do join strategy choices map to distributed systems (Spark track)?**
What a good answer covers:
- Nested loop with tiny outer set resembles broadcast join
- Hash join maps to shuffle-based joins at scale
- The same selectivity and size tradeoffs apply
Why this is asked: Connects joins to the Spark basics track.

**Q2: In c057_nested_loop_vs_hash_join.py, how would join strategy choices affect analytics modeling (modeling/analytics tracks)?**
What a good answer covers:
- Expensive joins may drive denormalization in star schemas
- Indexing and join design affect warehouse query cost
- The demo shows how plan shifts change performance
Why this is asked: Tests cross-track architectural reasoning.

---

## Topic - Join With Index vs Without

### Level 1 - Starter

**Q1: In d01_joins_story.md, why can the same JOIN feel fast in one environment and slow in another?**
What a good answer covers:
- Join strategy changes as data grows
- Planner chooses by cost, not by SQL text alone
- Index presence can flip the strategy
Why this is asked: Confirms basic join variability from the story.

**Q2: In c058_join_with_index_vs_without.py, what does the index on orders.customer_id change?**
What a good answer covers:
- Enables faster lookup on the join key
- Reduces total time for the join in Case A
- Influences the planner to pick a cheaper plan
Why this is asked: Checks understanding of index impact in the demo.

**Q3: In c058_join_with_index_vs_without.py, what happens in Case B after the index is dropped?**
What a good answer covers:
- The join becomes slower
- Planner is more likely to use a Hash Join
- EXPLAIN ANALYZE shows higher total time
Why this is asked: Verifies the without-index behavior in the demo.

**Q4: In d01_joins_story.md, what is the simple fix when lookups are selective?**
What a good answer covers:
- Add the right index
- Use the index to make join probes cheaper
- Accept that the planner still chooses by cost
Why this is asked: Tests basic remediation guidance from the story.

### Level 2 - Mid

**Q1: In c058_join_with_index_vs_without.py, why is the WHERE c.region = 'US' filter important for the index case?**
What a good answer covers:
- It makes the outer set small
- Fewer rows means fewer index probes
- This makes the indexed plan cheaper
Why this is asked: Probes selectivity-driven performance reasoning.

**Q2: Using d01_joins_story.md, what common mistake do teams make when they add an index expecting guaranteed speedups?**
What a good answer covers:
- Assuming the index forces a specific join strategy
- Ignoring planner cost estimates and join shape
- Not checking the actual plan with EXPLAIN
Why this is asked: Checks for real-world misconceptions.

**Q3: In c058_join_with_index_vs_without.py, what tradeoff do you accept when adding the index?**
What a good answer covers:
- Faster reads for the join query
- Extra write cost to maintain the index
- Storage overhead for the index structure
Why this is asked: Tests understanding of index tradeoffs.

**Q4: In c058_join_with_index_vs_without.py, what would be a mistake when comparing Case A and Case B results?**
What a good answer covers:
- Comparing without resetting data or stats
- Ignoring that EXPLAIN ANALYZE includes execution time
- Assuming the plan never changes as data grows
Why this is asked: Verifies correct interpretation of the demo.

### Level 3 - Senior

**Q1: In c058_join_with_index_vs_without.py, what failure mode appears if table statistics are stale?**
What a good answer covers:
- Planner may underestimate or overestimate selectivity
- It may choose the wrong plan (nested loop vs hash join)
- Performance can regress despite the index
Why this is asked: Tests plan stability awareness.

**Q2: Using d01_joins_story.md, when would you accept a hash join even if an index exists?**
What a good answer covers:
- When the join scans a large portion of the table
- When index probes would be too many random reads
- Planner cost model can favor a hash join in that case
Why this is asked: Checks nuanced plan selection judgment.

**Q3: In c058_join_with_index_vs_without.py, how would you validate that the index is actually being used?**
What a good answer covers:
- Inspect EXPLAIN ANALYZE output for index scan usage
- Compare total time and plan nodes between cases
- Confirm the join type and access paths
Why this is asked: Tests practical plan verification skills.

### Level 4 - Architect

**Q1: Using c058_join_with_index_vs_without.py, how do index-driven join choices affect analytics warehouse modeling (modeling/analytics tracks)?**
What a good answer covers:
- Heavy joins can push denormalization for read speed
- Index strategy can reduce join cost in normalized models
- The demo shows how plan shifts impact performance
Why this is asked: Connects join performance to data modeling decisions.

**Q2: In d01_joins_story.md, how would you apply join strategy thinking to distributed processing (Spark track)?**
What a good answer covers:
- Indexes are replaced by partitioning and broadcast choices
- Small filtered sets map to broadcast joins
- Large joins map to shuffle-based hash joins
Why this is asked: Tests cross-track system design reasoning.
