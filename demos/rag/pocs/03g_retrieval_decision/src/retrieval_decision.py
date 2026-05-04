"""Deterministic retrieval-decision engine for 03g."""

from __future__ import annotations

import json
import re
from pathlib import Path

from schemas import (
    DecisionLabel,
    DecisionSignals,
    HybridQueryInput,
    HybridRetrievalBatchInput,
    RetrievalCandidate,
    RetrievalDecisionBatch,
    RetrievalDecisionConfig,
    RetrievalDecisionResult,
)

TOKEN_RE = re.compile(r"[a-z0-9]+")

SERVICE_KEYWORDS = {
    "ac",
    "air",
    "cooling",
    "heater",
    "heating",
    "furnace",
    "hvac",
    "plumbing",
    "plumber",
    "drain",
    "water",
    "tankless",
    "appliance",
    "refrigerator",
    "fridge",
    "washer",
    "dryer",
    "dishwasher",
}


def load_hybrid_results(input_path: Path) -> HybridRetrievalBatchInput:
    """Read and validate 03f output artifact."""

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    return HybridRetrievalBatchInput.model_validate(payload)


def load_decision_config(config_path: Path | None = None) -> RetrievalDecisionConfig:
    """Load configurable deterministic thresholds."""

    if config_path is None:
        return RetrievalDecisionConfig()
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return RetrievalDecisionConfig.model_validate(payload)


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _guess_service_area(candidate: RetrievalCandidate) -> str:
    key_text = f"{candidate.source_file} {candidate.normalized_text}".lower()
    if "water heater" in key_text or "tankless" in key_text:
        return "water_heater"
    if "plumb" in key_text or "drain" in key_text:
        return "plumbing"
    if any(token in key_text for token in ["ac ", "hvac", "furnace", "heating", "cooling", "thermostat"]):
        return "hvac"
    if any(token in key_text for token in ["refrigerator", "appliance", "dishwasher", "washer", "dryer"]):
        return "appliance"
    if any(token in key_text for token in ["finance", "billing", "payment", "coupon"]):
        return "billing_or_finance"
    if any(token in key_text for token in ["schedule", "dispatch", "service area", "zip code"]):
        return "scheduling_or_dispatch"
    return "general"


def _confidence_band(score: float, config: RetrievalDecisionConfig) -> str:
    if score <= config.no_match_max_score:
        return "none"
    if score < config.weak_match_min_score:
        return "low"
    if score < config.strong_match_min_score:
        return "medium"
    return "high"


def _top_candidates_by_window(candidates: list[RetrievalCandidate], top_k_window: int) -> list[RetrievalCandidate]:
    ranked = sorted(candidates, key=lambda item: (item.rank, -item.hybrid_score))
    return ranked[:top_k_window]


def _select_close_candidate_ids(
    candidates: list[RetrievalCandidate], top_score: float, delta: float, max_count: int
) -> list[str]:
    close = [item.chunk_id for item in candidates if (top_score - item.hybrid_score) <= delta]
    return close[:max_count]


def _build_decision_signals(
    query: str,
    candidates: list[RetrievalCandidate],
    config: RetrievalDecisionConfig,
    clarification_triggered: bool,
    ambiguity_triggered: bool,
) -> DecisionSignals:
    if not candidates:
        top_score = 0.0
        second_score = 0.0
        score_gap = 0.0
        close_candidate_count = 0
        distinct_source_count = 0
        distinct_service_area_count = 0
    else:
        top_score = float(candidates[0].hybrid_score)
        second_score = float(candidates[1].hybrid_score) if len(candidates) > 1 else 0.0
        score_gap = max(top_score - second_score, 0.0)
        close_candidate_count = sum(1 for item in candidates if (top_score - item.hybrid_score) <= config.close_score_delta)
        distinct_source_count = len({item.source_file for item in candidates})
        distinct_service_area_count = len({_guess_service_area(item) for item in candidates})

    query_tokens = _tokenize(query)
    query_has_service_keyword = any(token in SERVICE_KEYWORDS for token in query_tokens)
    query_is_underspecified = (
        len(query_tokens) < config.min_query_tokens_for_specificity or not query_has_service_keyword
    )

    return DecisionSignals(
        top_score=top_score,
        second_score=second_score,
        score_gap=score_gap,
        close_candidate_count=close_candidate_count,
        top_k_considered=len(candidates),
        distinct_source_count=distinct_source_count,
        distinct_service_area_count=distinct_service_area_count,
        query_token_count=len(query_tokens),
        query_has_service_keyword=query_has_service_keyword,
        query_is_underspecified=query_is_underspecified,
        ambiguity_triggered=ambiguity_triggered,
        clarification_triggered=clarification_triggered,
    )


def decide_for_query(query_row: HybridQueryInput, config: RetrievalDecisionConfig) -> RetrievalDecisionResult:
    """Apply deterministic precedence to one query result set."""

    candidates = _top_candidates_by_window(query_row.results, config.top_k_window)
    query_tokens = _tokenize(query_row.normalized_query)
    has_service_keyword = any(token in SERVICE_KEYWORDS for token in query_tokens)
    is_query_underspecified = (
        len(query_tokens) < config.min_query_tokens_for_specificity or not has_service_keyword
    )

    if not candidates:
        signals = _build_decision_signals(
            query=query_row.normalized_query,
            candidates=[],
            config=config,
            clarification_triggered=False,
            ambiguity_triggered=False,
        )
        return RetrievalDecisionResult(
            query=query_row.query,
            normalized_query=query_row.normalized_query,
            decision_label="no_match",
            recommended_route="no_answer_path",
            confidence_score=0.0,
            confidence_band="none",
            selected_candidate_ids=[],
            reason_codes=["NO_CANDIDATES", "TOP_SCORE_BELOW_NO_MATCH_THRESHOLD"],
            precedence_rule_applied="NO_MATCH_PRECEDENCE",
            decision_signals=signals,
        )

    top_score = float(candidates[0].hybrid_score)
    second_score = float(candidates[1].hybrid_score) if len(candidates) > 1 else 0.0
    score_gap = max(top_score - second_score, 0.0)
    close_candidate_count = sum(1 for item in candidates if (top_score - item.hybrid_score) <= config.close_score_delta)
    distinct_service_area_count = len({_guess_service_area(item) for item in candidates})
    distinct_source_count = len({item.source_file for item in candidates})

    ambiguity_triggered = (
        close_candidate_count > config.max_close_candidates_before_ambiguous
        or score_gap < config.min_score_gap_for_strong
        or distinct_source_count >= config.source_diversity_ambiguity_threshold
    )
    low_nonzero_evidence = config.no_match_max_score < top_score < config.weak_match_min_score
    clarification_triggered = config.enable_needs_clarification and (
        (
            is_query_underspecified
            and distinct_service_area_count >= config.clarification_min_service_areas
            and close_candidate_count >= 2
        )
        or (is_query_underspecified and low_nonzero_evidence)
        or (ambiguity_triggered and is_query_underspecified and distinct_service_area_count >= 2)
    )

    # 1. no_match precedence
    if top_score <= config.no_match_max_score:
        signals = _build_decision_signals(
            query=query_row.normalized_query,
            candidates=candidates,
            config=config,
            clarification_triggered=clarification_triggered,
            ambiguity_triggered=ambiguity_triggered,
        )
        return RetrievalDecisionResult(
            query=query_row.query,
            normalized_query=query_row.normalized_query,
            decision_label="no_match",
            recommended_route="no_answer_path",
            confidence_score=top_score,
            confidence_band=_confidence_band(top_score, config),
            selected_candidate_ids=[],
            reason_codes=["TOP_SCORE_BELOW_NO_MATCH_THRESHOLD"],
            precedence_rule_applied="NO_MATCH_PRECEDENCE",
            decision_signals=signals,
        )

    # 2. strong_match precedence
    if (
        top_score >= config.strong_match_min_score
        and score_gap >= config.min_score_gap_for_strong
        and close_candidate_count <= config.max_close_candidates_before_ambiguous
    ):
        signals = _build_decision_signals(
            query=query_row.normalized_query,
            candidates=candidates,
            config=config,
            clarification_triggered=clarification_triggered,
            ambiguity_triggered=ambiguity_triggered,
        )
        return RetrievalDecisionResult(
            query=query_row.query,
            normalized_query=query_row.normalized_query,
            decision_label="strong_match",
            recommended_route="answer_candidate_path",
            confidence_score=top_score,
            confidence_band=_confidence_band(top_score, config),
            selected_candidate_ids=[candidates[0].chunk_id],
            reason_codes=["TOP_SCORE_STRONG", "CLEAR_SCORE_GAP", "LOW_CLOSE_CANDIDATE_COUNT"],
            precedence_rule_applied="STRONG_MATCH_PRECEDENCE",
            decision_signals=signals,
        )

    # 3. needs_clarification precedence
    if clarification_triggered:
        reason_codes = ["CLARIFICATION_POLICY_TRIGGERED"]
        if is_query_underspecified and distinct_service_area_count >= config.clarification_min_service_areas:
            reason_codes.append("QUERY_UNDERSPECIFIED_MULTI_SERVICE")
        if ambiguity_triggered:
            reason_codes.append("AMBIGUITY_REQUIRES_CLARIFICATION")
        if low_nonzero_evidence:
            reason_codes.append("LOW_CONFIDENCE_REQUIRES_CLARIFICATION")

        signals = _build_decision_signals(
            query=query_row.normalized_query,
            candidates=candidates,
            config=config,
            clarification_triggered=clarification_triggered,
            ambiguity_triggered=ambiguity_triggered,
        )
        return RetrievalDecisionResult(
            query=query_row.query,
            normalized_query=query_row.normalized_query,
            decision_label="needs_clarification",
            recommended_route="clarification_path",
            confidence_score=top_score,
            confidence_band=_confidence_band(top_score, config),
            selected_candidate_ids=_select_close_candidate_ids(
                candidates, top_score, config.close_score_delta, config.top_k_window
            ),
            reason_codes=reason_codes,
            precedence_rule_applied="CLARIFICATION_BEATS_AMBIGUOUS_OR_WEAK",
            decision_signals=signals,
        )

    # 4. ambiguous_match precedence
    if ambiguity_triggered:
        reason_codes: list[str] = []
        if score_gap < config.min_score_gap_for_strong:
            reason_codes.append("SMALL_TOP_GAP")
        if close_candidate_count > config.max_close_candidates_before_ambiguous:
            reason_codes.append("MULTIPLE_CLOSE_CANDIDATES")
        if distinct_source_count >= config.source_diversity_ambiguity_threshold:
            reason_codes.append("HIGH_SOURCE_DIVERSITY_IN_TOP_K")
        if not reason_codes:
            reason_codes.append("TOP_SCORE_MID")

        signals = _build_decision_signals(
            query=query_row.normalized_query,
            candidates=candidates,
            config=config,
            clarification_triggered=clarification_triggered,
            ambiguity_triggered=ambiguity_triggered,
        )
        return RetrievalDecisionResult(
            query=query_row.query,
            normalized_query=query_row.normalized_query,
            decision_label="ambiguous_match",
            recommended_route="clarification_path",
            confidence_score=top_score,
            confidence_band=_confidence_band(top_score, config),
            selected_candidate_ids=_select_close_candidate_ids(
                candidates, top_score, config.close_score_delta, config.top_k_window
            ),
            reason_codes=reason_codes,
            precedence_rule_applied="AMBIGUOUS_MATCH_PRECEDENCE",
            decision_signals=signals,
        )

    # 5. weak_match precedence (default branch)
    reason_codes = ["TOP_SCORE_LOW_NONZERO", "BELOW_WEAK_CONFIDENCE_TARGET"]
    signals = _build_decision_signals(
        query=query_row.normalized_query,
        candidates=candidates,
        config=config,
        clarification_triggered=clarification_triggered,
        ambiguity_triggered=ambiguity_triggered,
    )
    return RetrievalDecisionResult(
        query=query_row.query,
        normalized_query=query_row.normalized_query,
        decision_label="weak_match",
        recommended_route="fallback_path",
        confidence_score=top_score,
        confidence_band=_confidence_band(top_score, config),
        selected_candidate_ids=[candidates[0].chunk_id],
        reason_codes=reason_codes,
        precedence_rule_applied="WEAK_MATCH_PRECEDENCE",
        decision_signals=signals,
    )


def run_decision_batch(
    hybrid_batch: HybridRetrievalBatchInput,
    input_source: str,
    config: RetrievalDecisionConfig | None = None,
) -> RetrievalDecisionBatch:
    """Run deterministic decisioning for all query rows in one artifact."""

    effective_config = config or RetrievalDecisionConfig()
    decisions = [decide_for_query(item, effective_config) for item in hybrid_batch.queries]
    return RetrievalDecisionBatch(
        input_source=input_source,
        decision_config=effective_config,
        query_decisions=decisions,
    )
