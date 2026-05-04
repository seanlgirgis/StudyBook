from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_runner_writes_output_file():
    poc_root = Path(__file__).resolve().parents[1]
    runner = poc_root / "src" / "run_pipeline_tests.py"

    result = subprocess.run([sys.executable, str(runner)], cwd=str(poc_root), check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

    output_file = poc_root / "outputs" / "sample_pipeline_runs.json"
    assert output_file.exists()

    payload = json.loads(output_file.read_text(encoding="utf-8"))
    assert payload["failed"] == 0
    assert payload["total"] >= 4
