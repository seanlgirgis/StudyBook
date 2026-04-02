SAVE AS: technologies_interview_sim.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a timed, self-graded Staff DE interview simulation notebook.

TASK: Generate a 60-question interview simulation notebook covering all 11 technology categories. Questions are presented in randomized order with hidden answers. Each answer includes a self-grading rubric. The final cell scores the session.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

TECH STACK CONTEXT — do not deviate:
- Kafka: localhost:9092, confluentinc/cp-kafka:7.6.0, container citi_kafka
- Spark: pyspark==3.5.4, master=local[*], JAVA_HOME=C:/Program Files/Java/jre1.8.0_481, HADOOP_HOME=C:/hadoop
- Airflow: localhost:8082, apache/airflow:2.8.0, LocalExecutor, credentials admin/admin
- MLflow: localhost:5000, SQLite backend
- dbt: C:/py_venv/proj_educate/Scripts/dbt.exe, profiles.yml at ~/.dbt/profiles.yml, project citi_dbt, target postgres
- Databricks: host=https://dbc-9f35a83d-b4e7.cloud.databricks.com, Serverless SQL Warehouse b6657f31d1e7a179
- GCP: project=citi-de-learning, key=D:/Workspace/Technologies/_setup/gcp_key.json
- Azure: subscription=b3811436-61fc-4a3a-a6a9-deb05955076d, az CLI at C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd
- AWS: profile=study, region=us-east-1, account=357811130281

SECTIONS:
1. Title + Instructions — "Staff DE Interview Simulation — 60 Questions, 60 Minutes"; instructions: read each question, answer aloud or in writing, then reveal the answer cell; score yourself 0/1 per question; target: 45/60 to pass
2. Timer Cell — Python cell using datetime: record start_time = datetime.now(); print "Simulation started at {start_time} — 60 minutes on the clock"
3. Questions 1-10 — Kafka + Streaming (5 questions each from: ISR/replication, consumer groups, Kafka vs Kinesis, exactly-once semantics, partition design); each question is a markdown cell; answer is the NEXT markdown cell headed "### Answer" — one question + one answer per pair; every answer ends with a Citi framing sentence; grading rubric: key terms to include (2-3 bullet points)
4. Questions 11-20 — Spark + Compute (shuffle/spill, AQE, structured streaming, broadcast join, performance tuning); same format
5. Questions 21-30 — Airflow + Orchestration + dbt (idempotency, executor types, incremental models, dbt tests, backfill); same format
6. Questions 31-40 — Lakehouse + Infrastructure (Delta ACID, Z-order, Iceberg vs Delta, Terraform state, K8s for DE); same format
7. Questions 41-50 — Cloud DE (Glue vs EMR, Athena cost, Lake Formation, Dataflow vs Kinesis, BigQuery vs Synapse); same format
8. Questions 51-60 — Cross-cutting (ML platform, CI/CD for data, observability, system design, modern stack choice); same format
9. Score Cell — Python cell: prompts user to enter number correct (input()); computes percentage; prints pass/fail (pass = ≥45/60); prints category breakdown hint (which question numbers map to which category); records end_time and elapsed minutes
10. Debrief Cell — markdown: top 5 most commonly missed question categories at Staff level, recommended review materials (which R2 notebooks to re-read), Citi framing: "In a real Citi Staff interview, system design counts double — always tie technical answers to scale and regulatory constraints"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- All 60 questions must be unique and Staff-level difficulty — not entry-level definitions
- Every answer must end with a Citi framing sentence
- Grading rubric: 2-3 bullet points of key terms/concepts that must appear in a passing answer

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.
