"""Per-case evaluation logic for 03h retrieval evaluation (baby step 3)."""

from __future__ import annotations

from schemas import AlignedCaseResult, EvaluatedCaseResult, FailureCategory


def _find_expected_chunk_rank(
    *,
    expected_chunk_id: str,
    retrieval_results: list[dict[str, object]],
) -> int | None:
    for item in retrieval_results:
        chunk_id = item.get("chunk_id")
        if chunk_id == expected_chunk_id:
            rank_value = item.get("rank")
            if isinstance(rank_value, int):
                return rank_value
            return None
    return None


def _failure_from_ordered_checks(
    *,
    aligned_case: AlignedCaseResult,
    expected_chunk_found: bool,
    expected_chunk_rank: int | None,
    hit_at_5: bool,
    decision_label_match: bool,
    recommended_route_match: bool,
) -> tuple[FailureCategory | None, str | None]:
    if not aligned_case.matched_03f:
        return ("MISSING_CASE_IN_03F_OUTPUT", "No matching 03f retrieval record for fixture case.")

    if not aligned_case.matched_03g:
        return ("MISSING_CASE_IN_03G_OUTPUT", "No matching 03g decision record for fixture case.")

    if not expected_chunk_found:
        return ("EXPECTED_CHUNK_NOT_FOUND", "Expected chunk_id was not found in retrieval results.")

    if not hit_at_5:
        return ("EXPECTED_CHUNK_RANK_TOO_LOW", f"Expected chunk rank {expected_chunk_rank} is below top 5.")

    if not decision_label_match:
        return ("DECISION_LABEL_MISMATCH", "Actual decision_label does not match expected_decision_label.")

    if not recommended_route_match:
        return (
            "RECOMMENDED_ROUTE_MISMATCH",
            "Actual recommended_route does not match expected_recommended_route.",
        )

    return (None, None)


def evaluate_aligned_case(aligned_case: AlignedCaseResult) -> EvaluatedCaseResult:
    """Evaluate one aligned case with deterministic status and failure precedence."""

    retrieval_results: list[dict[str, object]] = []
    if aligned_case.retrieval_record is not None:
        retrieval_results = aligned_case.retrieval_record.results

    expected_rank = _find_expected_chunk_rank(
        expected_chunk_id=aligned_case.fixture_case.expected_chunk_id,
        retrieval_results=retrieval_results,
    )
    expected_chunk_found = expected_rank is not None
    hit_at_1 = expected_rank == 1
    hit_at_3 = expected_rank is not None and expected_rank <= 3
    hit_at_5 = expected_rank is not None and expected_rank <= 5

    decision_label_match = False
    recommended_route_match = False
    if aligned_case.decision_record is not None:
        decision_label_match = (
            aligned_case.decision_record.decision_label == aligned_case.fixture_case.expected_decision_label
        )
        recommended_route_match = (
            aligned_case.decision_record.recommended_route
            == aligned_case.fixture_case.expected_recommended_route
        )

    failure_category, failure_reason = _failure_from_ordered_checks(
        aligned_case=aligned_case,
        expected_chunk_found=expected_chunk_found,
        expected_chunk_rank=expected_rank,
        hit_at_5=hit_at_5,
        decision_label_match=decision_label_match,
        recommended_route_match=recommended_route_match,
    )

    # Warning conditions are intentionally deferred in current baby step.
    if failure_category is not None:
        status = "fail"
    else:
        status = "pass"

    return EvaluatedCaseResult(
        case_id=aligned_case.case_id,
        fixture_case=aligned_case.fixture_case,
        retrieval_record=aligned_case.retrieval_record,
        decision_record=aligned_case.decision_record,
        expected_chunk_found=expected_chunk_found,
        expected_chunk_rank=expected_rank,
        hit_at_1=hit_at_1,
        hit_at_3=hit_at_3,
        hit_at_5=hit_at_5,
        decision_label_match=decision_label_match,
        recommended_route_match=recommended_route_match,
        status=status,
        failure_category=failure_category,
        failure_reason=failure_reason,
    )


def evaluate_aligned_cases(aligned_cases: list[AlignedCaseResult]) -> list[EvaluatedCaseResult]:
    """Evaluate all aligned cases independently (no aggregate reporting yet)."""

    return [evaluate_aligned_case(item) for item in aligned_cases]
