# RAG Application Builder Foundation — Coverage Tracker

**Canonical foundation:**

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation
```

**Canonical shared library:**

```text
D:\py_libs\rag_foundation
```

**Purpose:** Track what must be learned, demonstrated, tested, documented, and—when justified—promoted into the central `rag_foundation` library.

## Status legend

- `[x]` Complete and run successfully
- `[~]` Partly covered; needs another brick, test, or documentation pass
- `[ ]` Not started
- `[L]` Candidate for the shared library
- `[A]` Application/lab-specific; normally do not promote
- `[MUST]` Required before the foundation is considered complete
- `[OPTIONAL]` Useful extension after the core is stable

## Governing rules

1. **All practical functionality covered in the completed DataCamp AI courses must be reproduced or consciously mapped.**
2. Shared mechanics belong in `D:\py_libs\rag_foundation`; lesson behavior belongs in tiny lab scripts.
3. When a reusable shape is clear, implement and test the shared mechanic first, then use it directly in the brick. If later bricks expose a better abstraction, refactor the shared code and update affected bricks.
4. OpenAI and IBM watsonx are the core provider implementations for this foundation.
5. Claude, Grok, local models, or a multi-provider gateway are optional comparison/fallback adapters—not blockers for the core curriculum.
6. Privacy, provider approval, latency, quality, and total cost come before “cheapest token price.”
7. Do not invent new business applications while a DataCamp-aligned capability remains uncovered.
8. **Reject any proposed brick that merely renames, repackages, or repeats functionality already demonstrated. A new brick must prove a genuinely new behavior, state transition, provider capability, validation path, or RAG component.**

---

# A. Current checkpoint

## Stage 1 — Application basics

- [x] 01 First request through the shared provider
- [x] 02 Instructions versus user prompt
- [x] 03 Vague versus precise instructions
- [x] 04 Prompt variables
- [x] 05 Normalized result metadata and token usage
- [x] 06 Request-level model override and return to provider default
- [x] 07 Maximum output-token ceiling and truncation behavior
- [x] 08 Request validation before an API call
- [x] 09 Provider configuration validation
- [x] 10 Provider error translation with a fake client
- [x] 11 Same task compared across mini and nano
- [x] 12 Simple model-routing demonstration
- [x] 13 Constrained classification plus local validation
- [x] 14 Privacy-first provider-routing rules
- [x] 15 Route decision object
- [x] 16 Manual normalization demonstration
- [x] 17 Use shared `OpenAITextProvider`
- [x] 18 Instructions and prompt separation through shared models
- [x] 19 Output-token-limit follow-up
- [x] 20 JSON structured ticket triage [A]
- [x] 21 Validated ticket domain object [A]
- [x] 22 Conceptual system/user/assistant role mapping
- [x] 23 Shared `ChatMessage` object
- [x] 24 Ordered shared message history
- [x] 25 Shared two-turn conversation
- [x] 26 Follow-up requiring previous context
- [x] 27 Conversation token growth
- [REJECTED] 28 Duplicate prompt-variable exercise; not counted
- [x] 29 Answer plus updated state across two calls
- [x] 30 Structured application-specific chat state
- [x] 31 State validation
- [x] 32 Invalid state repair and revalidation
- [x] 33 Zero-shot versus few-shot
- [x] 34 Live two-turn conversation through shared library mechanics
- [x] 35 Shared JSON-object parsing used by a functional brick
- [x] 36 Trusted instructions versus delimited untrusted content
- [~] 37 Protected versus unprotected injection comparison; both happened to classify correctly
- [x] 38 Dedicated summarization pattern

### Stage 1 cleanup

- [ ] Resolve duplicate/ambiguous numbering around the two `19_*` scripts.
- [ ] Update `stage_01_application_basics\README.md` with a numbered brick index and one-line purpose per script through Brick 38.
- [ ] Update `lab_run_book.md` with successful runs through Brick 38.
- [ ] Mark Bricks 20–21 as application examples, not general library features.
- [ ] Confirm the old `lab\src\rag_foundation` scaffold is not treated as the canonical library; canonical library is `D:\py_libs\rag_foundation`.

---

# B. DataCamp functionality coverage — mandatory

This section is the primary no-drift checklist.

## B1. Working with the OpenAI API

- [x] [MUST] One direct model request
- [x] [MUST] Environment-based secret and model configuration
- [x] [MUST] Instructions/system behavior versus user input
- [x] [MUST] Prompt variables and dynamic prompt construction
- [x] [MUST] Response text extraction through normalized result
- [x] [MUST] Request ID and token metadata
- [x] [MUST] Model override
- [x] [MUST] Output-token limit
- [x] [MUST] Provider/configuration error handling
- [x] [MUST] Classification with constrained labels
- [x] [MUST] Summarization pattern — Brick 38
- [ ] [MUST] Rewriting/transformation pattern
- [ ] [MUST] Extraction pattern with validated fields
- [ ] [MUST] Repeated-call variability experiment
- [ ] [MUST] Sampling/temperature-equivalent controls, only after current API/model support is verified
- [ ] [MUST] Cost comparison calculated from normalized usage rather than discussed manually

## B2. Prompt Engineering with the OpenAI API

- [x] [MUST] Clear task contract
- [x] [MUST] Precise, measurable output constraints
- [x] [MUST] Classification labels with definitions
- [x] [MUST] Structured JSON output demonstration
- [x] [MUST] Application-specific validation demonstration
- [x] [MUST] Delimiters separating instructions from untrusted/user content — Brick 36
- [x] [MUST] Prompt-injection boundary demonstration — Bricks 36–37; no forced failure claimed
- [x] [MUST] Zero-shot versus few-shot comparison — Brick 33
- [x] [MUST] Structured output using reusable `parse_json_object()` mechanics — Brick 35
- [x] [MUST] Invalid structured output handling — shared structured/stateful tests and Brick 32
- [x] [MUST] Repair and revalidation flow after validation failure — Brick 32
- [x] [MUST] Separate application instructions and user input across chat requests — Bricks 22, 25, 34
- [x] [MUST] Stateful chatbot context across calls — Brick 29
- [x] [MUST] Answer plus updated state — Brick 29
- [x] [MUST] Structured chat state — Brick 30
- [x] [MUST] Chat-state validation — Bricks 31–32

## B3. Message roles and conversation

- [x] [MUST] Conceptual mapping: instructions → system/application; prompt → user; result → assistant
- [x] [MUST] `ChatMessage` object with validated role and content
- [x] [MUST] Ordered list of messages
- [x] [MUST] `ConversationRequest` model
- [x] [MUST] OpenAI provider support for multi-message input
- [x] [MUST] Two-turn conversation
- [x] [MUST] Follow-up that requires prior context (“it”)
- [x] [MUST] Explicit ordered history resent through `ConversationRequest`
- [x] [MUST] Conversation token growth
- [ ] [MUST] History trimming or summarization
- [x] [MUST] Real external application state across turns: stored, sent, updated, validated, persisted, and reused
- [x] [MUST] Answer plus updated state — Brick 29
- [x] [MUST] Validated structured state across turns

## B4. Hugging Face and document QA reuse

- [ ] [MUST] Load plain-text document
- [ ] [MUST] Extract PDF text
- [ ] [MUST] Preserve page/source metadata
- [ ] [MUST] Clean extracted text
- [ ] [MUST] Split text into chunks
- [ ] [MUST] Add chunk IDs and metadata
- [ ] [MUST] Run extractive QA on document text
- [ ] [MUST] Compare extractive QA with generative answer
- [ ] [MUST] Explain what a Hugging Face pipeline hides
- [ ] [MUST] Compare local CPU inference with hosted provider call

## B5. Ethics and privacy applied—not repeated as theory

- [~] [MUST] Privacy-first provider-routing concept demonstrated
- [ ] [MUST] Document sensitivity classification before ingestion
- [ ] [MUST] Data minimization before external model calls
- [ ] [MUST] Log-redaction rules
- [ ] [MUST] Retention/deletion/re-indexing plan
- [ ] [MUST] Human override and feedback path
- [ ] [MUST] Unsupported-answer/refusal behavior
- [ ] [MUST] Source transparency and limitations

---

# C. RAG application builder curriculum

## Stage 2 — Prompt engineering as application engineering

- [ ] Task contract template
- [x] Trusted instructions versus untrusted content
- [x] Delimiters
- [x] Few-shot examples
- [x] Structured outputs
- [x] General validation
- [x] Retry/repair
- [x] Prompt-injection boundary
- [ ] Prompt tests and expected outputs

**Exit gate:** A prompt-driven feature returns validated, predictable output and handles failure without business-specific code in the provider.

## Stage 3 — Document processing

- [ ] Text loader
- [ ] PDF loader
- [ ] Cleaning
- [ ] Page metadata
- [ ] Chunking by size
- [ ] Chunk overlap
- [ ] Structure-aware chunking
- [ ] Chunk metadata
- [ ] Document/chunk inspection report

**Exit gate:** One document becomes a reproducible list of clean, traceable chunks.

## Stage 4 — Embeddings and vectors

- [ ] Embedding request/result concepts
- [ ] OpenAI embedding provider
- [ ] IBM/watsonx embedding comparison if available/required
- [ ] Generate embeddings
- [ ] Inspect dimensions
- [ ] Similar versus dissimilar text comparison
- [ ] Cosine similarity
- [ ] Batch embedding
- [ ] Cost/latency measurement
- [ ] Local persistence format

**Exit gate:** Chunks and queries can be embedded and similarity can be explained numerically.

## Stage 5 — Retrieval

- [ ] Vector index/store selection for the learning lab
- [ ] Add chunks and metadata
- [ ] Query embedding
- [ ] Top-k search
- [ ] Similarity scores
- [ ] Metadata filtering
- [ ] Retrieval inspection
- [ ] Retrieval failure examples
- [ ] Precision/recall intuition
- [ ] Query rewriting
- [ ] Optional reranking

**Exit gate:** A query returns relevant, traceable chunks with scores and metadata.

## Stage 6 — Grounded generation

- [ ] Context construction
- [ ] Grounding instructions
- [ ] Answer only from supplied evidence
- [ ] Refuse when evidence is insufficient
- [ ] Source citation formatting
- [ ] Detect unsupported claims
- [ ] Compare grounded versus ungrounded answer
- [ ] Context-window budgeting

**Exit gate:** The generated answer is tied to retrieved evidence and identifies its sources.

## Stage 7 — Complete RAG

- [ ] Ingest document
- [ ] Extract and clean
- [ ] Chunk and tag
- [ ] Embed and index
- [ ] Retrieve
- [ ] Generate grounded answer
- [ ] Cite sources
- [ ] Handle no-answer case
- [ ] Command-line end-to-end app
- [ ] Small reusable application service layer

**Exit gate:** One transparent end-to-end RAG application runs locally and can be explained step by step.

## Stage 8 — Evaluation and observability

- [ ] Request latency
- [ ] Token usage
- [ ] Estimated provider cost
- [ ] Error/retry counts
- [ ] Retrieval latency
- [ ] Retrieval scores
- [ ] Source coverage
- [ ] Answer relevance
- [ ] Faithfulness/groundedness
- [ ] No-answer correctness
- [ ] Provider/model comparison
- [ ] Local budget tracking
- [ ] Privacy-safe logs

**Exit gate:** The application can show why an answer was produced, what it cost, how long it took, and whether it was supported.

## Stage 9 — IBM watsonx and Coursera alignment

- [ ] Watsonx credentials/configuration loaded safely
- [ ] One direct watsonx generation call
- [ ] `WatsonxTextProvider`
- [ ] Normalize watsonx output into `TextGenerationResult`
- [ ] OpenAI versus watsonx same-task comparison
- [ ] Watsonx embedding/retrieval capability comparison where relevant
- [ ] Map each IBM course lesson/project to foundation artifacts
- [ ] Complete course reconnaissance before each official course

**Exit gate:** Required IBM work can be completed without abandoning the provider-neutral architecture.

---

# D. Provider strategy

## Core providers

- [x] [MUST] OpenAI text generation
- [ ] [MUST] IBM watsonx text generation

## Optional comparison/fallback providers

- [ ] [OPTIONAL] Anthropic/Claude adapter
- [ ] [OPTIONAL] xAI/Grok adapter
- [ ] [OPTIONAL] Multi-provider gateway adapter using one key and provider/model routing
- [ ] [OPTIONAL] Local provider adapter for privacy/offline experiments

## Provider-adapter acceptance checklist

Each new provider must:

- [ ] Accept the common request model where the feature truly matches
- [ ] Return the common normalized result model
- [ ] Preserve `raw_response`
- [ ] Translate provider errors into `ProviderError`
- [ ] Expose the underlying client for advanced access
- [ ] Extract token/usage fields where available
- [ ] Have fake-client unit tests
- [ ] Have one live smoke test
- [ ] Document provider-specific differences instead of pretending all APIs are identical

---

# E. Promotion decisions

## Promote to the shared library when repeated and general

- [x] Configuration helpers
- [x] Common exception hierarchy
- [x] Base/text request models
- [x] Base/text result models
- [x] OpenAI text provider
- [x] `ChatMessage` and `ConversationRequest`; conversation results reuse `TextGenerationResult`
- [x] General JSON-object parser and stateful-turn parser with application validation callback
- [ ] Retry/timeout policy after failure bricks
- [ ] Usage/cost record after two providers or repeated monitoring needs
- [ ] Provider registry/factory only after at least two real providers
- [ ] Routing policy types only after real provider choices exist
- [ ] Document loaders/chunk models after Stage 3 demonstrations
- [ ] Embedding request/result/provider after Stage 4 demonstrations
- [ ] Retrieval interfaces after Stage 5 demonstrations

## Keep in lab/application

- [x] Ticket categories and urgency rules
- [x] `TicketTriage`
- [x] Specific teaching prompts
- [x] One-off comparison scripts
- [x] Business workflows and domain schemas

---

# F. Immediate next sequence

The chat/state promotion cycle is complete. Continue with the remaining mandatory DataCamp functionality in this order:

1. [ ] Brick 39 — rewriting/transformation without changing meaning
   - Shared mechanics: existing `TextGenerationRequest`, `OpenAITextProvider`, and `TextGenerationResult`; no new abstraction justified.
   - Functional proof: rewrite text for a different audience or tone while preserving required facts.
2. [ ] Brick 40 — extraction with validated fields
   - First review whether the existing structured/stateful helpers are sufficient.
   - Add shared mechanics only if a genuinely reusable gap exists.
3. [ ] Brick 41 — repeated-call variability experiment
   - Use existing mechanics; capture outputs and normalized usage for comparison.
4. [ ] Brick 42 — sampling-control verification and experiment
   - Verify current Responses API and selected-model support before changing request models.
5. [ ] Brick 43 — calculated request cost from normalized usage
   - Generalize pricing/cost calculation in the shared library first.
6. [ ] Stage 1 reconciliation
   - Update README, run book, trackers, exports, and full pytest suite.
7. [ ] Begin Stage 3 document processing only after all mandatory Stage 1/DataCamp items are complete or explicitly mapped.

For each brick:

```text
Is a reusable mechanic missing?
→ yes: implement and test it in rag_foundation first
→ no: use the existing mechanics and keep the brick functional only
```

# G. Rejected or superseded bricks

## Brick 28 — `28_external_application_state.py`

**Status:** `[REJECTED]`

**Reason for rejection:**

The script created a Python dictionary and interpolated its values into a single prompt. That behavior was already covered by Brick 4 — prompt variables.

It did **not** demonstrate genuine application state because it did not:

- preserve state between model calls;
- receive a proposed state update from the model;
- parse or validate an update;
- persist the updated state in Python;
- send updated state into a later request;
- demonstrate a state transition.

**Action:**

- Keep the script only as a rejected-learning artifact if desired.
- Do not count it as completed curriculum.
- Replace it with a real two-call state workflow.
- Future bricks must pass the new-behavior test before being added.

## New-behavior test for every future brick

Before creating a new brick, answer all four questions:

1. What new behavior does this prove?
2. How is it different from an earlier brick?
3. What visible output proves the difference?
4. Does it belong in the lab, the shared library, or both?

If those questions do not have clear answers, do not create the brick.

---

# H. Foundation completion definition

The foundation is complete when:

- [ ] Every mandatory DataCamp functionality item above is complete or explicitly mapped with a written reason.
- [ ] OpenAI and watsonx provider paths work through normalized models.
- [ ] A transparent document-to-RAG pipeline works end to end.
- [ ] The system records usage, cost, latency, retrieval evidence, and errors.
- [ ] Privacy and source-grounding controls are demonstrated.
- [ ] The IBM Coursera course sequence is mapped to, and supported by, the local foundation.
- [ ] Shared-library mechanics are documented and tested.
- [ ] Lab scripts remain small, numbered, and concept-focused.

## Last updated checkpoint

```text
Bricks 23–38 completed or reconciled, except Brick 28 rejected and Brick 37 marked partial.
Shared mechanics now include chat messages, conversation requests, OpenAI ordered-message support,
JSON-object parsing, stateful-turn results/parsing, application validation callbacks, and repair/revalidation.
Next required brick: 39 rewriting/transformation without changing meaning.
```
