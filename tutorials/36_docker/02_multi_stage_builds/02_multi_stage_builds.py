# ============================================================
# Topic   : Docker for Data Engineers
# File    : 02_multi_stage_builds.py
# Covers  : Multi-stage builds and dev/prod image workflow
# Prereqs : Docker Desktop installed and running
# Run     : python 02_multi_stage_builds.py
# ============================================================

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def emit(message: str) -> None:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    print(message.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    emit(f"\n$ {' '.join(command)}")
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if (completed.stdout or "").strip():
        emit(completed.stdout.rstrip())
    if (completed.stderr or "").strip():
        emit(completed.stderr.rstrip())
    return completed


def validate_required_files() -> bool:
    required = [
        "Dockerfile.base", "Dockerfile.optimized", "Dockerfile.multistage",
        "Dockerfile.dev", "requirements.txt", "requirements-dev.txt", "app"
    ]
    missing = [path for path in required if not Path(path).exists()]
    if not missing:
        return True

    emit("\nMissing required files/folders:")
    for path in missing:
        emit(f"  - {path}")
    emit("\nRun this script from the 02_multi_stage_builds folder.")
    return False


def build_image(tag: str, dockerfile: str, target: str | None = None) -> bool:
    command = ["docker", "build", "-f", dockerfile, "-t", tag]
    if target:
        command.extend(["--target", target])
    command.append(".")
    result = run_command(command)
    if result.returncode != 0:
        emit(f"Build failed for {tag}.")
    return result.returncode == 0


def image_size(tag: str) -> str:
    result = run_command(["docker", "images", tag, "--format", "{{.Size}}"])
    lines = [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]
    return lines[0] if lines else "not built"


def build_and_compare_stages() -> None:
    emit("\n=== Multi-stage build: build-time tools vs runtime image ===")
    builds = [
        ("tutorial36-pipeline:base-1.0.0", "Dockerfile.base", None),
        ("tutorial36-pipeline:optimized-1.0.0", "Dockerfile.optimized", None),
        ("tutorial36-pipeline:multistage-1.0.0", "Dockerfile.multistage", "runtime"),
        ("tutorial36-pipeline:dev-1.0.0", "Dockerfile.dev", None),
    ]

    for tag, dockerfile, target in builds:
        emit(f"\nBuilding {tag} from {dockerfile}")
        build_image(tag, dockerfile, target)

    emit("\nImage size comparison:")
    emit(f"{'Image':42} | Size")
    emit("-" * 58)
    for tag, _, _ in builds:
        emit(f"{tag:42} | {image_size(tag)}")


def demonstrate_copy_from() -> None:
    emit("\n=== COPY --from patterns ===")
    emit("Builder stage installs heavy tools. Runtime stage copies only finished artifacts.")
    emit("Key pattern: COPY --from=builder /install /usr/local")


def dev_vs_prod_workflow() -> None:
    emit("\n=== Dev vs Prod workflow ===")
    emit("DEV:  docker build -f Dockerfile.dev -t tutorial36-pipeline:dev-1.0.0 .")
    emit("PROD: docker build --target runtime -f Dockerfile.multistage -t tutorial36-pipeline:prod-1.0.0 .")


def main() -> int:
    emit("Docker for Data Engineers - Bundle 02: Multi-stage Builds")

    if shutil.which("docker") is None:
        emit("Docker CLI not found.")
        return 1
    if run_command(["docker", "version", "--format", "{{.Server.Version}}"]).returncode != 0:
        emit("Docker Engine is not reachable.")
        return 1
    if not validate_required_files():
        return 1

    build_and_compare_stages()
    demonstrate_copy_from()
    dev_vs_prod_workflow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
