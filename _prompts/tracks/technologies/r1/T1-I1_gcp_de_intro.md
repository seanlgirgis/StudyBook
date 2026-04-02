# Canonical Derived Prompt

> Source legacy: D:\StudyBook\_prompts\legacy\technologies\R1\\T1-I1_gcp_de_intro.md

SAVE AS: gcp_de_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
GCP data engineering services for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate gcp_de_intro.ipynb — a Jupyter notebook covering the GCP DE mental model,
BigQuery as the data warehouse, Cloud Storage as data lake, and Pub/Sub as the streaming layer,
using the Citi telemetry dataset.

NOTE: Uses GCP free tier. Users need a GCP account with gcloud CLI configured and billing enabled.
Resources are cleaned up at the end.

DATASET CONTEXT — do not deviate:
- Local Postgres: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: GCP alternative to the AWS stack — BigQuery instead of Athena+Redshift,
  Pub/Sub instead of Kinesis, Dataflow instead of EMR

TECH STACK CONTEXT — do not deviate:
- GCP project: read from gcloud config (gcloud config get-value project)
- Region: us-central1
- BigQuery dataset: citi_telemetry
- GCS bucket: citi-telemetry-gcs-{project_id}
- Pub/Sub topic: citi-alerts

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "GCP Data Engineering — First Contact"
- 3-paragraph mental model: GCP DE stack overview (GCS → BigQuery → Dataflow → Pub/Sub),
  BigQuery as serverless warehouse + analytics engine (no cluster), BigQuery vs Athena (BQ stores data, Athena queries S3)
- Citi framing: "GCP's edge: BigQuery is fully managed — no Glue catalog needed, no Parquet format decisions.
  Load CSV, BigQuery handles storage optimization internally."
- ASCII diagram: [Postgres] → [GCS] → [BigQuery] ← [Pub/Sub → Dataflow]

SECTION 2 — Install + Setup (code cell)
- pip install google-cloud-bigquery google-cloud-storage google-cloud-pubsub psycopg2-binary pandas pyarrow
- imports: google.cloud.bigquery, google.cloud.storage, google.cloud.pubsub_v1, psycopg2, pandas, json, os
- Code:
  import subprocess
  result = subprocess.run(["gcloud", "config", "get-value", "project"], capture_output=True, text=True)
  PROJECT_ID = result.stdout.strip()
  DATASET_ID = "citi_telemetry"
  BUCKET_NAME = f"citi-telemetry-gcs-{PROJECT_ID}"
  REGION = "us-central1"
  print(f"GCP Project: {PROJECT_ID}")
  If PROJECT_ID is empty: print gcloud auth + project setup instructions and raise ValueError

SECTION 3 — Create GCS Bucket + BigQuery Dataset (code cell + markdown)
- Markdown: "Create the GCS bucket and BigQuery dataset"
- Code:
  - storage_client.create_bucket(BUCKET_NAME, location=REGION) — handle Conflict (already exists)
  - bigquery_client.create_dataset(DATASET_ID, exists_ok=True)
  - Print: "GCS bucket {BUCKET_NAME} ready. BigQuery dataset {DATASET_ID} ready."

SECTION 4 — Load Telemetry to BigQuery (code cell + markdown)
- Markdown: H2 "Loading Data into BigQuery"
  - Explain: BigQuery accepts CSV, JSON, Parquet, Avro — we use pandas DataFrame → BigQuery native load
- Code:
  - Connect to Postgres, read endpoints and alerts into pandas DataFrames
  - Load to BigQuery using pandas_gbq or BigQuery client:
    bigquery_client.load_table_from_dataframe(df, f"{PROJECT_ID}.{DATASET_ID}.endpoints", ...)
    with WriteDisposition=WRITE_TRUNCATE
  - Wait for job completion: job.result()
  - Print: f"Loaded {len(endpoints_df)} endpoints and {len(alerts_df)} alerts to BigQuery"

SECTION 5 — BigQuery SQL Queries (code cell + markdown)
- Markdown: H2 "BigQuery — Serverless SQL at Scale"
  - Explain: Standard SQL dialect, slot-based pricing (on-demand: $5/TB), free tier: 1TB/month
- Code: use bigquery_client.query() for 3 queries:

  Query 1 — Alert counts by severity:
  ```sql
  SELECT severity, COUNT(*) as cnt
  FROM `{PROJECT_ID}.{DATASET_ID}.alerts`
  GROUP BY severity ORDER BY cnt DESC
  ```

  Query 2 — Regional alert summary with endpoint join:
  ```sql
  SELECT e.region, a.severity, COUNT(*) as alert_count
  FROM `{PROJECT_ID}.{DATASET_ID}.alerts` a
  JOIN `{PROJECT_ID}.{DATASET_ID}.endpoints` e ON a.endpoint_id = e.endpoint_id
  GROUP BY e.region, a.severity
  ORDER BY alert_count DESC
  LIMIT 20
  ```

  Query 3 — Top 10 most alerted endpoints:
  ```sql
  SELECT e.name, e.region, COUNT(*) as alert_count
  FROM `{PROJECT_ID}.{DATASET_ID}.alerts` a
  JOIN `{PROJECT_ID}.{DATASET_ID}.endpoints` e ON a.endpoint_id = e.endpoint_id
  GROUP BY e.name, e.region
  ORDER BY alert_count DESC
  LIMIT 10
  ```

  Print results of each query as formatted tables

SECTION 6 — Pub/Sub Publish (code cell + markdown)
- Markdown: H2 "Pub/Sub — GCP's Message Queue"
  - Explain: Pub/Sub = GCP's Kafka equivalent, topics + subscriptions, push vs pull,
    global by default, no partition management (handled internally)
- Code:
  - publisher = pubsub_v1.PublisherClient()
  - topic_path = publisher.topic_path(PROJECT_ID, "citi-alerts")
  - Create topic (handle AlreadyExists)
  - Create subscription: subscriber.create_subscription(sub_path, topic_path) — handle AlreadyExists
  - Publish 10 sample alert events as JSON bytes
  - Print: "Published 10 messages to citi-alerts topic"

SECTION 7 — Pub/Sub Pull (code cell)
- Code:
  - subscriber.pull(subscription=sub_path, max_messages=10)
  - Print each message's data (json.loads)
  - Acknowledge messages
  - Print: f"Pulled and acked {len(messages)} messages"

SECTION 8 — BigQuery vs Athena Comparison (markdown cell)
- H2: "BigQuery vs Athena — Staff DE Decision Matrix"
- Table:

| Feature | BigQuery | Athena |
|---------|---------|--------|
| Storage | Managed (Capacitor format) | S3 (you choose format) |
| Pricing model | $5/TB scanned (on-demand) or flat slots | $5/TB scanned |
| Schema catalog | Built-in | Glue Data Catalog |
| Streaming inserts | Native (BigQuery Storage Write API) | Not supported natively |
| ML integration | BigQuery ML (SQL to train models) | SageMaker (separate) |
| Multi-cloud | GCP only | AWS only |
| Best for | GCP shops, streaming analytics, ML SQL | AWS shops, existing S3 data lake |

SECTION 9 — Clean Up (code cell)
- Code: delete Pub/Sub subscription and topic, delete BigQuery dataset (delete_contents=True),
  delete GCS bucket and all objects
  Print: "Clean up complete — all GCP resources deleted"

SECTION 10 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: BigQuery dataset created, Postgres → BigQuery loaded, 3 SQL queries run,
  Pub/Sub topic + subscription created, 10 messages published and consumed, cleaned up
- Citi tie-in: "GCP alternative to AWS: BigQuery replaces Athena + Redshift, Pub/Sub replaces Kinesis,
  Dataflow replaces EMR. The SQL is identical — the infrastructure is different."
- Next: "Run azure_de_intro.ipynb for the third cloud, then multicloud_concepts.md."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All GCP API calls handle exceptions (AlreadyExists, NotFound) without crashing
- Pub/Sub pull loop terminates — max 10 messages
- Clean up is the mandatory final code cell
- If PROJECT_ID is empty, Section 2 raises ValueError with setup instructions

ACCEPTANCE: Every code cell executes. Section 5 prints BigQuery query results.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.


