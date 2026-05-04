from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_runner_writes_output():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([sys.executable, str(root / "src" / "run_pipeline_tests.py")], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    payload = json.loads((root / "outputs" / "sample_pipeline_runs.json").read_text(encoding="utf-8"))
    assert payload["failed"] == 0
    assert payload["total"] >= 5
    assert all("execution_time_ms" in item for item in payload["results"])
