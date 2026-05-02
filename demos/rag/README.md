# RAG Demo Projects

Interview-demonstrable GenAI systems built on Retrieval Augmented Generation.

## Projects

| # | Name | Status | Stack |
|---|------|--------|-------|
| 01 | [Ops Runbook RAG](01_ops_runbook_rag/README.md) | 🔧 In Progress | LangChain, ChromaDB, Streamlit |
| 02 | [Job Search RAG](02_job_search_rag/README.md) | 🔧 In Progress | LangChain, ChromaDB, FastAPI |

## Common Stack

- **LLM**: Claude API (claude-sonnet-4-6) or OpenAI
- **Embeddings**: OpenAI `text-embedding-3-small` or HuggingFace local
- **Vector Store**: ChromaDB (local) → Pinecone (cloud demo)
- **Orchestration**: LangChain or LlamaIndex
- **UI**: Streamlit (quick demos) / FastAPI (API-first)
- **Docs**: PDF, Word, plain text via `unstructured`
