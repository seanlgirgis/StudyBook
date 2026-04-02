SAVE AS: aws_de_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 30 Q&A pairs. Sections: Glue (Q1-8), Athena (Q9-14), EMR (Q15-18), Kinesis (Q19-23), Lake Formation (Q24-27), Design Decisions (Q28-30).

Cover: Glue DPU calculation, Glue vs EMR decision, Athena partition projection, Athena query result caching, EMR Serverless vs provisioned, Kinesis shard math, Firehose buffering, KCL consumer library, Lake Formation column masking, LF vs S3 bucket policy, when to use S3 Select.

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
