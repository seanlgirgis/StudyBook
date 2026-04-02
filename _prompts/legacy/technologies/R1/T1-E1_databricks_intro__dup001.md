SAVE AS: databricks_intro.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

ROLE: You are a senior Data Engineer writing a Jupyter notebook for an engineer learning
Databricks and Delta Lake for the first time. You write production-quality, fully working code.
No placeholders. No TODO comments. Every cell must be executable.

TASK: Generate databricks_intro.ipynb — a Jupyter notebook covering the Databricks mental model,
Unity Catalog, Delta Lake basics, and a first pipeline using the Databricks free trial.

NOTE: Databricks is cloud-only — there is no local Docker container for this category.
The notebook guides the user through free trial setup and runs code in Databricks notebooks.
Some sections are instructional (markdown) with code meant to run IN the Databricks workspace,
not locally. Mark these clearly.

DATASET CONTEXT — do not deviate:
- We will upload a sample of our telemetry data to Databricks for this exercise
- endpoints: 10,000 rows | endpoint_id, name, region, status, category
- alerts: 25,000 rows | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: Databricks is the lakehouse platform — Spark + Delta Lake + Unity Catalog managed

STRUCTURE — produce exactly these sections in order:

SECTION 1 — Title + Mental Model (markdown cell)
- H1: "Databricks — First Contact"
- 3-paragraph mental model: what Databricks is (managed Spark + Delta + governance), lakehouse vs data lake vs warehouse,
  Unity Catalog as the governance layer
- Citi framing: "A Staff DE at Citi might be asked: 'We have 50TB of telemetry in S3. How do you organize,
  govern, and query it?' — Databricks + Delta Lake + Unity Catalog is the answer."
- ASCII diagram: [S3/ADLS] → [Delta Lake] → [Databricks Spark] → [Unity Catalog] → [Analyst/ML]

SECTION 2 — Free Trial Setup (markdown cell)
- H2: "Setting Up the Free Trial"
- Step-by-step instructions:
  1. Go to databricks.com → Try Free → choose AWS (14-day free trial)
  2. Create workspace — name it "citi-telemetry-learning"
  3. Note your workspace URL: https://<workspace-id>.cloud.databricks.com
  4. Create a Personal Access Token: User Settings → Developer → Access Tokens → Generate New Token
  5. Save token — you will need it in the next section
- Note: "The free trial includes a single-node cluster. All notebooks in this section run on that cluster."

SECTION 3 — Databricks CLI Setup (code cell + markdown)
- Markdown: "Install the Databricks CLI to interact with your workspace from the host"
- Code:
  - pip install databricks-sdk
  - Code: prompt user to set DATABRICKS_HOST and DATABRICKS_TOKEN environment variables
  - Use os.environ.get() to read them; if missing, print instructions and raise ValueError
  - Test connection: from databricks.sdk import WorkspaceClient; w = WorkspaceClient(); print(w.current_user.me())

SECTION 4 — Upload Sample Data (code cell + markdown)
- Markdown: "We export a sample of our telemetry data from local Postgres and upload to Databricks DBFS"
- Code:
  - Connect to local Postgres (localhost:5432, de_telemetry, de_admin, DeAdmin2026!)
  - Export endpoints and alerts to /tmp/endpoints.csv and /tmp/alerts.csv using psycopg2 + csv module
  - Upload to DBFS using Databricks SDK: w.dbfs.upload("/FileStore/citi/endpoints.csv", ...)
    and w.dbfs.upload("/FileStore/citi/alerts.csv", ...)
  - Print: "Uploaded endpoints.csv and alerts.csv to DBFS"

SECTION 5 — Cluster Setup (markdown cell)
- H2: "Creating a Cluster"
- Instructions: Compute → Create Compute → Single Node → Runtime 14.3 LTS (Spark 3.5, Scala 2.12)
  → Node type: smallest available (e.g., m5d.large on AWS) → Auto-terminate: 30 min
- Note cluster ID from the URL — needed for job submissions

SECTION 6 — Delta Lake First Write (markdown cell with embedded code)
- Markdown: H2 "Delta Lake — First Write"
  - This code runs IN a Databricks notebook, not locally
  - Label: "📋 Copy this code into a new Databricks notebook and run it on your cluster"
- Embedded code block (Python, formatted as a code fence):
  ```python
  # Read CSVs from DBFS into Delta tables
  endpoints = spark.read.option("header", True).option("inferSchema", True) \
      .csv("dbfs:/FileStore/citi/endpoints.csv")
  alerts = spark.read.option("header", True).option("inferSchema", True) \
      .csv("dbfs:/FileStore/citi/alerts.csv")

  # Write as Delta tables in the default schema
  endpoints.write.format("delta").mode("overwrite").saveAsTable("citi.endpoints")
  alerts.write.format("delta").mode("overwrite").saveAsTable("citi.alerts")

  print(f"endpoints: {endpoints.count()} rows written as Delta")
  print(f"alerts: {alerts.count()} rows written as Delta")
  ```

SECTION 7 — Time Travel Demo (markdown cell with embedded code)
- Markdown: H2 "Delta Lake Time Travel"
  - Explain: Delta maintains a transaction log (_delta_log), every write is a version
  - "📋 Run in Databricks notebook:"
- Embedded code:
  ```python
  # Check Delta history
  display(spark.sql("DESCRIBE HISTORY citi.alerts"))

  # Overwrite with a modified dataset (simulate a bad write)
  alerts_modified = spark.sql("SELECT *, 'CORRUPTED' AS severity FROM citi.alerts LIMIT 100")
  alerts_modified.write.format("delta").mode("overwrite").saveAsTable("citi.alerts")

  # Time travel back to version 0
  alerts_v0 = spark.read.format("delta").option("versionAsOf", 0).table("citi.alerts")
  print(f"Version 0 row count: {alerts_v0.count()}")
  print(f"Current version row count: {spark.table('citi.alerts').count()}")

  # Restore
  spark.sql("RESTORE TABLE citi.alerts TO VERSION AS OF 0")
  print("Restored to version 0")
  ```

SECTION 8 — Unity Catalog Overview (markdown cell)
- H2: "Unity Catalog — Governance Layer"
- 3-paragraph explanation: three-level namespace (catalog.schema.table), centralized access control,
  data lineage tracking, column-level masking, row-level filtering
- Citi framing: "In a regulated environment, Unity Catalog enforces that only the risk team
  can see CRITICAL alerts, while ops see all. Column masking hides PII in message field."
- Commands to know:
  - CREATE CATALOG citi_telemetry
  - CREATE SCHEMA citi_telemetry.telemetry
  - GRANT SELECT ON TABLE citi_telemetry.telemetry.alerts TO `ops-team`

SECTION 9 — First Databricks Job via SDK (code cell + markdown)
- Markdown: "Submit a job programmatically via the Databricks SDK"
- Code:
  - Use WorkspaceClient to list clusters and print cluster IDs
  - Print instructions: "Replace CLUSTER_ID below with your cluster ID from the output above"
  - Code (with CLUSTER_ID = "your-cluster-id" placeholder — mark as the ONE allowed placeholder):
    ```python
    job = w.jobs.create(
        name="citi_alert_summary",
        tasks=[{
            "task_key": "run_summary",
            "existing_cluster_id": CLUSTER_ID,
            "notebook_task": {"notebook_path": "/Users/your@email.com/alert_summary"}
        }]
    )
    print(f"Job created: {job.job_id}")
    ```

SECTION 10 — Summary (markdown cell)
- H2: "What Just Happened"
- Bullets: free trial setup, uploaded telemetry data, wrote Delta tables, time travel demo,
  Unity Catalog governance overview, job submission via SDK
- Citi tie-in: "This is the Databricks interview answer: Delta Lake for ACID on S3,
  Unity Catalog for governance, Spark for processing — all managed."
- Next: "Run lakehouse_concepts.md for Delta vs Iceberg vs Hudi comparison."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4
- Sections 6-7 code is in markdown cells as embedded fences (NOT executable code cells) — clearly labeled
- Sections 3-4 and 9 are executable code cells
- Section 3 must handle missing env vars gracefully (ValueError with instructions)
- No hardcoded tokens anywhere — always read from environment

ACCEPTANCE: Sections 3-4 and 9 execute locally. Sections 6-7 execute in Databricks.

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
