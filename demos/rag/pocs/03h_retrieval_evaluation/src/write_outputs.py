"""Output writing layer for 03h evaluation artifacts (baby step 6)."""

from __future__ import annotations

import json
from pathlib import Path

from schemas import EvaluationRunResult


def write_evaluation_report(result: EvaluationRunResult, output_path: Path) -> Path:
    """Write full EvaluationRunResult to JSON report file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = result.model_dump(mode="json")
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def write_evaluation_summary_md(result: EvaluationRunResult, output_path: Path) -> Path:
    """Write compact markdown summary from EvaluationRunResult."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = result.summary

    lines: list[str] = [
        "# Retrieval Evaluation Summary",
        "",
        f"- Schema Version: `{result.schema_version}`",
        f"- Fixture Path: `{result.fixture_path}`",
        f"- Retrieval Output Path: `{result.retrieval_output_path}`",
        f"- Decision Output Path: `{result.decision_output_path}`",
        "",
        "## Aggregate",
        "",
        f"- Total Cases: {summary.total_cases}",
        f"- Passed: {summary.passed_cases}",
        f"- Failed: {summary.failed_cases}",
        f"- Warning: {summary.warning_cases}",
        f"- Pass Rate: {summary.pass_rate:.6f}",
        f"- Expected Chunk Found Rate: {summary.expected_chunk_found_rate:.6f}",
        f"- Hit@1 Rate: {summary.hit_at_1_rate:.6f}",
        f"- Hit@3 Rate: {summary.hit_at_3_rate:.6f}",
        f"- Hit@5 Rate: {summary.hit_at_5_rate:.6f}",
        f"- Decision Label Match Rate: {summary.decision_label_match_rate:.6f}",
        f"- Recommended Route Match Rate: {summary.recommended_route_match_rate:.6f}",
        "",
        "## Failure Counts",
        "",
    ]

    if not summary.failure_counts:
        lines.append("No failures")
    else:
        lines.extend(
            [
                "| failure_category | count |",
                "|---|---:|",
            ]
        )
        for key in sorted(summary.failure_counts.keys()):
            lines.append(f"| {key} | {summary.failure_counts[key]} |")

    lines.extend(
        [
            "",
            "## Cases",
            "",
            "| case_id | status | expected_chunk_rank | hit_at_1 | hit_at_3 | hit_at_5 | decision_label_match | recommended_route_match | failure_category |",
            "|---|---|---:|---|---|---|---|---|---|",
        ]
    )

    for case in result.cases:
        rank = "" if case.expected_chunk_rank is None else str(case.expected_chunk_rank)
        failure_category = "" if case.failure_category is None else case.failure_category
        lines.append(
            "| "
            + " | ".join(
                [
                    case.case_id,
                    case.status,
                    rank,
                    str(case.hit_at_1),
                    str(case.hit_at_3),
                    str(case.hit_at_5),
                    str(case.decision_label_match),
                    str(case.recommended_route_match),
                    failure_category,
                ]
            )
            + " |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def write_evaluation_outputs(result: EvaluationRunResult, output_dir: Path) -> dict[str, Path]:
    """Write both JSON and markdown output artifacts under output_dir."""

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = write_evaluation_report(result, output_dir / "evaluation_report.json")
    summary_md_path = write_evaluation_summary_md(result, output_dir / "evaluation_summary.md")
    return {"evaluation_report": report_path, "evaluation_summary": summary_md_path}
