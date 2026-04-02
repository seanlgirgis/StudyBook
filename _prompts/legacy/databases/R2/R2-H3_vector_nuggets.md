SAVE AS: vector_nuggets.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing gotcha nuggets for vector databases.

TASK: Generate 10 vector database gotcha nuggets covering pgvector, Pinecone, and general embedding patterns. Cover: HNSW index build failing silently when maintenance_work_mem is too low (increase to 1GB+ before indexing), IVFFlat requiring ANALYZE after data load or lists parameter is ignored, embedding model version change invalidating all stored vectors (must re-embed entire corpus), pgvector cosine distance returning wrong results when vectors are not normalized (use l2_normalize or vector_cosine_ops), metadata filtering post-ANN retrieval reducing recall below acceptable threshold (use pre-filtering with vector DB that supports it natively), Pinecone upsert silently overwriting existing vector when ID matches (idempotent but lossy for incremental updates), dimensionality mismatch between query vector and index not raising error in all clients (silent wrong results), pgvector exact scan (no index) faster than HNSW for small tables (<10K rows) — index adds overhead, RAG chunk size mismatch causing irrelevant context retrieval (too large = noise, too small = missing context), vector index not used for ORDER BY + LIMIT pattern without explicit index scan hint in some Postgres versions.

DATASET CONTEXT — do not deviate:
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

CONSTRAINTS:
- Each nugget: title + 2-sentence setup + 1-sentence fix/lesson
- Gotcha framing — something that bites engineers who think they know vector search
- Citi framing woven naturally into setup or fix sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

