from __future__ import annotations

import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = POC_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evaluate_cases import evaluate_aligned_case  # noqa: E402
from schemas import (  # noqa: E402
    AlignedCaseResult,
    LabeledRetrievalCase,
    UpstreamDecisionRecord,
    UpstreamRetrievalQueryRecord,
)


def _fixture_case(
    *,
    expected_chunk_id: str = "target_chunk",
    expected_label: str = "strong_match",
    expected_route: str = "answer_candidate_path",
) -> LabeledRetrievalCase:
    return LabeledRetrievalCase(
        case_id="case_001",
        query="sample query",
        normalized_query="sample query",
        expected_chunk_id=expected_chunk_id,
        expected_decision_label=expected_label,
        expected_recommended_route=expected_route,
    )


def _retrieval_record(ranks: list[tuple[int, str]]) -> UpstreamRetrievalQueryRecord:
    return UpstreamRetrievalQueryRecord(
        query="sample query",
        normalized_query="sample query",
        results=[{"rank": rank, "chunk_id": chunk_id} for rank, chunk_id in ranks],
    )


def _decision_record(
    *,
    label: str = "strong_match",
    route: str = "answer_candidate_path",
) -> UpstreamDecisionRecord:
    return UpstreamDecisionRecord(
        query="sample query",
        normalized_query="sample query",
        decision_label=label,
        recommended_route=route,
    )


def _aligned(
    *,
    fixture_case: LabeledRetrievalCase,
    retrieval_record: UpstreamRetrievalQueryRecord | None,
    decision_record: UpstreamDecisionRecord | None,
    matched_03f: bool = True,
    matched_03g: bool = True,
    alignment_status: str = "matched",
) -> AlignedCaseResult:
    return AlignedCaseResult(
        case_id=fixture_case.case_id,
        fixture_case=fixture_case,
        retrieval_record=retrieval_record,
        decision_record=decision_record,
        matched_03f=matched_03f,
        matched_03g=matched_03g,
        alignment_status=alignment_status,  # type: ignore[arg-type]
    )


def test_perfect_pass_rank_1_and_decision_route_match() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record([(1, "target_chunk"), (2, "other_chunk")]),
            decision_record=_decision_record(),
        )
    )
    assert evaluated.status == "pass"
    assert evaluated.expected_chunk_rank == 1
    assert evaluated.hit_at_1 is True
    assert evaluated.hit_at_3 is True
    assert evaluated.hit_at_5 is True
    assert evaluated.decision_label_match is True
    assert evaluated.recommended_route_match is True
    assert evaluated.failure_category is None
    assert evaluated.failure_reason is None


def test_expected_chunk_rank_3_sets_hit_at_3_and_hit_at_5_true() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record([(1, "x"), (2, "y"), (3, "target_chunk")]),
            decision_record=_decision_record(),
        )
    )
    assert evaluated.expected_chunk_rank == 3
    assert evaluated.hit_at_1 is False
    assert evaluated.hit_at_3 is True
    assert evaluated.hit_at_5 is True
    assert evaluated.status == "pass"


def test_expected_chunk_rank_5_sets_hit_at_5_true() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record([(1, "x"), (2, "y"), (3, "z"), (4, "q"), (5, "target_chunk")]),
            decision_record=_decision_record(),
        )
    )
    assert evaluated.expected_chunk_rank == 5
    assert evaluated.hit_at_1 is False
    assert evaluated.hit_at_3 is False
    assert evaluated.hit_at_5 is True
    assert evaluated.status == "pass"


def test_expected_chunk_missing_fails_expected_chunk_not_found() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record([(1, "x"), (2, "y")]),
            decision_record=_decision_record(),
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.expected_chunk_found is False
    assert evaluated.expected_chunk_rank is None
    assert evaluated.failure_category == "EXPECTED_CHUNK_NOT_FOUND"


def test_expected_chunk_below_top_5_fails_expected_chunk_rank_too_low() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record(
                [(1, "x"), (2, "y"), (3, "z"), (4, "q"), (5, "w"), (6, "target_chunk")]
            ),
            decision_record=_decision_record(),
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.expected_chunk_found is True
    assert evaluated.expected_chunk_rank == 6
    assert evaluated.hit_at_5 is False
    assert evaluated.failure_category == "EXPECTED_CHUNK_RANK_TOO_LOW"


def test_missing_03f_fails_missing_case_in_03f_output() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=None,
            decision_record=_decision_record(),
            matched_03f=False,
            matched_03g=True,
            alignment_status="missing_03f",
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.failure_category == "MISSING_CASE_IN_03F_OUTPUT"


def test_missing_03g_fails_missing_case_in_03g_output() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(),
            retrieval_record=_retrieval_record([(1, "target_chunk")]),
            decision_record=None,
            matched_03f=True,
            matched_03g=False,
            alignment_status="missing_03g",
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.failure_category == "MISSING_CASE_IN_03G_OUTPUT"


def test_decision_label_mismatch_fails_decision_label_mismatch() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(expected_label="strong_match"),
            retrieval_record=_retrieval_record([(1, "target_chunk")]),
            decision_record=_decision_record(label="ambiguous_match"),
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.failure_category == "DECISION_LABEL_MISMATCH"


def test_recommended_route_mismatch_fails_recommended_route_mismatch() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(expected_route="answer_candidate_path"),
            retrieval_record=_retrieval_record([(1, "target_chunk")]),
            decision_record=_decision_record(route="clarification_path"),
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.failure_category == "RECOMMENDED_ROUTE_MISMATCH"


def test_multiple_failures_choose_first_primary_failure_in_documented_order() -> None:
    evaluated = evaluate_aligned_case(
        _aligned(
            fixture_case=_fixture_case(expected_label="strong_match"),
            retrieval_record=_retrieval_record([(1, "x"), (2, "y"), (3, "z"), (4, "q"), (5, "w"), (6, "not_target")]),
            decision_record=_decision_record(label="ambiguous_match"),
        )
    )
    assert evaluated.status == "fail"
    assert evaluated.failure_category == "EXPECTED_CHUNK_NOT_FOUND"
