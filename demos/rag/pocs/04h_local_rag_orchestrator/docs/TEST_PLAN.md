# TEST PLAN - POC 04h Local RAG Orchestrator

## Goal
Define validation strategy before implementation.

## Unit Tests (Planned)
- KB loader loads valid records.
- KB safety-guidance records load correctly.
- KB loader rejects missing required fields.
- Retriever finds plumbing leak section for pipe/sink/water query.
- Retriever finds AC repair section for cooling/not cooling query.
- Local intent prompt contains strict JSON-only / no-customer-answer instructions.
- JSON extraction handles extra non-JSON wrapper text.
- Ambiguous intent can return `clarification_needed`.
- `answer_query` does not use local 8-bit as final answer when final provider is unavailable.
- Grok-unavailable path returns `status = final_provider_unavailable`.
- Clear intent still returns retrieved sections.
- Provider gateway can be monkeypatched.

Unit-test rule:
- No tests should require Grok/OpenAI.
- Normal unit tests should not require the local LLM container.

## Smoke Test (Planned)
Prerequisite:
- `04g-quantized` container is running:
  - `llm_7b_8bit_run`
  - `http://localhost:8002/health`

Planned orchestrator endpoints:
- `http://localhost:8010/health`
- `http://localhost:8010/ask`

Planned smoke query:
```text
Hi, sorry to bother you. There is water under my sink and I think a pipe is leaking. Can someone help?
```

Expected smoke outcome:
- `service_type` is `plumbing`
- retrieved sections include plumbing leak repair and plumbing safety guidance
- if Grok key is unavailable:
  - `final_answer` is blank
  - `final_provider_used` is `unavailable`
  - `status` is `final_provider_unavailable`
- for ambiguous query, `clarification_needed` can be true with clarifying questions

## Validation Commands (Planned)
From repo root:
```powershell
cd D:\Workarea\StudyBook\demos\rag
python -m pytest -q pocs/04h_local_rag_orchestrator/tests
```

With local 8-bit LLM running:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
uvicorn src.app:app --host 127.0.0.1 --port 8010
python .\smoke_test_04h.py
```

Interactive hybrid check:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
python .\interactive_hybrid_test.py
```

Suggested manual inputs:
1. `Hi, there is water under my sink and I think a pipe is leaking.`
2. `Something is wrong with water.`
3. `My AC is running but the house is not cooling.`
4. `exit`

## Non-Goals for This Test Phase
- no Docker build for 04h
- no vector DB validation yet
- no integrated lane validation yet
