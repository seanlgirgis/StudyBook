# TEST PLAN - POC 04h Local RAG Orchestrator

## Unit Test Scope
### KB Loader
- loads valid KB JSON
- rejects missing required fields

### Retriever
- finds plumbing leak record for pipe/sink/water query
- finds AC repair record for cooling/not cooling query
- returns weighted scored results

### Service
- deterministic fallback path does not crash without LLM
- `answer_query` works with monkeypatched LLM gateway
- tests do not require local 8-bit container

## Commands
Run unit tests:
```powershell
cd D:\Workarea\StudyBook\demos\rag
. D:\Workarea\StudyBook\env_setter.ps1
python -m pytest -q pocs/04h_local_rag_orchestrator/tests
```

Run local app:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
. D:\Workarea\StudyBook\env_setter.ps1
uvicorn src.app:app --host 127.0.0.1 --port 8010
```

Run smoke test (requires running app and reachable 8-bit container):
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
. D:\Workarea\StudyBook\env_setter.ps1
python .\smoke_test_04h.py
```

## Smoke Query
```text
Hi, sorry to bother you. There is water under my sink and I think a pipe is leaking. Can someone help?
```

## Expected Smoke Behavior
- `/health` returns `{"ok": true}`
- `/ask` returns structured JSON response
- script writes `outputs/SMOKE_TEST_RESULT.md`

## Non-Goals in Tests
- no Grok/OpenAI dependency
- no vector DB behavior
- no Docker requirement for unit tests