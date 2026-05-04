"""In-memory aggregate summary calculation for 03h evaluated cases."""

from __future__ import annotations

from schemas import EvaluatedCaseResult, EvaluationSummary


def _safe_rate(*, numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def summarize_evaluated_cases(cases: list[EvaluatedCaseResult]) -> EvaluationSummary:
    """Calculate aggregate summary metrics from per-case evaluation results."""

    total_cases = len(cases)
    passed_cases = sum(1 for item in cases if item.status == "pass")
    failed_cases = sum(1 for item in cases if item.status == "fail")
    warning_cases = sum(1 for item in cases if item.status == "warning")

    expected_chunk_found_count = sum(1 for item in cases if item.expected_chunk_found)
    hit_at_1_count = sum(1 for item in cases if item.hit_at_1)
    hit_at_3_count = sum(1 for item in cases if item.hit_at_3)
    hit_at_5_count = sum(1 for item in cases if item.hit_at_5)
    decision_label_match_count = sum(1 for item in cases if item.decision_label_match)
    recommended_route_match_count = sum(1 for item in cases if item.recommended_route_match)

    failure_counts: dict[str, int] = {}
    for item in cases:
        if item.status != "fail":
            continue
        if item.failure_category is None:
            continue
        failure_counts[item.failure_category] = failure_counts.get(item.failure_category, 0) + 1

    return EvaluationSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        warning_cases=warning_cases,
        pass_rate=_safe_rate(numerator=passed_cases, denominator=total_cases),
        expected_chunk_found_rate=_safe_rate(numerator=expected_chunk_found_count, denominator=total_cases),
        hit_at_1_rate=_safe_rate(numerator=hit_at_1_count, denominator=total_cases),
        hit_at_3_rate=_safe_rate(numerator=hit_at_3_count, denominator=total_cases),
        hit_at_5_rate=_safe_rate(numerator=hit_at_5_count, denominator=total_cases),
        decision_label_match_rate=_safe_rate(numerator=decision_label_match_count, denominator=total_cases),
        recommended_route_match_rate=_safe_rate(numerator=recommended_route_match_count, denominator=total_cases),
        failure_counts=failure_counts,
    )
