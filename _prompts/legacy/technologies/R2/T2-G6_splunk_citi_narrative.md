SAVE AS: splunk_citi_narrative.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing an interview narrative document.

TASK: Write a structured interview story connecting Splunk to the Citi 6,000-endpoint telemetry system. This document is read before interviews to prep the "tell me about a monitoring system you've built" story.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

STRUCTURE:
1. The Problem — 6,000+ API endpoints, 10 events/sec each = 60,000 events/sec; need real-time alerting, 7-year retention, regulatory auditability
2. The Architecture — HEC ingest → Indexer cluster (3 nodes) → Search Head cluster → Dashboards + Alerts; include ASCII diagram
3. The Key Decisions — why Splunk over ELK (regulatory), why HEC over forwarders (latency), index design choices (citi_telemetry vs splitting by region), retention tiers (hot 7 days, warm 90 days, cold 7 years on S3)
4. The SPL Queries — 5 actual SPL queries used in production: severity distribution, endpoint storm detection, regional failure rate, SLA breach detection, alert correlation
5. The Interview Answers — 3 ready-to-deliver interview answers: "Tell me about a monitoring system", "How do you handle 60K events/sec?", "What would you do differently?"
6. The Numbers — key metrics to memorize: event rate, index size, query latency, alert response time, retention policy

CONSTRAINTS:
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

