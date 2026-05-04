from __future__ import annotations

import json
from pathlib import Path

from .mock_evidence_sets import build_mock_scenarios
from .pipeline_test_harness import run_pipeline_harness


def main() -> int:
    scenarios = build_mock_scenarios()
    summary = run_pipeline_harness(scenarios)

    output_path = Path(__file__).resolve().parents[1] / "outputs" / "sample_pipeline_runs.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")

    print(f"POC 04d pipeline run completed: {summary.passed}/{summary.total} scenario checks passed.")
    print(f"Wrote: {output_path}")
    return 0 if summary.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
