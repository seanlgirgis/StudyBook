# ============================================================
# Topic   : Docker for Data Engineers
# File    : 03_docker_compose.py
# Covers  : Docker Compose services, health checks, volumes, and networks
# Prereqs : Docker Desktop installed and running
# Run     : python 03_docker_compose.py
# ============================================================

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


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
    required = [".env", "docker-compose.yml", "Dockerfile.optimized", "requirements.txt", "init_db.sql", "app/pipeline.py"]
    missing = [item for item in required if not Path(item).exists()]
    if not missing:
        return True
    emit("\nMissing required files:")
    for item in missing:
        emit(f"  - {item}")
    emit("\nRun from 03a_compose_stack. If .env is missing: copy .env.example .env")
    return False


def compose_up(detach: bool = True) -> bool:
    command = ["docker", "compose", "up", "--build"]
    if detach:
        command.append("-d")
    return run_command(command).returncode == 0


def wait_for_healthy(service: str, timeout: int = 90) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        result = run_command(["docker", "compose", "ps", service, "--format", "json"])
        output = (result.stdout or "").strip()
        if "healthy" in output.lower():
            emit(f"{service} is healthy.")
            return True
        time.sleep(2)
    emit(f"{service} did not become healthy.")
    return False


def print_stack_status() -> None:
    result = run_command(["docker", "compose", "ps"])
    if result.returncode != 0:
        emit("Could not read Compose status.")


def main() -> int:
    emit("Docker for Data Engineers - Bundle 03A: Compose Data Stack")
    if shutil.which("docker") is None:
        emit("Docker CLI not found.")
        return 1
    if run_command(["docker", "version", "--format", "{{.Server.Version}}"]).returncode != 0:
        return 1
    if not validate_required_files():
        return 1
    if not compose_up(detach=True):
        return 1
    wait_for_healthy("postgres")
    wait_for_healthy("redis")
    print_stack_status()
    emit("\nVerify DB write:")
    emit('  docker compose exec postgres psql -U pipeline -d studybook -c "SELECT * FROM pipeline_runs ORDER BY id DESC;"')
    emit("\nStop:")
    emit("  docker compose down")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
