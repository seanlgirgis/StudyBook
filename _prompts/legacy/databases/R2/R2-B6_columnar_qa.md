SAVE AS: columnar_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for columnar/OLAP databases.

TASK: Generate 30 Q&A pairs covering DuckDB, Snowflake, BigQuery, Redshift, and columnar storage internals. Group into sections: Columnar Internals (Q1-8), Snowflake (Q9-14), BigQuery (Q15-20), Redshift (Q21-26), Decision Scenarios (Q27-30).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- Source data: Citi telemetry — 10K endpoints, 500K metrics, 25K alerts
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: columnar vs row storage for aggregates, vectorized execution vs volcano model, dictionary encoding compression, run-length encoding, Snowflake virtual warehouse credit cost, Snowflake micro-partition pruning vs partitioning, Time Travel cost at enterprise scale, BigQuery on-demand vs flat-rate slot decision, BigQuery partition expiration, Redshift DISTKEY selection criteria, Redshift sort key interleaved vs compound, COPY vs INSERT for bulk load, Spectrum vs loaded table cost, DuckDB sweet spot vs Postgres, DuckDB Parquet predicate pushdown, OLAP vs OLTP workload identification.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

