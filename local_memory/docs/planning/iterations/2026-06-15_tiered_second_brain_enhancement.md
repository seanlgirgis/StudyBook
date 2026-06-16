# Iteration: Tiered Second Brain Enhancement

**Date:** 2026-06-15  
**Status:** exploratory draft — not a decision  
**Source:** Grok Build planning discussion  
**Related:** `LOCAL_MEMORY_HANDOFF.md`, LifeVault hot/cold concept, `rag_foundation` library

---

## Context

Sean is studying Generative AI application development (vector databases, LangChain, foundation models). Question: how might `local_memory` evolve into a multimodal second brain that:

- Uses cheaper tokens for routine work
- Safely handles sensitive information
- Uses cloud AI for complex answering and formatting
- Uses local cheap models for short answers

---

## What works well today

1. **Repository-as-memory** — files are source of truth; no chat drift
2. **Topic-based routing** — `runbooks/`, `locations/`, `chat_captures/`
3. **Instruction-driven writes** — low ceremony, high reliability
4. **Separation of concerns** — shared memory vs `GROK_*` vs other private repositories (out of scope here)
5. **Building blocks exist elsewhere** — `rag_foundation`, RAG Application Builder Foundation, LifeVault hot/cold idea

**Main gap:** no retrieval layer, no classification, no secret boundary.

---

## Vision: three-layer tiered second brain

```text
[Ingest]  markdown, captures, PDFs, images, audio/video refs
    ↓
[Hot layer - local]  catalog, metadata, chunks, embeddings, vector index, answer cache
[Cold layer - encrypted]  originals, secrets vault
    ↓
[Query router]  complexity → grep/cache | local model | retrieve+cite | cloud synthesize
```

**Principle:** cheap/local for lookup and repetition; retrieval for grounding; cloud only when synthesis or formatting needs it.

Aligns with LifeVault ~85% local hit rate and existing `questions_cache.md` manual tiering.

---

## Model routing strategy (token economics)

| Task | Who answers | Why |
|------|-------------|-----|
| Stored command lookup | No LLM — `rg` + file cite | Zero tokens |
| Short recall from stored facts | Local small model or template | Cheap, grounded |
| Multi-file synthesis / next-step advice | Retrieve + cloud model | Needs cross-doc reasoning |
| Formatting (RemNote cards, etc.) | Cloud model | Structure worth the cost |
| Secret location | No LLM — registry pointer only | Never send secrets to models |

**Router signals (start simple):**

- Match in `questions_cache.md` → direct answer
- High-confidence retrieval → local model with citations
- Multi-file / explain / build / format → cloud + retrieved context
- Sensitive tags → block from cloud

Reuse RAG foundation "route decision object" pattern from stage 01 labs.

---

## Sensitive information boundary (non-negotiable before multimodal)

```
local_memory/     → operational facts, no secret values
secrets/          → outside git, encrypted
secret_registry   → pointers only: name, purpose, load command, last verified
```

**Classification tags per chunk:**

- `public` — safe anywhere
- `internal` — ok in repo, not in cloud prompts
- `secret` — registry pointer only

Private repositories use sanitized Git content plus encrypted originals for git-ignored files. `local_memory` does not duplicate private work-repository knowledge.

---

## Multimodal phases

### Phase 1 — Smarter text memory (highest value, lowest cost)

- Chunk + embed `runbooks/`, `questions_cache.md`, key planning docs
- Local FAISS/Chroma under gitignored `local_memory/.index/`
- Retrieve → cite → optional local LLM glue
- Human-approved promotion to `questions_cache.md`

### Phase 2 — Structured captures

- Formalize `chat_captures/` schema: `original_reference/` + `memory/` + `embeddings/`
- YouTube capture (`BqBsT6ZjurA`) as template
- Each capture: summary, provenance, tags, sensitivity class

### Phase 3 — Multimodal ingest

- Images → OCR/caption → text chunks
- PDFs → text + page anchors
- Audio/video → local Whisper transcript → same pipeline
- Originals in cold/encrypted; hot keeps text + metadata

### Phase 4 — Unified router service

- Small CLI or FastAPI: `ask`, `remember`, `ingest`, `route`
- Lives beside `rag_foundation` — shared providers, monitoring, cost tracking
- `local_memory` stays human-readable markdown; service is retrieval/orchestration

---

## Composition with existing work

| Component | Role |
|-----------|------|
| `local_memory` | Canonical markdown truth |
| `rag_foundation` (`D:\py_libs\rag_foundation`) | Shared Python mechanics |
| Future memory service / LifeVault ops | Retrieve, route, ingest |
| `docs/planning/` | Exploratory thinking (this file) |
| `docs/adr/` | Accepted decisions |

| Study topic | Second-brain use |
|-------------|------------------|
| Vector DBs | Hot-layer index |
| LangChain / LCEL | Ingest, retrieval, router chains |
| Foundation models | Cloud tier synthesis; local tier Q&A |
| RAG | Ground non-trivial answers |
| Structured output | RemNote exports, capture manifests |
| Observability | Token/cost/latency per route |

---

## What to avoid

1. Replacing markdown with a database — lose grep, git diff, manual edit
2. Embedding everything on day one — stale embeddings worse than good file routing
3. Cloud-first answers — burns tokens on cached questions
4. One giant vault — keep personal / work / study boundaries
5. Auto-writing memories without approval — especially sensitive tags

---

## North star

> Markdown vault for truth. Local index for speed. Encrypted store for secrets. Router picks: grep → cache → RAG+local → RAG+cloud.

---

## Suggested first implementation bite

1. Add `runbooks/security.md` — classification + secret registry rules
2. Gitignored `memory_index/` + script: chunk `runbooks/*.md` → FAISS
3. CLI: `memory ask "..."` → retrieve → cite → no cloud unless `--explain`

Lab-sized; uses RAG course skills; does not break current vault.

---

## Open questions (for future sessions)

- Single `memory_service` repo vs module inside LifeVault?
- Which local model for tier-2 answers on Windows?
- How much auto-ingest vs manual capture approval?
- When does an iteration graduate to ADR?

**Tags:** `planning`, `second-brain`, `rag`, `architecture`, `iteration`