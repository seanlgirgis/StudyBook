SAVE AS: kafka_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 30 Q&A pairs covering Kafka internals, operations, and design decisions. Group into sections: Fundamentals (Q1-8), Replication and Durability (Q9-15), Consumer Mechanics (Q16-22), Performance and Tuning (Q23-27), Design Decisions (Q28-30).

Include questions on: ISR, exactly-once, acks settings, partition count sizing, consumer lag, log compaction vs retention, rebalancing triggers, offset management, producer batching, compression codecs, Kafka vs database queue, when to use Kafka vs Kinesis, monitoring key metrics (consumer lag, under-replicated partitions), schema registry, topic naming conventions.

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

