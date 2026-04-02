SAVE AS: keyvalue_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for key-value databases.

TASK: Generate 25 Q&A pairs covering Redis internals, caching patterns, and operational gotchas. Group into sections: Redis Internals (Q1-7), Caching Patterns (Q8-14), Data Structures and Use Cases (Q15-20), Operations and Scaling (Q21-25).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Redis: localhost:6380, password=DeRedis2026!
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: why Redis is single-threaded and why it's still fast, Redis persistence modes (RDB vs AOF vs hybrid), eviction policies and when each applies, cache-aside vs write-through vs write-behind comparison, cache stampede / thundering herd problem and prevention, TTL design for session vs reference data, Redis cluster vs Redis Sentinel vs standalone, pub/sub limitations vs Kafka (no persistence, no consumer groups), Lua script atomicity guarantee, Redis sorted set internals (skip list), RESP protocol, Redis 7 multi-part transactions (MULTI/EXEC) vs Lua, Redis vs Memcached decision (data structures vs pure cache), hot key problem and mitigation.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

