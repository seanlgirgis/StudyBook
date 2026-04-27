# ============================================================
# Topic   : Docker for Data Engineers
# File    : 01_dockerfile_basics.py
# Covers  : Dockerfile basics, layer caching, and image comparison
# Prereqs : Docker Desktop installed and running
# Run     : python 01_dockerfile_basics.py
# ============================================================

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

BUILD_OUTPUTS: dict[str, str] = {}


def _emit(message: str) -> None:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe = message.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(safe)


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _print_combined_output(result: subprocess.CompletedProcess[str]) -> str:
    combined = "\n".join(part for part in [result.stdout, result.stderr] if part)
    if combined:
        for line in combined.splitlines():
            _emit(line)
    return combined


def _size_to_bytes(size_token: str) -> int:
    match = re.match(r"^(?P<value>[0-9]*\.?[0-9]+)(?P<unit>B|kB|MB|GB)$", size_token.strip())
    if not match:
        return 0
    value = float(match.group("value"))
    unit = match.group("unit")
    return int(value * {"B": 1, "kB": 1000, "MB": 1000**2, "GB": 1000**3}[unit])


def build_image(tag: str, dockerfile: str, context: str = ".") -> bool:
    cmd = ["docker", "build", "-t", tag, "-f", dockerfile, context]
    print(f"\n[BUILD] {' '.join(cmd)}")
    result = _run(cmd)
    combined = _print_combined_output(result)
    BUILD_OUTPUTS[tag] = combined
    success = result.returncode == 0
    print(f"[BUILD RESULT] {tag}: {'SUCCESS' if success else 'FAILURE'}")
    return success


def compare_image_sizes(tags: list[str]) -> None:
    print("\n[SIZE COMPARISON]")
    print(f"{'Image':45} {'Size':>12}")
    print("-" * 58)
    for tag in tags:
        result = _run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}", tag])
        lines = [line for line in (result.stdout or "").splitlines() if line.strip()]
        if result.returncode != 0:
            print(f"{tag:45} {'<error>':>12}")
        elif not lines:
            print(f"{tag:45} {'<missing>':>12}")
        else:
            image_ref, size = lines[0].split("\t", 1)
            print(f"{image_ref:45} {size:>12}")


def inspect_layers(tag: str) -> None:
    cmd = ["docker", "history", tag, "--no-trunc", "--format", "{{.Size}}\t{{.CreatedBy}}"]
    print(f"\n[LAYER HISTORY] {tag}")
    result = _run(cmd)
    if result.returncode != 0:
        _print_combined_output(result)
        return

    rows: list[tuple[int, str, str]] = []
    for line in (result.stdout or "").splitlines():
        if not line.strip():
            continue
        size, created_by = line.split("\t", 1)
        rows.append((_size_to_bytes(size), size, created_by))
        _emit(f"{size:>10} | {created_by}")

    print("\nLargest layers:")
    for _, size_text, command in sorted(rows, key=lambda row: row[0], reverse=True)[:3]:
        _emit(f"- {size_text}: {command}")


def run_pipeline_container(tag: str, input_dir: str, output_dir: str) -> str:
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    input_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{input_path}:/data/input",
        "-v", f"{output_path}:/data/output",
        tag,
    ]
    print(f"\n[RUN] {' '.join(cmd)}")
    result = _run(cmd)
    if result.returncode != 0:
        raise RuntimeError(_print_combined_output(result))
    return (result.stdout or "").strip()


def explain_caching() -> None:
    print("\n[CACHE EXPLANATION]")
    print("- Change requirements.txt -> dependency layer rebuilds.")
    print("- Change app/pipeline.py -> dependency layer is reused.")
    for tag, output in BUILD_OUTPUTS.items():
        hits = sum(1 for line in output.splitlines() if "CACHED" in line or "Using cache" in line)
        print(f"- {tag}: detected {hits} cache-hit line(s).")


def main() -> int:
    if shutil.which("docker") is None:
        print("Docker CLI was not found in PATH.")
        return 1

    base_tag = "tutorial36-pipeline:base-1.0.0"
    optimized_tag = "tutorial36-pipeline:optimized-1.0.0"

    base_ok = build_image(base_tag, "Dockerfile.base")
    optimized_ok = build_image(optimized_tag, "Dockerfile.optimized")

    built = [tag for tag, ok in [(base_tag, base_ok), (optimized_tag, optimized_ok)] if ok]
    if built:
        compare_image_sizes(built)
        for tag in built:
            inspect_layers(tag)

    explain_caching()

    if optimized_ok:
        output = run_pipeline_container(
            optimized_tag,
            str(Path.cwd() / "runtime_data" / "input"),
            str(Path.cwd() / "runtime_data" / "output"),
        )
        print("\n[CONTAINER STDOUT]")
        _emit(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
