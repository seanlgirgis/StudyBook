# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-A1_kafka_intro.md

SAVE AS: kafka_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Apache Kafka for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against the real running stack.

TASK: Generate kafka_intro.ipynb — a complete Jupyter notebook covering the Kafka mental model,
core concepts, and first real produce/consume cycle against the Citi telemetry dataset.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

TECH STACK CONTEXT — do not deviate:
- Kafka: localhost:9092, confluentinc/cp-kafka:7.6.0, container name citi_kafka
- All credentials in Technologies/_setup/tech.env

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Apache Kafka — First Contact"
- 3-paragraph mental model: what Kafka is, why it exists, where it fits in a DE stack
- Citi framing: "In Citi's telemetry system, 6,000+ endpoints emit latency and error events continuously.
  A database cannot absorb that write rate without becoming a bottleneck. Kafka decouples producers
  (monitoring agents) from consumers (alerting, analytics, ML pipelines)."
- Diagram in ASCII art showing: [Monitoring Agent] → [Kafka Topic] → [Alerting Consumer] / [Analytics Consumer]

SECTION 2 — Install + Imports (code cell)
- pip install confluent-kafka psycopg2-binary
- imports: confluent_kafka Producer/Consumer, psycopg2, json, time, datetime, uuid

SECTION 3 — Config (code cell)
- KAFKA_CONFIG dict: bootstrap.servers=localhost:9092
- PG_CONFIG dict: host, port, dbname, user, password (use real values from context)
- Print confirmation: "Kafka bootstrap: {KAFKA_CONFIG['bootstrap.servers']}"

SECTION 4 — Topic Setup (code cell + markdown)
- Markdown: explain topics, partitions, replication factor
- Code: use confluent_kafka.admin.AdminClient to create topic "citi.alerts" with
  num_partitions=3, replication_factor=1
- Print result: "Topic citi.alerts created (3 partitions, RF=1)"
- Handle case where topic already exists gracefully (print "already exists — OK")

SECTION 5 — Load Alerts from Postgres (code cell + markdown)
- Markdown: "We pull 100 HIGH/CRITICAL alerts from Postgres to produce into Kafka"
- Code: connect to Postgres, SELECT 100 alerts WHERE severity IN ('HIGH','CRITICAL'),
  convert to list of dicts with json-serializable values (timestamps → isoformat strings)
- Print: f"Loaded {len(alerts)} alerts from Postgres"

SECTION 6 — Producer (code cell + markdown)
- Markdown: explain producer, serialization, delivery callback
- Code:
  - delivery_callback(err, msg) function that prints ✓ or ✗ per message
  - Create Producer with KAFKA_CONFIG
  - Produce all 100 alerts to topic "citi.alerts", key=str(alert_id), value=json.dumps(alert)
  - producer.flush()
  - Print: "Produced 100 alerts to citi.alerts"

SECTION 7 — Consumer (code cell + markdown)
- Markdown: explain consumer groups, offsets, poll loop
- Code:
  - Create Consumer with bootstrap.servers, group.id="notebook-group-1", auto.offset.reset=earliest
  - Subscribe to ["citi.alerts"]
  - Poll loop: poll(timeout=1.0), consume up to 100 messages, break when no more messages for 3s
  - Decode each message: json.loads(msg.value())
  - Print first 5 consumed messages as formatted JSON
  - consumer.close()
  - Print: f"Consumed {count} messages from citi.alerts"

SECTION 8 — Offset Exploration (code cell + markdown)
- Markdown: explain what offsets are and why they matter for replay/recovery
- Code: use AdminClient to list topic offsets for citi.alerts (all 3 partitions)
  Print: "Partition 0: offset X, Partition 1: offset Y, Partition 2: offset Z"

SECTION 9 — Key Insight Summary (markdown cell)
- H2: "What Just Happened"
- Bullet list of 5 insights: topic as durable log, consumer group isolation, offset as bookmark,
  replication factor vs availability, why Kafka beats a database queue for this use case
- Citi tie-in: "This pattern scales to 6,000 endpoints emitting every 10 seconds = 600 events/sec.
  Kafka handles this trivially. A Postgres INSERT loop would not."

SECTION 10 — Next Steps (markdown cell)
- "Run kafka_concepts.md to lock in the vocabulary"
- "T1-A2 is next — concept definitions before the deep dive in Round 2"

CONSTRAINTS:
- Valid .ipynb JSON — 4-space indented, nbformat 4, all cells have source/cell_type/metadata/outputs
- All code cells: language python, kernel python3
- No placeholder credentials or table names
- Delivery callback must not crash on error — always print either ✓ or ✗
- Consumer poll loop must terminate — do not produce an infinite loop
- All imports at top of their respective cells, not scattered

ACCEPTANCE: Every code cell executes top-to-bottom without error against the running stack.
Final output shows "Consumed 100 messages from citi.alerts".

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


