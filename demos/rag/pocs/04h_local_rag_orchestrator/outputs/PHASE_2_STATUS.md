# 04h Phase 2 Status (Pause Snapshot)

Date: 2026-05-05
POC: `pocs/04h_local_rag_orchestrator`
Support runtime: `pocs/04g-quantized`

## Pause Reason
Work is paused so Sean can switch to interview preparation. This file preserves exact 04h resume context.

## 04g-quantized Runtime Snapshot
Validated local runtime:
- model container: `llm_7b_8bit_run`
- image: `llm_7b_8bit`
- host endpoint: `http://localhost:8002`
- infer endpoint: `http://localhost:8002/infer`
- health endpoint: `http://localhost:8002/health`
- model mount: `C:\LLM_models\Mistral7B -> /app/llm_model`
- duplicate `.bin` archive: `D:\LLM_models\Mistral7B_unused_bin`
- active runtime uses safetensors + tokenizer/config
- 8-bit preferred over FP16 for local helper workloads
- FP16 container intentionally removed/stopped due to PC resource pressure

## 04h Architecture Snapshot
Validated architecture:
- local 8-bit LLM is intent clarification engine only
- deterministic local code owns:
  - policy control
  - supported/unsupported classification
  - clarification retry logic
  - human escalation decision
  - KB retrieval
  - provider routing
- Grok/final provider is final customer-answer provider only
- local 8-bit is not used as final-answer fallback
- when Grok key/config is unavailable:
  - supported requests return intent + retrieved sections
  - `final_answer = ""`
  - `final_provider_used = unavailable`
  - `status = final_provider_unavailable`

## 04h Classification Support
Current classes:
- `supported`
- `clarification_needed`
- `unsupported`
- `human_escalation_required`
- `multi_intent`

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

Unsupported examples:
- car AC / vehicle AC
- vehicle repair
- carpet cleaning
- vent/duct cleaning unless explicitly supported later
- pest control
- roofing
- remodeling
- electrical panel work
- medical/legal/insurance questions

## Clarification + Escalation Policy
- `MAX_CLARIFICATION_ATTEMPTS = 3`
- if still unclear after max attempts:
  - `status = human_escalation_required`
  - includes `handoff_summary`
  - includes `recommended_next_message`
- no real email/CRM/live-chat handoff yet
- handoff package is structured but local-only

## Multi-Intent Behavior Snapshot
When multiple intents are detected in one message:
- `classification = multi_intent`
- `status = clarification_needed`
- `intents` array returned
- `retrieved_sections = []`
- `final_answer = ""`
- `final_provider_used = none`
- no Grok call
- asks which issue to handle first

Validated examples:
1) `My AC is not cooling and there is water under my sink.`
- `multi_intent`
- intents include AC repair + plumbing leak repair
- no retrieval, no final answer

2) `My car AC is broken and my home AC is not cooling.`
- `multi_intent`
- one unsupported vehicle AC intent + one supported home AC intent
- asks whether to continue with supported home AC issue
- no retrieval, no final answer

3) `My water heater pilot light keeps going out and my kitchen drain is clogged.`
- `multi_intent`
- intents include water heater pilot light + clogged drains
- no retrieval, no final answer

Validated multi-sentence single-intent example:
- query: `Hi, sorry to bother you. I had a long day. There is water under my sink and I think a pipe is leaking.`
- observed:
  - `classification = supported`
  - `service_type = plumbing`
  - `matched_capability = plumbing leak repair`
  - `clarification_needed = false`
  - retrieved includes:
    - `kb_plumbing_leak_001`
    - `kb_plumbing_leak_safety_001`
  - `status = final_provider_unavailable` (no Grok key)

## Latest Validation Snapshot
Command:
```powershell
cd D:\Workarea\StudyBook\demos\rag
python -m pytest -q pocs/04h_local_rag_orchestrator/tests
```
Result:
- `21 passed`

Interactive command:
```powershell
cd D:\Workarea\StudyBook\demos\rag\pocs\04h_local_rag_orchestrator
python .\interactive_hybrid_test.py
```
Manual run paused after initial multi-intent/single-intent cases passed.

## Pending Manual Tests on Resume
1) `Something is wrong with water. I am not sure where it is coming from.`
- expected: `clarification_needed`, `service_type=unknown`, asks plumbing/drain/water-heater disambiguation, no retrieval/final answer

2) `My sink is leaking and I also need carpet cleaning.`
- expected: `multi_intent` with supported plumbing + unsupported carpet cleaning, asks whether to continue with supported plumbing issue, no final answer

## Known Limitations
1. No persistent multi-turn session state yet.
- no `session_id`
- no customer profile
- no contact/address capture
- no stored selected priority intent after multi-intent clarification

2. Grok final provider has not been live-tested yet.
- no-key behavior is intentionally `final_provider_unavailable`

3. Retrieval is deterministic keyword scoring.
- can include noisy secondary sections (for example water-heater records on plumbing water queries)

4. No orchestrator Docker container yet.
- intentional while behavior stabilizes

5. No dashboard/stats endpoints yet.
- future container should own event schema/metrics/dashboard API
- local state persistence likely via mounted volume first, then S3/DB later

## Recommended Resume Choices
A. Finish pending manual 04h Phase 2 tests.
B. Tune retrieval ranking noise.
C. Wire and test real Grok final-answer provider.
D. Start `04i_stateful_customer_intake`:
- `session_id`
- customer name/contact/address
- `conversation_history`
- selected priority intent
- handoff preference (phone/email/live chat)
- persistent clarification-attempt tracking
E. Containerize orchestrator later after behavior stabilizes.

## Interview Framing Note
This POC demonstrates:
- bounded LLM behavior
- LLM failure-mode control
- local 8-bit model as private/cheap intent engine
- deterministic business policy layer
- supported/unsupported handling
- clarification retry limits
- human-in-the-loop escalation contract
- multi-intent handling
- KB-grounded final provider routing
- separation between reusable model container and business orchestrator

Strong summary:
"I built a home-services AI intake/RAG orchestrator where a local 8-bit LLM is constrained to intent clarification only, deterministic code owns policy/retrieval/escalation, and a stronger final provider is reserved for customer-facing answers. I added supported/unsupported service boundaries, clarification retry limits, human handoff contracts, multi-intent detection, and structured logging so the system can be evaluated operationally rather than just demoed."