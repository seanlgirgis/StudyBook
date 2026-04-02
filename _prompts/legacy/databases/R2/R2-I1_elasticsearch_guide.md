SAVE AS: elasticsearch_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep Elasticsearch guide notebook.

TASK: Cover inverted index internals, mappings, aggregations, relevance tuning, and shard management — all running live against the Citi telemetry Elasticsearch instance with 25,000 alert documents.

DATASET CONTEXT — do not deviate:
- Elasticsearch: localhost:9200, user=elastic, password=DeElastic2026!
- Index: citi-alerts | 25,000 alert documents | fields: alert_id (int), endpoint_id (int), severity (keyword), message (text), created_at (date), region (keyword)
- Kibana: localhost:5601
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Elasticsearch — Inverted Index, Relevance Scoring, Distributed Search"; explain inverted index: term → list of document IDs; TF-IDF and BM25 scoring; Lucene segment architecture; why Elasticsearch beats SQL LIKE for full-text; ASCII diagram of shard → segment → inverted index
2. Imports + setup (elasticsearch-py, client = Elasticsearch("http://localhost:9200", basic_auth=("elastic","DeElastic2026!")), no pip install); client.info(); print "ES version: {version} | citi-alerts: {count} docs"
3. Mappings Deep Dive — GET citi-alerts/_mapping; explain keyword vs text (analyzed vs not analyzed); dynamic mapping pitfalls; add a new field with explicit mapping: PUT citi-alerts/_mapping {"properties": {"endpoint_category": {"type": "keyword"}}}; show mapping explosion risk with dynamic templates
4. Query Types — 5 queries: (1) match query on message field; (2) bool query (must + filter + should); (3) multi_match across message + severity; (4) range on created_at; (5) fuzzy match for typo tolerance; print hit count + top 3 _source for each
5. Aggregations — 5 aggregations: (1) terms on severity (bucket counts); (2) date_histogram on created_at by day; (3) avg + max value per region nested in terms agg; (4) significant_terms to find terms overrepresented in CRITICAL alerts; (5) top_hits to get most recent alert per endpoint; print results
6. Relevance Tuning — explain _score; boost a field: {"match": {"severity": {"query": "critical", "boost": 3}}}; use function_score to boost recent alerts; compare result ordering with and without boost; explain when relevance matters vs when to use filter context
7. Shard and Performance — GET _cat/shards/citi-alerts?v; explain primary vs replica shards; why more shards ≠ better performance (oversharding); GET _cluster/health; force segment merge: POST citi-alerts/_forcemerge?max_num_segments=1; explain when to use it
8. What Just Happened — ES vs Splunk vs SQL LIKE decision table; 4 interview Q&A; Citi framing: "Elasticsearch powers Citi's alert search — 25K alerts full-text searchable in <50ms vs SQL LIKE taking 3s on unindexed text"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values (localhost:9200, elastic/DeElastic2026!)
- Every code cell must execute top-to-bottom without error

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

