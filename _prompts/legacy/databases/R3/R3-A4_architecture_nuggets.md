SAVE AS: architecture_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets on database architecture and polyglot persistence.

TASK: Generate 12 database architecture gotcha nuggets covering polyglot persistence, CAP theorem misapplication, and selection anti-patterns. Cover: Postgres chosen for everything until 500M rows causes full table scans that kill the prod API (monolithic DB anti-pattern), cache-aside pattern with no TTL causing stale endpoint status in Redis long after decommission, two-phase commit blocking all participants when one node is slow causing cascading timeout in Citi's alert pipeline, Cassandra used for a use case requiring multi-row transactions leading to silent partial writes, Elasticsearch used as primary store with data loss on index corruption because no durable source of truth, polyglot stack with 6 databases where no engineer understands all 6 causing blind spots in incident response, write fan-out to 4 databases with no idempotency key causing duplicate records on retry after timeout, CAP theorem misread as "pick any 2" when partition tolerance is non-negotiable in distributed systems, schema migration on a 500K-row table with an exclusive lock causing 90-second downtime in prod, DynamoDB hot partition from non-uniform access pattern causing throttling on a single endpoint_id, InfluxDB retention policy set to infinite causing disk exhaustion after 6 months of 500K metrics/day, eventual consistency in Cassandra read after write returning stale data when consistency level is ONE.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

