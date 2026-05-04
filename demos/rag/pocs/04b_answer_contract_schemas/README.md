# 04b Answer Contract Schemas

## Status

Implemented and validated (PASS).

Contract authority rule:

- `docs/CONTRACT.md` contains must-level implementation rules.
- `docs/DESIGN.md` explains rationale and boundaries.
- `docs/TEST_PLAN.md` mirrors must-level rules as planned validation tests.
- Ambiguous guidance must not be converted into implementation behavior without first updating `docs/CONTRACT.md`.

This POC converts the approved `04a_answer_contract_design` answer assembly contract into concrete schema implementation requirements for a later Pydantic implementation.

This POC now includes implemented Pydantic schemas and pytest validation coverage for the approved contract.

## Why this POC exists

Answer assembly is the point where a RAG system becomes risky.

Before this layer, the system is mostly retrieving, ranking, evaluating, and selecting evidence. After this layer, the system may produce something that a user reads as an answer, a refusal, a clarification request, or an escalation handoff.

A schema contract protects that boundary.

It makes sure the answer assembly layer receives structured, validated information instead of loose dictionaries. It also prevents common RAG failures:

- answering without enough evidence
- citing text that does not exist in the selected evidence
- mixing outcome branches together
- returning escalation payloads without safe routing fields
- generating unsupported factual claims
- treating conversational glue text as if it needed citations
- silently accepting malformed retrieval outputs

In this POC, the schema layer is treated as a safety and quality gate before answer generation.

## Scope

This POC will define the planned schema requirements for:

- answer assembly input payloads
- retrieved evidence records
- selected evidence records
- citation spans
- supported claims
- groundedness summaries
- answer-ready payloads
- insufficient-evidence payloads
- clarification payloads
- escalation payloads
- outcome events
- full top-level answer assembly outcomes

The implementation will happen only after these design documents are reviewed and approved.

## Required design documents

This design-only POC creates:

- `README.md`
- `docs/DESIGN.md`
- `docs/CONTRACT.md`
- `docs/TEST_PLAN.md`

## Explicit non-goals

This POC will not:

- create `src/`
- create `tests/`
- create `outputs/`
- implement Pydantic models
- write Python code
- call an LLM
- generate customer-facing answers
- tune retrieval thresholds
- modify `03d`, `03e`, `03f`, `03g`, or `03h` artifacts
- move anything into `integrated/servicecall-ai`

## Planned implementation after approval

After design review, a later implementation pass may add:

- `src/schemas.py`
- validation helper functions if needed
- pytest validation tests
- sample valid and invalid JSON payloads
- local validation output evidence

That later pass is intentionally not part of this design-only step.

## Relationship to earlier POCs

`04b_answer_contract_schemas` will consume the contract approved in `04a_answer_contract_design` and turn it into planned Pydantic schema requirements.

Later, the schemas should be able to validate payloads that originate from retrieval and evaluation work in `03g_retrieval_decision` and `03h_retrieval_evaluation`.

The planned dependency flow is:

```text
03g retrieval decision
        |
        v
03h retrieval evaluation
        |
        v
04a answer contract design
        |
        v
04b answer contract schemas
        |
        v
future answer assembly implementation
```

## Acceptance for this design step

This POC is acceptable when:

- design documents exist and remain contract authority references
- schema/validator implementation exists under `src/`
- validation tests exist under `tests/` and pass
- non-goals remain explicit and preserved
