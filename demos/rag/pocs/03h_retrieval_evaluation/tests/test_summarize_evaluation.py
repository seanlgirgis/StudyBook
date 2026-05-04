from __future__ import annotations

import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from schemas import EvaluatedCaseResult, LabeledRetrievalCase  # noqa: E402
from summarize_evaluation import summarize_evaluated_cases  # noqa: E402


def _fixture_case(case_id: str) -> LabeledRetrievalCase:
    return LabeledRetrievalCase(
        case_id=case_id,
        query=f"query {case_id}",
        normalized_query=f"query {case_id}",
        expected_chunk_id="chunk_001",
        expected_decision_label="strong_match",
        expected_recommended_route="answer_candidate_path",
    )


def _evaluated_case(
    *,
    case_id: str,
    status: str = "pass",
    expected_chunk_found: bool = True,
    expected_chunk_rank: int | None = 1,
    hit_at_1: bool = True,
    hit_at_3: bool = True,
    hit_at_5: bool = True,
    decision_label_match: bool = True,
    recommended_route_match: bool = True,
    failure_category: str | None = None,
    failure_reason: str | None = None,
) -> EvaluatedCaseResult:
    return EvaluatedCaseResult(
        case_id=case_id,
        fixture_case=_fixture_case(case_id),
        retrieval_record=None,
        decision_record=None,
        expected_chunk_found=expected_chunk_found,
        expected_chunk_rank=expected_chunk_rank,
        hit_at_1=hit_at_1,
        hit_at_3=hit_at_3,
        hit_at_5=hit_at_5,
        decision_label_match=decision_label_match,
        recommended_route_match=recommended_route_match,
        status=status,  # type: ignore[arg-type]
        failure_category=failure_category,  # type: ignore[arg-type]
        failure_reason=failure_reason,
    )


def test_empty_case_list_returns_zero_counts_and_zero_rates() -> None:
    summary = summarize_evaluated_cases([])
    assert summary.total_cases == 0
    assert summary.passed_cases == 0
    assert summary.failed_cases == 0
    assert summary.warning_cases == 0
    assert summary.pass_rate == 0.0
    assert summary.expected_chunk_found_rate == 0.0
    assert summary.hit_at_1_rate == 0.0
    assert summary.hit_at_3_rate == 0.0
    assert summary.hit_at_5_rate == 0.0
    assert summary.decision_label_match_rate == 0.0
    assert summary.recommended_route_match_rate == 0.0
    assert summary.failure_counts == {}


def test_all_pass_case_list_returns_100_percent_rates_and_empty_failure_counts() -> None:
    cases = [
        _evaluated_case(case_id="case_001"),
        _evaluated_case(case_id="case_002"),
        _evaluated_case(case_id="case_003"),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.total_cases == 3
    assert summary.passed_cases == 3
    assert summary.failed_cases == 0
    assert summary.warning_cases == 0
    assert summary.pass_rate == 1.0
    assert summary.expected_chunk_found_rate == 1.0
    assert summary.hit_at_1_rate == 1.0
    assert summary.hit_at_3_rate == 1.0
    assert summary.hit_at_5_rate == 1.0
    assert summary.decision_label_match_rate == 1.0
    assert summary.recommended_route_match_rate == 1.0
    assert summary.failure_counts == {}


def test_mixed_pass_fail_warning_counts_are_correct() -> None:
    cases = [
        _evaluated_case(case_id="case_001", status="pass"),
        _evaluated_case(
            case_id="case_002",
            status="fail",
            failure_category="EXPECTED_CHUNK_NOT_FOUND",
            failure_reason="missing expected chunk",
        ),
        _evaluated_case(case_id="case_003", status="warning"),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.total_cases == 3
    assert summary.passed_cases == 1
    assert summary.failed_cases == 1
    assert summary.warning_cases == 1
    assert summary.pass_rate == 1 / 3


def test_hit_at_1_hit_at_3_hit_at_5_rates_are_correct() -> None:
    cases = [
        _evaluated_case(case_id="case_001", hit_at_1=True, hit_at_3=True, hit_at_5=True),
        _evaluated_case(case_id="case_002", hit_at_1=False, hit_at_3=True, hit_at_5=True),
        _evaluated_case(case_id="case_003", hit_at_1=False, hit_at_3=False, hit_at_5=True),
        _evaluated_case(case_id="case_004", hit_at_1=False, hit_at_3=False, hit_at_5=False),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.hit_at_1_rate == 1 / 4
    assert summary.hit_at_3_rate == 2 / 4
    assert summary.hit_at_5_rate == 3 / 4


def test_expected_chunk_found_rate_is_correct() -> None:
    cases = [
        _evaluated_case(case_id="case_001", expected_chunk_found=True),
        _evaluated_case(case_id="case_002", expected_chunk_found=True),
        _evaluated_case(case_id="case_003", expected_chunk_found=False, expected_chunk_rank=None),
        _evaluated_case(case_id="case_004", expected_chunk_found=False, expected_chunk_rank=None),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.expected_chunk_found_rate == 2 / 4


def test_decision_label_match_rate_is_correct() -> None:
    cases = [
        _evaluated_case(case_id="case_001", decision_label_match=True),
        _evaluated_case(case_id="case_002", decision_label_match=False),
        _evaluated_case(case_id="case_003", decision_label_match=True),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.decision_label_match_rate == 2 / 3


def test_recommended_route_match_rate_is_correct() -> None:
    cases = [
        _evaluated_case(case_id="case_001", recommended_route_match=True),
        _evaluated_case(case_id="case_002", recommended_route_match=False),
        _evaluated_case(case_id="case_003", recommended_route_match=False),
        _evaluated_case(case_id="case_004", recommended_route_match=True),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.recommended_route_match_rate == 2 / 4


def test_failure_counts_group_by_failure_category() -> None:
    cases = [
        _evaluated_case(
            case_id="case_001",
            status="fail",
            failure_category="EXPECTED_CHUNK_NOT_FOUND",
            failure_reason="missing",
        ),
        _evaluated_case(
            case_id="case_002",
            status="fail",
            failure_category="EXPECTED_CHUNK_NOT_FOUND",
            failure_reason="missing",
        ),
        _evaluated_case(
            case_id="case_003",
            status="fail",
            failure_category="DECISION_LABEL_MISMATCH",
            failure_reason="label mismatch",
        ),
        _evaluated_case(case_id="case_004", status="pass"),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.failure_counts == {
        "EXPECTED_CHUNK_NOT_FOUND": 2,
        "DECISION_LABEL_MISMATCH": 1,
    }


def test_failed_case_with_null_failure_category_not_counted_in_failure_counts() -> None:
    cases = [
        _evaluated_case(
            case_id="case_001",
            status="fail",
            failure_category=None,
            failure_reason="failed but missing explicit category",
        ),
        _evaluated_case(
            case_id="case_002",
            status="fail",
            failure_category="MISSING_CASE_IN_03F_OUTPUT",
            failure_reason="missing 03f",
        ),
    ]
    summary = summarize_evaluated_cases(cases)
    assert summary.failed_cases == 2
    assert summary.failure_counts == {"MISSING_CASE_IN_03F_OUTPUT": 1}
