"""Pydantic schemas for 03g retrieval decision contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

DecisionLabel = Literal["strong_match", "ambiguous_match", "weak_match", "no_match", "needs_clarification"]
RecommendedRoute = Literal["answer_candidate_path", "clarification_path", "fallback_path", "no_answer_path"]
ConfidenceBand = Literal["high", "medium", "low", "none"]


class RetrievalCandidate(BaseModel):
    """Input candidate row from 03f hybrid retrieval output."""

    rank: int = Field(ge=1)
    chunk_id: str
    hybrid_score: float = Field(ge=0.0)
    word_score: float = Field(ge=0.0)
    char_score: float = Field(ge=0.0)
    source_file: str
    title: str
    section: str | None = None
    text: str
    normalized_text: str

    @field_validator("chunk_id", "source_file", "title", "text", "normalized_text")
    @classmethod
    def validate_non_empty_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("string fields cannot be empty")
        return value


class HybridQueryInput(BaseModel):
    """Input query payload from 03f artifact."""

    query: str
    normalized_query: str
    results: list[RetrievalCandidate]

    @field_validator("query", "normalized_query")
    @classmethod
    def validate_non_empty_query_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query fields cannot be empty")
        return value


class HybridRetrievalBatchInput(BaseModel):
    """03f batch artifact shape consumed by 03g."""

    poc: str
    description: str | None = None
    config: dict[str, object] | None = None
    queries: list[HybridQueryInput]


class RetrievalDecisionConfig(BaseModel):
    """Configurable deterministic thresholds for retrieval decisions.

    All default numeric values are initial placeholders and should be tuned
    later with retrieval-evaluation fixtures.
    """

    strong_match_min_score: float = Field(default=0.15, ge=0.0, le=1.0)
    weak_match_min_score: float = Field(default=0.05, ge=0.0, le=1.0)
    no_match_max_score: float = Field(default=0.01, ge=0.0, le=1.0)
    min_score_gap_for_strong: float = Field(default=0.03, ge=0.0, le=1.0)
    close_score_delta: float = Field(default=0.015, ge=0.0, le=1.0)
    max_close_candidates_before_ambiguous: int = Field(default=2, ge=1)
    top_k_window: int = Field(default=5, ge=1)
    source_diversity_ambiguity_threshold: int = Field(default=3, ge=1)
    enable_needs_clarification: bool = True
    min_query_tokens_for_specificity: int = Field(default=3, ge=1)
    clarification_min_service_areas: int = Field(default=2, ge=1)


class DecisionSignals(BaseModel):
    """Debug/evidence signals used to support deterministic decisions."""

    top_score: float = Field(ge=0.0)
    second_score: float = Field(ge=0.0)
    score_gap: float = Field(ge=0.0)
    close_candidate_count: int = Field(ge=0)
    top_k_considered: int = Field(ge=0)
    distinct_source_count: int = Field(ge=0)
    distinct_service_area_count: int = Field(ge=0)
    query_token_count: int = Field(ge=0)
    query_has_service_keyword: bool
    query_is_underspecified: bool
    ambiguity_triggered: bool
    clarification_triggered: bool


class RetrievalDecisionResult(BaseModel):
    """Deterministic decision result for one query."""

    query: str
    normalized_query: str
    decision_label: DecisionLabel
    recommended_route: RecommendedRoute
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_band: ConfidenceBand
    selected_candidate_ids: list[str]
    reason_codes: list[str]
    precedence_rule_applied: str
    decision_signals: DecisionSignals
    deterministic: bool = True

    @field_validator("reason_codes")
    @classmethod
    def validate_reason_codes_not_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("reason_codes cannot be empty")
        return value


class RetrievalDecisionBatch(BaseModel):
    """Top-level 03g output artifact."""

    poc: Literal["03g_retrieval_decision"] = "03g_retrieval_decision"
    input_source: str
    decision_config: RetrievalDecisionConfig
    query_decisions: list[RetrievalDecisionResult]
