SAVE AS: splunk_vs_elk.ipynb
PLACE IN: D:\Workspace\Technologies\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing an observability platform comparison.

TASK: Splunk vs ELK (Elasticsearch/Logstash/Kibana) vs Datadog — architecture, cost model, use case fit. Splunk live demo; ELK and Datadog as markdown comparisons.

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
1. Title + Mental Model — "Splunk vs ELK vs Datadog — Cost, Scale, Use Case"
2. Splunk live — send 100 events, run 3 SPL queries; show results; measure query time
3. Architecture Comparison table — rows: deployment model, query language, schema enforcement, ML capabilities, licensing model, cost at 100GB/day, cloud SaaS option, Citi fit
4. ELK deep dive (markdown) — Elasticsearch as distributed search engine; Logstash for ETL; Kibana for visualization; Beats as lightweight shippers; cost = infrastructure only; downside: schema-on-write for performance
5. Datadog deep dive (markdown) — APM + infrastructure + logs unified; agent-based; pay-per-host + per-GB logs; strength: correlating metrics + traces + logs; weakness: cost at scale
6. Decision Framework — "You have 10TB/day of telemetry logs, a 20-person DE team, and a FinTech regulatory requirement for 7-year retention. Which platform?" — walk through the decision
7. What Just Happened — "Splunk wins in regulated financial services because of its audit trail, RBAC, and 20+ years of financial services integrations. ELK wins when cost is the primary constraint. Datadog wins for cloud-native APM."

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed; comment them out or skip entirely
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error against the running stack
- No infinite loops — all poll/consume loops must have a termination condition

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

