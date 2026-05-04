# Test Plan — 04b Answer Contract Schemas

## Status

Implemented and validated (PASS). Planned tests have been implemented and executed for 04b.

Contract authority rule:

- `CONTRACT.md` contains must-level implementation rules.
- `DESIGN.md` explains rationale and boundaries.
- This `TEST_PLAN.md` mirrors must-level rules as planned validation tests.
- Ambiguous guidance must not be converted into implementation behavior without first updating `CONTRACT.md`.

This document defines the planned validation tests for the later Pydantic implementation. No tests are created in this design-only step.

## Test goal

The tests should prove that the planned schema layer accepts safe, complete, traceable payloads and rejects malformed or unsafe payloads before answer assembly.

The tests should focus on contract behavior, not retrieval scoring and not generated answer quality.

## Test strategy

The later implementation should use pytest to validate:

1. model construction for valid payloads
2. enum restrictions
3. required fields
4. branch-specific validation
5. citation traceability
6. claim support rules
7. event consistency
8. safe escalation structure
9. compatibility with expected `03g` and `03h` evidence-style records

## Planned test groups

### 1. Model smoke tests

Purpose:

Confirm every planned schema model can be instantiated with a minimal valid payload.

Planned cases:

- valid `AnswerAssemblyRequest`
- valid `RetrievedEvidenceItem`
- valid `SelectedEvidenceItem`
- valid `CitationSpan`
- valid `SupportedClaim`
- valid `GroundednessSummary`
- valid `AnswerPayload`
- valid `InsufficientEvidencePayload`
- valid `ClarificationPayload`
- valid `EscalationPayload`
- valid `OutcomeEvent`
- valid `AnswerAssemblyOutcome`

Expected result:

- valid payloads pass validation
- parsed objects preserve expected field values

---

### 2. Enum validation tests

Purpose:

Confirm controlled values prevent unsafe free-form states.

Planned cases:

- valid `OutcomeType` values pass
- invalid outcome type fails
- valid `RouteApplied` values pass
- invalid route fails
- valid `ClaimType` values pass
- invalid claim type fails
- valid `SupportStatus` values pass
- invalid support status fails
- valid `Severity` values pass
- invalid severity fails
- valid `HandoffTarget` values pass
- invalid handoff target fails

Expected result:

- only documented enum values are accepted

---

### 2a. Route/outcome mapping tests

Purpose:

Enforce required `outcome_type` to `route_applied` mapping.

Planned valid cases:

- `answer_ready` with `answer_from_retrieval`
- `insufficient_evidence` with `insufficient_evidence`
- `clarification_needed` with `clarification`
- `escalation_required` with `human_escalation`

Planned invalid cases:

- `answer_ready` with `human_escalation`
- `escalation_required` with `answer_from_retrieval`
- `clarification_needed` with `insufficient_evidence`
- `insufficient_evidence` with `clarification`

Expected result:

- each outcome accepts only its mapped route

---

### 3. Full top-level outcome shape tests

Purpose:

Make sure every outcome branch uses the full `AnswerAssemblyOutcome` structure.

Planned valid cases:

- `answer_ready` with full top-level shape
- `insufficient_evidence` with full top-level shape
- `clarification_needed` with full top-level shape
- `escalation_required` with full top-level shape

Planned invalid cases:

- non-answer branch returns only its branch payload
- outcome missing `schema_version`
- outcome missing `request_id`
- outcome missing `route_applied`
- outcome missing `groundedness`
- outcome missing `outcome_event`

Expected result:

- full shape passes
- partial branch-only payloads fail

---

### 4. Branch exclusivity tests

Purpose:

Make sure exactly one branch payload exists and matches `outcome_type`.

Planned valid cases:

- `answer_ready` includes only `answer_payload`
- `insufficient_evidence` includes only `insufficient_evidence_payload`
- `clarification_needed` includes only `clarification_payload`
- `escalation_required` includes only `escalation_payload`

Planned invalid cases:

- `answer_ready` missing `answer_payload`
- `answer_ready` includes both answer and escalation payloads
- `insufficient_evidence` includes `answer_payload`
- `clarification_needed` includes no clarification payload
- `escalation_required` includes insufficient evidence payload instead of escalation payload

Expected result:

- exactly one matching branch payload is required

---

### 5. Selected evidence validation tests

Purpose:

Protect answer assembly from malformed selected evidence.

Planned valid cases:

- selected evidence includes `selected_text`
- selected evidence `chunk_id` exists in retrieved evidence
- optional `text_excerpt` is allowed

Planned invalid cases:

- selected evidence missing `selected_text`
- selected evidence has blank `selected_text`
- selected evidence references a missing `chunk_id`
- selected evidence has blank `source_path`

Expected result:

- selected evidence must remain traceable and citeable

---

### 6. Citation span validation tests

Purpose:

Prevent fake or broken citations.

Planned valid cases:

- citation span resolves against `SelectedEvidenceItem.selected_text`
- citation span resolves against `RetrievedEvidenceItem.text` when selected text does not contain the full span but original text does
- exact span match passes
- normalized whitespace match passes (trim edges and collapse repeated whitespace)
- `quoted_text` matches the resolved span in normalized-exact mode

Planned invalid cases:

- citation span references missing `chunk_id`
- `start_char` is negative
- `end_char` is not greater than `start_char`
- span is outside the evidence text length
- `quoted_text` does not match resolved span text
- punctuation mismatch fails
- case mismatch fails
- span text not found fails

Expected result:

- citations must point to real evidence text by `chunk_id`
- matching is normalized-exact, case-sensitive, punctuation-sensitive, and non-fuzzy

---

### 7. Claim support tests

Purpose:

Enforce citation requirements for document-derived claims.

Planned valid cases:

- factual claim with citation passes
- instructional claim with citation passes
- policy claim with citation passes
- conversational glue claim without citation passes when `support_status = not_required`
- conversational glue claim with `support_status = supported` passes only when citations are intentionally present

Planned invalid cases:

- factual claim without citation fails
- instructional claim without citation fails
- policy claim without citation fails
- factual claim with `support_status = not_required` fails
- instructional claim with `support_status = not_required` fails
- policy claim with `support_status = not_required` fails
- unsupported factual claim appears in `answer_ready`
- unsupported policy claim appears in `answer_ready`

Expected result:

- document-derived claims require citations
- conversational glue text does not require citations
- `not_required` cannot bypass citation rules for factual, instructional, or policy claims

---

### 8. Answer-ready validation tests

Purpose:

Ensure `answer_ready` means the system is actually ready to answer.

Planned valid cases:

- answer payload has non-empty answer text
- answer payload has at least one cited supported claim
- groundedness shows all document claims cited
- unsupported claim count is zero
- citation count is greater than zero

Planned invalid cases:

- answer text is blank
- supported claim list is empty
- citation count is zero
- unsupported claim count is greater than zero
- groundedness says not all document claims are cited
- factual claim has no citation span

Expected result:

- `answer_ready` cannot pass without cited support

---

### 9. Insufficient-evidence validation tests

Purpose:

Ensure insufficient evidence does not become a fake answer.

Planned valid cases:

- payload includes reason
- payload includes missing information
- payload includes safe next step framed as limitation or follow-up

Planned invalid cases:

- missing reason
- blank reason
- includes `answer_payload`
- includes confident answer wording as answer text
- outcome type is `insufficient_evidence` but event says `answer_ready`

Expected result:

- insufficient evidence branch explains the gap and does not pretend to answer

---

### 10. Clarification validation tests

Purpose:

Ensure clarification branch gives the user actionable questions.

Planned valid cases:

- one clarification question
- multiple clarification questions
- reason explains ambiguity

Planned invalid cases:

- no clarification questions
- blank question
- missing reason
- includes answer payload
- event outcome mismatch

Expected result:

- clarification branch must ask at least one useful question

---

### 11. Escalation validation tests

Purpose:

Ensure escalation branch is controlled and safe.

Planned valid cases:

- valid severity
- valid handoff target
- reason included
- required handoff summary included
- required safe user message included
- handoff summary within 1-1000 chars
- safe user message within 1-500 chars
- plain text content accepted (including documented punctuation and line breaks)

Planned invalid cases:

- unknown severity
- unknown handoff target
- missing severity
- missing handoff target
- missing handoff summary
- missing safe user message
- empty or whitespace-only handoff summary
- empty or whitespace-only safe user message
- handoff summary longer than 1000 chars
- safe user message longer than 500 chars
- HTML tag content
- script-like content
- event route mismatch
- event outcome mismatch

Expected result:

- escalation payloads cannot route to uncontrolled targets

---

### 12. Outcome event consistency tests

Purpose:

Ensure top-level outcome and event data agree.

Planned valid cases:

- event request ID matches top-level request ID
- event outcome type matches top-level outcome type
- event route matches top-level route

Planned invalid cases:

- event request ID differs
- event outcome differs
- event route differs

Expected result:

- inconsistent logging events are rejected

---

### 13. Future 03g/03h compatibility tests

Purpose:

Ensure the schema layer can consume retrieval/evaluation-style records later without depending on scoring internals.

Planned valid cases:

- retrieved evidence record with `score` and `rank`
- retrieved evidence record with retrieval metadata
- selected evidence referencing a retrieved chunk
- request includes optional retrieval metadata from evaluation
- `answer_from_retrieval` request with non-empty retrieved evidence
- `insufficient_evidence` with `evidence_attempted=true` and zero retrieved evidence when no usable chunks were found
- `clarification` with `evidence_attempted=false` and zero retrieved evidence when not safe to route yet
- `human_escalation` with `evidence_attempted=false` and zero retrieved evidence when escalation occurs before retrieval for safety/risk

Planned invalid cases:

- selected chunk not present in retrieved evidence
- retrieved evidence missing full text
- retrieved evidence has blank chunk ID
- rank is zero or negative
- `answer_from_retrieval` with zero retrieved evidence
- `insufficient_evidence` with `evidence_attempted=false`
- branch contains selected evidence but no corresponding retrieved evidence by `chunk_id`
- branch contains cited claims but no corresponding retrieved evidence by `chunk_id`

Expected result:

- schema accepts useful retrieval metadata but validates evidence shape strictly

## Planned acceptance command for later implementation

When implementation exists, validation should use a command like:

```powershell
pytest -v .\pocs\04b_answer_contract_schemas\tests
```

This command is not run in the design-only step because no tests should exist yet.

## Planned test file boundaries for later

Possible later test files:

- `tests/test_schema_models.py`
- `tests/test_outcome_branches.py`
- `tests/test_citation_validation.py`
- `tests/test_claim_validation.py`
- `tests/test_escalation_validation.py`
- `tests/test_03g_03h_compatibility.py`

These files are intentionally not created yet.

## What not to test in this POC

The later schema tests should not test:

- retrieval ranking quality
- TF-IDF math
- confidence threshold tuning
- LLM answer quality
- FastAPI routes
- database writes
- UI behavior
- integrated service behavior

Those belong to other POCs or later integration work.

## Design review checklist

Before implementation, confirm:

- planned valid payloads match the approved 04a contract
- invalid payload examples cover the most dangerous failure modes
- enum values are acceptable
- citation resolution strategy is agreed
- selected evidence requirements are clear
- branch exclusivity rules are clear
- no implementation files were created during the design-only step
