SAVE AS: redis_patterns.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep Redis patterns notebook.

TASK: Cover Redis data structures, pub/sub, Lua scripts, cache-aside, write-through, and eviction strategies — all running live against the Citi telemetry Redis instance.

DATASET CONTEXT — do not deviate:
- Redis: localhost:6380, password=DeRedis2026!
- 10,000 endpoint keys already seeded (key pattern: "endpoint:{endpoint_id}", value: JSON with name, region, status, category)
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026! (source of truth)
- endpoints: 10,000 rows | metrics: 500,000 rows | alerts: 25,000 rows
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Redis — Data Structures and Caching Patterns"; explain Redis single-threaded event loop; why single-thread is fast (no lock contention); the 5 core data structures and when each fits; ASCII diagram of cache-aside pattern
2. Imports + setup (redis-py, host=localhost, port=6380, password=DeRedis2026!, decode_responses=True, no pip install); r.ping(); print "Redis connected — {r.dbsize()} keys"
3. Data Structures Deep Dive — 5 cells, one per structure: (1) String: GET/SET/INCR alert counter; (2) Hash: HSET endpoint:{id} field value, HGETALL; (3) List: LPUSH/RPOP for alert queue simulation; (4) Set: SADD/SMEMBERS/SINTER for endpoint categories; (5) Sorted Set: ZADD with latency score, ZRANGE/ZREVRANGEBYSCORE for top-10 slowest endpoints
4. Cache-Aside Pattern — implement: try GET "endpoint:{id}" → if miss, load from Postgres, SET with TTL=300s; run 100 lookups (first pass: all misses, second pass: all hits); time both passes; print "Cache hit rate: 100% on second pass | Latency: Xms vs Yms"
5. Write-Through Pattern — on every Postgres endpoint UPDATE, also SET the Redis key; demonstrate consistency; show the two-phase write; discuss failure scenario (Postgres succeeds, Redis fails)
6. Pub/Sub — PUBLISH citi.alerts.critical <JSON>; SUBSCRIBE in a separate thread; produce 10 alert events; consumer receives all 10; print "Pub/Sub: 10/10 messages delivered"; explain fire-and-forget vs Kafka (no persistence)
7. Lua Script — write a Lua script for atomic check-and-set: IF current severity < new severity THEN UPDATE; demonstrate it prevents race condition on concurrent severity escalation; r.register_script(); run with 2 concurrent threads
8. Eviction Policies — SET maxmemory-policy allkeys-lru in a test namespace; load 1000 keys; add 200 more; show key eviction; compare LRU vs LFU vs noeviction; Citi framing: "Citi's endpoint cache uses allkeys-lru — oldest unseen endpoints evicted first to fit 10K active endpoints in memory"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values (port 6380, password DeRedis2026!)
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

