from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.schemas import (
    AnswerAssemblyOutcome,
    AnswerAssemblyRequest,
    ClaimType,
    OutcomeType,
    RouteApplied,
    SupportStatus,
    validate_outcome_against_request,
)


def make_retrieved(*, chunk_id: str = "chunk-1", text: str = "A/C repair available.") -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc-1",
        "source_file": "services.md",
        "source_path": "data/services.md",
        "title": "Services",
        "text": text,
        "score": 0.91,
        "rank": 1,
    }


def make_selected(*, chunk_id: str = "chunk-1", selected_text: str = "A/C repair available.") -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc-1",
        "source_file": "services.md",
        "source_path": "data/services.md",
        "title": "Services",
        "selected_text": selected_text,
    }


def make_request(route: RouteApplied = RouteApplied.ANSWER_FROM_RETRIEVAL) -> dict:
    return {
        "schema_version": "04b.v1",
        "request_id": "req-1",
        "user_query": "Do you offer AC repair?",
        "route_applied": route,
        "retrieved_evidence": [make_retrieved()],
        "selected_evidence": [make_selected()],
        "evidence_attempted": True,
    }


def make_supported_claim() -> dict:
    return {
        "claim_id": "claim-1",
        "claim_type": ClaimType.FACTUAL,
        "text": "The company offers A/C repair.",
        "support_status": SupportStatus.SUPPORTED,
        "citation_spans": [
            {
                "chunk_id": "chunk-1",
                "start_char": 0,
                "end_char": 10,
                "quoted_text": "A/C repair",
            }
        ],
    }


def make_outcome(outcome: OutcomeType = OutcomeType.ANSWER_READY) -> dict:
    base = {
        "schema_version": "04b.v1",
        "request_id": "req-1",
        "outcome_type": outcome,
        "route_applied": {
            OutcomeType.ANSWER_READY: RouteApplied.ANSWER_FROM_RETRIEVAL,
            OutcomeType.INSUFFICIENT_EVIDENCE: RouteApplied.INSUFFICIENT_EVIDENCE,
            OutcomeType.CLARIFICATION_NEEDED: RouteApplied.CLARIFICATION,
            OutcomeType.ESCALATION_REQUIRED: RouteApplied.HUMAN_ESCALATION,
        }[outcome],
        "groundedness": {
            "all_document_claims_cited": outcome == OutcomeType.ANSWER_READY,
            "unsupported_claim_count": 0,
            "citation_count": 1 if outcome == OutcomeType.ANSWER_READY else 0,
        },
        "outcome_event": {
            "event_type": "answer_assembly_outcome_created",
            "request_id": "req-1",
            "outcome_type": outcome,
            "route_applied": {
                OutcomeType.ANSWER_READY: RouteApplied.ANSWER_FROM_RETRIEVAL,
                OutcomeType.INSUFFICIENT_EVIDENCE: RouteApplied.INSUFFICIENT_EVIDENCE,
                OutcomeType.CLARIFICATION_NEEDED: RouteApplied.CLARIFICATION,
                OutcomeType.ESCALATION_REQUIRED: RouteApplied.HUMAN_ESCALATION,
            }[outcome],
        },
    }

    if outcome == OutcomeType.ANSWER_READY:
        base["answer_payload"] = {
            "answer_text": "A/C repair is offered.",
            "supported_claims": [make_supported_claim()],
        }
    elif outcome == OutcomeType.INSUFFICIENT_EVIDENCE:
        base["insufficient_evidence_payload"] = {
            "reason": "No matching service chunk.",
            "safe_next_step": "Please provide additional details.",
        }
    elif outcome == OutcomeType.CLARIFICATION_NEEDED:
        base["clarification_payload"] = {
            "reason": "Ambiguous request.",
            "clarification_questions": ["Do you need A/C or heating service?"],
        }
    else:
        base["escalation_payload"] = {
            "reason": "Operational risk.",
            "severity": "high",
            "handoff_target": "dispatcher",
            "handoff_summary": "Needs urgent dispatch review.",
            "safe_user_message": "I need to route this to the right team.",
        }

    return base


def test_answer_assembly_request_valid():
    model = AnswerAssemblyRequest.model_validate(make_request())
    assert model.request_id == "req-1"


@pytest.mark.parametrize(
    ("outcome", "route"),
    [
        (OutcomeType.ANSWER_READY, RouteApplied.ANSWER_FROM_RETRIEVAL),
        (OutcomeType.INSUFFICIENT_EVIDENCE, RouteApplied.INSUFFICIENT_EVIDENCE),
        (OutcomeType.CLARIFICATION_NEEDED, RouteApplied.CLARIFICATION),
        (OutcomeType.ESCALATION_REQUIRED, RouteApplied.HUMAN_ESCALATION),
    ],
)
def test_route_outcome_mapping_valid(outcome: OutcomeType, route: RouteApplied):
    payload = make_outcome(outcome)
    payload["route_applied"] = route
    payload["outcome_event"]["route_applied"] = route
    model = AnswerAssemblyOutcome.model_validate(payload)
    assert model.outcome_type == outcome


@pytest.mark.parametrize(
    ("outcome", "bad_route"),
    [
        (OutcomeType.ANSWER_READY, RouteApplied.HUMAN_ESCALATION),
        (OutcomeType.ESCALATION_REQUIRED, RouteApplied.ANSWER_FROM_RETRIEVAL),
        (OutcomeType.CLARIFICATION_NEEDED, RouteApplied.INSUFFICIENT_EVIDENCE),
        (OutcomeType.INSUFFICIENT_EVIDENCE, RouteApplied.CLARIFICATION),
    ],
)
def test_route_outcome_mapping_invalid(outcome: OutcomeType, bad_route: RouteApplied):
    payload = make_outcome(outcome)
    payload["route_applied"] = bad_route
    payload["outcome_event"]["route_applied"] = bad_route
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_branch_exclusive_invalid_two_payloads():
    payload = make_outcome(OutcomeType.ANSWER_READY)
    payload["escalation_payload"] = {
        "reason": "x",
        "severity": "high",
        "handoff_target": "dispatcher",
        "handoff_summary": "s",
        "safe_user_message": "m",
    }
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_claim_support_status_not_required_for_factual_invalid():
    claim = make_supported_claim()
    claim["support_status"] = SupportStatus.NOT_REQUIRED
    payload = make_outcome(OutcomeType.ANSWER_READY)
    payload["answer_payload"]["supported_claims"] = [claim]
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_conversational_glue_not_required_valid_without_citation():
    claim = {
        "claim_id": "c2",
        "claim_type": ClaimType.CONVERSATIONAL_GLUE,
        "text": "Thanks for clarifying.",
        "support_status": SupportStatus.NOT_REQUIRED,
        "citation_spans": [],
    }
    payload = make_outcome(OutcomeType.ANSWER_READY)
    payload["answer_payload"]["supported_claims"] = [
        {**make_supported_claim()},
        claim,
    ]
    model = AnswerAssemblyOutcome.model_validate(payload)
    assert model.answer_payload is not None


def test_unsupported_claim_not_allowed_in_final_answer():
    claim = make_supported_claim()
    claim["support_status"] = SupportStatus.UNSUPPORTED
    payload = make_outcome(OutcomeType.ANSWER_READY)
    payload["answer_payload"]["supported_claims"] = [claim]
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


@pytest.mark.parametrize("bad", ["<b>html</b>", "<script>alert(1)</script>", "javascript:alert(1)"])
def test_escalation_plain_text_rejects_html_script(bad: str):
    payload = make_outcome(OutcomeType.ESCALATION_REQUIRED)
    payload["escalation_payload"]["handoff_summary"] = bad
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_escalation_length_limits_enforced():
    payload = make_outcome(OutcomeType.ESCALATION_REQUIRED)
    payload["escalation_payload"]["safe_user_message"] = "x" * 501
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_clarification_requires_question():
    payload = make_outcome(OutcomeType.CLARIFICATION_NEEDED)
    payload["clarification_payload"]["clarification_questions"] = []
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_insufficient_evidence_no_confident_answer_text():
    payload = make_outcome(OutcomeType.INSUFFICIENT_EVIDENCE)
    payload["insufficient_evidence_payload"]["safe_next_step"] = "The answer is definitely yes."
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(payload)


def test_request_selected_chunk_must_exist_in_retrieved():
    req = make_request()
    req["selected_evidence"][0]["chunk_id"] = "missing"
    with pytest.raises(ValidationError):
        AnswerAssemblyRequest.model_validate(req)


def test_empty_evidence_gating_answer_from_retrieval_invalid():
    req = make_request(RouteApplied.ANSWER_FROM_RETRIEVAL)
    req["retrieved_evidence"] = []
    req["selected_evidence"] = []
    with pytest.raises(ValidationError):
        AnswerAssemblyRequest.model_validate(req)


def test_empty_evidence_gating_insufficient_requires_attempted_true():
    req = make_request(RouteApplied.INSUFFICIENT_EVIDENCE)
    req["retrieved_evidence"] = []
    req["selected_evidence"] = []
    req["evidence_attempted"] = False
    with pytest.raises(ValidationError):
        AnswerAssemblyRequest.model_validate(req)


def test_empty_evidence_gating_clarification_allows_zero_retrieved():
    req = make_request(RouteApplied.CLARIFICATION)
    req["retrieved_evidence"] = []
    req["selected_evidence"] = []
    req["evidence_attempted"] = False
    model = AnswerAssemblyRequest.model_validate(req)
    assert model.route_applied == RouteApplied.CLARIFICATION


def test_empty_evidence_gating_human_escalation_allows_zero_retrieved():
    req = make_request(RouteApplied.HUMAN_ESCALATION)
    req["retrieved_evidence"] = []
    req["selected_evidence"] = []
    req["evidence_attempted"] = False
    model = AnswerAssemblyRequest.model_validate(req)
    assert model.route_applied == RouteApplied.HUMAN_ESCALATION


def test_cross_validation_exact_citation_match():
    request = AnswerAssemblyRequest.model_validate(make_request())
    outcome = AnswerAssemblyOutcome.model_validate(make_outcome(OutcomeType.ANSWER_READY))
    validate_outcome_against_request(request, outcome)


def test_cross_validation_normalized_whitespace_match():
    req = make_request()
    req["selected_evidence"][0]["selected_text"] = "A/C   repair available."
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["end_char"] = 12
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["quoted_text"] = "  A/C repair "
    request = AnswerAssemblyRequest.model_validate(req)
    outcome = AnswerAssemblyOutcome.model_validate(out)
    validate_outcome_against_request(request, outcome)


def test_cross_validation_wrong_chunk_id_rejected():
    request = AnswerAssemblyRequest.model_validate(make_request())
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["chunk_id"] = "missing"
    outcome = AnswerAssemblyOutcome.model_validate(out)
    with pytest.raises(ValueError):
        validate_outcome_against_request(request, outcome)


def test_cross_validation_punctuation_mismatch_rejected():
    request = AnswerAssemblyRequest.model_validate(make_request())
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["quoted_text"] = "A/C repair!"
    outcome = AnswerAssemblyOutcome.model_validate(out)
    with pytest.raises(ValueError):
        validate_outcome_against_request(request, outcome)


def test_cross_validation_case_mismatch_rejected():
    request = AnswerAssemblyRequest.model_validate(make_request())
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["quoted_text"] = "a/c repair"
    outcome = AnswerAssemblyOutcome.model_validate(out)
    with pytest.raises(ValueError):
        validate_outcome_against_request(request, outcome)


def test_cross_validation_span_not_found_rejected():
    request = AnswerAssemblyRequest.model_validate(make_request())
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["answer_payload"]["supported_claims"][0]["citation_spans"][0]["end_char"] = 200
    outcome = AnswerAssemblyOutcome.model_validate(out)
    with pytest.raises(ValueError):
        validate_outcome_against_request(request, outcome)


def test_event_consistency_mismatch_rejected():
    out = make_outcome(OutcomeType.ANSWER_READY)
    out["outcome_event"]["request_id"] = "wrong"
    with pytest.raises(ValidationError):
        AnswerAssemblyOutcome.model_validate(out)
