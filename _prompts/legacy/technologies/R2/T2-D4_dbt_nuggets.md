SAVE AS: dbt_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 10 dbt gotcha nuggets. Cover: full-refresh cost on large incremental models (strategy matters), late-arriving data breaking incremental logic (need a lookback window), unique_key uniqueness not enforced at DB level (dbt upsert may silently duplicate), dbt test on large tables scanning full table (expensive), ephemeral model recursion depth limit, packages.yml version pinning ignored on dbt deps upgrade, dbt compile succeeds but SQL fails at runtime (Jinja renders but DB rejects), snapshot not detecting changes when check_cols has NULLs (NULL != NULL), dbt-generated model names colliding with existing DB objects, macro called in config block running at compile time not run time.

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

