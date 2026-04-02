SAVE AS: cicd_data_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 25 Q&A pairs covering CI/CD for data pipelines, pipeline testing strategies, data contracts, and Great Expectations vs dbt tests. Group into sections: CI/CD Fundamentals (Q1-6), Testing Strategies (Q7-13), Data Contracts (Q14-18), Great Expectations vs dbt Tests (Q19-22), DataOps and Deployment Patterns (Q23-25).

Include questions on: when to run dbt tests in CI vs CD, difference between singular and generic dbt tests, what a data contract is and who owns it, GE expectations vs dbt tests (scope, triggers, audience), blue-green pipeline deploys, idempotent pipeline design, schema evolution safety, how to handle flaky data tests, testing pyramid layers for data, GitHub Actions matrix strategy for dbt, what breaks in CI when a schema changes, detecting data drift vs schema drift, data contract enforcement at ingestion vs transformation, GE checkpoint performance at scale, secrets management in CI workflows.

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
