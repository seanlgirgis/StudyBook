SAVE AS: influxdb_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep InfluxDB guide notebook.

TASK: Cover InfluxDB measurements, tags, fields, continuous queries, Flux query language, retention policies, and downsampling — all running live against the Citi telemetry InfluxDB instance.

DATASET CONTEXT — do not deviate:
- InfluxDB: localhost:8086, org=de_org, bucket=telemetry, token=de-influxdb-super-secret-token-2026
- ~5,000 metric points already seeded (measurement=telemetry, tags: endpoint_id, region, metric_name; fields: value)
- PostgreSQL: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026! (source for bulk load)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "InfluxDB — Time-Series Data Model, Flux, Retention, Downsampling"; explain the data model: measurement (table), tag (indexed string metadata), field (numeric value), timestamp; why tags are indexed and fields are not; TSM storage engine; when InfluxDB beats Postgres for time-series
2. Imports + setup (influxdb-client, client = InfluxDBClient(url="http://localhost:8086", token="de-influxdb-super-secret-token-2026", org="de_org"), no pip install); client.ping(); print "InfluxDB connected"
3. Write Data — use WriteAPI to write 1000 time-series points: for each of 10 endpoints, write 100 metric readings (latency_ms, error_rate) across last 24 hours; use Point("telemetry").tag("endpoint_id", ...).tag("region", ...).field("value", ...).time(...); verify total count with Flux query
4. Flux Query Basics — 5 Flux queries: (1) all data from last 1h; (2) filter by tag (region='APAC'); (3) mean value per 5-minute window using aggregateWindow(); (4) top 5 endpoints by max latency; (5) count alerts above threshold per hour; print results for each
5. Retention Policy — create a second bucket "telemetry_30d" with retention=30d; create task to downsample hourly means from "telemetry" into "telemetry_30d"; explain hot/warm/cold tier pattern; Citi use case: raw data 7 days, hourly rollup 90 days, daily rollup 7 years
6. Continuous Downsampling — write Flux task for P95 downsampling: every 1h, compute P95 of value per endpoint and write to "telemetry_30d"; show task creation API call; explain how this reduces storage 60× for historical queries
7. InfluxDB vs Postgres for Time-Series — run the same "hourly P95 latency per region" query on both; time both; print comparison; explain when each wins (InfluxDB: billions of points, high write rate; Postgres: <100M points, mixed OLTP/analytics)
8. What Just Happened — InfluxDB vs TimescaleDB vs Prometheus decision table; 4 interview Q&A; Citi framing: "Citi's telemetry uses InfluxDB for raw metric ingestion at 60K events/sec — TimescaleDB for analytics that need SQL joins"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

