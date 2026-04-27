# ============================================================
# Topic   : Docker for Data Engineers
# File    : 04_data_pipeline_container.py
# Covers  : Volume mounts, env vars, secrets, SIGTERM, and resource limits
# Prereqs : Docker Desktop installed and running
# Run     : python 04_data_pipeline_container.py
# ============================================================

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

IMAGE_TAG = "tutorial36-pipeline:signals-1.0.0"


def emit(message: str) -> None:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    print(message.encode(encoding, errors="replace").decode(encoding, errors="replace"))


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    emit(f"\n$ {' '.join(command)}")
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if (completed.stdout or "").strip():
        emit(completed.stdout.rstrip())
    if (completed.stderr or "").strip():
        emit(completed.stderr.rstrip())
    return completed


def validate_required_files() -> bool:
    required = ["Dockerfile", "app/graceful_pipeline.py", "requirements.txt"]
    missing = [item for item in required if not Path(item).exists()]
    if not missing:
        return True
    emit("\nMissing required files:")
    for item in missing:
        emit(f"  - {item}")
    emit("\nRun this from the 04_pipeline_container folder.")
    return False


def build_pipeline_image() -> bool:
    return run_command(["docker", "build", "-f", "Dockerfile", "-t", IMAGE_TAG, "."]).returncode == 0


def demonstrate_volume_patterns() -> None:
    emit("\n=== Volume patterns ===")
    emit(f"Named volume: docker run --rm -v pipeline_data:/data {IMAGE_TAG}")
    emit(f"Bind mount:   docker run --rm -v ${{PWD}}/runtime_data/output:/data/output {IMAGE_TAG}")
    emit(f"tmpfs:        docker run --rm --tmpfs /tmp:size=512m {IMAGE_TAG}")
    emit("Secret file:  mount a file to /run/secrets/db_password:ro")


def demonstrate_env_and_secrets() -> None:
    emit("\n=== Env vars and secrets ===")
    emit(f"Config: docker run --rm -e MAX_BATCHES=5 {IMAGE_TAG}")
    emit("Secrets: prefer mounted files or cloud secret managers over plain env vars.")


def resource_limits() -> None:
    emit("\n=== Resource limits ===")
    emit(f"docker run --rm --memory=2g --memory-swap=2g --cpus=2.0 --pids-limit=200 {IMAGE_TAG}")


def sigterm_demo() -> None:
    emit("\n=== SIGTERM graceful shutdown demo ===")
    output_dir = Path.cwd() / "runtime_data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    name = "tutorial36-sigterm-demo"
    run_command(["docker", "rm", "-f", name])

    started = run_command([
        "docker", "run", "-d", "--name", name,
        "-e", "MAX_BATCHES=30",
        "-v", f"{output_dir}:/data/output",
        IMAGE_TAG,
    ])
    if started.returncode != 0:
        return

    time.sleep(4)
    run_command(["docker", "stop", "--time", "30", name])
    run_command(["docker", "logs", name])
    run_command(["docker", "rm", name])

    summary = output_dir / "graceful_summary.json"
    if summary.exists():
        emit("\nSummary file:")
        emit(summary.read_text(encoding="utf-8"))


def main() -> int:
    emit("Docker for Data Engineers - Bundle 04: Production Pipeline Container")
    if shutil.which("docker") is None:
        emit("Docker CLI not found.")
        return 1
    if run_command(["docker", "version", "--format", "{{.Server.Version}}"]).returncode != 0:
        return 1
    if not validate_required_files():
        return 1

    demonstrate_volume_patterns()
    demonstrate_env_and_secrets()
    resource_limits()

    if not build_pipeline_image():
        return 1

    sigterm_demo()
    emit("\nBundle 04 complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
