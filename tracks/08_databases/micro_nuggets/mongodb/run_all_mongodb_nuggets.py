from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class NuggetResult:
    script: Path
    ok: bool
    return_code: int
    latency_s: float
    output_tail: str


def safe_print(text: str) -> None:
    # Windows consoles may use cp1252 and fail on characters like ✓/✗.
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def discover_nuggets(root: Path) -> list[Path]:
    scripts = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root)
        if "__pycache__" in rel.parts:
            continue
        if rel.name in {"_mg_connect.py", "run_all_mongodb_nuggets.py"}:
            continue
        scripts.append(path)
    return sorted(scripts, key=lambda p: str(p.relative_to(root)).lower())


def run_one(script: Path, root: Path, timeout_s: int) -> NuggetResult:
    started = time.perf_counter()
    command = [sys.executable, str(script)]
    try:
        completed = subprocess.run(
            command,
            cwd=str(root),
            capture_output=True,
            text=False,
            timeout=timeout_s,
        )
        stdout_text = (completed.stdout or b"").decode("utf-8", errors="replace")
        stderr_text = (completed.stderr or b"").decode("utf-8", errors="replace")
        output = stdout_text + ("\n" + stderr_text if stderr_text else "")
        tail = "\n".join(output.strip().splitlines()[-8:]).strip()
        return NuggetResult(
            script=script,
            ok=completed.returncode == 0,
            return_code=completed.returncode,
            latency_s=time.perf_counter() - started,
            output_tail=tail,
        )
    except subprocess.TimeoutExpired as exc:
        stdout_text = (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr_text = (exc.stderr or b"").decode("utf-8", errors="replace")
        partial = (stdout_text + ("\n" + stderr_text if stderr_text else "")).strip()
        tail = "\n".join(partial.splitlines()[-8:]).strip()
        return NuggetResult(
            script=script,
            ok=False,
            return_code=124,
            latency_s=time.perf_counter() - started,
            output_tail=tail if tail else f"Timed out after {timeout_s}s",
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run all MongoDB micro-nugget scripts with one-line status output."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-script timeout in seconds (default: 120).",
    )
    parser.add_argument(
        "--stop-on-fail",
        action="store_true",
        help="Stop immediately on the first failing script.",
    )
    parser.add_argument(
        "--show-pass-output",
        action="store_true",
        help="Also print tail output for passing scripts.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    scripts = discover_nuggets(root)
    if not scripts:
        safe_print("No nugget scripts found.")
        return 1

    safe_print(f"MongoDB nuggets discovered: {len(scripts)}")
    safe_print("-" * 80)

    results: list[NuggetResult] = []
    for script in scripts:
        rel = script.relative_to(root)
        result = run_one(script, root, timeout_s=args.timeout)
        results.append(result)
        status = "PASS" if result.ok else "FAIL"
        safe_print(f"{status:4} | {rel.as_posix():62} | {result.latency_s:6.2f}s")
        if result.ok and args.show_pass_output and result.output_tail:
            safe_print(result.output_tail)
            safe_print("-" * 80)
        if not result.ok:
            if result.output_tail:
                safe_print(result.output_tail)
            safe_print("-" * 80)
            if args.stop_on_fail:
                break

    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed
    total_s = sum(r.latency_s for r in results)
    safe_print(
        f"SUMMARY | total={len(results)} passed={passed} failed={failed} duration={total_s:.2f}s"
    )

    if failed:
        safe_print("FAILED SCRIPTS:")
        for r in results:
            if not r.ok:
                rel = r.script.relative_to(root).as_posix()
                safe_print(f"- {rel} (rc={r.return_code}, {r.latency_s:.2f}s)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
