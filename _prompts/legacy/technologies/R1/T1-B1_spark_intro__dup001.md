SAVE AS: spark_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Apache Spark for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute against the real running stack.

TASK: Generate spark_intro.ipynb — a complete Jupyter notebook covering the Spark mental model,
RDD vs DataFrame, DAG execution, and first real batch job against the Citi telemetry dataset.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput

TECH STACK CONTEXT — do not deviate:
- Spark container: apache/spark:3.5.3, master UI on localhost:8081
- CRITICAL: From host notebooks use master=local[*] NOT spark://localhost:7077
  (Spark executors inside Docker cannot route traffic back to the host driver process)
- Read from Postgres via JDBC — requires postgresql JDBC jar
- JDBC jar: download from https://jdbc.postgresql.org/download/ or mvnrepository
  Use: spark.jars.packages = org.postgresql:postgresql:42.7.3

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Apache Spark — First Contact"
- 3-paragraph mental model: what Spark is, distributed in-memory processing, DAG execution
- Citi framing: "Kafka ingests 600 events/sec. Once in storage, we need to process 500,000 metric
  rows for anomaly scoring, aggregation, and reporting. This is a Spark job."
- ASCII diagram: [Postgres/S3] → [SparkSession] → [DAG: Read → Transform → Aggregate → Write] → [Output]

SECTION 2 — Install + Imports (code cell)
- pip install pyspark
- imports: pyspark.sql SparkSession, functions (col, avg, count, when, desc), types

SECTION 3 — SparkSession (code cell + markdown)
- Markdown: explain SparkSession as entry point, local[*] vs cluster mode
- Code: create SparkSession with:
  - appName="CityTelemetryFirstJob"
  - master="local[*]"
  - config spark.jars.packages = "org.postgresql:postgresql:42.7.3"
  - config spark.sql.adaptive.enabled = "true"
  - config spark.executor.memory = "1g"
- Print: spark.version and "SparkSession ready — running in local[*] mode"

SECTION 4 — Read from Postgres via JDBC (code cell + markdown)
- Markdown: explain JDBC source, pushdown predicates, fetchsize
- Code: read all 3 tables (endpoints, metrics, alerts) using spark.read.format("jdbc") with:
  url = "jdbc:postgresql://localhost:5432/de_telemetry"
  user, password from context
  fetchsize = 10000
  Store as endpoints_df, metrics_df, alerts_df
- Print schema for each: endpoints_df.printSchema(), etc.
- Print counts: f"endpoints: {endpoints_df.count()}, metrics: {metrics_df.count()}, alerts: {alerts_df.count()}"

SECTION 5 — RDD vs DataFrame Explainer (markdown cell)
- H2: "RDD vs DataFrame — which one to use"
- Table comparing: abstraction level, optimization, type safety, when to use each
- Conclusion: "Use DataFrame/Dataset API always in 2024+. RDDs are legacy."

SECTION 6 — First Transform: Endpoint Alert Summary (code cell + markdown)
- Markdown: "Group alerts by endpoint and severity, join to endpoint metadata"
- Code:
  - alert_counts = alerts_df.groupBy("endpoint_id", "severity").agg(count("*").alias("alert_count"))
  - enriched = alert_counts.join(endpoints_df, on="endpoint_id", how="left")
  - result = enriched.select("name", "region", "category", "severity", "alert_count")
               .orderBy(desc("alert_count"))
  - result.show(20, truncate=False)

SECTION 7 — Second Transform: Average Metric by Region (code cell + markdown)
- Markdown: "Aggregate 500k metric rows — show Spark's strength vs SQL"
- Code:
  - joined = metrics_df.join(endpoints_df, on="endpoint_id", how="left")
  - regional_avg = joined.groupBy("region", "metric_name") \
      .agg(avg("value").alias("avg_value"), count("*").alias("sample_count")) \
      .orderBy("region", "metric_name")
  - regional_avg.show(30, truncate=False)

SECTION 8 — Explain Plan (code cell + markdown)
- Markdown: "Spark's Catalyst optimizer rewrites your query before execution"
- Code: regional_avg.explain(mode="formatted")
- Markdown after: short explanation of what Exchange (shuffle) and HashAggregate mean

SECTION 9 — Write Output (code cell + markdown)
- Markdown: "Write results to Postgres — Spark can write back via JDBC"
- Code: write result (alert summary) to Postgres table "spark_alert_summary" using:
  - mode="overwrite"
  - JDBC with same connection params
- Print: "Written spark_alert_summary to de_telemetry"

SECTION 10 — Stop Session + Summary (code cell + markdown)
- Code: spark.stop()
- Markdown:
  - H2: "What Just Happened"
  - Bullet: read 535,000 rows in seconds, two aggregations, Catalyst plan shown, wrote back to Postgres
  - Citi tie-in: "A nightly Spark job over 500k metrics rows takes seconds. The same work in pandas
    on a single machine risks OOM and takes minutes."
  - Next: "Run spark_concepts.md then move to Round 2 for internals and tuning."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs
- master=local[*] — never spark://localhost:7077 in this notebook
- JDBC URL must be jdbc:postgresql:// not postgresql+psycopg2://
- fetchsize must be set on all reads
- spark.stop() must be the last code cell
- No placeholder credentials

ACCEPTANCE: Every code cell executes top-to-bottom. Final output: "Written spark_alert_summary to de_telemetry"

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
