from __future__ import annotations

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


HTML_TAG_RE = re.compile(r"<[^>]+>")
SCRIPTY_RE = re.compile(r"(?i)(<\s*script|javascript:|onerror\s*=|onload\s*=)")
REPEATED_WS_RE = re.compile(r"\s+")
ANSWER_LIKE_RE = re.compile(r"(?i)(\bthe answer is\b|\bdefinitely\b|\bcertainly\b|\bguaranteed\b)")


class OutcomeType(str, Enum):
    ANSWER_READY = "answer_ready"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CLARIFICATION_NEEDED = "clarification_needed"
    ESCALATION_REQUIRED = "escalation_required"


class RouteApplied(str, Enum):
    ANSWER_FROM_RETRIEVAL = "answer_from_retrieval"
    CLARIFICATION = "clarification"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    HUMAN_ESCALATION = "human_escalation"


class ClaimType(str, Enum):
    FACTUAL = "factual"
    INSTRUCTIONAL = "instructional"
    POLICY = "policy"
    CONVERSATIONAL_GLUE = "conversational_glue"


class SupportStatus(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    NOT_REQUIRED = "not_required"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class HandoffTarget(str, Enum):
    CUSTOMER_SERVICE = "customer_service"
    DISPATCHER = "dispatcher"
    TECHNICIAN = "technician"
    MANAGER = "manager"
    EMERGENCY_GUIDANCE = "emergency_guidance"


def _must_not_be_blank(value: str, field_name: str) -> str:
    if value.strip() == "":
        raise ValueError(f"{field_name} must not be blank")
    return value


def _normalize_text(value: str) -> str:
    return REPEATED_WS_RE.sub(" ", value.strip())


def _validate_plain_text(value: str, field_name: str, max_len: int) -> str:
    _must_not_be_blank(value, field_name)
    if len(value) > max_len:
        raise ValueError(f"{field_name} must be <= {max_len} characters")
    if HTML_TAG_RE.search(value):
        raise ValueError(f"{field_name} must be plain text only")
    if SCRIPTY_RE.search(value):
        raise ValueError(f"{field_name} contains script-like content")
    return value


class BaseContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RetrievedEvidenceItem(BaseContractModel):
    chunk_id: str
    document_id: str
    source_file: str
    source_path: str
    title: str
    text: str
    score: float | None = None
    rank: int | None = None
    metadata: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "RetrievedEvidenceItem":
        _must_not_be_blank(self.chunk_id, "chunk_id")
        _must_not_be_blank(self.document_id, "document_id")
        _must_not_be_blank(self.source_file, "source_file")
        _must_not_be_blank(self.source_path, "source_path")
        _must_not_be_blank(self.text, "text")
        if self.rank is not None and self.rank <= 0:
            raise ValueError("rank must be positive")
        return self


class SelectedEvidenceItem(BaseContractModel):
    chunk_id: str
    document_id: str
    source_file: str
    source_path: str
    title: str
    selected_text: str
    text_excerpt: str | None = None
    selection_reason: str | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "SelectedEvidenceItem":
        _must_not_be_blank(self.chunk_id, "chunk_id")
        _must_not_be_blank(self.document_id, "document_id")
        _must_not_be_blank(self.source_file, "source_file")
        _must_not_be_blank(self.source_path, "source_path")
        _must_not_be_blank(self.selected_text, "selected_text")
        return self


class CitationSpan(BaseContractModel):
    chunk_id: str
    start_char: int
    end_char: int
    quoted_text: str

    @model_validator(mode="after")
    def validate_fields(self) -> "CitationSpan":
        _must_not_be_blank(self.chunk_id, "chunk_id")
        _must_not_be_blank(self.quoted_text, "quoted_text")
        if self.start_char < 0:
            raise ValueError("start_char must be >= 0")
        if self.end_char <= self.start_char:
            raise ValueError("end_char must be > start_char")
        return self


class SupportedClaim(BaseContractModel):
    claim_id: str
    claim_type: ClaimType
    text: str
    support_status: SupportStatus
    citation_spans: list[CitationSpan] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_fields(self) -> "SupportedClaim":
        _must_not_be_blank(self.claim_id, "claim_id")
        _must_not_be_blank(self.text, "text")

        document_claim = self.claim_type in {
            ClaimType.FACTUAL,
            ClaimType.INSTRUCTIONAL,
            ClaimType.POLICY,
        }

        if document_claim and self.support_status == SupportStatus.NOT_REQUIRED:
            raise ValueError("document-derived claims cannot use support_status=not_required")

        if self.claim_type == ClaimType.CONVERSATIONAL_GLUE and self.support_status == SupportStatus.SUPPORTED:
            if not self.citation_spans:
                raise ValueError("conversational_glue supported claims require citations when intentionally supported")

        if document_claim and self.support_status == SupportStatus.SUPPORTED and not self.citation_spans:
            raise ValueError("supported factual/instructional/policy claims require citations")

        return self


class GroundednessSummary(BaseContractModel):
    all_document_claims_cited: bool
    unsupported_claim_count: int
    citation_count: int
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_fields(self) -> "GroundednessSummary":
        if self.unsupported_claim_count < 0:
            raise ValueError("unsupported_claim_count must be >= 0")
        if self.citation_count < 0:
            raise ValueError("citation_count must be >= 0")
        return self


class AnswerPayload(BaseContractModel):
    answer_text: str
    supported_claims: list[SupportedClaim]

    @model_validator(mode="after")
    def validate_fields(self) -> "AnswerPayload":
        _must_not_be_blank(self.answer_text, "answer_text")
        if not self.supported_claims:
            raise ValueError("answer_payload must include at least one supported claim")
        for claim in self.supported_claims:
            if (
                claim.claim_type == ClaimType.CONVERSATIONAL_GLUE
                and claim.support_status == SupportStatus.NOT_REQUIRED
            ):
                continue
            if claim.support_status != SupportStatus.SUPPORTED:
                raise ValueError("final answer claims must be supported")
        return self


class InsufficientEvidencePayload(BaseContractModel):
    reason: str
    missing_information: list[str] = Field(default_factory=list)
    safe_next_step: str | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "InsufficientEvidencePayload":
        _must_not_be_blank(self.reason, "reason")
        if self.safe_next_step is not None and ANSWER_LIKE_RE.search(self.safe_next_step):
            raise ValueError("safe_next_step must not pretend to provide a confident answer")
        return self


class ClarificationPayload(BaseContractModel):
    reason: str
    clarification_questions: list[str]

    @model_validator(mode="after")
    def validate_fields(self) -> "ClarificationPayload":
        _must_not_be_blank(self.reason, "reason")
        if not self.clarification_questions:
            raise ValueError("clarification_questions must contain at least one question")
        for question in self.clarification_questions:
            _must_not_be_blank(question, "clarification_questions item")
        return self


class EscalationPayload(BaseContractModel):
    reason: str
    severity: Severity
    handoff_target: HandoffTarget
    handoff_summary: str
    safe_user_message: str

    @model_validator(mode="after")
    def validate_fields(self) -> "EscalationPayload":
        _must_not_be_blank(self.reason, "reason")
        _validate_plain_text(self.handoff_summary, "handoff_summary", 1000)
        _validate_plain_text(self.safe_user_message, "safe_user_message", 500)
        return self


class OutcomeEvent(BaseContractModel):
    event_type: str
    request_id: str
    outcome_type: OutcomeType
    route_applied: RouteApplied
    diagnostics: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "OutcomeEvent":
        _must_not_be_blank(self.event_type, "event_type")
        _must_not_be_blank(self.request_id, "request_id")
        return self


ROUTE_FOR_OUTCOME: dict[OutcomeType, RouteApplied] = {
    OutcomeType.ANSWER_READY: RouteApplied.ANSWER_FROM_RETRIEVAL,
    OutcomeType.INSUFFICIENT_EVIDENCE: RouteApplied.INSUFFICIENT_EVIDENCE,
    OutcomeType.CLARIFICATION_NEEDED: RouteApplied.CLARIFICATION,
    OutcomeType.ESCALATION_REQUIRED: RouteApplied.HUMAN_ESCALATION,
}


class AnswerAssemblyOutcome(BaseContractModel):
    schema_version: str
    request_id: str
    outcome_type: OutcomeType
    route_applied: RouteApplied
    groundedness: GroundednessSummary
    answer_payload: AnswerPayload | None = None
    insufficient_evidence_payload: InsufficientEvidencePayload | None = None
    clarification_payload: ClarificationPayload | None = None
    escalation_payload: EscalationPayload | None = None
    outcome_event: OutcomeEvent

    @model_validator(mode="after")
    def validate_fields(self) -> "AnswerAssemblyOutcome":
        _must_not_be_blank(self.schema_version, "schema_version")
        _must_not_be_blank(self.request_id, "request_id")

        expected_route = ROUTE_FOR_OUTCOME[self.outcome_type]
        if self.route_applied != expected_route:
            raise ValueError("route_applied does not match required mapping for outcome_type")

        if self.outcome_event.request_id != self.request_id:
            raise ValueError("outcome_event.request_id must match request_id")
        if self.outcome_event.outcome_type != self.outcome_type:
            raise ValueError("outcome_event.outcome_type must match outcome_type")
        if self.outcome_event.route_applied != self.route_applied:
            raise ValueError("outcome_event.route_applied must match route_applied")

        payloads = {
            OutcomeType.ANSWER_READY: self.answer_payload,
            OutcomeType.INSUFFICIENT_EVIDENCE: self.insufficient_evidence_payload,
            OutcomeType.CLARIFICATION_NEEDED: self.clarification_payload,
            OutcomeType.ESCALATION_REQUIRED: self.escalation_payload,
        }
        present_payloads = [name for name, payload in payloads.items() if payload is not None]

        if len(present_payloads) != 1:
            raise ValueError("exactly one branch payload must be present")
        if payloads[self.outcome_type] is None:
            raise ValueError("branch payload must match outcome_type")

        if self.outcome_type == OutcomeType.ANSWER_READY:
            if not self.groundedness.all_document_claims_cited:
                raise ValueError("answer_ready requires all_document_claims_cited=true")
            if self.groundedness.unsupported_claim_count != 0:
                raise ValueError("answer_ready requires unsupported_claim_count=0")
            if self.groundedness.citation_count <= 0:
                raise ValueError("answer_ready requires citation_count > 0")

            assert self.answer_payload is not None
            for claim in self.answer_payload.supported_claims:
                if claim.claim_type in {ClaimType.FACTUAL, ClaimType.INSTRUCTIONAL, ClaimType.POLICY} and not claim.citation_spans:
                    raise ValueError("document-derived supported claims in answer_ready require citations")

        return self


class AnswerAssemblyRequest(BaseContractModel):
    schema_version: str
    request_id: str
    user_query: str
    route_applied: RouteApplied
    retrieved_evidence: list[RetrievedEvidenceItem]
    selected_evidence: list[SelectedEvidenceItem]
    evidence_attempted: bool
    retrieval_metadata: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_fields(self) -> "AnswerAssemblyRequest":
        _must_not_be_blank(self.schema_version, "schema_version")
        _must_not_be_blank(self.request_id, "request_id")
        _must_not_be_blank(self.user_query, "user_query")

        retrieved_ids = {item.chunk_id for item in self.retrieved_evidence}

        for selected in self.selected_evidence:
            if selected.chunk_id not in retrieved_ids:
                raise ValueError("selected evidence chunk_id must exist in retrieved_evidence")

        if self.route_applied == RouteApplied.ANSWER_FROM_RETRIEVAL and not self.retrieved_evidence:
            raise ValueError("answer_from_retrieval requires at least one retrieved evidence item")

        if self.route_applied == RouteApplied.INSUFFICIENT_EVIDENCE and not self.evidence_attempted:
            raise ValueError("insufficient_evidence route requires evidence_attempted=true")

        if self.selected_evidence and not self.retrieved_evidence:
            raise ValueError("selected evidence requires corresponding retrieved evidence")

        return self


def validate_outcome_against_request(request: AnswerAssemblyRequest, outcome: AnswerAssemblyOutcome) -> None:
    """Cross-object validator for rules that require request evidence context."""
    if request.request_id != outcome.request_id:
        raise ValueError("request_id mismatch between request and outcome")

    if outcome.route_applied != request.route_applied:
        raise ValueError("request.route_applied must match outcome.route_applied")

    selected_by_chunk = {item.chunk_id: item.selected_text for item in request.selected_evidence}
    retrieved_by_chunk = {item.chunk_id: item.text for item in request.retrieved_evidence}

    if outcome.answer_payload is None:
        return

    for claim in outcome.answer_payload.supported_claims:
        for citation in claim.citation_spans:
            base_text = selected_by_chunk.get(citation.chunk_id)
            if base_text is None:
                base_text = retrieved_by_chunk.get(citation.chunk_id)

            if base_text is None:
                raise ValueError("citation chunk_id must resolve to selected or retrieved evidence")

            if citation.end_char > len(base_text):
                raise ValueError("citation span is outside evidence text length")

            source_slice = base_text[citation.start_char:citation.end_char]
            if _normalize_text(source_slice) != _normalize_text(citation.quoted_text):
                raise ValueError("citation quoted_text must match resolved span in normalized-exact mode")

    cited_chunk_ids = {
        citation.chunk_id
        for claim in outcome.answer_payload.supported_claims
        for citation in claim.citation_spans
    }

    for chunk_id in cited_chunk_ids:
        if chunk_id not in retrieved_by_chunk:
            raise ValueError("cited claims require corresponding retrieved evidence chunk_id")
