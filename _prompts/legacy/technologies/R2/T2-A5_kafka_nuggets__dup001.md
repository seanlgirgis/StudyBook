SAVE AS: kafka_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 Kafka gotcha nuggets. Cover: consumer group rebalance storm (too many partitions + slow consumers), ISR shrink under load (acks=all + min.insync.replicas deadlock), log compaction and consumer lag interaction, __consumer_offsets topic corruption, auto.offset.reset=latest losing events on first deploy, producer buffer.memory exhaustion under backpressure, Kafka Connect offset reset gotcha, schema registry backward vs forward compatibility confusion, KRaft migration gotchas, partition count can only go up (never down), linger.ms + batch.size tradeoff, Zookeeper session timeout causing leader elections.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.
