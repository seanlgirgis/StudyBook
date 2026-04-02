SAVE AS: keyvalue_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for key-value databases.

TASK: Generate 10 Redis gotcha nuggets. Cover: cache stampede when TTL expires simultaneously for popular keys (use jitter on TTL), KEYS * command blocking Redis for seconds on large keyspace (use SCAN instead), Redis pub/sub dropping messages when subscriber disconnects (no persistence), MULTI/EXEC not rolling back on command error (only syntax errors abort, logic errors don't), sorted set ZRANGEBYSCORE with large offset doing O(n) skip-list walk, Redis cluster keyslot mismatch when using multi-key commands across slots (use hashtags {user}:key pattern), AOF rewrite blocking Redis event loop during fork on large datasets, TTL not propagated on RENAME (old key TTL applied to new name), DEL inside Lua script not triggering keyspace notifications, Redis connection pool exhaustion under burst traffic causing silent timeouts.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know Redis
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

