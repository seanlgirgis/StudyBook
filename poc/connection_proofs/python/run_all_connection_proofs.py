from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ProofResult:
    resource: str
    script: str
    ok: bool
    latency_ms: int
    reason: str
    return_code: int


def discover_scripts(root: Path) -> list[Path]:
    scripts = []
    for path in sorted(root.glob("*_proof.py")):
        if path.name.startswith("run_all_"):
            continue
        scripts.append(path)
    return scripts


def parse_json_output(stdout: str) -> dict[str, Any] | None:
    text = stdout.strip()
    if not text:
        return None

    # Most proof scripts print pure JSON; this fallback extracts the outer JSON object.
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0 or end <= start:
        return None

    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def pick_reason(payload: dict[str, Any] | None, return_code: int, stderr: str, stdout: str) -> str:
    if payload is None:
        if stderr.strip():
            return stderr.strip().splitlines()[-1]
        if stdout.strip():
            return stdout.strip().splitlines()[-1]
        return f"No JSON output (rc={return_code})"

    if payload.get("ok"):
        return "ok"

    if isinstance(payload.get("checks"), list):
        failed = [c for c in payload["checks"] if not c.get("ok")]
        if failed:
            first = failed[0]
            detail = str(first.get("detail") or "failed")
            return f"{first.get('name', 'check')} -> {detail}"

    for key in ("error", "hint", "detail", "message"):
        val = payload.get(key)
        if val:
            return str(val)

    if stderr.strip():
        return stderr.strip().splitlines()[-1]

    return f"failed (rc={return_code})"


def run_script(script: Path, timeout_sec: int) -> ProofResult:
    start = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=max(timeout_sec, 1),
        check=False,
    )
    latency_ms = int((time.perf_counter() - start) * 1000)
    payload = parse_json_output(completed.stdout)

    if payload is not None and payload.get("service"):
        resource = str(payload.get("service") or script.stem)
    elif payload is not None and payload.get("proof"):
        resource = str(payload.get("proof") or script.stem)
    else:
        resource = script.stem.replace("_proof", "")

    ok = bool(payload.get("ok")) if payload is not None else completed.returncode == 0
    reason = pick_reason(payload, completed.returncode, completed.stderr, completed.stdout)

    return ProofResult(
        resource=resource,
        script=script.name,
        ok=ok,
        latency_ms=latency_ms,
        reason=reason,
        return_code=int(completed.returncode),
    )


def print_report(results: list[ProofResult]) -> None:
    status_width = 6
    resource_width = max(8, max(len(r.resource) for r in results)) if results else 8
    print(f"{'STATUS':<{status_width}} {'RESOURCE':<{resource_width}} {'LATENCY_MS':>10}  REASON")
    print(f"{'-' * status_width} {'-' * resource_width} {'-' * 10}  {'-' * 40}")
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        print(f"{status:<{status_width}} {r.resource:<{resource_width}} {r.latency_ms:>10}  {r.reason}")

    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed
    print()
    print(f"Summary: total={len(results)} pass={passed} fail={failed}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all connection proof scripts and print one-line status per resource.")
    parser.add_argument("--timeout-sec", type=int, default=90, help="Per-script timeout in seconds.")
    parser.add_argument("--json-out", default="", help="Optional output file for full structured results.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    scripts = discover_scripts(root)

    if not scripts:
        print("No proof scripts found.")
        return 2

    results: list[ProofResult] = []
    for script in scripts:
        try:
            results.append(run_script(script, args.timeout_sec))
        except subprocess.TimeoutExpired:
            results.append(
                ProofResult(
                    resource=script.stem.replace("_proof", ""),
                    script=script.name,
                    ok=False,
                    latency_ms=args.timeout_sec * 1000,
                    reason=f"timeout after {args.timeout_sec}s",
                    return_code=124,
                )
            )

    print_report(results)

    if args.json_out:
        out_path = Path(args.json_out)
        payload = {
            "ok": all(r.ok for r in results),
            "generated_at_epoch": int(time.time()),
            "results": [
                {
                    "resource": r.resource,
                    "script": r.script,
                    "ok": r.ok,
                    "latency_ms": r.latency_ms,
                    "reason": r.reason,
                    "return_code": r.return_code,
                }
                for r in results
            ],
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

