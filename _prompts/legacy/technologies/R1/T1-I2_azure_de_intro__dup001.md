SAVE AS: azure_de_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Azure data engineering services for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must execute.

TASK: Generate azure_de_intro.ipynb — a Jupyter notebook covering the Azure DE mental model,
Azure Data Lake Storage Gen2, Azure Synapse Analytics, and Event Hubs, using the Citi telemetry dataset.

NOTE: Uses Azure free tier or student account. Users need az CLI configured (az login).
Resources are created in a new resource group and cleaned up at the end.

DATASET CONTEXT — do not deviate:
- Local Postgres: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: Azure alternative to AWS/GCP — ADLS Gen2 + Synapse + Event Hubs + Data Factory

TECH STACK CONTEXT — do not deviate:
- Azure CLI configured (az login)
- Resource group: citi-telemetry-rg, location: eastus
- Storage account: cititelemetry{random_suffix} (must be globally unique, lowercase, no hyphens, max 24 chars)
- ADLS Gen2 container: telemetry
- Synapse workspace: citi-synapse-{suffix}
- Event Hubs namespace: citi-events-{suffix}

NOTEBOOK STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Azure Data Engineering — First Contact"
- 3-paragraph mental model: Azure DE stack (ADLS Gen2 → Synapse → Data Factory → Event Hubs),
  ADLS Gen2 = Azure Blob + hierarchical namespace (POSIX-like paths), Synapse = unified analytics
  (SQL + Spark + Data Factory in one workspace)
- Citi framing: "Many financial institutions are Azure-first due to Microsoft enterprise agreements.
  Citi uses Azure Synapse for SQL Analytics and ADLS Gen2 as the data lake foundation."
- ASCII diagram: [Postgres] → [ADLS Gen2] → [Synapse SQL] ← [Event Hubs → Synapse Streaming]

SECTION 2 — Install + Setup (code cell)
- pip install azure-storage-file-datalake azure-eventhub azure-identity psycopg2-binary pandas
- imports: azure.storage.filedatalake, azure.eventhub, azure.identity, psycopg2, pandas, json, os, subprocess, random, string
- Code:
  result = subprocess.run(["az", "account", "show", "--query", "id", "-o", "tsv"], capture_output=True, text=True)
  SUBSCRIPTION_ID = result.stdout.strip()
  If empty: print az login instructions and raise ValueError
  SUFFIX = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
  RG_NAME = "citi-telemetry-rg"
  STORAGE_NAME = f"cititelemetry{SUFFIX}"
  LOCATION = "eastus"
  print(f"Subscription: {SUBSCRIPTION_ID}, Suffix: {SUFFIX}")

SECTION 3 — Create Resource Group + ADLS Gen2 (code cell + markdown)
- Markdown: "Create Azure resources via CLI (subprocess) and Python SDK"
- Code using subprocess for CLI commands:
  - az group create --name citi-telemetry-rg --location eastus
  - az storage account create --name {STORAGE_NAME} --resource-group citi-telemetry-rg
    --location eastus --sku Standard_LRS --kind StorageV2
    --hns true (hierarchical namespace = ADLS Gen2)
  - Get storage account key: az storage account keys list ...
  - Create container: az storage container create --name telemetry --account-name {STORAGE_NAME} ...
  - Print: "ADLS Gen2 account {STORAGE_NAME} ready with container 'telemetry'"

SECTION 4 — Upload Telemetry to ADLS Gen2 (code cell + markdown)
- Markdown: H2 "ADLS Gen2 — Azure Data Lake Storage"
  - Explain: hierarchical namespace enables folder operations (rename, atomic move), POSIX ACLs,
    Parquet on ADLS Gen2 = Azure's equivalent of Parquet on S3
- Code:
  - Connect to Postgres, read endpoints and alerts into pandas DataFrames
  - Convert to Parquet bytes (io.BytesIO)
  - Use DataLakeFileClient to upload:
    - telemetry/endpoints/endpoints.parquet
    - telemetry/alerts/alerts.parquet
  - Print: f"Uploaded {len(endpoints_df)} endpoints and {len(alerts_df)} alerts to ADLS Gen2"

SECTION 5 — Synapse Serverless SQL Overview (markdown cell)
- H2: "Azure Synapse — Serverless SQL"
  - Explain: Synapse Serverless SQL Pool can query ADLS Gen2 directly via OPENROWSET (like Athena),
    no data movement, pay per TB scanned, native Parquet/Delta support
  - Full Synapse workspace setup requires Azure portal — show the SQL that would run in Synapse Studio:

  Embedded SQL code fence (labeled "Run in Synapse Studio"):
  ```sql
  -- Create external data source pointing to ADLS Gen2
  CREATE EXTERNAL DATA SOURCE CityTelemetry
  WITH (
      LOCATION = 'https://{STORAGE_NAME}.dfs.core.windows.net/telemetry'
  );

  -- Query Parquet files directly
  SELECT severity, COUNT(*) as cnt
  FROM OPENROWSET(
      BULK 'alerts/alerts.parquet',
      DATA_SOURCE = 'CityTelemetry',
      FORMAT = 'PARQUET'
  ) AS alerts
  GROUP BY severity
  ORDER BY cnt DESC;
  ```
  - Note: "Create a free Synapse workspace at portal.azure.com — takes 5 minutes"

SECTION 6 — Event Hubs (code cell + markdown)
- Markdown: H2 "Azure Event Hubs — Kafka-Compatible Streaming"
  - Explain: Event Hubs = Azure's Kafka equivalent, Kafka protocol compatible (can use confluent-kafka
    client against Event Hubs), partition-based, consumer groups, retention up to 7 days,
    Event Hubs Premium = exactly-once semantics
- Code:
  - az eventhubs namespace create --name citi-events-{SUFFIX} --resource-group citi-telemetry-rg --sku Basic
  - az eventhubs eventhub create --name citi-alerts --namespace-name citi-events-{SUFFIX} --resource-group citi-telemetry-rg --partition-count 2
  - Get connection string: az eventhubs namespace authorization-rule keys list ...
  - Use EventHubProducerClient to send 10 sample alert events as JSON bytes
  - Print: "Sent 10 events to Event Hubs citi-alerts"

SECTION 7 — Event Hubs Consumer (code cell)
- Code: use EventHubConsumerClient to receive events (consumer group $Default)
  - on_event callback prints decoded JSON
  - receive with max_wait_time=5
  - Print: f"Received {count} events from Event Hubs"

SECTION 8 — Azure DE Service Map (markdown cell)
- H2: "Azure vs AWS vs GCP — Service Mapping"
- Table:

| Function | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Object storage | S3 | Blob Storage | Cloud Storage |
| Data lake | S3 + Lake Formation | ADLS Gen2 | GCS + Data Catalog |
| Serverless SQL | Athena | Synapse Serverless | BigQuery |
| Managed Spark | EMR | Synapse Spark / Databricks | Dataproc |
| ETL/pipeline | Glue ETL | Azure Data Factory | Cloud Dataflow |
| Event streaming | Kinesis | Event Hubs | Pub/Sub |
| Data warehouse | Redshift | Synapse Dedicated Pool | BigQuery |
| Governance | Lake Formation | Microsoft Purview | Dataplex |

SECTION 9 — Clean Up (code cell)
- Code: az group delete --name citi-telemetry-rg --yes --no-wait
  Print: "Resource group citi-telemetry-rg deletion initiated (runs in background)"

SECTION 10 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: ADLS Gen2 + resource group, Postgres → ADLS Gen2, Synapse SQL shown, Event Hubs created,
  10 events published and consumed, cleaned up
- Citi tie-in: "Azure is Citi's primary cloud in EMEA. ADLS Gen2 + Synapse + ADF is the standard
  Citi data platform — the same pattern as AWS but with Microsoft tooling."
- Next: "Run multicloud_concepts.md for service mapping and when to choose which cloud."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- All subprocess CLI calls: capture_output=True, text=True
- Section 2 raises ValueError with instructions if az login not configured
- Clean up (Section 9) is mandatory final code cell
- STORAGE_NAME must be <= 24 chars, no hyphens — enforce this in code

ACCEPTANCE: Every code cell executes. Section 4 uploads to ADLS Gen2. Section 6 sends events.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
