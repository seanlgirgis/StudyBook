SAVE AS: splunk_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Splunk for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate splunk_intro.ipynb — a Jupyter notebook covering the Splunk mental model,
HEC (HTTP Event Collector) ingestion, and first SPL queries against the Citi telemetry alerts.

NOTE: Splunk runs as a standalone Docker container (separate from the citi_tech stack).
The setup guide is at Technologies/_setup/splunk_setup.md — the notebook assumes Splunk is running.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- Citi narrative: 6,000+ API endpoints; Splunk is the SIEM/observability platform — ops and security teams live here

TECH STACK CONTEXT — do not deviate:
- Splunk: running as container citi_splunk, web UI on localhost:8000
- Splunk HEC: https://localhost:8088 (HTTPS — HTTP returns empty reply)
  Token: f9d0f92a-fcad-4a02-a76e-0b9a325cffe8 (token name: citi_telemetry_hec)
  Use verify=False in requests (self-signed cert)
- Splunk REST API: https://localhost:8089 (HTTPS, verify=False)
- Splunk credentials: admin / DeSplunk2026!
- Index name: citi_telemetry (exists — pre-created)

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Splunk — First Contact"
- 3-paragraph mental model: what Splunk is, machine data → indexed events → SPL searches,
  where Splunk fits (SIEM, operational intelligence, log aggregation)
- Citi framing: "Kafka handles stream ingestion. Splunk handles operational intelligence — ops teams
  write SPL searches to find endpoint anomalies, build dashboards, and trigger alerts in real time."
- ASCII diagram: [Postgres alerts] → [Python HEC sender] → [Splunk Indexer] → [SPL Search] → [Dashboard]

SECTION 2 — Install + Imports (code cell)
- pip install requests psycopg2-binary
- imports: requests, psycopg2, json, time, datetime

SECTION 3 — Splunk Health Check (code cell + markdown)
- Markdown: "Verify Splunk is running before we ingest data"
- Code:
  - GET https://localhost:8089/services/server/info?output_mode=json with auth=('admin','DeSplunk2026!'), verify=False
  - Print: Splunk version, build, server name
  - Note: suppress InsecureRequestWarning with requests.packages.urllib3.disable_warnings()
  - If unreachable: print "citi_splunk container not running — check docker ps"

SECTION 4 — Load Alerts from Postgres (code cell + markdown)
- Markdown: "Pull 500 alerts from Postgres — enrich with endpoint metadata"
- Code:
  - psycopg2 connect to de_telemetry
  - SELECT a.alert_id, a.endpoint_id, a.severity, a.message, a.created_at,
           e.name as endpoint_name, e.region, e.category
    FROM alerts a JOIN endpoints e USING (endpoint_id)
    ORDER BY a.created_at DESC LIMIT 500
  - Convert rows to list of dicts, timestamps to ISO strings
  - Print: f"Loaded {len(alerts)} enriched alerts from Postgres"

SECTION 5 — Send to Splunk via HEC (code cell + markdown)
- Markdown: H2 "HEC — HTTP Event Collector"
  - Explain: HEC is Splunk's high-throughput ingestion endpoint, token-based auth,
    each event is a JSON object with time/host/source/sourcetype/index/event fields
- Code:
  - HEC_URL = "https://localhost:8088/services/collector/event"
  - HEC_TOKEN = "f9d0f92a-fcad-4a02-a76e-0b9a325cffe8"
  - headers = {"Authorization": f"Splunk {HEC_TOKEN}", "Content-Type": "application/json"}
  - All requests.post calls: verify=False (self-signed cert)
  - Batch alerts in groups of 50 (one HTTP POST per batch, newline-delimited JSON events)
  - Each event formatted as:
    ```json
    {
      "time": <unix timestamp from created_at>,
      "host": "postgres-exporter",
      "source": "citi_telemetry",
      "sourcetype": "citi:alert",
      "index": "citi_telemetry",
      "event": {<alert dict>}
    }
    ```
  - Print progress every 100 events, print total at end: "Sent 500 events to Splunk HEC"

SECTION 6 — Wait for Indexing (code cell)
- Code: print("Waiting 5s for Splunk to index events..."); time.sleep(5)

SECTION 7 — SPL Queries via REST API (code cell + markdown)
- Markdown: H2 "SPL — Search Processing Language"
  - Explain: Splunk's query language, pipeline: search | transform | output
  - Base search: "index=citi_telemetry sourcetype=citi:alert"
- Code: define run_spl(query, count=20) function that:
  - POSTs to https://localhost:8089/services/search/jobs with auth=('admin','DeSplunk2026!'), verify=False
  - Body: search=query, output_mode=json, exec_mode=blocking, count=count
  - Returns parsed results
- Run 4 queries and print formatted results:

  Query 1 — Count by severity:
  `search index=citi_telemetry sourcetype=citi:alert | stats count by severity | sort -count`

  Query 2 — Count by region:
  `search index=citi_telemetry sourcetype=citi:alert | spath event.region | stats count by event.region | sort -count`

  Query 3 — Top 10 endpoints by alert count:
  `search index=citi_telemetry sourcetype=citi:alert | spath event.endpoint_name | top limit=10 event.endpoint_name`

  Query 4 — CRITICAL alerts in last 24h (use earliest=-24h):
  `search index=citi_telemetry sourcetype=citi:alert earliest=-24h | spath event.severity | search event.severity=CRITICAL | stats count`

SECTION 8 — SPL Syntax Reference (markdown cell)
- H2: "SPL — Commands You Must Know"
- Table:

| Command | What it does | Example |
|---------|-------------|---------|
| search | Filter events (implicit at start) | search severity=CRITICAL |
| stats | Aggregate (count, avg, sum, dc) | stats count by region |
| timechart | Time-series aggregation | timechart span=1h count by severity |
| eval | Compute new fields | eval is_critical=if(severity="CRITICAL",1,0) |
| rex | Extract fields with regex | rex field=message "endpoint=(?<ep>\w+)" |
| top/rare | Most/least common values | top 10 endpoint_name |
| dedup | Remove duplicate events | dedup endpoint_id |
| sort | Order results | sort -count |
| spath | Extract from nested JSON | spath event.region |
| transaction | Group events into sessions | transaction endpoint_id maxspan=1h |

SECTION 9 — Splunk UI Tour (markdown cell)
- H2: "Splunk UI — Where to Find Things"
- Bullet list:
  - http://localhost:8000 — Splunk Web (admin/CitiSplunk2026!)
  - Apps → Search & Reporting → Search bar → paste SPL queries
  - Save As → Dashboard Panel to build dashboards
  - Settings → Indexes → verify citi_telemetry index exists
  - Settings → Data Inputs → HTTP Event Collector → verify citi-hec-token is enabled
  - Data Summary → Sourcetypes → citi:alert → view your events

SECTION 10 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: Splunk mental model, HEC ingestion, 500 enriched events indexed, 4 SPL queries run,
  REST API for programmatic search
- Citi tie-in: "An ops engineer at Citi types:
  index=citi_telemetry sourcetype=citi:alert severity=CRITICAL | timechart span=15m count
  — real-time view of critical alerts per 15-minute window, no SQL, no Python."
- Next: "Run splunk_concepts.md for vocabulary, then Round 2 for SPL internals and Citi narrative."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- HEC sends must handle non-200 responses: print error and continue (never crash on one bad batch)
- run_spl function handles search errors gracefully (print error message, return empty list)
- Section 3 failure must print clear instructions before raising
- No placeholder values

ACCEPTANCE: Every code cell executes. Section 7 prints results for all 4 SPL queries.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
