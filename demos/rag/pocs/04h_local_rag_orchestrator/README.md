# POC 04h - Local RAG Orchestrator (Python/FastAPI, No Docker Yet)

## Purpose
POC 04h builds a local orchestrator service that is separate from the local LLM container.

The 04h orchestrator owns:
- business knowledge base files
- deterministic retrieval
- intent cleanup orchestration
- prompt assembly
- provider routing
- `/ask` API

## Architecture Boundary
The 8-bit LLM container remains an independent reusable inference service:
- health: `http://localhost:8002/health`
- infer: `http://localhost:8002/infer`

04h must not embed business KB/retrieval inside the LLM container.

## Scope In This Step
- local Python/FastAPI only
- no Docker for 04h
- no vector database
- no external LLM providers (Grok/OpenAI)

## Folder Layout
```text
pocs/04h_local_rag_orchestrator/
  README.md
  docs/
    DESIGN.md
    CONTRACT.md
    TEST_PLAN.md
  data/
    knowledge_base.json
  src/
    kb_loader.py
    retriever.py
    llm_gateway.py
    service.py
    app.py
  tests/
    test_kb_loader.py
    test_retriever.py
    test_service.py
  outputs/
  smoke_test_04h.py
```

## Quick Start
1. Run tests:
```powershell
cd D:\Workarea\StudyBook\demos\rag
. D:\Workarea\StudyBook\env_setter.ps1
python -m pytest -q pocs/04h_local_rag_orchestrator/tests
```

2. Run API locally:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
. D:\Workarea\StudyBook\env_setter.ps1
uvicorn src.app:app --host 127.0.0.1 --port 8010
```

3. Run smoke test (in a second terminal):
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
. D:\Workarea\StudyBook\env_setter.ps1
python .\smoke_test_04h.py
```

## Expected Result
- `GET /health` responds with `{"ok": true}`
- `POST /ask` returns orchestrated response payload including:
  - cleaned intent
  - service type
  - symptoms
  - urgency
  - retrieved KB sections
  - draft answer
  - provider/status fields

## Non-Goals
- no containerization of 04h yet
- no move to `integrated/servicecall-ai`
- no full production RAG claims