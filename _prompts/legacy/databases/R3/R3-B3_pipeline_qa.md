SAVE AS: pipeline_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A on data pipelines and CDC.

TASK: Generate 30 Q&A pairs covering CDC, ETL/ELT, batch vs streaming, pipeline reliability, and data movement patterns. Group into sections: CDC & Replication (Q1-8), ETL vs ELT (Q9-14), Batch Pipeline Design (Q15-20), Streaming Ingestion (Q21-26), Pipeline Reliability & Observability (Q27-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: WAL-based CDC vs trigger-based CDC vs polling (tradeoffs for each), Debezium connector architecture and why it uses Kafka as the transport, exactly-once vs at-least-once delivery and why exactly-once is expensive, outbox pattern guarantees vs dual-write race conditions, ETL vs ELT — when ELT wins in cloud data warehouse context, why COPY is 100× faster than INSERT for bulk Redshift loads, Parquet vs CSV for S3 staging (predicate pushdown, compression, schema evolution), incremental load watermark pattern and why deleted_at column beats hard deletes for CDC, S3 as a staging layer — atomicity and resumability benefits, partition pruning in Redshift and Snowflake and how staging partition structure affects it, schema evolution in pipelines — adding a nullable column vs renaming a column (breaking change), pipeline idempotency — why replaying the same batch twice must produce the same result, dead letter queue pattern for poison pill messages, pipeline SLA monitoring — what to alert on (row count drop, latency spike, schema drift), data quality checks in the pipeline (not after loading), Lambda architecture vs Kappa architecture tradeoffs for Citi's telemetry use case.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

