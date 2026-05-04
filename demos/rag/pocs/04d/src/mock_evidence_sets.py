from __future__ import annotations

from .schemas import PipelineScenario


def _retrieved(chunk_id: str, text: str, rank: int = 1, score: float = 0.9) -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc-1",
        "source_file": "services.md",
        "source_path": "data/services.md",
        "title": "Services",
        "text": text,
        "score": score,
        "rank": rank,
    }


def _selected(chunk_id: str, selected_text: str) -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc-1",
        "source_file": "services.md",
        "source_path": "data/services.md",
        "title": "Services",
        "selected_text": selected_text,
    }


def build_mock_scenarios() -> list[PipelineScenario]:
    return [
        PipelineScenario(
            scenario_id="std-answer-ready",
            category="standard",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-std-1",
                "user_query": "Do you offer AC repair?",
                "route_applied": "answer_from_retrieval",
                "retrieved_evidence": [_retrieved("chunk-1", "A/C repair available weekdays.")],
                "selected_evidence": [_selected("chunk-1", "A/C repair available weekdays.")],
                "evidence_attempted": True,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-std-1",
                "outcome_type": "answer_ready",
                "route_applied": "answer_from_retrieval",
                "answer_payload": {"answer_text": "Yes, A/C repair is available.", "supported_claims": [{"claim_id": "c1", "claim_type": "factual", "text": "A/C repair is available.", "support_status": "supported", "citation_spans": [{"chunk_id": "chunk-1", "start_char": 0, "end_char": 10, "quoted_text": "A/C repair"}]}]},
                "groundedness": {"all_document_claims_cited": True, "unsupported_claim_count": 0, "citation_count": 1},
                "outcome_event": {"event_type": "answer_assembly_outcome_created", "request_id": "req-std-1", "outcome_type": "answer_ready", "route_applied": "answer_from_retrieval"},
            },
        ),
        PipelineScenario(
            scenario_id="edge-clarification",
            category="edge",
            expected_success=True,
            request_payload={"schema_version": "04b.v1", "request_id": "req-edge-1", "user_query": "Need heater help", "route_applied": "clarification", "retrieved_evidence": [], "selected_evidence": [], "evidence_attempted": False},
            outcome_payload={"schema_version": "04b.v1", "request_id": "req-edge-1", "outcome_type": "clarification_needed", "route_applied": "clarification", "clarification_payload": {"reason": "Ambiguous", "clarification_questions": ["Furnace or water heater?"]}, "groundedness": {"all_document_claims_cited": False, "unsupported_claim_count": 0, "citation_count": 0}, "outcome_event": {"event_type": "answer_assembly_outcome_created", "request_id": "req-edge-1", "outcome_type": "clarification_needed", "route_applied": "clarification"}},
        ),
        PipelineScenario(
            scenario_id="negative-bad-citation",
            category="failure",
            expected_success=False,
            request_payload={"schema_version": "04b.v1", "request_id": "req-neg-1", "user_query": "Do you offer AC repair?", "route_applied": "answer_from_retrieval", "retrieved_evidence": [_retrieved("chunk-1", "A/C repair available weekdays.")], "selected_evidence": [_selected("chunk-1", "A/C repair available weekdays.")], "evidence_attempted": True},
            outcome_payload={"schema_version": "04b.v1", "request_id": "req-neg-1", "outcome_type": "answer_ready", "route_applied": "answer_from_retrieval", "answer_payload": {"answer_text": "Yes", "supported_claims": [{"claim_id": "c1", "claim_type": "factual", "text": "A/C repair is available.", "support_status": "supported", "citation_spans": [{"chunk_id": "chunk-1", "start_char": 0, "end_char": 8, "quoted_text": "WrongTxt"}]}]}, "groundedness": {"all_document_claims_cited": True, "unsupported_claim_count": 0, "citation_count": 1}, "outcome_event": {"event_type": "answer_assembly_outcome_created", "request_id": "req-neg-1", "outcome_type": "answer_ready", "route_applied": "answer_from_retrieval"}},
        ),
        PipelineScenario(
            scenario_id="failure-insufficient-evidence",
            category="failure",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-ins-1",
                "user_query": "Do you service geothermal heat pumps?",
                "route_applied": "insufficient_evidence",
                "retrieved_evidence": [],
                "selected_evidence": [],
                "evidence_attempted": True,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-ins-1",
                "outcome_type": "insufficient_evidence",
                "route_applied": "insufficient_evidence",
                "insufficient_evidence_payload": {
                    "reason": "No matching chunks found in approved corpus.",
                    "safe_next_step": "Please share model details and issue symptoms.",
                },
                "groundedness": {"all_document_claims_cited": False, "unsupported_claim_count": 0, "citation_count": 0},
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-ins-1",
                    "outcome_type": "insufficient_evidence",
                    "route_applied": "insufficient_evidence",
                },
            },
        ),
        PipelineScenario(
            scenario_id="failure-escalation-required",
            category="failure",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-esc-1",
                "user_query": "There is a strong gas smell by the furnace.",
                "route_applied": "human_escalation",
                "retrieved_evidence": [],
                "selected_evidence": [],
                "evidence_attempted": False,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-esc-1",
                "outcome_type": "escalation_required",
                "route_applied": "human_escalation",
                "escalation_payload": {
                    "reason": "Potential life-safety issue.",
                    "severity": "urgent",
                    "handoff_target": "emergency_guidance",
                    "handoff_summary": "Customer reported a gas odor near heating equipment.",
                    "safe_user_message": "Please leave the area and call emergency services immediately.",
                },
                "groundedness": {"all_document_claims_cited": False, "unsupported_claim_count": 0, "citation_count": 0},
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-esc-1",
                    "outcome_type": "escalation_required",
                    "route_applied": "human_escalation",
                },
            },
        ),
    ]


def build_performance_batch(batch_size: int = 50) -> list[PipelineScenario]:
    base = build_mock_scenarios()
    scenarios: list[PipelineScenario] = []
    for index in range(batch_size):
        source = base[index % len(base)]
        cloned = source.model_copy(deep=True)
        suffix = f"-perf-{index}"
        cloned.scenario_id = f"{source.scenario_id}{suffix}"
        cloned.request_payload["request_id"] = f"{source.request_payload['request_id']}{suffix}"
        cloned.outcome_payload["request_id"] = f"{source.outcome_payload['request_id']}{suffix}"
        cloned.outcome_payload["outcome_event"]["request_id"] = f"{source.outcome_payload['outcome_event']['request_id']}{suffix}"
        scenarios.append(cloned)
    return scenarios
