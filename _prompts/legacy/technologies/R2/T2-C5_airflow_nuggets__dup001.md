SAVE AS: airflow_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 Airflow gotcha nuggets. Cover: zombie tasks from worker death (task stays running forever in UI), scheduler heartbeat timeout causing all DAGs to pause, DAG import error silently disabling the whole file, XCom storing large DataFrames causing metadata DB bloat, catchup=True on a new DAG triggering hundreds of historical runs, max_active_runs=1 causing queue buildup during backfill, FileSensor with poke_mode holding a worker slot, task retry with exponential_backoff not resetting on manual clear, DagRun created before DAG file syncs (NameError on task), pool slot exhaustion silently queuing all tasks, TriggerDagRunOperator not waiting for child DAG completion, Airflow Variables fetched in top-level DAG code run on every scheduler heartbeat.

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
