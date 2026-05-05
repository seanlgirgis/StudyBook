# DESIGN - POC 04h Local RAG Orchestrator

## Problem
We need a local business orchestrator that can use a reusable local 8-bit LLM container without coupling business retrieval logic to the model container.

## Design Goal
Keep architecture split:
- local LLM container (`04g-quantized`) handles generic inference only
- local orchestrator (`04h`) handles business workflow

## Components
1. `kb_loader.py`
- loads and validates KB JSON records
- enforces required fields

2. `retriever.py`
- deterministic token-match scoring
- weighted matches for title/service_type/symptoms over body text

3. `llm_gateway.py`
- calls local container endpoint (`/infer`)
- returns `answer` text
- raises clear runtime error if unavailable

4. `service.py`
- intent cleanup via local LLM with strict JSON expectation
- robust JSON parse with deterministic fallback path
- retrieval + grounded prompt assembly
- draft answer generation via local LLM
- fallback answer when LLM unavailable

5. `app.py`
- `GET /health`
- `POST /ask`

## Data Flow
1. User sends query to `/ask`
2. Service cleans intent (LLM JSON parse or deterministic fallback)
3. KB is loaded
4. Retriever returns top scored KB sections
5. Grounded prompt assembled: "Use only these knowledge base sections..."
6. Local LLM called for draft answer
7. Structured response returned

## Why No Docker Yet
04h starts as local Python/FastAPI first to validate orchestrator behavior and tests quickly.
Containerization is deferred to a later step.

## Boundaries and Non-Goals
- no vector DB
- no Grok/OpenAI
- no integrated lane changes
- no modification to 04g/04g-quantized runtime behavior