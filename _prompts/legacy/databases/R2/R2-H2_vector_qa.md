SAVE AS: vector_qa.md
PLACE IN: D:\Workspace\Basics\Databases\
TOOL: Either (ChatGPT or Gemini)

---

You are a Senior Data Engineer writing Staff-level interview Q&A for vector databases.

TASK: Generate 20 Q&A pairs covering embeddings, ANN algorithms, vector database design, and RAG pipelines. Group into sections: Embeddings and Similarity (Q1-6), ANN Algorithms (Q7-12), Vector DB Design (Q13-16), RAG and Production (Q17-20).

Every answer ends with a Citi framing sentence.

DATASET CONTEXT — do not deviate:
- pgvector on PostgreSQL: localhost:5432 | 25,000 alert embeddings (384-dimensional)
- Citi narrative: 6,000+ API endpoints monitored for latency, error rate, throughput; alerts escalate through severity tiers

Include questions on: embedding model selection (MiniLM vs text-embedding-3-small trade-off), cosine similarity vs L2 distance vs dot product — when each applies, HNSW algorithm mechanics (hierarchical layers, ef_construction trade-off), IVFFlat k-means clustering and nprobe parameter, recall vs latency trade-off at scale, why exact nearest neighbor is impractical at 10M+ vectors, pgvector vs dedicated vector DB decision (Pinecone, Weaviate, Qdrant), metadata filtering in vector search (pre-filter vs post-filter), RAG retrieval pipeline design (chunking strategy, top-k selection, reranking), embedding drift when model is updated (requires re-embedding all vectors), dimensionality and index rebuild cost, vector DB for anomaly detection vs similarity search.

CONSTRAINTS:
- Questions must be answerable from memory in a 45-minute Staff DE interview
- Answers: 3-6 sentences, precise, no filler
- Always end each answer with a Citi framing sentence
- Valid GitHub Flavored Markdown

OUTPUT: Return ONLY the raw markdown. No explanation, no fences, no extra text.

