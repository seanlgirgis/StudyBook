SAVE AS: columnar_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for columnar/OLAP databases.

TASK: Generate 10 columnar database gotcha nuggets covering DuckDB, Snowflake, BigQuery, and Redshift. Cover: Snowflake warehouse left running after query (credits burn at idle), BigQuery query on unpartitioned table scanning full table on every run (cost explosion), Redshift DISTKEY mismatch causing broadcast join instead of collocated join, DuckDB attached Postgres query pulling all rows before filtering (no predicate pushdown for complex expressions), Snowflake Time Travel on large table consuming 2× storage (often ignored until bill arrives), BigQuery flat-rate slots not auto-released causing over-allocation in shared reservation, Redshift VACUUM not running automatically (sort order degrades silently), DuckDB in-memory mode losing data on process exit (no persistence by default), Snowflake clustering key chosen on low-cardinality column providing no pruning benefit, BigQuery ARRAY_AGG without LIMIT causing memory-exceeded errors on large groups.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know the tool
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

