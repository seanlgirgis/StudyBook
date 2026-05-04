"""In-memory orchestration for 03h retrieval evaluation (baby step 5)."""

from __future__ import annotations

from pathlib import Path

from align_cases import align_fixture_cases_to_upstream
from evaluate_cases import evaluate_aligned_cases
from load_fixtures import load_labeled_retrieval_fixture
from load_upstream_outputs import load_03f_retrieval_output, load_03g_decision_output
from schemas import EvaluationRunResult
from summarize_evaluation import summarize_evaluated_cases


def run_retrieval_evaluation(
    fixture_path: Path,
    retrieval_output_path: Path,
    decision_output_path: Path,
) -> EvaluationRunResult:
    """Run full in-memory 03h flow without writing artifacts."""

    fixture = load_labeled_retrieval_fixture(fixture_path)
    retrieval_output = load_03f_retrieval_output(retrieval_output_path)
    decision_output = load_03g_decision_output(decision_output_path)
    aligned = align_fixture_cases_to_upstream(fixture, retrieval_output, decision_output)
    evaluated_cases = evaluate_aligned_cases(aligned)
    summary = summarize_evaluated_cases(evaluated_cases)

    return EvaluationRunResult(
        schema_version=fixture.schema_version,
        fixture_path=str(fixture_path),
        retrieval_output_path=str(retrieval_output_path),
        decision_output_path=str(decision_output_path),
        cases=evaluated_cases,
        summary=summary,
    )
