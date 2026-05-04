from __future__ import annotations

import json
import sys
from pathlib import Path

POC_ROOT = Path(__file__).resolve().parents[1]
if str(POC_ROOT) not in sys.path:
    sys.path.insert(0, str(POC_ROOT))

from src.mock_evidence_sets import build_mock_scenarios
from src.pipeline_test_harness import run_pipeline_harness


def main() -> int:
    summary = run_pipeline_harness(build_mock_scenarios())
    out = POC_ROOT / "outputs" / "sample_pipeline_runs.json"
    out.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")
    print(f"Wrote: {out}")
    return 0 if summary.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
