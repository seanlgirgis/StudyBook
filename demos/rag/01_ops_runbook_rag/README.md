# Ops Runbook RAG

> "Ask your runbooks a question" — instead of searching through PDFs, just ask.

## Problem it solves

Enterprise IT teams have hundreds of runbooks, SOPs, and alert playbooks that nobody can find under pressure. This lets an ops engineer ask plain-English questions and get the right procedure instantly.

## Architecture

```
PDF/Word Runbooks
      ↓
  [ingest/]  chunk + embed → ChromaDB (vector store)
      ↓
  [retrieval/]  query → top-k chunks → LLM → answer + source citation
      ↓
  [app/]  Streamlit UI
```

## Example queries

- "What do I do when disk utilization exceeds 90%?"
- "How do I restart the payment processing service?"
- "What is the escalation path for a P1 database outage?"

## Run it

```bash
pip install -r requirements.txt
python ingest/load_docs.py          # loads data/ into ChromaDB
streamlit run app/app.py            # launches UI
```

## Interview talking points

- Chunking strategy tradeoffs (fixed vs semantic)
- Embedding model choices and cost
- Why RAG vs fine-tuning for this use case
- How you'd scale this: Pinecone + ECS + API gateway
