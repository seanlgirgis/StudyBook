# ============================================================
# Topic   : Docker for Data Engineers
# File    : 01_dockerfile_basics.py
# Covers  : Dockerfile basics, layer caching, and image comparison
# Prereqs : Docker Desktop installed and running
# Run     : python 01_dockerfile_basics.py
# ============================================================

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BUILD_OUTPUTS: dict[str, str] = {}


def _emit(message: str) -> None:
    """Print text safely on consoles with limited encodings."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe = message.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(safe)


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command with captured text output."""
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
    token = size_token.strip()
    match = re.match(r"^(?P<value>[0-9]*\.?[0-9]+)(?P<unit>B|kB|MB|GB)$", token)
    if not match:
        return 0
    value = float(match.group("value"))
    unit = match.group("unit")
    multipliers = {
        "B": 1,
        "kB": 1000,
        "MB": 1000**2,
        "GB": 1000**3,
    }
    return int(value * multipliers[unit])


def build_image(tag: str, dockerfile: str, context: str = ".") -> bool:
    """
    Run: docker build -t {tag} -f {dockerfile} {context}
    Print build output line by line.
    Return True if exit code 0.
    """
    cmd = ["docker", "build", "-t", tag, "-f", dockerfile, context]
    print(f"\n[BUILD] {' '.join(cmd)}")
    result = _run(cmd)
    combined = _print_combined_output(result)
    BUILD_OUTPUTS[tag] = combined
    success = result.returncode == 0
    print(f"[BUILD RESULT] {tag}: {'SUCCESS' if success else 'FAILURE'}")
    return success


def compare_image_sizes(tags: list[str]) -> None:
    """
    Run: docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}" for each tag.
    Print comparison table showing base vs optimized image size.
    """
    print("\n[SIZE COMPARISON]")
    print(f"{'Image':45} {'Size':>12}")
    print("-" * 58)

    for tag in tags:
        cmd = ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}", tag]
        result = _run(cmd)
        if result.returncode != 0:
            print(f"{tag:45} {'<error>':>12}")
            continue

        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            print(f"{tag:45} {'<missing>':>12}")
            continue

        image_ref, size = lines[0].split("\t", 1)
        print(f"{image_ref:45} {size:>12}")


def inspect_layers(tag: str) -> None:
    """
    Run: docker history {tag} --no-trunc --format "{{.Size}}\t{{.CreatedBy}}"
    Print each layer with its size and the command that created it.
    Explain which layers are largest and why.
    """
    cmd = ["docker", "history", tag, "--no-trunc", "--format", "{{.Size}}\t{{.CreatedBy}}"]
    print(f"\n[LAYER HISTORY] {tag}")
    result = _run(cmd)

    if result.returncode != 0:
        _print_combined_output(result)
        print(f"Could not inspect layers for {tag}")
        return

    layer_rows: list[tuple[int, str, str]] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        size, created_by = line.split("\t", 1)
        layer_rows.append((_size_to_bytes(size), size, created_by))
        _emit(f"{size:>10} | {created_by}")

    if not layer_rows:
        print("No layers returned.")
        return

    largest = sorted(layer_rows, key=lambda row: row[0], reverse=True)[:3]
    print("\nLargest layers (typically dependency install or large COPY steps):")
    for _, size_text, command in largest:
        _emit(f"- {size_text}: {command}")


def run_pipeline_container(tag: str, input_dir: str, output_dir: str) -> str:
    """
    Run: docker run --rm -v {input_dir}:/data/input -v {output_dir}:/data/output {tag}
    Return stdout from container.
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    input_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{input_path}:/data/input",
        "-v",
        f"{output_path}:/data/output",
        tag,
    ]
    print(f"\n[RUN] {' '.join(cmd)}")
    result = _run(cmd)

    if result.returncode != 0:
        details = _print_combined_output(result)
        raise RuntimeError(f"Container run failed for {tag}: {details}")

    if result.stderr:
        for line in result.stderr.splitlines():
            _emit(line)

    return result.stdout.strip()


def explain_caching() -> None:
    """
    Print explanation of Docker layer caching with example:
    - Change requirements.txt -> invalidates pip layer and all subsequent
    - Change app/pipeline.py -> only rebuilds the COPY app/ layer (pip layer reused)
    Show the actual layer cache hit/miss in build output.
    """
    print("\n[CACHE EXPLANATION]")
    print("- If requirements.txt changes, dependency install must rebuild, so later layers rebuild too.")
    print("- If only app/pipeline.py changes, the dependency layer can be reused from cache.")

    for tag, output in BUILD_OUTPUTS.items():
        cached_hits = sum(1 for line in output.splitlines() if "CACHED" in line or "Using cache" in line)
        print(f"- {tag}: detected {cached_hits} cache-hit line(s) in current build output.")


def main() -> int:
    if shutil.which("docker") is None:
        print("Docker CLI was not found in PATH. Install Docker Desktop and retry.")
        return 1

    base_tag = "tutorial36-pipeline:base-1.0.0"
    optimized_tag = "tutorial36-pipeline:optimized-1.0.0"

    base_ok = build_image(base_tag, "Dockerfile.base")
    optimized_ok = build_image(optimized_tag, "Dockerfile.optimized")

    built_tags = [tag for tag, ok in [(base_tag, base_ok), (optimized_tag, optimized_ok)] if ok]
    if built_tags:
        compare_image_sizes(built_tags)
        for tag in built_tags:
            inspect_layers(tag)

    explain_caching()

    if optimized_ok:
        input_dir = str(Path.cwd() / "runtime_data" / "input")
        output_dir = str(Path.cwd() / "runtime_data" / "output")
        try:
            container_stdout = run_pipeline_container(optimized_tag, input_dir, output_dir)
            print("\n[CONTAINER STDOUT]")
            _emit(container_stdout)

            summary_file = Path(output_dir) / "summary.json"
            if summary_file.exists():
                print("\n[SUMMARY FILE]")
                print(summary_file.read_text(encoding="utf-8"))
        except RuntimeError as exc:
            print(str(exc))
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
