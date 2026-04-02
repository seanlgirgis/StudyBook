# Interview Questions - Distributed

> Topics covered: partitioning
> Levels: Starter | Mid | Senior | Architect

---

## Topic - Partitioning

### Level 1 - Starter

**Q1: In d01_partitioning_story.md, what is partitioning in plain language?**
What a good answer covers:
- Split one dataset across multiple shards
- A routing rule chooses the shard
- Keys decide the destination
Why this is asked: Confirms the core definition from the story.

**Q2: In c080_partitioning_demo.py, what does balanced hash routing show?**
What a good answer covers:
- Keys spread evenly across partitions
- No single hot shard dominates
- The demo prints similar counts per partition
Why this is asked: Checks understanding of balanced distribution.

**Q3: In c080_partitioning_demo.py, what does skewed routing demonstrate?**
What a good answer covers:
- Hot keys pile onto one shard
- Other shards stay underused
- The demo shows a hot partition
Why this is asked: Verifies recognition of skewed routing.

**Q4: In d01_partitioning_story.md, what is the router rule responsible for?**
What a good answer covers:
- Mapping a key to a shard
- Ensuring consistent placement
- Determining load distribution
Why this is asked: Tests router role understanding.

### Level 2 - Mid

**Q1: In d01_partitioning_story.md, what makes a routing rule "good"?**
What a good answer covers:
- Even distribution of keys
- One shard per key lookup
- Avoids hot partitions
Why this is asked: Probes practical routing criteria.

**Q2: In c080_partitioning_demo.py, why is skewed routing dangerous?**
What a good answer covers:
- Creates a single bottleneck shard
- Limits system throughput
- Increases tail latency
Why this is asked: Tests understanding of performance impact.

**Q3: In c080_partitioning_demo.py, what mistake leads to hot partitions?**
What a good answer covers:
- Using a key with low cardinality or hot prefix
- Poorly designed routing function
- Ignoring traffic patterns
Why this is asked: Checks common partitioning mistakes.

**Q4: In d01_partitioning_story.md, what does partitioning not solve?**
What a good answer covers:
- Cross-shard joins and coordination
- Global consistency problems
- Multi-shard transactions
Why this is asked: Tests limits of partitioning.

### Level 3 - Senior

**Q1: In c080_partitioning_demo.py, how would you detect hot shards in production?**
What a good answer covers:
- Skewed traffic or storage metrics per shard
- Latency spikes on one partition
- Imbalanced key distribution logs
Why this is asked: Probes operational awareness.

**Q2: Using d01_partitioning_story.md, how would you choose a partition key for a workload with hot tenants?**
What a good answer covers:
- Use a composite key or hashing to spread hot tenants
- Avoid natural keys that cluster traffic
- Consider tenant + time to distribute load
Why this is asked: Tests design decisions for skewed workloads.

**Q3: In c080_partitioning_demo.py, what edge case appears if the routing function changes over time?**
What a good answer covers:
- Keys map to different shards
- Requires data rebalancing or dual routing
- Can cause inconsistent reads if not migrated carefully
Why this is asked: Evaluates migration risk awareness.

### Level 4 - Architect

**Q1: Using d01_partitioning_story.md, how does partitioning influence downstream analytics or warehouse modeling?**
What a good answer covers:
- Partition keys affect query pruning and scan cost
- Poor partitioning increases full scans in analytics
- Modeling must align with partitioned access patterns
Why this is asked: Connects partitioning to analytics/modeling tracks.

**Q2: In c080_partitioning_demo.py, how would you design partitioning to balance consistency and performance in distributed systems?**
What a good answer covers:
- Favor single-shard writes when possible
- Use routing to minimize cross-shard coordination
- Accept tradeoffs between strong consistency and scale
Why this is asked: Tests system design tradeoffs at scale.

---

## Topic - Consistency Models

### Level 1 - Starter

**Q1: In d02_consistency_story.md, what is strong consistency in plain language?**
What a good answer covers:
- Every read sees the latest write
- Requires coordination across replicas
- Slower but correct
Why this is asked: Checks basic definition of strong consistency.

**Q2: In d02_consistency_story.md, what is eventual consistency in plain language?**
What a good answer covers:
- Reads may be stale temporarily
- Replicas converge over time
- Faster and more available
Why this is asked: Verifies definition of eventual consistency.

**Q3: In c081_consistency_demo.py, what does a stale read look like?**
What a good answer covers:
- Replicas return older version values
- Primary read shows the newest version
- Replicas catch up after lag
Why this is asked: Ties the concept to the demo output.

**Q4: In d02_consistency_story.md, what is a causal consistency intuition?**
What a good answer covers:
- Reads respect cause-and-effect order
- If one update depends on another, that order is preserved
- It is stronger than eventual but weaker than strong
Why this is asked: Ensures the candidate can explain causal consistency.

### Level 2 - Mid

**Q1: In c081_consistency_demo.py, why do replicas return stale values initially?**
What a good answer covers:
- Replication lag delays updates
- Reads hit replicas before they apply the write
- Lag is shown with time-based updates
Why this is asked: Tests understanding of read path delays.

**Q2: In c082_cassandra_demo.py, what tradeoff appears between single-partition reads and cross-partition scans?**
What a good answer covers:
- Single-partition reads are targeted and fast
- Cross-partition scans touch many nodes
- Consistency and performance degrade with wide scans
Why this is asked: Connects access patterns to consistency tradeoffs.

**Q3: In c083_dynamodb_demo.py, why does a scan across status fields behave differently than a partition-key query?**
What a good answer covers:
- Partition-key query hits one partition
- Scan touches many partitions and is slower
- Consistency guarantees vary by access path
Why this is asked: Tests understanding of read paths.

**Q4: In d02_consistency_story.md, what is the core tradeoff between latency and correctness?**
What a good answer covers:
- Strong consistency increases latency
- Eventual consistency reduces latency but allows stale reads
- Availability improves under eventual models
Why this is asked: Probes basic consistency tradeoffs.

### Level 3 - Senior

**Q1: In c081_consistency_demo.py, how would you explain replication lag’s impact on read correctness?**
What a good answer covers:
- Reads from lagging replicas return older versions
- Lag duration defines the stale-read window
- Application must tolerate or avoid it
Why this is asked: Tests operational understanding of lag.

**Q2: In c082_cassandra_demo.py, how do quorum reads reduce stale data risk?**
What a good answer covers:
- Reading from multiple replicas increases chance of latest value
- Quorum reads balance latency and correctness
- Requires more coordination than single-replica reads
Why this is asked: Evaluates knowledge of quorum consistency.

**Q3: In c083_dynamodb_demo.py, how would you tune consistency level for hot keys?**
What a good answer covers:
- Stronger consistency for critical reads
- Eventual consistency for lower-latency reads
- Use read/write capacity tradeoffs
Why this is asked: Tests tuning decisions for key workloads.

### Level 4 - Architect

**Q1: Using c081_consistency_demo.py, how would you choose consistency levels for a partitioned system with hot shards?**
What a good answer covers:
- Hot shards need careful read/write consistency tradeoffs
- Strong consistency may bottleneck hot partitions
- Eventual consistency improves throughput with stale risk
Why this is asked: Connects consistency to partitioning tradeoffs.

**Q2: In c082_cassandra_demo.py and c083_dynamodb_demo.py, how do consistency choices influence caching strategies?**
What a good answer covers:
- Stale reads impact cache freshness
- Cache-aside must tolerate eventual consistency
- Strong consistency reduces cache invalidation complexity
Why this is asked: Links consistency models to caching and distributed design.
---

## Topic - DynamoDB Patterns

### Level 1 - Starter

**Q1: In d04_dynamodb_story.md, what is the partition key in the mailroom analogy and what does it control?**
What a good answer covers:
- The partition key is the bin label in the mailroom
- It routes items to a single partition
- It determines where reads and writes land
Why this is asked: Checks the core DynamoDB mental model from the story.

**Q2: In c083_dynamodb_demo.py, what do pk=customer_id and sk=order_ts mean for how items are stored?**
What a good answer covers:
- All orders for one customer live in the same partition
- The sort key orders those items by order_ts
- This creates a wide row per customer
Why this is asked: Verifies understanding of basic key mechanics in the demo.

**Q3: In c083_dynamodb_demo.py, why does the point read (pk + sk) touch only one partition?**
What a good answer covers:
- The partition key routes to one partition deterministically
- The sort key narrows to a single item inside the partition
- This is the fastest access pattern in the demo
Why this is asked: Confirms the mechanics of efficient DynamoDB reads.

**Q4: In d04_dynamodb_story.md, what is a GSI in plain language and why does it exist?**
What a good answer covers:
- A GSI is an extra lookup table with a different key
- It supports new access patterns not covered by the base keys
- It avoids full scans across partitions
Why this is asked: Tests basic GSI purpose from the story map.

### Level 2 - Mid

**Q1: In c083_dynamodb_demo.py, why is "orders for one customer" a good access pattern?**
What a good answer covers:
- The query hits a single partition
- Results are already ordered by the sort key
- It scales predictably with partitioned routing
Why this is asked: Probes query-driven design using the demo scenario.

**Q2: In c083_dynamodb_demo.py, what is the common mistake behind the "status = shipped" scan?**
What a good answer covers:
- The access pattern is not modeled by the primary key
- It forces a scan across many partitions
- It is slow and expensive compared to a targeted query
Why this is asked: Checks recognition of anti-patterns from the demo.

**Q3: In d04_dynamodb_story.md, how would you choose a partition key for an orders table to match access patterns?**
What a good answer covers:
- Start with the most frequent query (orders by customer)
- Use the partition key to route those queries to one partition
- Avoid keys that require full scans for common reads
Why this is asked: Tests access-pattern-first modeling.

**Q4: In c080_partitioning_demo.py, what DynamoDB mistake maps to the skewed routing example?**
What a good answer covers:
- Picking a low-cardinality or hot-prefix partition key
- Concentrating traffic on one partition (hot shard)
- Causing throttling and uneven throughput
Why this is asked: Connects partitioning mistakes to DynamoDB key design.

### Level 3 - Senior

**Q1: In c080_partitioning_demo.py, how would skewed routing show up as a hot partition in c083_dynamodb_demo.py?**
What a good answer covers:
- Many items share the same partition key, overloading one partition
- Reads and writes for that key throttle while others are idle
- The model needs a different key or additional sharding
Why this is asked: Tests hot-partition diagnosis and mitigation.

**Q2: In c083_dynamodb_demo.py, what tradeoff does the GSI-style query introduce compared to a partition-key query?**
What a good answer covers:
- GSIs add write overhead and extra storage
- They enable new targeted reads without scans
- They can shift throughput and capacity planning
Why this is asked: Evaluates GSI tradeoffs beyond the happy path.

**Q3: In c081_consistency_demo.py, how does replica lag inform DynamoDB consistency choices at scale?**
What a good answer covers:
- Eventual consistency can return stale data under lag
- Strong consistency reduces stale reads but costs latency/throughput
- The choice depends on correctness needs for the access pattern
Why this is asked: Probes consistency vs scale judgment using the demo.

### Level 4 - Architect

**Q1: Using c083_dynamodb_demo.py and c080_partitioning_demo.py, how would you design a streaming ingestion pipeline (streaming track) that avoids hot partitions while supporting point reads?**
What a good answer covers:
- Partition key design that spreads write load (hashing or bucketing)
- Streamed events land in a schema aligned with access patterns
- The pipeline enforces idempotency to avoid duplicate writes
Why this is asked: Tests cross-track integration with streaming and partitioning.

**Q2: Using c081_consistency_demo.py and d04_dynamodb_story.md, how would you integrate DynamoDB with cache-aside (cache track) while controlling stale reads at scale?**
What a good answer covers:
- Cache invalidation or TTL aligned to consistency guarantees
- Strong vs eventual reads chosen per endpoint
- The design balances latency, correctness, and cache freshness
Why this is asked: Probes system design across consistency and cache tracks.
