# Contract — 04b Answer Contract Schemas

## Status

Implemented and validated (PASS). This document remains the must-level contract reference.

Contract authority rule:

- This `CONTRACT.md` contains must-level implementation rules.
- `DESIGN.md` explains rationale and boundaries.
- `TEST_PLAN.md` mirrors these must-level rules as planned validation tests.
- Ambiguous guidance must not be converted into implementation behavior without first updating this `CONTRACT.md`.

This document defines the planned schema contract for the later Pydantic implementation. It is intentionally written as implementation requirements, not Python code.

## Contract goal

The schema contract must ensure that answer assembly receives and returns safe, structured, traceable payloads.

The contract should make invalid states difficult to represent and easy to reject.

## Planned top-level objects

### AnswerAssemblyRequest

Planned purpose:

Input object for answer assembly.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `schema_version` | yes | string | Contract version, for example `04b.design` during design or a stable version later. |
| `request_id` | yes | string | Stable ID for traceability. |
| `user_query` | yes | string | Original user request. |
| `route_applied` | yes | `RouteApplied` | Route chosen before answer assembly. |
| `retrieved_evidence` | yes | list of `RetrievedEvidenceItem` | Evidence from retrieval/evaluation. May be empty only when the route did not retrieve. |
| `selected_evidence` | yes | list of `SelectedEvidenceItem` | Evidence selected for answer construction. Required for `answer_ready`. |
| `evidence_attempted` | yes | boolean | Indicates whether retrieval was attempted for this request. |
| `retrieval_metadata` | no | object | Optional metadata from `03g` or `03h`. |

Planned validation rules:

- `request_id` must not be blank.
- `user_query` must not be blank.
- `route_applied` must be one of the allowed enum values.
- `route_applied` must satisfy the required `outcome_type` mapping in this contract.
- every selected evidence item must reference a `chunk_id` present in `retrieved_evidence`.
- selected evidence must include `selected_text`.
- `answer_from_retrieval` requires at least one `RetrievedEvidenceItem`.
- `insufficient_evidence` requires `evidence_attempted=true` and may have zero retrieved items only when retrieval produced no usable chunks.
- `clarification` may have zero retrieved items only when the request cannot be safely routed to retrieval yet.
- `human_escalation` may have zero retrieved items only when escalation occurs before retrieval due to safety/risk.
- any branch that contains selected evidence or cited claims requires corresponding retrieved evidence by `chunk_id`.

---

### RetrievedEvidenceItem

Planned purpose:

Represents one evidence chunk returned by retrieval.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `chunk_id` | yes | string | Stable chunk identifier. |
| `document_id` | yes | string | Source document identifier. |
| `source_file` | yes | string | Source file name. |
| `source_path` | yes | string | Repo-relative or source-relative path. |
| `title` | yes | string | Human-readable source title. |
| `text` | yes | string | Full retrieved chunk text. |
| `score` | no | number | Retrieval score if available. |
| `rank` | no | integer | Retrieval rank if available. |
| `metadata` | no | object | Additional retrieval metadata. |

Planned validation rules:

- `chunk_id`, `document_id`, `source_file`, `source_path`, and `text` must not be blank.
- `rank`, if present, must be positive.
- `score`, if present, must be numeric.

---

### SelectedEvidenceItem

Planned purpose:

Represents evidence selected for answer assembly.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `chunk_id` | yes | string | Must match retrieved evidence. |
| `document_id` | yes | string | Source document identifier. |
| `source_file` | yes | string | Source file name. |
| `source_path` | yes | string | Source path. |
| `title` | yes | string | Source title. |
| `selected_text` | yes | string | Full selected evidence text used for citation resolution. |
| `text_excerpt` | no | string | Short display excerpt only. |
| `selection_reason` | no | string | Why this evidence was selected. |

Planned validation rules:

- `selected_text` is required when selected evidence is used.
- `selected_text` must not be blank.
- `text_excerpt` must not be treated as the authoritative citation text.
- `chunk_id` must exist in retrieved evidence for the same request.

---

### CitationSpan

Planned purpose:

Represents the exact evidence span supporting a claim.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `chunk_id` | yes | string | Evidence chunk referenced by the citation. |
| `start_char` | yes | integer | Inclusive start character offset. |
| `end_char` | yes | integer | Exclusive end character offset. |
| `quoted_text` | yes | string | Text expected at the span. |

Planned validation rules:

- `start_char` must be greater than or equal to `0`.
- `end_char` must be greater than `start_char`.
- `quoted_text` must not be blank.
- `chunk_id` must exist in selected evidence or retrieved evidence.
- citation spans must resolve against `selected_text` or original retrieved evidence `text` for the same `chunk_id`.
- `quoted_text` must match the resolved span using normalized-exact matching:
  - trim leading/trailing whitespace
  - collapse repeated whitespace
  - compare case-sensitively
  - do not ignore punctuation
  - do not use fuzzy matching

---

### SupportedClaim

Planned purpose:

Represents a claim that answer assembly may include or rely on.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `claim_id` | yes | string | Stable claim identifier. |
| `claim_type` | yes | `ClaimType` | Type of claim. |
| `text` | yes | string | Claim text. |
| `support_status` | yes | `SupportStatus` | Whether the claim is supported. |
| `citation_spans` | yes | list of `CitationSpan` | Required for document-derived supported claims. |

Planned validation rules:

- claim text must not be blank.
- `factual`, `instructional`, and `policy` claims require citations.
- `factual`, `instructional`, and `policy` claims must use `support_status` of `supported` or `unsupported`; `not_required` is invalid.
- `conversational_glue` claims may use `not_required`; `supported` is allowed only when citations are intentionally present.
- document-derived claims in `answer_ready` must have `support_status = supported`.
- unsupported factual, instructional, or policy claims are not allowed in `answer_ready`.
- `not_required` must never be used to bypass citation requirements for factual, instructional, or policy claims.

---

### GroundednessSummary

Planned purpose:

Summarizes evidence grounding for the outcome.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `all_document_claims_cited` | yes | boolean | Whether document-derived claims have citations. |
| `unsupported_claim_count` | yes | integer | Count of unsupported document-derived claims. |
| `citation_count` | yes | integer | Total citation span count. |
| `notes` | no | list of strings | Optional diagnostic notes. |

Planned validation rules:

- counts must be zero or positive.
- `answer_ready` requires `all_document_claims_cited = true`.
- `answer_ready` requires `unsupported_claim_count = 0`.
- `answer_ready` requires `citation_count > 0`.

---

### AnswerPayload

Planned purpose:

Branch payload for `answer_ready`.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `answer_text` | yes | string | Final answer text generated later by answer assembly. |
| `supported_claims` | yes | list of `SupportedClaim` | Claims used in the answer. |

Planned validation rules:

- `answer_text` must not be blank.
- must include at least one supported claim.
- every factual, instructional, or policy claim must include citation spans.
- all citation spans must resolve.

---

### InsufficientEvidencePayload

Planned purpose:

Branch payload for `insufficient_evidence`.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `reason` | yes | string | Why evidence is insufficient. |
| `missing_information` | no | list of strings | What is missing. |
| `safe_next_step` | no | string | Safe next step without pretending to answer. |

Planned validation rules:

- `reason` must not be blank.
- this payload must not include answer text.
- this branch must not pretend to answer the user query.
- any next step must be framed as a limitation or safe follow-up, not as a factual answer.

---

### ClarificationPayload

Planned purpose:

Branch payload for `clarification_needed`.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `reason` | yes | string | Why clarification is needed. |
| `clarification_questions` | yes | list of strings | Questions needed from the user. |

Planned validation rules:

- `reason` must not be blank.
- at least one clarification question is required.
- questions must not be blank.
- this branch should not contain a final answer payload.

---

### EscalationPayload

Planned purpose:

Branch payload for `escalation_required`.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `reason` | yes | string | Why escalation is required. |
| `severity` | yes | `Severity` | Controlled severity value. |
| `handoff_target` | yes | `HandoffTarget` | Controlled handoff target value. |
| `handoff_summary` | yes | string | Operational summary for later handoff. |
| `safe_user_message` | yes | string | Safe message that may be shown to the user later. |

Planned validation rules:

- `reason` must not be blank.
- `severity` must be a valid enum value.
- `handoff_target` must be a valid enum value.
- `handoff_summary` is required for `escalation_required`.
- `safe_user_message` is required for `escalation_required`.
- `handoff_summary` must be plain text only and must be 1-1000 characters.
- `safe_user_message` must be plain text only and must be 1-500 characters.
- HTML tags must be rejected.
- script-like content must be rejected.
- empty or whitespace-only values must be rejected.
- punctuation is allowed.
- line breaks are allowed.
- unknown free-form escalation targets are rejected.
- escalation event fields must match top-level outcome fields.

---

### OutcomeEvent

Planned purpose:

Structured event describing the outcome for logging or later workflow use.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `event_type` | yes | string | Example: `answer_assembly_outcome_created`. |
| `request_id` | yes | string | Must match top-level request ID. |
| `outcome_type` | yes | `OutcomeType` | Must match top-level outcome. |
| `route_applied` | yes | `RouteApplied` | Must match top-level route. |
| `diagnostics` | no | object | Optional counts or notes. |

Planned validation rules:

- event request ID must match top-level request ID.
- event outcome type must match top-level outcome type.
- event route must match top-level route.

---

### AnswerAssemblyOutcome

Planned purpose:

Full top-level final output shape for every branch.

Planned fields:

| Field | Required | Type | Notes |
|---|---:|---|---|
| `schema_version` | yes | string | Contract version. |
| `request_id` | yes | string | Stable request ID. |
| `outcome_type` | yes | `OutcomeType` | Determines active branch payload. |
| `route_applied` | yes | `RouteApplied` | Route used. |
| `groundedness` | yes | `GroundednessSummary` | Grounding summary. |
| `answer_payload` | conditional | `AnswerPayload` | Required only for `answer_ready`. |
| `insufficient_evidence_payload` | conditional | `InsufficientEvidencePayload` | Required only for `insufficient_evidence`. |
| `clarification_payload` | conditional | `ClarificationPayload` | Required only for `clarification_needed`. |
| `escalation_payload` | conditional | `EscalationPayload` | Required only for `escalation_required`. |
| `outcome_event` | yes | `OutcomeEvent` | Event record. |

Planned validation rules:

- every outcome branch must use full top-level `AnswerAssemblyOutcome` shape.
- exactly one branch payload must be present.
- the present branch payload must match `outcome_type`.
- branch payloads for other outcomes must be absent.
- top-level request, route, and outcome fields must match the `outcome_event`.

## Planned enums

### OutcomeType

Allowed values:

- `answer_ready`
- `insufficient_evidence`
- `clarification_needed`
- `escalation_required`

### RouteApplied

Allowed values:

- `answer_from_retrieval`
- `clarification`
- `insufficient_evidence`
- `human_escalation`

### ClaimType

Allowed values:

- `factual`
- `instructional`
- `policy`
- `conversational_glue`

### SupportStatus

Allowed values:

- `supported`
- `unsupported`
- `not_required`

### Severity

Allowed values:

- `low`
- `medium`
- `high`
- `urgent`

### HandoffTarget

Allowed values:

- `customer_service`
- `dispatcher`
- `technician`
- `manager`
- `emergency_guidance`

## Branch contract summary

| Outcome type | Required payload | Must include | Must not include |
|---|---|---|---|
| `answer_ready` | `answer_payload` | cited supported document claims | unsupported document-derived claims |
| `insufficient_evidence` | `insufficient_evidence_payload` | reason evidence is insufficient | confident answer text |
| `clarification_needed` | `clarification_payload` | at least one clarification question | final answer payload |
| `escalation_required` | `escalation_payload` | valid severity and handoff target | unknown routing labels |

## Sample valid payload shapes

These are design samples, not output files.

### Valid `answer_ready`

```json
{
  "schema_version": "04b.design",
  "request_id": "req-001",
  "outcome_type": "answer_ready",
  "route_applied": "answer_from_retrieval",
  "groundedness": {
    "all_document_claims_cited": true,
    "unsupported_claim_count": 0,
    "citation_count": 1,
    "notes": []
  },
  "answer_payload": {
    "answer_text": "North Texas Comfort & Home Services offers A/C repair based on the selected company service document.",
    "supported_claims": [
      {
        "claim_id": "claim-001",
        "claim_type": "factual",
        "text": "The company offers A/C repair.",
        "support_status": "supported",
        "citation_spans": [
          {
            "chunk_id": "chunk-services-001",
            "start_char": 0,
            "end_char": 16,
            "quoted_text": "A/C repair"
          }
        ]
      }
    ]
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "req-001",
    "outcome_type": "answer_ready",
    "route_applied": "answer_from_retrieval",
    "diagnostics": {
      "supported_claim_count": 1
    }
  }
}
```

### Valid `insufficient_evidence`

```json
{
  "schema_version": "04b.design",
  "request_id": "req-002",
  "outcome_type": "insufficient_evidence",
  "route_applied": "insufficient_evidence",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0,
    "notes": ["No selected evidence supported the requested answer."]
  },
  "insufficient_evidence_payload": {
    "reason": "The retrieved evidence does not contain enough information to answer safely.",
    "missing_information": ["service availability for the requested item"],
    "safe_next_step": "Ask for more details or route to a human review step."
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "req-002",
    "outcome_type": "insufficient_evidence",
    "route_applied": "insufficient_evidence"
  }
}
```

### Valid `clarification_needed`

```json
{
  "schema_version": "04b.design",
  "request_id": "req-003",
  "outcome_type": "clarification_needed",
  "route_applied": "clarification",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0,
    "notes": ["User intent is ambiguous."]
  },
  "clarification_payload": {
    "reason": "The request does not include enough detail to choose the correct service path.",
    "clarification_questions": [
      "Are you asking about A/C repair, heating repair, plumbing, or appliance repair?"
    ]
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "req-003",
    "outcome_type": "clarification_needed",
    "route_applied": "clarification"
  }
}
```

### Valid `escalation_required`

```json
{
  "schema_version": "04b.design",
  "request_id": "req-004",
  "outcome_type": "escalation_required",
  "route_applied": "human_escalation",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0,
    "notes": ["The request requires operational handling."]
  },
  "escalation_payload": {
    "reason": "The case should be reviewed by dispatch before giving guidance.",
    "severity": "high",
    "handoff_target": "dispatcher",
    "handoff_summary": "Customer request appears operationally urgent and should be routed to dispatch.",
    "safe_user_message": "I need to route this to the right team for help."
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "req-004",
    "outcome_type": "escalation_required",
    "route_applied": "human_escalation"
  }
}
```

## Sample invalid payload expectations

### Invalid: answer-ready without cited claims

Reason to reject:

- `answer_ready` requires cited supported claims.

```json
{
  "schema_version": "04b.design",
  "request_id": "bad-001",
  "outcome_type": "answer_ready",
  "route_applied": "answer_from_retrieval",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 1,
    "citation_count": 0
  },
  "answer_payload": {
    "answer_text": "The company offers every requested service.",
    "supported_claims": []
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "bad-001",
    "outcome_type": "answer_ready",
    "route_applied": "answer_from_retrieval"
  }
}
```

### Invalid: selected evidence missing selected_text

Reason to reject:

- selected evidence requires `selected_text`.

```json
{
  "chunk_id": "chunk-services-001",
  "document_id": "services",
  "source_file": "services.md",
  "source_path": "data/services.md",
  "title": "Services"
}
```

### Invalid: citation references missing chunk

Reason to reject:

- citation span must resolve against selected or retrieved evidence by `chunk_id`.

```json
{
  "claim_id": "bad-claim-001",
  "claim_type": "factual",
  "text": "The company offers emergency plumbing.",
  "support_status": "supported",
  "citation_spans": [
    {
      "chunk_id": "missing-chunk",
      "start_char": 0,
      "end_char": 10,
      "quoted_text": "plumbing"
    }
  ]
}
```

### Invalid: insufficient evidence pretends to answer

Reason to reject:

- `insufficient_evidence` must not include a confident answer payload.

```json
{
  "schema_version": "04b.design",
  "request_id": "bad-002",
  "outcome_type": "insufficient_evidence",
  "route_applied": "insufficient_evidence",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0
  },
  "insufficient_evidence_payload": {
    "reason": "Evidence is missing.",
    "safe_next_step": "The answer is definitely yes."
  },
  "answer_payload": {
    "answer_text": "Yes, the company definitely provides this service.",
    "supported_claims": []
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "bad-002",
    "outcome_type": "insufficient_evidence",
    "route_applied": "insufficient_evidence"
  }
}
```

### Invalid: clarification without questions

Reason to reject:

- `clarification_needed` requires at least one clarification question.

```json
{
  "schema_version": "04b.design",
  "request_id": "bad-003",
  "outcome_type": "clarification_needed",
  "route_applied": "clarification",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0
  },
  "clarification_payload": {
    "reason": "The request is ambiguous.",
    "clarification_questions": []
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "bad-003",
    "outcome_type": "clarification_needed",
    "route_applied": "clarification"
  }
}
```

### Invalid: escalation with unknown severity and target

Reason to reject:

- `severity` and `handoff_target` must be controlled enum values.

```json
{
  "schema_version": "04b.design",
  "request_id": "bad-004",
  "outcome_type": "escalation_required",
  "route_applied": "human_escalation",
  "groundedness": {
    "all_document_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_count": 0
  },
  "escalation_payload": {
    "reason": "Needs help.",
    "severity": "super_critical",
    "handoff_target": "whoever_is_available"
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome_created",
    "request_id": "bad-004",
    "outcome_type": "escalation_required",
    "route_applied": "human_escalation"
  }
}
```

## Required route/outcome mapping

The implementation must enforce the following mapping:

| `outcome_type` | allowed `route_applied` |
|---|---|
| `answer_ready` | `answer_from_retrieval` |
| `insufficient_evidence` | `insufficient_evidence` |
| `clarification_needed` | `clarification` |
| `escalation_required` | `human_escalation` |

Reject examples:

- `outcome_type=answer_ready` with `route_applied=human_escalation`
- `outcome_type=escalation_required` with `route_applied=answer_from_retrieval`

## Contract non-goals

This contract does not define:

- retrieval scoring algorithms
- confidence thresholds
- LLM prompting
- final answer wording style
- FastAPI request/response routes
- database logging schema
- customer-facing UI behavior
