# POC 04h - Local RAG Orchestrator (Design-First)

## What 04h Is
`04h_local_rag_orchestrator` is the planned business-orchestration layer for ServiceCall AI in the `pocs/` lane.

It is responsible for:
- business knowledge handling
- retrieval
- intent cleanup orchestration
- prompt assembly
- provider routing
- `/ask` API behavior

## Why 04h Exists After 04g-quantized
`04g-quantized` proved that a standalone local 8-bit LLM container can run reliably and quickly enough for local helper workloads.

04h exists to add business orchestration around that reusable model service, without embedding business logic into the model container.

## How 04h Differs From 04g-quantized
`04g-quantized`:
- generic inference runtime only
- containerized local LLM endpoint (`/health`, `/infer`)

`04h`:
- business KB + retrieval + orchestration layer
- decides what context is retrieved
- builds grounded prompts
- calls provider through a gateway
- returns structured `/ask` response contract

## Intended Flow
User request -> orchestrator -> intent cleanup -> retrieve KB sections -> prompt assembly -> LLM provider -> structured response

## Current Preferred Provider
Local 8-bit provider (validated):
- `http://localhost:8002/health`
- `http://localhost:8002/infer`

Runtime notes from prior validation:
- image: `llm_7b_8bit`
- container: `llm_7b_8bit_run`
- model mount: `C:\LLM_models\Mistral7B -> /app/llm_model`
- active runtime uses safetensors + tokenizer/config
- duplicate `.bin` files archived at `D:\LLM_models\Mistral7B_unused_bin`

## Provider Roles (Realigned)
- `local_8bit` role: intent clarification engine only.
  - classifies as `supported|clarification_needed|unsupported|human_escalation_required`
  - cleans noisy input
  - extracts `service_type`, `matched_capability`, `symptoms`, `urgency`
  - decides `clarification_needed` and asks 1-3 concise follow-up questions
- `grok_3` (or configured final provider) role: final customer-facing answer generation only for `classification=supported`.

Important:
- local 8-bit is not treated as the final customer-answer model.
- if final provider is unavailable, 04h returns structured intent and retrieved sections with:
  - `final_answer = ""`
  - `final_provider_used = "unavailable"`
  - `status = "final_provider_unavailable"`
  - note explaining final provider is unavailable.

## Supported Capability Policy
Supported capabilities:
- AC repair
- AC replacement
- heating repair
- plumbing leak repair
- clogged drains
- water heater no hot water
- water heater pilot light
- maintenance plans
- emergency service
- appliance repair

Unsupported examples (policy-bounded):
- car/vehicle AC
- carpet cleaning
- pest control
- roofing
- remodeling
- electrical panel work
- medical/legal/insurance questions

## Clarification Retry and Escalation
- `max_clarification_attempts` defaults to `3`.
- if intent remains unclear after max attempts:
  - `status = human_escalation_required`
  - `handoff_summary` is returned
  - `recommended_next_message` asks for callback details

## Multi-Intent Detection (Phase 2)
04h now detects when one message contains multiple service intents.

Behavior:
- classification becomes `multi_intent`
- system returns an `intents` list and asks which issue to handle first
- retrieval is skipped
- Grok final provider is not called
- final answer remains blank until the customer chooses a priority issue

This is intentionally clarification-first for safer intake and scheduling handoff.

## Interactive Hybrid Tester
`interactive_hybrid_test.py` is a local terminal script to validate a hybrid answer flow before orchestrator containerization.

Hybrid behavior:
- uses `service.answer_query(...)` for two-stage orchestration output
- Stage A: local 8-bit intent clarification
- Stage B: Grok final answer (when key exists)
- if Grok unavailable, no final answer is generated locally
- appends logs to `outputs/hybrid_ask_logs.jsonl`

Run:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
python .\interactive_hybrid_test.py
```

## Scope Clarifications
This POC is not:
- full integrated ServiceCall AI
- website integration
- Docker Compose orchestration yet
- vector database retrieval yet

## Project Lane Guardrail
Work remains in `pocs/`.
Nothing moves into `integrated/servicecall-ai` during this step.

## Implementation Status
This step is design-only.
Implementation begins only after explicit design approval.
