# Design — 04b Answer Contract Schemas

## Status

Implemented and validated (PASS). This document remains the rationale/boundaries reference.

Contract authority rule:

- `CONTRACT.md` contains must-level implementation rules.
- This `DESIGN.md` explains rationale and boundaries.
- `TEST_PLAN.md` mirrors must-level rules as planned validation tests.
- Ambiguous guidance must not be converted into implementation behavior without first updating `CONTRACT.md`.

## Purpose

This POC defines the planned Pydantic schema layer for the answer assembly contract approved in `04a_answer_contract_design`.

The schema layer should sit between retrieval/evaluation outputs and answer assembly. It should validate that the system has a complete, safe, traceable structure before any answer text is produced or any escalation handoff is logged.

## Teaching idea

In a RAG system, retrieval can return messy evidence and answer generation can sound confident even when the input is weak.

Schemas are the guardrails in the middle.

They do not make the system intelligent by themselves. They make the system disciplined. They force the pipeline to say:

- What kind of outcome is this?
- What evidence was retrieved?
- What evidence was selected?
- Which claims are supported?
- Which citations prove those claims?
- Is this really an answer, or should it be clarification, insufficient evidence, or escalation?

Without this contract, downstream answer assembly would have to trust loosely shaped dictionaries. That is fragile and unsafe.

## Design principles

### 1. Full outcome shape for every branch

Every final branch must return the full top-level `AnswerAssemblyOutcome` shape.

This includes:

- `schema_version`
- `request_id`
- `outcome_type`
- `route_applied`
- `groundedness`
- branch-specific payload
- `outcome_event`

This prevents the system from returning small, incompatible objects for non-answer branches.

### 2. Evidence traceability is mandatory

When selected evidence is used, `selected_text` is required.

Citation spans must resolve against either:

- `SelectedEvidenceItem.selected_text`, or
- the original retrieved evidence text for the same `chunk_id`

This prevents fake citations and broken span references.

### 3. Claims are separate from final answer wording

The schema should model claims separately from answer text.

A claim is a factual, instructional, policy, or conversational unit that can be validated. The final answer may be generated later, but the schema should already know which claims require citations and whether they are supported.

### 4. Branch rules are explicit

Each outcome branch has a different purpose:

- `answer_ready` means the system has enough cited support to answer.
- `insufficient_evidence` means the system should not pretend to answer.
- `clarification_needed` means the system needs more user input.
- `escalation_required` means the case should be routed to a human or operational handoff target.

The schema should reject payloads that mix these meanings.

### 5. Retrieval and answer assembly stay decoupled

This schema layer should be able to consume structured retrieval/evaluation outputs from `03g` and `03h` later, but it should not call retrieval itself.

It validates evidence records; it does not rank evidence.

## Planned model boundaries

### AnswerAssemblyRequest

Planned role:

Represents the structured input to answer assembly.

Expected fields:

- `schema_version`
- `request_id`
- `user_query`
- `route_applied`
- `retrieved_evidence`
- `selected_evidence`
- `evidence_attempted`
- optional retrieval/evaluation metadata from `03g` and `03h`

Validation intent:

- require a non-empty `request_id`
- require a non-empty `user_query`
- require `route_applied` to be a known enum value
- allow empty selected evidence only for non-answer branches
- enforce route/outcome mapping rules defined in `CONTRACT.md`
- enforce request-level empty evidence rules defined in `CONTRACT.md`
- preserve chunk-level traceability from retrieved evidence

### RetrievedEvidenceItem

Planned role:

Represents one evidence chunk returned by retrieval or evaluation.

Expected fields:

- `chunk_id`
- `document_id`
- `source_file`
- `source_path`
- `title`
- `text`
- optional `score`
- optional `rank`
- optional retrieval metadata

Validation intent:

- require non-empty identifiers
- require non-empty evidence text
- keep scores numeric when present
- keep chunk IDs stable because citations depend on them

### SelectedEvidenceItem

Planned role:

Represents evidence chosen for answer assembly.

Expected fields:

- `chunk_id`
- `document_id`
- `source_file`
- `source_path`
- `title`
- `selected_text`
- optional `text_excerpt`
- optional selection reason

Validation intent:

- require `selected_text`
- require selected evidence to reference a retrieved `chunk_id`
- allow `text_excerpt` only as display-friendly helper text, not as the citation authority

### CitationSpan

Planned role:

Represents a citation pointer into selected or retrieved evidence text.

Expected fields:

- `chunk_id`
- `start_char`
- `end_char`
- `quoted_text`

Validation intent:

- require `start_char >= 0`
- require `end_char > start_char`
- require `quoted_text` to match the text slice identified by the span
- require the span to resolve against `selected_text` or original retrieved text for the same `chunk_id`
- use normalized-exact matching (trim edges, collapse repeated whitespace, case-sensitive, punctuation-sensitive, no fuzzy matching)

### SupportedClaim

Planned role:

Represents one claim the final answer may rely on.

Expected fields:

- `claim_id`
- `claim_type`
- `text`
- `support_status`
- `citation_spans`

Validation intent:

- factual, instructional, and policy claims require citations
- conversational glue claims do not require citations
- `answer_ready` outcomes must not include unsupported document-derived claims
- `not_required` must not be used for factual, instructional, or policy claims

### GroundednessSummary

Planned role:

Summarizes whether the assembled answer is grounded in selected evidence.

Expected fields:

- `all_document_claims_cited`
- `unsupported_claim_count`
- `citation_count`
- optional notes or failure reasons

Validation intent:

- `answer_ready` requires all document-derived claims cited
- `answer_ready` requires unsupported claim count to be zero
- non-answer branches may include groundedness explaining why no answer was produced

### AnswerPayload

Planned role:

Branch payload for `answer_ready`.

Expected fields:

- `answer_text`
- `supported_claims`
- optional citation display records

Validation intent:

- require non-empty answer text
- require at least one cited supported claim
- reject unsupported factual, instructional, or policy claims

### InsufficientEvidencePayload

Planned role:

Branch payload for `insufficient_evidence`.

Expected fields:

- `reason`
- optional `missing_information`
- optional `safe_next_step`

Validation intent:

- must not contain answer text pretending to satisfy the user request
- should explain the evidence gap
- may suggest a safe next step without inventing facts

### ClarificationPayload

Planned role:

Branch payload for `clarification_needed`.

Expected fields:

- `reason`
- `clarification_questions`

Validation intent:

- require at least one clarification question
- questions should be user-facing but not final answer text
- should not include unsupported claims as if answering

### EscalationPayload

Planned role:

Branch payload for `escalation_required`.

Expected fields:

- `reason`
- `severity`
- `handoff_target`
- `handoff_summary`
- `safe_user_message`

Validation intent:

- require valid severity
- require valid handoff target
- require non-empty plain-text `handoff_summary` (max 1000 chars)
- require non-empty plain-text `safe_user_message` (max 500 chars)
- reject HTML tags and script-like content
- prevent unsafe free-form routing labels
- keep the handoff summary operational and concise

### OutcomeEvent

Planned role:

Represents the structured event that can be logged later.

Expected fields:

- `event_type`
- `request_id`
- `outcome_type`
- `route_applied`
- optional counts and diagnostic metadata

Validation intent:

- event outcome must match top-level outcome
- event request ID must match top-level request ID
- event route must match top-level route

### AnswerAssemblyOutcome

Planned role:

Represents the final validated output of answer assembly.

Expected fields:

- `schema_version`
- `request_id`
- `outcome_type`
- `route_applied`
- `groundedness`
- one branch payload:
  - `answer_payload`
  - `insufficient_evidence_payload`
  - `clarification_payload`
  - `escalation_payload`
- `outcome_event`

Validation intent:

- require full top-level shape for every outcome
- require exactly one branch payload matching `outcome_type`
- reject missing required branch payloads
- reject extra branch payloads from other outcomes
- enforce branch-specific safety rules

## Planned enum boundaries

### OutcomeType

Planned values:

- `answer_ready`
- `insufficient_evidence`
- `clarification_needed`
- `escalation_required`

### RouteApplied

Planned values:

- `answer_from_retrieval`
- `clarification`
- `insufficient_evidence`
- `human_escalation`

The exact values should match the approved 04a contract during implementation.

### ClaimType

Planned values:

- `factual`
- `instructional`
- `policy`
- `conversational_glue`

### SupportStatus

Planned values:

- `supported`
- `unsupported`
- `not_required`

### Severity

Planned values:

- `low`
- `medium`
- `high`
- `urgent`

### HandoffTarget

Planned values:

- `customer_service`
- `dispatcher`
- `technician`
- `manager`
- `emergency_guidance`

The implementation should keep these values intentionally narrow so escalation routing is controlled.

## Required route/outcome mapping

The contract must enforce this one-to-one mapping:

| `outcome_type` | allowed `route_applied` |
|---|---|
| `answer_ready` | `answer_from_retrieval` |
| `insufficient_evidence` | `insufficient_evidence` |
| `clarification_needed` | `clarification` |
| `escalation_required` | `human_escalation` |

Examples that must be rejected:

- `outcome_type=answer_ready` with `route_applied=human_escalation`
- `outcome_type=escalation_required` with `route_applied=answer_from_retrieval`

## Claim type and support status boundaries

The contract must enforce:

- `factual` claims: `support_status` must be `supported` or `unsupported`; `not_required` is invalid.
- `instructional` claims: `support_status` must be `supported` or `unsupported`; `not_required` is invalid.
- `policy` claims: `support_status` must be `supported` or `unsupported`; `not_required` is invalid.
- `conversational_glue` claims: `support_status` may be `not_required`; `supported` is allowed only when citations are intentionally present.

Additional required behavior:

- supported document-derived claims require citations.
- unsupported document-derived claims must not be used as final answer claims.
- `not_required` must never be used to bypass citation requirements for factual, instructional, or policy claims.

## Request-level empty evidence boundaries

`AnswerAssemblyRequest.retrieved_evidence` may be empty only under controlled conditions:

- `answer_from_retrieval` requires at least one `RetrievedEvidenceItem`.
- `insufficient_evidence` requires `evidence_attempted=true` and may have zero retrieved items only when retrieval produced no usable chunks.
- `clarification` may have zero retrieved items when the request cannot be safely routed to retrieval yet.
- `human_escalation` may have zero retrieved items only when escalation happens before retrieval due to safety/risk.
- any branch containing `selected_evidence` or cited claims requires corresponding retrieved evidence by `chunk_id`.

`evidence_attempted` exists to distinguish "retrieval was attempted but yielded no usable chunks" from "retrieval was intentionally skipped".

## How 04b will consume 03g and 03h later

`03g_retrieval_decision` and `03h_retrieval_evaluation` are expected to provide structured evidence and decision metadata.

The planned schema should consume that data through fields such as:

- retrieved evidence items
- selected evidence items
- retrieval scores
- retrieval ranks
- retrieval decision labels
- evaluation summaries
- confidence or quality signals

However, `04b` should not depend on the internal scoring algorithm of those POCs. It should care about the shape and validity of evidence, not how the evidence was scored.

This separation lets retrieval improve later without rewriting the answer assembly schema contract.

## Safety protections

The schema layer should protect answer assembly from:

### Malformed evidence

Examples:

- missing `chunk_id`
- empty evidence text
- invalid source path
- selected evidence not present in retrieved evidence

### Missing citations

Examples:

- factual claim without citation span
- policy claim without citation span
- answer-ready payload with zero supported claims

### Invalid citations

Examples:

- span points outside text range
- `quoted_text` does not match the referenced span
- span references a missing `chunk_id`

### Invalid outcome branches

Examples:

- `outcome_type = answer_ready` but only escalation payload exists
- `outcome_type = clarification_needed` but no clarification questions exist
- `insufficient_evidence` contains a confident answer

### Unsafe escalation payloads

Examples:

- unknown severity such as `super_critical`
- free-form handoff target such as `somebody_call_them`
- escalation event does not match top-level outcome

## What this POC will not do

This POC will not:

- implement Pydantic models
- implement validators
- write tests
- create sample JSON files
- call retrieval code
- call an LLM
- generate user-facing answers
- modify retrieval thresholds
- integrate with FastAPI
- write logs
- update `integrated/servicecall-ai`

## Design review questions

Before implementation, review these questions:

1. Are the model names clear enough to become `schemas.py` classes?
2. Are the enum values narrow enough for safety but flexible enough for the demo?
3. Should citation span matching require exact string equality, normalized equality, or both?
4. Should selected evidence always be a subset of retrieved evidence?
5. Should branch payloads be modeled as optional fields with cross-field validation, or as a discriminated union?
6. What minimum metadata from `03g` and `03h` should be preserved without coupling too tightly to those POCs?
