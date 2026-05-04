# 04a Answer Contract Test Plan

## Test Plan Purpose
Define how future implementation should validate the `04a` answer assembly contract.

This is a planning artifact only.  
No tests are implemented in this step.

## Validation Strategy
- Contract-first validation with strict schema checks.
- Branch-specific invariant checks by `outcome_type`.
- Groundedness checks at claim and citation level.
- Compatibility checks against known `03g` and `03h` artifact shapes.
- Negative-path tests to prove unsafe outputs are rejected.

## Planned Test Levels

### 1) Schema Validation Tests
Objective:
- ensure request, evidence packet, and outcome objects obey required field/type constraints

Examples:
- reject missing `request_id`
- reject empty `normalized_query`
- reject unknown `outcome_type`
- reject missing `outcome_event`
- reject any outcome branch object that does not include full top-level `AnswerAssemblyOutcome` fields (`schema_version`, `request_id`, `outcome_type`, `route_applied`, `reason_codes`, `groundedness`, `payload`, `outcome_event`)
- reject invalid enum values for decision labels/routes passed from `03g`

### 2) Upstream Compatibility Tests
Objective:
- verify `04a` input adapters can read expected minimal fields from `03f`/`03g`/`03h` outputs

Examples:
- accept `03f` candidate fields (`rank`, `chunk_id`, score fields, text/meta fields)
- accept `03g` decision fields (`decision_label`, `recommended_route`, `reason_codes`)
- accept `03h` summary context fields when present
- fail cleanly when upstream records are missing required minimal fields

### 3) Evidence Selection Integrity Tests
Objective:
- enforce valid transition from retrieved evidence to selected evidence

Examples:
- selected chunk id must exist in retrieved list
- selected rank must map to retrieved rank
- duplicate `selection_id` rejected
- empty selection for `answer_ready` rejected

### 4) Citation Integrity Tests
Objective:
- enforce citation traceability and span correctness

Examples:
- citation must reference a selected evidence `chunk_id`
- selected evidence used by citations must include `selected_text`
- `span_start_char` must be less than `span_end_char`
- citation span must resolve against `selected_text` or original retrieved evidence `text` by matching `chunk_id`
- quote excerpt must be non-empty
- duplicate `citation_id` rejected

### 5) Claim Groundedness Tests
Objective:
- protect against unsupported factual assertions

Examples:
- `claim_type=factual` and `supported=true` requires at least one citation id
- `claim_type=instructional` and `supported=true` requires at least one citation id when document-derived
- `claim_type=policy` and `supported=true` requires at least one citation id when document-derived
- cited claim ids must reference existing citations
- `answer_ready` fails when `unsupported_claim_count > 0`
- `answer_ready` fails when `all_factual_claims_cited=false`

### 6) Outcome Branch Invariant Tests
Objective:
- ensure each outcome branch is valid and mutually exclusive

Examples:
- `answer_ready` requires selected evidence, citations, and final answer candidate
- `insufficient_evidence` requires insufficiency reasons and must not include final answer candidate
- `clarification_needed` requires missing slots/options and must not include final answer candidate
- `escalation_required` requires `do_not_answer=true` and handoff target
- reject payloads containing multiple branch objects at once

### 7) Clarification Outcome Tests
Objective:
- validate representation of clarification-needed scenarios

Examples:
- allow `03g` label `needs_clarification` to map to `clarification_needed` outcome
- require at least one clarification option or missing slot
- ensure reason codes are present and non-empty

### 8) Insufficient Evidence Outcome Tests
Objective:
- validate no-answer behavior when evidence is inadequate

Examples:
- low-confidence or conflicting evidence maps to `insufficient_evidence`
- ensure fallback template exists
- ensure final answer candidate is absent

### 9) Escalation Outcome Tests
Objective:
- validate risky-case routing behavior

Examples:
- safety-risk reason triggers `escalation_required`
- severity enum validation
- handoff target required
- handoff target enum validation (`dispatch_review`, `supervisor_review`, `emergency_instruction_template`, `human_reviewer`)
- `do_not_answer` must be true

### 10) Outcome Event Logging Contract Tests
Objective:
- ensure every interaction emits an outcome event payload

Examples:
- event exists for all outcomes
- `event_status` matches `outcome_type`
- `request_id` consistency between request and event

## Planned Acceptance Checks for 04a Design Approval
- all required docs exist:
  - `README.md`
  - `docs/DESIGN.md`
  - `docs/CONTRACT.md`
  - `docs/TEST_PLAN.md`
- contract includes sample JSON for primary inputs and all outcome branches
- groundedness/citation protections are explicit
- insufficient evidence, clarification, and escalation outcomes are explicitly represented
- non-goals preserve no-code and no-integrated-lane constraints

## Exit Criteria for Future Implementation Readiness
- design approved by reviewer
- no unresolved contract ambiguities on required fields/enums
- test plan provides enough detail to implement deterministic validation tests in a later POC
