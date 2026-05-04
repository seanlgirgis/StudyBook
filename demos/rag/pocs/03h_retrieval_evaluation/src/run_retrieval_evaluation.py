"""Minimal runnable script for 03h retrieval evaluation (baby step 7)."""

from __future__ import annotations

from pathlib import Path

from run_evaluation import run_retrieval_evaluation
from write_outputs import write_evaluation_outputs


def main() -> None:
    src_dir = Path(__file__).resolve().parent
    poc_dir = src_dir.parent
    repo_root = poc_dir.parent.parent

    fixture_path = poc_dir / "fixtures" / "labeled_retrieval_cases.json"
    retrieval_output_path = repo_root / "pocs" / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
    decision_output_path = repo_root / "pocs" / "03g_retrieval_decision" / "outputs" / "sample_retrieval_decisions.json"
    output_dir = poc_dir / "outputs"

    result = run_retrieval_evaluation(
        fixture_path=fixture_path,
        retrieval_output_path=retrieval_output_path,
        decision_output_path=decision_output_path,
    )
    written = write_evaluation_outputs(result, output_dir)

    print("03h retrieval evaluation completed.")
    print(f"Total cases: {result.summary.total_cases}")
    print(
        f"Passed: {result.summary.passed_cases} | "
        f"Failed: {result.summary.failed_cases} | "
        f"Warning: {result.summary.warning_cases}"
    )
    print(f"Pass rate: {result.summary.pass_rate:.6f}")
    print(f"Report JSON: {written['evaluation_report']}")
    print(f"Summary MD: {written['evaluation_summary']}")


if __name__ == "__main__":
    main()
