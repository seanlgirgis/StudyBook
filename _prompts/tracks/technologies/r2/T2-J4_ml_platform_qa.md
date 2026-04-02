# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-J4_ml_platform_qa.md

SAVE AS: ml_platform_qa.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A.

TASK: Generate 25 Q&A pairs. Sections: MLflow (Q1-6), Feature Stores (Q7-12), SageMaker (Q13-17), Vertex AI (Q18-20), MLOps (Q21-25).

Cover: experiment tracking vs model registry, artifact versioning, model serving patterns, feature skew detection, point-in-time join, online vs offline latency requirements, SageMaker endpoint scaling, shadow deployment, A/B testing, canary deployment, model drift detection, retraining triggers, MLOps maturity model.

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


