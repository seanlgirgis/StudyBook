SAVE AS: timeseries_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for time-series databases.

TASK: Generate 25 Q&A pairs covering InfluxDB, TimescaleDB, and time-series data modeling. Group into sections: Time-Series Data Model (Q1-6), InfluxDB (Q7-13), TimescaleDB (Q14-19), Operations and Decision (Q20-25).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: why time-series requires special storage (append-only, high ingestion, time-range queries), InfluxDB tag vs field distinction and query impact, cardinality explosion from high-cardinality tags, InfluxDB TSM storage engine compaction, Flux vs InfluxQL, downsampling strategies for retention tiers, TimescaleDB hypertable chunk exclusion mechanics, TimescaleDB continuous aggregate vs materialized view, chunk-level compression ratio expectations, time_bucket vs date_trunc difference, Prometheus vs InfluxDB for infrastructure metrics, InfluxDB vs TimescaleDB decision (no SQL joins vs SQL native), retention policy and data lifecycle design, hot partition pattern in time-series (all writes to latest chunk).

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

