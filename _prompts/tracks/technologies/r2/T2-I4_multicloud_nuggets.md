# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-I4_multicloud_nuggets.md

SAVE AS: multicloud_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 10 multi-cloud gotcha nuggets. Cover: GCP egress cost from cross-region Pub/Sub reads (always use same-region subscription), Azure pricing confusion (Synapse Dedicated Pool vs Serverless have wildly different cost models), S3 cross-region replication costing more than re-ingesting data, BigQuery slot reservation vs on-demand pricing switching mid-month, Kinesis shard cost accumulating even when idle, ADF Integration Runtime self-hosted not supporting all connectors, Dataflow job leaking (not cancelled, running forever), multi-cloud data transfer via internet vs dedicated interconnect cost difference, Azure Event Hubs Basic vs Standard partition count limit surprise, GCP service account key rotation causing pipeline failures if hardcoded.

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


