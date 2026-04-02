# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R2\\T2-G5_splunk_nuggets.md

SAVE AS: splunk_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 10 Splunk gotcha nuggets. Cover: license throttling from noisy index (all searches return 0 results), spath not working on nested JSON (need spath event.field for HEC events, but flat dict needs spath field directly), summary index vs report acceleration tradeoffs, SPL stats count vs count(*) difference, props.conf LINE_BREAKER causing multi-line event merging, HEC token scoped to wrong index, sourcetype AUTO_KV not parsing fields because of custom delimiter, search-time field extraction vs index-time (performance vs flexibility), Splunk free license 500MB/day limit causing indexing pause, summary index not being searched by default (need index=summary explicitly).

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


