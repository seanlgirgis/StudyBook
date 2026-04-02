SAVE AS: architecture_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A on database architecture and polyglot persistence.

TASK: Generate 30 Q&A pairs covering polyglot persistence, database selection, CAP theorem, ACID vs BASE, and production architecture patterns. Group into sections: CAP & Consistency (Q1-8), ACID vs BASE (Q9-14), Polyglot Persistence Patterns (Q15-22), Database Selection Scenarios (Q23-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: CAP theorem partition tolerance always chosen in distributed systems, why CA databases still exist, ACID isolation levels and when READ COMMITTED is sufficient, BASE eventual consistency in practice (not just theory), two-phase commit cost in microservices, saga pattern vs 2PC, write fan-out to multiple DBs and idempotency, cache invalidation strategies (write-through vs write-behind vs cache-aside), polyglot persistence operational complexity (N databases = N failure modes), when to use a document store vs relational for the same data, Cassandra wide row vs Postgres partitioned table for time-series, Redis as primary store anti-pattern, choosing Elasticsearch vs Postgres ILIKE at scale, OLTP vs OLAP split decision point (row count / query pattern), event sourcing and why it pairs with append-only stores, Lambda architecture dead/alive debate, Kappa architecture tradeoffs, database-per-service microservice pattern.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

