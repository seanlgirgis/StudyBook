"""Pydantic schemas for 03h labeled retrieval fixtures."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class LabeledRetrievalCase(BaseModel):
    """One labeled case used for retrieval and decision evaluation."""

    case_id: str
    query: str
    normalized_query: str | None = None
    expected_chunk_id: str
    expected_decision_label: str
    expected_recommended_route: str

    @field_validator(
        "case_id",
        "query",
        "expected_chunk_id",
        "expected_decision_label",
        "expected_recommended_route",
    )
    @classmethod
    def validate_non_empty_required_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required string fields cannot be blank")
        return value

    @field_validator("normalized_query")
    @classmethod
    def validate_optional_normalized_query(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("normalized_query cannot be blank when provided")
        return value


class LabeledRetrievalFixture(BaseModel):
    """Top-level labeled fixture contract for 03h."""

    schema_version: str
    cases: list[LabeledRetrievalCase]

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("schema_version cannot be blank")
        return value

    @model_validator(mode="after")
    def validate_unique_case_ids(self) -> "LabeledRetrievalFixture":
        seen: set[str] = set()
        duplicates: set[str] = set()
        for item in self.cases:
            if item.case_id in seen:
                duplicates.add(item.case_id)
            seen.add(item.case_id)

        if duplicates:
            duplicate_list = ", ".join(sorted(duplicates))
            raise ValueError(f"duplicate case_id values found: {duplicate_list}")
        return self


class UpstreamRetrievalQueryRecord(BaseModel):
    """Minimal 03f query record used for deterministic alignment."""

    query: str
    normalized_query: str | None = None
    results: list[dict[str, object]] = Field(default_factory=list)

    @field_validator("query")
    @classmethod
    def validate_query_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query cannot be blank")
        return value

    @field_validator("normalized_query")
    @classmethod
    def validate_optional_normalized_query_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("normalized_query cannot be blank when provided")
        return value


class UpstreamRetrievalOutput(BaseModel):
    """Minimal 03f output contract required by 03h alignment helper."""

    queries: list[UpstreamRetrievalQueryRecord]


class UpstreamDecisionRecord(BaseModel):
    """Minimal 03g decision record used for deterministic alignment."""

    query: str
    normalized_query: str | None = None
    decision_label: str
    recommended_route: str

    @field_validator("query", "decision_label", "recommended_route")
    @classmethod
    def validate_required_non_blank_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required string fields cannot be blank")
        return value

    @field_validator("normalized_query")
    @classmethod
    def validate_optional_decision_normalized_query(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            raise ValueError("normalized_query cannot be blank when provided")
        return value


class UpstreamDecisionOutput(BaseModel):
    """Minimal 03g output contract required by 03h alignment helper."""

    query_decisions: list[UpstreamDecisionRecord]


AlignmentStatus = Literal["matched", "missing_03f", "missing_03g", "missing_both"]
CaseStatus = Literal["pass", "fail", "warning"]
FailureCategory = Literal[
    "EXPECTED_CHUNK_NOT_FOUND",
    "EXPECTED_CHUNK_RANK_TOO_LOW",
    "DECISION_LABEL_MISMATCH",
    "RECOMMENDED_ROUTE_MISMATCH",
    "MISSING_CASE_IN_03F_OUTPUT",
    "MISSING_CASE_IN_03G_OUTPUT",
    "MALFORMED_FIXTURE_CASE",
]


class AlignedCaseResult(BaseModel):
    """Single aligned case row bridging fixture, 03f, and 03g records."""

    case_id: str
    fixture_case: LabeledRetrievalCase
    retrieval_record: UpstreamRetrievalQueryRecord | None
    decision_record: UpstreamDecisionRecord | None
    matched_03f: bool
    matched_03g: bool
    alignment_status: AlignmentStatus


class EvaluatedCaseResult(BaseModel):
    """Per-case evaluation output produced from aligned records."""

    case_id: str
    fixture_case: LabeledRetrievalCase
    retrieval_record: UpstreamRetrievalQueryRecord | None
    decision_record: UpstreamDecisionRecord | None
    expected_chunk_found: bool
    expected_chunk_rank: int | None = None
    hit_at_1: bool
    hit_at_3: bool
    hit_at_5: bool
    decision_label_match: bool
    recommended_route_match: bool
    status: CaseStatus
    failure_category: FailureCategory | None = None
    failure_reason: str | None = None


class EvaluationSummary(BaseModel):
    """In-memory aggregate summary for a batch of evaluated cases."""

    total_cases: int = Field(ge=0)
    passed_cases: int = Field(ge=0)
    failed_cases: int = Field(ge=0)
    warning_cases: int = Field(ge=0)
    pass_rate: float = Field(ge=0.0, le=1.0)
    expected_chunk_found_rate: float = Field(ge=0.0, le=1.0)
    hit_at_1_rate: float = Field(ge=0.0, le=1.0)
    hit_at_3_rate: float = Field(ge=0.0, le=1.0)
    hit_at_5_rate: float = Field(ge=0.0, le=1.0)
    decision_label_match_rate: float = Field(ge=0.0, le=1.0)
    recommended_route_match_rate: float = Field(ge=0.0, le=1.0)
    failure_counts: dict[str, int] = Field(default_factory=dict)


class EvaluationRunResult(BaseModel):
    """In-memory result for one orchestration run."""

    schema_version: str
    fixture_path: str
    retrieval_output_path: str
    decision_output_path: str
    cases: list[EvaluatedCaseResult]
    summary: EvaluationSummary
