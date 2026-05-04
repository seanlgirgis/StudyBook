# 04a Answer Contract Design

## Purpose
Define the design and data contract for safe answer assembly with citations before any implementation work.

This POC is documentation-only and is the bridge from retrieval quality (`03g`, `03h`) into answer construction.

## Why This Exists
Retrieval quality is now evaluated, but answer generation is still undefined.  
Without a contract, future implementation can drift into ungrounded answers, missing citations, or unsafe handling of low-confidence and risky cases.

`04a` solves that by defining:
- required input shapes for answer assembly
- required output shapes for answer outcomes
- citation and groundedness rules
- explicit handling for insufficient evidence, clarification-needed, and escalation-required outcomes

## Upstream Dependencies
- `pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json`
- `pocs/03h_retrieval_evaluation/outputs/evaluation_report.json`
- `pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json` (retrieved candidate evidence source)

Dependency intent:
- `03g` provides per-query retrieval confidence/routing signals.
- `03h` provides known quality behavior and evaluation metrics for retrieval+decision outputs.
- `03f` provides ranked retrieval evidence records used for citation anchoring.

## Deliverables
- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`

No implementation artifacts are created in this step.

## Scope
In scope:
- answer assembly contract design
- groundedness and citation design
- outcome branching design (`answer_ready`, `insufficient_evidence`, `clarification_needed`, `escalation_required`)
- test/validation planning for future implementation

Out of scope:
- Python code
- `src/`, `tests/`, or `outputs/` creation
- LLM calls
- threshold tuning
- customer-facing answer generation
- changes to `03d`, `03e`, `03f`, `03g`, or `03h`
- `integrated/servicecall-ai` changes

## Terminology (Core Teaching Distinctions)
- Retrieved evidence: raw top-k candidates returned by retrieval.
- Selected evidence: subset of retrieved candidates approved for claim support.
- Answer draft: internal structured draft tied to selected evidence and citations.
- Final answer: user-facing rendering produced only after groundedness gates pass.
- Citation coverage: fraction of answer claims supported by at least one valid citation.
- Insufficient evidence outcome: explicit no-answer branch when evidence cannot safely support claims.

## Review Guidance
Read in order:
1. `docs/DESIGN.md` for architecture and policy intent.
2. `docs/CONTRACT.md` for JSON shapes and validation rules.
3. `docs/TEST_PLAN.md` for enforcement strategy.

Approval of this design is the gate for any future implementation in `04b+`.
