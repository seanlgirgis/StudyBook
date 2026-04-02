SAVE AS: widecolumn_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for wide-column databases.

TASK: Generate 10 Cassandra gotcha nuggets. Cover: tombstone accumulation from DELETE-heavy workload causing read timeout (use TTL instead), wide partition exceeding 100MB causing coordinator timeout and GC pressure, ALLOW FILTERING doing full cluster scan on multi-GB keyspace (always provide partition key), secondary index on high-cardinality column causing broadcast read to every node, gc_grace_seconds expired tombstone resurrecting deleted data after node repair, Cassandra batch statement across partitions not atomic and not efficient (it's a logged batch for consistency hints only), counter column requiring read-before-write making it slower than expected under contention, schema change propagating asynchronously causing read errors on restarted nodes before gossip converges, TRUNCATE acquiring global lock — blocking all reads and writes cluster-wide, lightweight transaction (IF NOT EXISTS) having 4× latency due to Paxos round-trip.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know Cassandra
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

