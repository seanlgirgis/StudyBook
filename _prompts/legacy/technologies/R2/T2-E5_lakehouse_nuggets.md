SAVE AS: lakehouse_nuggets.md
PLACE IN: D:\Workspace\Technologies\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets.

TASK: Generate 12 lakehouse gotcha nuggets. Cover: small file explosion after streaming writes (need OPTIMIZE AUTO), VACUUM removing files still referenced by active queries, Z-order on high-cardinality columns providing no benefit, MERGE INTO on large tables causing full scan without file skipping, Delta log checkpoint not triggering until 10 commits (log gets huge), Iceberg requiring catalog that Spark doesn't have configured, Hudi MOR read amplification surprise (2x slower reads), Unity Catalog table access from older Spark clusters bypassing UC permissions, time travel retention limited by VACUUM interval, Delta table cloning (SHALLOW vs DEEP) unexpected cost, schema evolution with type changes failing silently, partition evolution in Iceberg vs add new partition column in Delta.

DATASET CONTEXT — do not deviate:
- Database: PostgreSQL on localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- endpoints table: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- metrics table: 500,000 rows | endpoint_id (int FK), metric_name (varchar), value (float), timestamp (timestamptz)
- alerts table: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

