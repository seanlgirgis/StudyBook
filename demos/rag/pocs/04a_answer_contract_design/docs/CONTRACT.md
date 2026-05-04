# 04a Answer Contract

## Contract Purpose
Define the planned input/output schemas for safe answer assembly with citations.

This is a design-only contract for approval before implementation.

## Upstream Inputs

### 1) Answer Request
Planned model: `AnswerRequest`

Required fields:
- `request_id` (string, unique per request)
- `query` (string, non-empty)
- `normalized_query` (string, non-empty)
- `conversation_turn` (integer, `>=1`)
- `channel` (enum: `chat`, `web_form`, `sms_demo`)
- `locale` (string, default `en-US`)
- `customer_context` (object; synthetic only)

Sample:
```json
{
  "request_id": "req_0001",
  "query": "water heater leaking near base",
  "normalized_query": "water heater leaking near base",
  "conversation_turn": 3,
  "channel": "chat",
  "locale": "en-US",
  "customer_context": {
    "service_city": "Plano",
    "is_return_customer": false
  }
}
```

### 2) Retrieval Evidence Packet
Planned model: `RetrievalEvidencePacket`

Purpose:
- carry retrieved candidates from `03f`
- carry decision signals from `03g`
- optionally carry evaluation context snapshot from `03h`

Required fields:
- `source_paths` (object with upstream artifact paths)
- `retrieved_evidence` (list of ranked candidates; from retrieval)
- `retrieval_decision` (single record; from `03g`)
- `evaluation_context` (object; optional but recommended)

Minimal candidate shape (`RetrievedEvidenceItem`):
- `rank`
- `chunk_id`
- `hybrid_score`
- `word_score`
- `char_score`
- `source_file`
- `title`
- `text`
- `normalized_text`

Decision minimum shape (`RetrievalDecisionSignal`):
- `decision_label`
- `recommended_route`
- `reason_codes`
- `decision_signals`

Sample:
```json
{
  "source_paths": {
    "retrieval_output_path": "pocs/03f_hybrid_retrieval/outputs/sample_hybrid_search_results.json",
    "decision_output_path": "pocs/03g_retrieval_decision/outputs/sample_retrieval_decisions.json",
    "evaluation_output_path": "pocs/03h_retrieval_evaluation/outputs/evaluation_report.json"
  },
  "retrieved_evidence": [
    {
      "rank": 1,
      "chunk_id": "water_heater_policy__chunk_000",
      "hybrid_score": 0.2206,
      "word_score": 0.1612,
      "char_score": 0.3310,
      "source_file": "water_heater_policy.md",
      "title": "Synthetic Demo Document",
      "text": "....",
      "normalized_text": "...."
    }
  ],
  "retrieval_decision": {
    "decision_label": "strong_match",
    "recommended_route": "answer_candidate_path",
    "reason_codes": [
      "TOP_SCORE_STRONG",
      "CLEAR_SCORE_GAP"
    ],
    "decision_signals": {
      "top_score": 0.2206,
      "score_gap": 0.0457
    }
  },
  "evaluation_context": {
    "evaluation_window_id": "03h_snapshot_001",
    "pass_rate": 1.0,
    "decision_label_match_rate": 1.0
  }
}
```

## Derived Internal Models (Planned)

### Selected Evidence
Planned model: `SelectedEvidenceItem`

Purpose:
- subset of retrieved evidence approved for claim support

Required fields:
- `selection_id`
- `chunk_id`
- `selection_reason_codes`
- `rank`
- `source_file`
- `title`
- `selected_text` (full selected evidence text used for citation span validation)

Optional/display-friendly fields:
- `text_excerpt`

### Citation
Planned model: `Citation`

Required fields:
- `citation_id`
- `chunk_id`
- `source_file`
- `title`
- `quote_excerpt`
- `span_start_char` (integer, `>=0`)
- `span_end_char` (integer, `> span_start_char`)

Citation rule:
- each citation must resolve to exactly one selected evidence chunk
- quote/span must be traceable against `selected_text` for that `chunk_id`, or against the original retrieved evidence `text` for that same `chunk_id`

### Claim Draft
Planned model: `ClaimDraft`

Required fields:
- `claim_id`
- `claim_text`
- `claim_type` (enum: `factual`, `instructional`, `policy`)
- `citation_ids` (list; required for all document-derived `factual`, `instructional`, and `policy` claims)
- `supported` (boolean)

Claim citation rule:
- all document-derived factual, policy, and instructional claims require citations
- conversational glue text (for example transitions, politeness scaffolding, and non-factual connective phrasing) does not require citation

## Primary Output Contract
Planned model: `AnswerAssemblyOutcome`

Top-level fields:
- `schema_version` (string)
- `request_id` (string)
- `outcome_type` (enum)
- `route_applied` (string)
- `reason_codes` (list of strings)
- `groundedness` (object)
- `payload` (one-of object by `outcome_type`)
- `outcome_event` (object; required for downstream logging)

`outcome_type` enum:
- `answer_ready`
- `insufficient_evidence`
- `clarification_needed`
- `escalation_required`

`outcome_event` minimum fields:
- `event_type` (`answer_assembly_outcome`)
- `event_status` (same enum as `outcome_type`)
- `event_timestamp_utc`
- `request_id`

## Payload Contracts by Outcome

### A) `answer_ready`
Payload model: `AnswerReadyPayload`

Required fields:
- `selected_evidence` (non-empty)
- `citations` (non-empty)
- `answer_draft` (structured claims)
- `final_answer_candidate` (rendered text + citation markers)
- `coverage` (citation coverage metrics)

Sample:
```json
{
  "schema_version": "1.0",
  "request_id": "req_0001",
  "outcome_type": "answer_ready",
  "route_applied": "answer_candidate_path",
  "reason_codes": [
    "EVIDENCE_SUFFICIENT",
    "CITATION_COVERAGE_OK"
  ],
  "groundedness": {
    "all_factual_claims_cited": true,
    "unsupported_claim_count": 0,
    "citation_coverage_ratio": 1.0
  },
  "payload": {
    "selected_evidence": [
      {
        "selection_id": "sel_001",
        "chunk_id": "water_heater_policy__chunk_000",
        "selection_reason_codes": [
          "TOP_RANKED",
          "HIGH_HYBRID_SCORE"
        ],
        "rank": 1,
        "source_file": "water_heater_policy.md",
        "title": "Synthetic Demo Document",
        "selected_text": "Repair-first if leak is not from tank body and cost is reasonable. Replace-first if tank is leaking from body seam or shows severe corrosion.",
        "text_excerpt": "Repair-first if leak is not from tank body..."
      }
    ],
    "citations": [
      {
        "citation_id": "cit_001",
        "chunk_id": "water_heater_policy__chunk_000",
        "source_file": "water_heater_policy.md",
        "title": "Synthetic Demo Document",
        "quote_excerpt": "Replace-first if tank is leaking from body seam...",
        "span_start_char": 120,
        "span_end_char": 182
      }
    ],
    "answer_draft": {
      "claims": [
        {
          "claim_id": "clm_001",
          "claim_text": "If the leak is from the tank body seam, replacement-first guidance applies.",
          "claim_type": "policy",
          "citation_ids": [
            "cit_001"
          ],
          "supported": true
        }
      ]
    },
    "final_answer_candidate": {
      "text": "For a leak from the tank body seam, replacement-first guidance is recommended. [cit_001]"
    },
    "coverage": {
      "total_claims": 1,
      "cited_claims": 1,
      "citation_coverage_ratio": 1.0
    }
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome",
    "event_status": "answer_ready",
    "event_timestamp_utc": "2026-05-03T15:04:00Z",
    "request_id": "req_0001"
  }
}
```

### B) `insufficient_evidence`
Payload model: `InsufficientEvidencePayload`

Required fields:
- `insufficiency_reasons` (non-empty list)
- `evidence_summary` (what was retrieved and why it was inadequate)
- `safe_fallback_message_template` (non-final, internal template)

Sample:
```json
{
  "schema_version": "1.0",
  "request_id": "req_0002",
  "outcome_type": "insufficient_evidence",
  "route_applied": "fallback_path",
  "reason_codes": [
    "LOW_RETRIEVAL_CONFIDENCE",
    "CITATION_COVERAGE_BELOW_MIN"
  ],
  "groundedness": {
    "all_factual_claims_cited": false,
    "unsupported_claim_count": 1,
    "citation_coverage_ratio": 0.5
  },
  "payload": {
    "insufficiency_reasons": [
      "Top evidence is weak and conflicting across service areas."
    ],
    "evidence_summary": {
      "retrieved_count": 5,
      "selected_count": 0
    },
    "safe_fallback_message_template": "I do not have enough reliable information to answer directly yet."
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome",
    "event_status": "insufficient_evidence",
    "event_timestamp_utc": "2026-05-03T15:05:00Z",
    "request_id": "req_0002"
  }
}
```

### C) `clarification_needed`
Payload model: `ClarificationNeededPayload`

Required fields:
- `clarification_reason_codes`
- `missing_slots`
- `clarification_options` (structured candidate choices)

Sample:
```json
{
  "schema_version": "1.0",
  "request_id": "req_0003",
  "outcome_type": "clarification_needed",
  "route_applied": "clarification_path",
  "reason_codes": [
    "QUERY_UNDERSPECIFIED_MULTI_SERVICE",
    "AMBIGUITY_REQUIRES_CLARIFICATION"
  ],
  "groundedness": {
    "all_factual_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_coverage_ratio": 0.0
  },
  "payload": {
    "clarification_reason_codes": [
      "MULTI_SERVICE_OVERLAP"
    ],
    "missing_slots": [
      "service_category"
    ],
    "clarification_options": [
      "Heating system repair",
      "Water heater repair",
      "Billing or pricing question"
    ]
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome",
    "event_status": "clarification_needed",
    "event_timestamp_utc": "2026-05-03T15:06:00Z",
    "request_id": "req_0003"
  }
}
```

### D) `escalation_required`
Payload model: `EscalationRequiredPayload`

Required fields:
- `risk_category`
- `severity`
- `handoff_target`
- `do_not_answer` (must be `true`)
- `escalation_notes`

Planned enums:
- `severity`: `low`, `medium`, `high`, `critical`
- `handoff_target`: `dispatch_review`, `supervisor_review`, `emergency_instruction_template`, `human_reviewer`

Sample:
```json
{
  "schema_version": "1.0",
  "request_id": "req_0004",
  "outcome_type": "escalation_required",
  "route_applied": "fallback_path",
  "reason_codes": [
    "SAFETY_RISK_GAS_SMELL"
  ],
  "groundedness": {
    "all_factual_claims_cited": false,
    "unsupported_claim_count": 0,
    "citation_coverage_ratio": 0.0
  },
  "payload": {
    "risk_category": "safety",
    "severity": "critical",
    "handoff_target": "dispatch_review",
    "do_not_answer": true,
    "escalation_notes": "Reported gas smell near water heater."
  },
  "outcome_event": {
    "event_type": "answer_assembly_outcome",
    "event_status": "escalation_required",
    "event_timestamp_utc": "2026-05-03T15:07:00Z",
    "request_id": "req_0004"
  }
}
```

## Validation Rules (Planned)
- `request_id` must be present and non-empty.
- `outcome_type` must be in enum.
- every outcome must include `outcome_event`.
- `retrieved_evidence` ranks must be positive and unique.
- `selected_evidence` chunk ids must exist in retrieved evidence.
- every citation must map to selected evidence.
- `selected_text` must be present for each selected evidence item used by citations.
- `span_start_char < span_end_char` for every citation span.
- citation spans must resolve against selected evidence `selected_text` or original retrieved evidence `text` for the same `chunk_id`.
- document-derived `factual`, `instructional`, and `policy` claims marked `supported=true` must include citation ids.
- `answer_ready` requires:
  - at least one selected evidence item
  - at least one citation
  - `groundedness.all_factual_claims_cited=true`
  - `unsupported_claim_count=0`
- `insufficient_evidence` requires:
  - non-empty insufficiency reasons
  - no final answer candidate text
- `clarification_needed` requires:
  - at least one missing slot or clarification option
  - no final answer candidate text
- `escalation_required` requires:
  - `do_not_answer=true`
  - handoff target present
  - no final answer candidate text
- `outcome_type` must be mutually exclusive; exactly one payload branch is allowed.

## Non-Goals for This Contract
- threshold tuning logic
- retrieval algorithm changes
- LLM prompt design
- final customer language policy
- integrated-lane orchestration
