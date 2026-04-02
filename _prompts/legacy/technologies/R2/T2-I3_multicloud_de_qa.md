SAVE AS: multicloud_de_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 25 Q&A pairs. Sections: Storage (Q1-4), Compute/ETL (Q5-10), Streaming (Q11-15), Warehousing/Querying (Q16-20), Governance (Q21-23), Design Decisions (Q24-25).

Cover: S3 vs GCS vs ADLS Gen2 differences, Glue vs Dataflow vs ADF, Kinesis vs Pub/Sub vs Event Hubs, Athena vs BigQuery vs Synapse cost models, Lake Formation vs Purview vs Dataplex, egress cost trap, vendor lock-in mitigation, multi-cloud data transfer patterns.

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

