from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_runner_smoke_executes_and_writes_outputs() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    runner_path = repo_root / "pocs" / "03h_retrieval_evaluation" / "src" / "run_retrieval_evaluation.py"

    completed = subprocess.run(
        [sys.executable, str(runner_path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "03h retrieval evaluation completed." in completed.stdout
    assert "Total cases:" in completed.stdout
    assert "Pass rate:" in completed.stdout

    report_path = repo_root / "pocs" / "03h_retrieval_evaluation" / "outputs" / "evaluation_report.json"
    summary_path = repo_root / "pocs" / "03h_retrieval_evaluation" / "outputs" / "evaluation_summary.md"

    assert report_path.exists()
    assert summary_path.exists()
