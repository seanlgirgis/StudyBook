SAVE AS: ha_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets on consistency, replication, and high availability.

TASK: Generate 12 HA and consistency gotcha nuggets. Cover: Postgres replica promoted to primary while old primary comes back online causing split-brain and duplicate writes into Citi's alert table, synchronous replication enabled on a high-write metrics table causing every INSERT to wait for replica acknowledgement and halving throughput, Cassandra RF=1 in production (single point of failure) discovered only when the one node hosting a partition fails and data is permanently lost, Redis AOF disabled meaning a crash between RDB snapshots loses the last hour of endpoint cache updates, Cassandra CONSISTENCY ALL used for reads causing every query to fail when any replica is unavailable, replication slot left unmonitored growing to 50GB of WAL and filling the Postgres disk causing the primary to halt all writes, read-your-writes violated at Cassandra CONSISTENCY ONE causing an alert to appear 'open' immediately after being acknowledged (stale replica), PITR not tested until a real incident when it turns out the WAL archive job silently failed 3 weeks ago, RTO of 4 hours discovered in prod incident when the team assumed it was 15 minutes based on untested runbooks, write skew at REPEATABLE READ allowing two concurrent transactions to both move the last critical alert to 'resolved' leaving zero open critical alerts when one should remain, Redis Cluster hash slot migration during a live topology change causing 2% of keys to return MOVED errors that the application does not handle, Aurora failover taking 30 seconds during which the application has no fallback causing a visible outage in Citi's monitoring dashboard.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

