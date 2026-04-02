# Interview Questions - Cache

> Topics covered: cache aside
> Levels: Starter | Mid | Senior | Architect

---

## Topic - Cache Aside

### Level 1 - Starter

**Q1: In c070_cache_aside_demo.py, what is the cache-aside flow on a miss?**
What a good answer covers:
- Check cache first, then fetch from DB on miss
- Store the fetched value back into cache
- The demo prints a miss for the first access
Why this is asked: Confirms basic cache-aside mechanics.

**Q2: In c070_cache_aside_demo.py, why is the second request faster?**
What a good answer covers:
- It is a cache hit
- No DB sleep is incurred
- The demo shows lower timing for the hit
Why this is asked: Tests understanding of hit vs miss behavior.

**Q3: In c071_ttl_demo.py, what does TTL mean for cache entries?**
What a good answer covers:
- Entries expire after a fixed time window
- Hits happen before expiry, misses after
- The demo prints "expired" after the TTL window
Why this is asked: Checks basic TTL behavior.

**Q4: In c072_stampede_demo.py, what is a cache stampede?**
What a good answer covers:
- Many threads miss at the same time
- All hit the DB and rebuild the same key
- The demo shows multiple DB fetches without protection
Why this is asked: Verifies stampede concept from the demo.

### Level 2 - Mid

**Q1: In c070_cache_aside_demo.py, what consistency risk appears with cache-aside?**
What a good answer covers:
- Cache can serve stale data after DB changes
- Without invalidation, old values persist
- Cache-aside requires explicit update or expiry
Why this is asked: Tests understanding of cache-aside tradeoffs.

**Q2: In c071_ttl_demo.py, what happens to freshness when TTL is too long?**
What a good answer covers:
- Stale data lasts longer
- Fewer misses but less fresh data
- The demo shows hits until expiry
Why this is asked: Probes TTL tuning judgment.

**Q3: In c071_ttl_demo.py, why does the post-expiry request behave like a miss?**
What a good answer covers:
- The cache entry is expired
- The code fetches from DB again
- The demo labels this as "expired"
Why this is asked: Confirms expiry-driven misses.

**Q4: In c072_stampede_demo.py, how does the single-flight lock reduce DB load?**
What a good answer covers:
- Only one thread rebuilds the cache key
- Others wait and use the same value
- DB fetch count drops to 1
Why this is asked: Tests mitigation strategy understanding.

### Level 3 - Senior

**Q1: In c072_stampede_demo.py, what failure mode appears if the rebuild lock is too coarse?**
What a good answer covers:
- Unrelated keys can block each other
- Latency increases under load
- Single-flight should be per-key where possible
Why this is asked: Evaluates concurrency design judgment.

**Q2: Using c071_ttl_demo.py, what invalidation strategy would you add for critical updates?**
What a good answer covers:
- Write-through or explicit delete on update
- Shorter TTL for critical keys
- Event-driven invalidation where possible
Why this is asked: Tests stale-data mitigation choices.

**Q3: In c070_cache_aside_demo.py, what happens if the DB is slow and the cache is cold under load?**
What a good answer covers:
- Many misses hit the DB at once
- Latency spikes and DB load increases
- Cache warm-up or prefill can help
Why this is asked: Probes real-world failure scenario thinking.

### Level 4 - Architect

**Q1: Using c071_ttl_demo.py and c072_stampede_demo.py, how would you design TTL and stampede protection in a distributed cache?**
What a good answer covers:
- TTL must balance freshness and load
- Use per-key locks or single-flight to avoid stampedes
- Coordinate across nodes to avoid duplicate rebuilds
Why this is asked: Connects TTL and stampede protection to distributed cache design.

**Q2: In c070_cache_aside_demo.py, how does cache-aside change DB load patterns at scale?**
What a good answer covers:
- Hits shift read load from DB to cache
- Misses still hit DB, so hot keys benefit most
- Incorrect invalidation can cause thundering herd
Why this is asked: Tests system-level tradeoffs with DB load.

---

## Topic - TTL (Time-to-Live)

### Level 1 - Starter

**Q1: In c071_ttl_demo.py, what does TTL mean for a cache entry?**
What a good answer covers:
- The entry expires after a fixed time window
- Hits happen before expiry, misses after expiry
- The demo prints hit/expired status
Why this is asked: Checks basic TTL definition.

**Q2: In c071_ttl_demo.py, what happens in Scenario B before expiry?**
What a good answer covers:
- The cache returns a hit
- The value is served without a DB fetch
- The demo shows faster timing
Why this is asked: Verifies pre-expiry behavior.

**Q3: In c071_ttl_demo.py, why does Scenario C act like a miss?**
What a good answer covers:
- The cached entry has expired
- The code fetches from DB again
- Status is labeled "expired"
Why this is asked: Confirms expiration-driven miss behavior.

**Q4: In c070_cache_aside_demo.py, how does TTL relate to cache-aside?**
What a good answer covers:
- Cache-aside fills on miss, TTL controls how long it stays
- TTL can force refresh to keep data from going stale
- Both patterns are often used together
Why this is asked: Connects TTL basics to cache-aside flow.

### Level 2 - Mid

**Q1: In c071_ttl_demo.py, what tradeoff do you see when TTL is short?**
What a good answer covers:
- Fresher data but more misses
- Higher DB load due to frequent refreshes
- The demo shows misses after expiry
Why this is asked: Tests TTL tuning judgment.

**Q2: In c071_ttl_demo.py, what tradeoff do you see when TTL is long?**
What a good answer covers:
- Fewer misses and lower DB load
- Higher risk of stale data
- TTL trades freshness for speed
Why this is asked: Probes the core freshness vs load tradeoff.

**Q3: In c070_cache_aside_demo.py, how would a TTL help with consistency issues?**
What a good answer covers:
- Expiration forces eventual refresh
- Reduces duration of stale cache values
- Still requires invalidation for critical updates
Why this is asked: Checks consistency reasoning in cache-aside.

**Q4: In c071_ttl_demo.py, what mistake would make TTL tests misleading?**
What a good answer covers:
- Not waiting long enough for expiry
- Reusing a cache without resetting
- Comparing times without consistent delays
Why this is asked: Tests practical demo interpretation.

### Level 3 - Senior

**Q1: Using c071_ttl_demo.py, how would you tune TTL to avoid cache churn?**
What a good answer covers:
- Avoid too-short TTLs that cause frequent refreshes
- Use different TTLs per key based on update rate
- Balance hit rate with freshness needs
Why this is asked: Evaluates tuning for stability and cost.

**Q2: In c072_stampede_demo.py, how can TTL expiry trigger a stampede?**
What a good answer covers:
- Many clients miss at the same time after expiry
- All rebuild the key concurrently
- The demo shows unprotected rebuilds spiking DB fetches
Why this is asked: Connects TTL to stampede risk.

**Q3: In c071_ttl_demo.py, what consistency issue appears if DB updates happen within the TTL window?**
What a good answer covers:
- Cache can serve stale data until expiry
- Users see old values even after DB changes
- Requires invalidation or write-through for critical data
Why this is asked: Tests consistency awareness with TTL.

### Level 4 - Architect

**Q1: Using c070_cache_aside_demo.py and c072_stampede_demo.py, how would you design TTL strategy with stampede protection in a distributed cache?**
What a good answer covers:
- Cache-aside needs TTL to bound staleness
- Use per-key locks or single-flight across nodes
- Staggered expirations or jitter reduce synchronized misses
Why this is asked: Connects TTL, cache-aside, and stampede protection at scale.

**Q2: In c071_ttl_demo.py, how would you balance DB load versus freshness across a large fleet?**
What a good answer covers:
- Longer TTL reduces DB load but increases staleness
- Shorter TTL improves freshness but raises load
- Use tiered TTLs based on data criticality
Why this is asked: Tests system-level tradeoffs in distributed caching.

---

## Topic - Cache Stampede

### Level 1 - Starter

**Q1: In d03_stampede_story.md, what is a cache stampede in simple terms?**
What a good answer covers:
- Many requests miss at the same time
- All hit the DB for the same key
- The kitchen/waiter analogy from the story
Why this is asked: Confirms the core definition from the story.

**Q2: In c072_stampede_demo.py, what happens in Mode A (no protection)?**
What a good answer covers:
- Multiple threads rebuild the same key
- DB fetch count is greater than 1
- Demonstrates the stampede effect
Why this is asked: Tests recognition of unprotected behavior.

**Q3: In c072_stampede_demo.py, what changes in Mode B (protected)?**
What a good answer covers:
- A lock ensures only one rebuild occurs
- DB fetch count drops to 1
- Other threads reuse the rebuilt value
Why this is asked: Verifies the protection mechanism.

**Q4: In c071_ttl_demo.py, how can TTL lead to stampedes?**
What a good answer covers:
- Many requests arrive right after expiry
- All see a miss at the same time
- Triggers simultaneous rebuilds
Why this is asked: Connects TTL expiry to stampede mechanics.

### Level 2 - Mid

**Q1: In c070_cache_aside_demo.py, why does cache-aside make stampedes possible?**
What a good answer covers:
- Misses trigger DB fetches per request
- If many miss together, DB load spikes
- No built-in coordination in cache-aside
Why this is asked: Links cache-aside flow to stampede risk.

**Q2: Using d03_stampede_story.md, what is a common mistake when trying to fix stampedes?**
What a good answer covers:
- Locking too broadly and blocking unrelated keys
- Not using per-key locking or single-flight
- Forgetting to add jitter to expirations
Why this is asked: Tests practical mitigation pitfalls.

**Q3: In c072_stampede_demo.py, what tradeoff does the single-flight lock introduce?**
What a good answer covers:
- Fewer DB hits but added waiting/serialization
- Slight latency for threads waiting on the lock
- Prevents duplicate rebuild work
Why this is asked: Probes tradeoff awareness.

**Q4: In c071_ttl_demo.py, how would TTL tuning reduce stampede risk?**
What a good answer covers:
- Use jitter to avoid synchronized expirations
- Stagger TTLs by key or shard
- Balance freshness with burst load risk
Why this is asked: Tests application of TTL tuning.

### Level 3 - Senior

**Q1: In c072_stampede_demo.py, what failure mode appears if the lock is held during slow DB calls?**
What a good answer covers:
- Waiting threads pile up
- Latency spikes under contention
- Throughput drops during rebuild windows
Why this is asked: Evaluates design consequences under load.

**Q2: Using d03_stampede_story.md, when would you serve stale data instead of blocking?**
What a good answer covers:
- When freshness is less critical than availability
- To avoid blocking many readers at once
- Stale-while-revalidate as a compromise
Why this is asked: Tests decision-making for edge cases.

**Q3: In c072_stampede_demo.py, how would you detect a stampede in production?**
What a good answer covers:
- Sudden spikes in DB read traffic
- Burst of cache misses for a hot key
- Increased latency during expiry windows
Why this is asked: Probes operational detection skills.

### Level 4 - Architect

**Q1: Using c072_stampede_demo.py and c070_cache_aside_demo.py, how would you design stampede protection in a distributed cache?**
What a good answer covers:
- Per-key locks or request coalescing across nodes
- Distributed lock or single-flight service
- Coordination to avoid duplicate rebuilds
Why this is asked: Tests system-level design for stampede protection.

**Q2: In c071_ttl_demo.py, how would you balance stampede protection with DB load and cache freshness at scale?**
What a good answer covers:
- Jittered TTLs to avoid synchronized misses
- Grace periods or stale-while-revalidate
- Tune TTL based on data criticality and DB capacity
Why this is asked: Connects stampede control to freshness and load tradeoffs.

---

## Topic - Distributed Locks

### Level 1 - Starter

**Q1: In d04_locks_story.md, what is the basic purpose of a lock?**
What a good answer covers:
- Only one actor enters the critical section
- Prevents races on shared state
- The single-key mental model from the story
Why this is asked: Confirms the core definition of a lock.

**Q2: In c073_locks_demo.py, what happens without a lock in Mode A?**
What a good answer covers:
- Threads race on the counter
- Actual value is lower than expected
- Demonstrates lost updates
Why this is asked: Tests recognition of race behavior.

**Q3: In c073_locks_demo.py, what changes when a lock is used in Mode B?**
What a good answer covers:
- Updates are serialized
- Final counter matches expected
- Correctness is restored
Why this is asked: Verifies the benefit of locking.

**Q4: In d04_locks_story.md, what does a lock not do?**
What a good answer covers:
- Locks do not make work faster
- Overuse causes waiting and reduced throughput
- They only coordinate access
Why this is asked: Checks understanding of lock tradeoffs.

### Level 2 - Mid

**Q1: In c073_locks_demo.py, what is a common mistake when locking shared cache state?**
What a good answer covers:
- Locking too broadly and blocking unrelated work
- Creating a bottleneck that hurts throughput
- Treating locks as performance tools instead of correctness tools
Why this is asked: Tests practical locking mistakes.

**Q2: Using d04_locks_story.md, why do cache systems use locks around rebuilds?**
What a good answer covers:
- Rebuilds are shared critical sections
- Locks prevent duplicate or conflicting updates
- Ensure one rebuild at a time
Why this is asked: Connects locks to cache rebuild safety.

**Q3: In c072_stampede_demo.py, how is the single-flight lock similar to a distributed lock?**
What a good answer covers:
- Both restrict one rebuild at a time
- Prevent duplicate work across concurrent requests
- Reduce DB load during misses
Why this is asked: Links lock patterns across demos.

**Q4: In c071_ttl_demo.py, why can TTL expiry make lock contention worse?**
What a good answer covers:
- Many keys expire together
- Rebuild requests pile up behind a lock
- Contention increases latency
Why this is asked: Tests understanding of expiry-driven contention.

### Level 3 - Senior

**Q1: In c073_locks_demo.py, what failure mode appears if the lock holder crashes mid-update?**
What a good answer covers:
- Shared state may be left inconsistent
- Other workers can block indefinitely without timeouts
- Distributed locks need expiry/lease mechanisms
Why this is asked: Probes failure handling for locks.

**Q2: Using d04_locks_story.md, how do you decide when to lock versus redesign the workflow?**
What a good answer covers:
- Use locks for short critical sections only
- Prefer idempotency or versioning if locks are too costly
- Avoid serializing large workloads
Why this is asked: Tests design judgment around lock usage.

**Q3: In c073_locks_demo.py, what edge case can still cause incorrect counts even with locks?**
What a good answer covers:
- Using multiple processes without shared lock state
- Lock scope not covering all writers
- Non-atomic updates outside the locked block
Why this is asked: Evaluates multi-process correctness risks.

### Level 4 - Architect

**Q1: Using c073_locks_demo.py and c072_stampede_demo.py, how would you design distributed locking to prevent stampedes at scale?**
What a good answer covers:
- Per-key distributed locks with expirations/leases
- Request coalescing to reduce duplicate rebuilds
- Balance lock contention with throughput
Why this is asked: Connects locks to stampede protection in distributed systems.

**Q2: In c071_ttl_demo.py, how would you integrate locks with cache-aside and TTL across a multi-node cache cluster?**
What a good answer covers:
- TTL bounds staleness, locks coordinate rebuilds
- Cache-aside misses should use a distributed lock
- Avoid synchronized expirations with jitter
Why this is asked: Tests cross-track integration and scale considerations.
