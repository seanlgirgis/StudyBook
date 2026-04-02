SAVE AS: ml_platform_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 ML platform gotcha nuggets. Cover: training-serving skew from different feature computation code paths, feature leakage from wrong point-in-time join, model registry without data version = non-reproducible model, MLflow artifact store on local filesystem not shared across team, SageMaker endpoint cold start latency (first request after idle), online store cache invalidation causing stale features in serving, feature store TTL expiry serving null features silently, SageMaker training job timeout from default 24h limit, Vertex AI quota limits causing job queuing with no visible error, MLflow search_runs() returning max 1000 rows by default, model A/B test statistical significance requiring more traffic than expected, feature backfill corrupting online store if materialization not idempotent.

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
