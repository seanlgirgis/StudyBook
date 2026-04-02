SAVE AS: pipeline_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets on data pipelines and CDC.

TASK: Generate 12 pipeline gotcha nuggets covering CDC, ETL, and data movement anti-patterns. Cover: dual-write to Postgres and Elasticsearch with no transaction causing one to succeed and one to fail leaving data inconsistent, incremental load using updated_at but hard deletes are invisible so deleted rows silently persist in the warehouse, COPY from S3 to Redshift fails silently on type mismatch with no row-level error surfaced unless STL_LOAD_ERRORS is queried, pipeline watermark stored in memory resets on restart causing full re-extract of 500K rows on every deploy, Parquet written without specifying schema causing type inference to silently cast endpoint_id from UUID to string breaking downstream joins, S3 staging path without date prefix causing all pipeline runs to overwrite the same file losing historical audit trail, Debezium connector falling behind WAL causing replication slot to grow unbounded and fill Postgres disk, pipeline with no row count check shipping zero rows to Redshift silently after upstream table rename, schema migration adding NOT NULL column without default causes CDC consumer to crash on every existing row update, ETL job reading entire 500K metrics table on every run instead of using watermark burning Postgres I/O during business hours, no dead letter queue causing a single malformed alert to block the entire pipeline indefinitely, pipeline success metric measured by job exit code only — not by rows loaded — masking partial loads.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

