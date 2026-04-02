SAVE AS: vector_db_guide.ipynb
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: ChatGPT (GPT-4o) — better at valid JSON notebook structure

---

You are a Senior Data Engineer writing a deep vector database guide notebook.

TASK: Cover embeddings, ANN algorithms (HNSW, IVFFlat), pgvector vs Pinecone vs Chroma, and RAG pipeline design — running live against the Citi telemetry dataset using pgvector in Postgres.

DATASET CONTEXT — do not deviate:
- PostgreSQL + pgvector: localhost:5432, db=de_telemetry, user=de_admin, password=DeAdmin2026!
- alerts: 25,000 rows | alert_id (int PK), endpoint_id (int FK), severity (varchar), message (text), created_at (timestamptz) — message field used for embeddings
- endpoints: 10,000 rows | endpoint_id (int PK), name (varchar), region (varchar), status (varchar), category (varchar)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

SECTIONS:
1. Title + Mental Model — "Vector Databases — Embeddings, ANN, and Semantic Search"; explain embedding: text → fixed-size float vector; cosine similarity vs L2 vs dot product; why exact nearest-neighbor is O(n) and why ANN (approximate) is necessary at scale; HNSW vs IVFFlat tradeoff (recall vs build time); ASCII diagram of HNSW graph layers
2. Imports + setup (psycopg2, sentence-transformers or openai embeddings, no pip install); verify pgvector: SELECT * FROM pg_extension WHERE extname='vector'; if not present: CREATE EXTENSION vector; print "pgvector ready"
3. Generate Embeddings — use sentence-transformers (model='all-MiniLM-L6-v2') to embed 1000 alert messages; each embedding is 384-dimensional; store as list of floats; print "1000 embeddings generated — shape: (1000, 384)"
4. Store in pgvector — ALTER TABLE alerts ADD COLUMN IF NOT EXISTS embedding vector(384); UPDATE 1000 alerts with their embedding vectors via psycopg2 executemany; verify: SELECT COUNT(*) FROM alerts WHERE embedding IS NOT NULL
5. HNSW vs IVFFlat Indexes — CREATE INDEX USING hnsw (embedding vector_cosine_ops); time a similarity search: SELECT message FROM alerts ORDER BY embedding <=> query_vec LIMIT 5; DROP INDEX; CREATE INDEX USING ivfflat (embedding vector_cosine_ops) WITH (lists=100); time same query; print "HNSW: Xms | IVFFlat: Yms"
6. Semantic Search — embed a natural language query: "critical network timeout error"; find 5 most similar alerts using pgvector cosine distance; print top 5 results with similarity scores; compare vs ILIKE '%timeout%' (show false negatives)
7. RAG Pipeline Design — 3-cell pipeline: (1) embed user question; (2) retrieve top-10 relevant alerts from pgvector; (3) format as context string for LLM prompt (no actual LLM call needed — show the prompt construction); explain how this enables "ask questions about your alerts"
8. pgvector vs Pinecone vs Chroma — decision table: data volume, latency, infrastructure, filtering, cost; Citi framing: "pgvector is Citi's choice for <10M vectors — no new infrastructure, SQL joins with alert metadata, ACID guarantees"

CONSTRAINTS:
- Valid .ipynb JSON — nbformat 4, all cells have source/cell_type/metadata/outputs/execution_count
- No %pip install cells — packages are pre-installed
- No placeholder credentials — use real values from context above
- Every code cell must execute top-to-bottom without error
- Use sentence-transformers for embeddings (not OpenAI API — avoids external API calls)

OUTPUT: Return ONLY the raw .ipynb JSON. No explanation, no markdown fences, no extra text.

