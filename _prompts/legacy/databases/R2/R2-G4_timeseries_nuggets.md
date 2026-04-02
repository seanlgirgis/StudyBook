SAVE AS: timeseries_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for time-series databases.

TASK: Generate 10 time-series database gotcha nuggets covering InfluxDB and TimescaleDB. Cover: InfluxDB cardinality explosion from putting user_id in a tag (10M unique tags → OOM), InfluxDB field key with no value stored as null breaking aggregations (use 0 not null for missing metrics), TimescaleDB continuous aggregate not refreshing until refresh policy runs (stale data after backfill), InfluxDB retention policy deleting data at chunk boundary not at exact timestamp (data may survive longer than expected), TimescaleDB compression locking chunk for writes during compression run, InfluxDB schema-on-write allowing typo field names to silently create new series, time_bucket_gapfill producing rows for intervals with no data (must filter explicitly), InfluxDB batch write silently dropping points with future timestamps beyond allowed clock skew, TimescaleDB parallel chunk scans disabled without timescaledb.max_background_workers set, InfluxDB token expiration causing silent write failures with no retry mechanism.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know time-series DBs
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

