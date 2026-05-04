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
                "answer_payload": {
                    "answer_text": "Yes, A/C repair is available on weekdays.",
                    "supported_claims": [
                        {
                            "claim_id": "c-1",
                            "claim_type": "factual",
                            "text": "A/C repair is available weekdays.",
                            "support_status": "supported",
                            "citation_spans": [
                                {
                                    "chunk_id": "chunk-1",
                                    "start_char": 0,
                                    "end_char": 10,
                                    "quoted_text": "A/C repair",
                                }
                            ],
                        }
                    ],
                },
                "groundedness": {
                    "all_document_claims_cited": True,
                    "unsupported_claim_count": 0,
                    "citation_count": 1,
                },
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-std-1",
                    "outcome_type": "answer_ready",
                    "route_applied": "answer_from_retrieval",
                },
            },
        ),
        PipelineScenario(
            scenario_id="edge-clarification",
            category="edge",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-edge-1",
                "user_query": "Need heater help",
                "route_applied": "clarification",
                "retrieved_evidence": [],
                "selected_evidence": [],
                "evidence_attempted": False,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-edge-1",
                "outcome_type": "clarification_needed",
                "route_applied": "clarification",
                "clarification_payload": {
                    "reason": "The query may refer to central heat or water heater.",
                    "clarification_questions": ["Do you need furnace service or water heater service?"],
                },
                "groundedness": {
                    "all_document_claims_cited": False,
                    "unsupported_claim_count": 0,
                    "citation_count": 0,
                },
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-edge-1",
                    "outcome_type": "clarification_needed",
                    "route_applied": "clarification",
                },
            },
        ),
        PipelineScenario(
            scenario_id="failure-insufficient",
            category="failure",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-failure-1",
                "user_query": "Do you provide solar panel repair?",
                "route_applied": "insufficient_evidence",
                "retrieved_evidence": [],
                "selected_evidence": [],
                "evidence_attempted": True,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-failure-1",
                "outcome_type": "insufficient_evidence",
                "route_applied": "insufficient_evidence",
                "insufficient_evidence_payload": {
                    "reason": "No matching evidence chunks found.",
                    "safe_next_step": "Please share equipment type and issue details.",
                },
                "groundedness": {
                    "all_document_claims_cited": False,
                    "unsupported_claim_count": 0,
                    "citation_count": 0,
                },
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-failure-1",
                    "outcome_type": "insufficient_evidence",
                    "route_applied": "insufficient_evidence",
                },
            },
        ),
        PipelineScenario(
            scenario_id="failure-escalation",
            category="failure",
            expected_success=True,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-failure-2",
                "user_query": "Gas smell near furnace.",
                "route_applied": "human_escalation",
                "retrieved_evidence": [],
                "selected_evidence": [],
                "evidence_attempted": False,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-failure-2",
                "outcome_type": "escalation_required",
                "route_applied": "human_escalation",
                "escalation_payload": {
                    "reason": "Potential safety hazard.",
                    "severity": "critical",
                    "handoff_target": "emergency_line",
                    "handoff_summary": "Possible gas leak reported near furnace.",
                    "safe_user_message": "Please leave the area and call emergency services now.",
                },
                "groundedness": {
                    "all_document_claims_cited": False,
                    "unsupported_claim_count": 0,
                    "citation_count": 0,
                },
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-failure-2",
                    "outcome_type": "escalation_required",
                    "route_applied": "human_escalation",
                },
            },
        ),
        PipelineScenario(
            scenario_id="negative-bad-citation",
            category="failure",
            expected_success=False,
            request_payload={
                "schema_version": "04b.v1",
                "request_id": "req-neg-1",
                "user_query": "Do you offer AC repair?",
                "route_applied": "answer_from_retrieval",
                "retrieved_evidence": [_retrieved("chunk-1", "A/C repair available weekdays.")],
                "selected_evidence": [_selected("chunk-1", "A/C repair available weekdays.")],
                "evidence_attempted": True,
            },
            outcome_payload={
                "schema_version": "04b.v1",
                "request_id": "req-neg-1",
                "outcome_type": "answer_ready",
                "route_applied": "answer_from_retrieval",
                "answer_payload": {
                    "answer_text": "Yes, A/C repair is available on weekdays.",
                    "supported_claims": [
                        {
                            "claim_id": "c-1",
                            "claim_type": "factual",
                            "text": "A/C repair is available weekdays.",
                            "support_status": "supported",
                            "citation_spans": [
                                {
                                    "chunk_id": "chunk-1",
                                    "start_char": 0,
                                    "end_char": 8,
                                    "quoted_text": "WrongTxt",
                                }
                            ],
                        }
                    ],
                },
                "groundedness": {
                    "all_document_claims_cited": True,
                    "unsupported_claim_count": 0,
                    "citation_count": 1,
                },
                "outcome_event": {
                    "event_type": "answer_assembly_outcome_created",
                    "request_id": "req-neg-1",
                    "outcome_type": "answer_ready",
                    "route_applied": "answer_from_retrieval",
                },
            },
        ),
    ]
