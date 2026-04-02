SAVE AS: mongodb_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep MongoDB guide notebook.

TASK: Cover MongoDB aggregation pipeline, index types, Atlas Search, and transactions — using the Citi telemetry dataset. Connection uses MongoDB Atlas free tier with variables at top for fill-in.

CONNECTION VARIABLES (define at top — user fills after Atlas cluster creation):
MONGO_URI = "mongodb+srv://<user>:<password>@de-learning.zur1dze.mongodb.net/?appName=de-learning"
MONGO_DB = "de_telemetry"

DATASET CONTEXT — do not deviate:
- Source data: same Citi telemetry schema
- endpoints collection: 10,000 documents | endpoint_id, name, region, status, category
- metrics collection: 100,000 documents (sample) | endpoint_id, metric_name, value, timestamp
- alerts collection: 25,000 documents | alert_id, endpoint_id, severity, message, created_at
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "MongoDB — Document Model, Aggregation Pipeline, Indexes"; explain BSON document model vs relational; embedding vs referencing trade-off; when MongoDB wins (flexible schema, hierarchical data, developer velocity)
2. Imports + setup (pymongo, real URI variable, no pip install); client.admin.command('ping'); print "MongoDB Atlas connected"
3. Data Load — insert 1K endpoints, 10K metrics, 25K alerts as Python dicts; verify counts; explain document model: alerts embed endpoint name as denormalized field
4. Aggregation Pipeline — 3 pipelines: (1) $group by severity + $count + $sort for alert distribution; (2) $match + $lookup (join alerts to endpoints) + $project for top endpoints by alert count; (3) $bucket on value to bin metrics into latency tiers; print results for each
5. Index Types — create single-field index on alerts.severity; compound index on (endpoint_id, created_at); explain index: show IXSCAN vs COLLSCAN; partial index on alerts where severity='critical'; text index on alerts.message; test each with explain("executionStats")
6. Transactions — multi-document ACID transaction: insert an alert and update endpoint status atomically in a session; abort a transaction and show rollback; explain session vs non-session write; Citi use case: alert insert must update endpoint status atomically
7. Schema Design Drill — embedded vs referenced: show the same endpoint+alerts data modeled both ways; compare query patterns (all alerts for endpoint: embedded is 1 query, referenced is 2); explain the 16MB document limit
8. What Just Happened — MongoDB vs DynamoDB decision table; 4 interview Q&A; Citi framing: "MongoDB's document model fits Citi's alert metadata — each alert can carry arbitrary key-value pairs without schema migration"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- URI defined as variable at top — clearly labeled for fill-in
- Every code cell must execute top-to-bottom without error once URI is set

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

