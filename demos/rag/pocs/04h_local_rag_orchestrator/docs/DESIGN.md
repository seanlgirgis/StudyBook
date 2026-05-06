# DESIGN - POC 04h Local RAG Orchestrator

## Architecture Overview
`04h_local_rag_orchestrator` is the business orchestration tier that sits between user-facing clients and model providers.

Design rule:
- LLM container remains generic and reusable inference only.
- Orchestrator owns business context selection and answer orchestration.

## Component Responsibilities
### KB Loader
- Loads synthetic business KB artifacts.
- Validates record shape before retrieval.

### Deterministic Retriever
- Scores and selects relevant KB sections using deterministic logic.
- Prioritizes clear field-weighted matching (title/service/symptoms over body text).

### Intent Cleanup Service
- Normalizes noisy customer phrasing into structured intent fields.
- Supports deterministic fallback behavior when provider output is unusable.
- Performs clarification gating:
  - `clarification_needed`
  - `clarifying_questions`
  - `confidence`
  - `classification`
  - `matched_capability`
  - `unsupported_reason`

### LLM Gateway
- Abstracts provider call mechanics from orchestration logic.
- Intent route: local 8-bit endpoint.
- Final-answer route: Grok (configured model).

### Answer Orchestrator
- Coordinates end-to-end flow:
  - intent cleanup
  - clarification gate
  - unsupported-service gate
  - max clarification retry gate
  - KB retrieval
  - Grok-only final answer call
  - structured response formatting

### FastAPI App
- Exposes health and ask contracts.
- Provides stable API boundary for local CLI/testing and later app integration.

## Why the LLM Container Stays Independent
The model service should remain reusable across POCs and future integrations.

If business retrieval is embedded in the model container, provider swapping becomes harder and architecture coupling increases.

Keeping model inference separate allows:
- local vs cloud provider substitution
- cleaner testing boundaries
- independent lifecycle of business logic and model runtime

## Why KB Lives in the Orchestrator Layer
Model containers do not automatically reason over host files unless context is explicitly passed.

The orchestrator must:
- read KB records
- retrieve relevant sections
- inject selected text into the prompt
- call the provider with grounded context

## Provider Routing Strategy
Planned provider route order:
1. `LOCAL_8BIT` for intent clarification (not final answer)
2. `GROK_MINI` (future low-cost final route option)
3. `GROK_3` (current preferred final-answer route)

Current validated local provider:
- `http://localhost:8002/infer`

## Interactive Hybrid Tester
An interactive script validates hybrid orchestration without changing the API contract:
- file: `interactive_hybrid_test.py`
- loop-based terminal input (`exit` to quit)
- calls `service.answer_query(...)` first
- prints intent structure + clarification state + retrieved sections
- final answer comes from configured Grok provider only
- if Grok is unavailable, status becomes `final_provider_unavailable` and final answer remains blank
- writes one JSON record per interaction to `outputs/hybrid_ask_logs.jsonl`

## Bounded Intake Policy
Intent classification classes:
- `supported`
- `clarification_needed`
- `unsupported`
- `human_escalation_required`
- `multi_intent`

Local deterministic code owns:
- clarification retry policy (`MAX_CLARIFICATION_ATTEMPTS = 3`)
- escalation decision and handoff payload shape
- retrieval and provider call gating

Policy enforcement:
- no Grok call for `unsupported`, `clarification_needed`, `human_escalation_required`, `no_context`
- no Grok call for `multi_intent` until customer picks one issue
- no local-8bit final-answer fallback

## Multi-Intent Policy
If a single customer message contains multiple distinct requests:
- classify as `multi_intent`
- include per-intent entries in `intents`
- ask which issue to handle first
- do not retrieve combined final context yet
- do not call Grok yet

Environment variables used for optional Grok route:
- `XAI_API_KEY` or `GROK_API_KEY`
- `GROK_MODEL` (default `grok-3`)
- `GROK_BASE_URL` (default `https://api.x.ai/v1`)

## ASCII Architecture Diagram
```text
Customer / CLI / Website
      |
      v
04h RAG Orchestrator
      |
      +--> KB Loader -> Knowledge Base JSON
      |
      +--> Retriever -> selected sections
      |
      +--> Prompt Assembly
      |
      +--> LLM Gateway
              |
              +--> local llm_7b_8bit container
              +--> future Grok-mini
              +--> future Grok-3
```

## Current Non-Goals
- no vector database
- no Docker container for 04h yet
- no move to `integrated/servicecall-ai`
- no local 8-bit final-customer-answer mode
- no production-readiness claims

## Safety Rule
Any practical or safety advice must come from retrieved KB sections.  
Neither local 8-bit intent output nor Grok final output should invent advice outside provided KB context.

## Design-Forward Path
- Phase A: local Python orchestrator
- Phase B: orchestrator container
- Phase C: Docker Compose with LLM + orchestrator
- Phase D: provider routing to Grok-3 for final answer
- Phase E: website/service integration later
