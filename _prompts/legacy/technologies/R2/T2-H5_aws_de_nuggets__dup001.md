SAVE AS: aws_de_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 AWS DE gotcha nuggets. Cover: Glue DPU cost surprise from small files (1 DPU/file minimum), Athena scanning full table when partition filter not applied correctly, EMR bootstrap action failure causing silent cluster termination, Kinesis shard hot partition from non-random partition keys, Firehose delivery failure when S3 bucket policy blocks Firehose role, Lake Formation hybrid mode (IAM + LF) causing permission confusion, Athena CTAS writing unpartitioned data losing all partition savings, Glue job bookmark not resetting after schema change, EMR Serverless job queued for 5 minutes (pre-warming needed), Kinesis iterator expiry after 5 minutes of inactivity, S3 eventual consistency causing Athena to miss recently written files (older AWS), Glue catalog partition limit (1M partitions per table).

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
