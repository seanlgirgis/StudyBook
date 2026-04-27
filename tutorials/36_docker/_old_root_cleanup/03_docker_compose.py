# ============================================================
# Topic   : Docker for Data Engineers
# File    : 03_docker_compose.py
# Covers  : Docker Compose services, networks, volumes, health checks, and env files
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
    """Print safely on Windows consoles."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe = message.encode(encoding, errors="replace").decode(encoding, errors="replace")
    print(safe)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command with safe captured output."""
    emit(f"\n$ {' '.join(command)}")
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""

    if stdout.strip():
        emit(stdout.rstrip())
    if stderr.strip():
        emit(stderr.rstrip())

    return completed


def validate_required_files() -> bool:
    """Fail early with a clear message if Compose support files are missing."""
    required_paths = [
        "docker-compose.yml",
        ".env",
        "Dockerfile.optimized",
        "Dockerfile.dev",
        "requirements.txt",
        "requirements-dev.txt",
        "init_db.sql",
        "app",
    ]
    missing = [path for path in required_paths if not Path(path).exists()]
    if not missing:
        return True

    emit("\nMissing required files/folders:")
    for path in missing:
        emit(f"  - {path}")

    emit("\nFix:")
    emit("  1. Run this from D:\\Workarea\\StudyBook\\tutorials\\36_docker")
    emit("  2. Copy .env.example to .env if .env is missing:")
    emit("     copy .env.example .env")
    emit("\nCompose needs these files because it builds local images and mounts init_db.sql.")
    return False


def compose_up(detach: bool = True) -> bool:
    """Run docker compose up --build (-d if detach). Return True on success."""
    command = ["docker", "compose", "up", "--build"]
    if detach:
        command.append("-d")
    result = run_command(command)
    return result.returncode == 0


def compose_down(volumes: bool = False) -> None:
    """Run docker compose down (--volumes if volumes=True). Print status."""
    command = ["docker", "compose", "down"]
    if volumes:
        command.append("--volumes")
    result = run_command(command)
    if result.returncode == 0:
        emit("\nCompose stack is stopped.")
    else:
        emit("\nCompose stack did not stop cleanly. Review output above.")


def wait_for_healthy(service: str, timeout: int = 60) -> bool:
    """
    Poll docker compose ps {service} every 2 seconds until health = healthy.
    Return True if healthy within timeout, False if timeout.
    Print: "Waiting for {service}... (10s)" with progress.
    """
    start = time.time()
    while time.time() - start <= timeout:
        elapsed = int(time.time() - start)
        emit(f"Waiting for {service}... ({elapsed}s)")

        result = run_command(["docker", "compose", "ps", service, "--format", "json"])
        output = (result.stdout or "").strip()

        if result.returncode == 0 and output:
            try:
                parsed = json.loads(output)
                rows = parsed if isinstance(parsed, list) else [parsed]
                for row in rows:
                    health = str(row.get("Health", "")).lower()
                    state = str(row.get("State", "")).lower()
                    if health == "healthy" or "healthy" in state:
                        emit(f"{service} is healthy.")
                        return True
            except json.JSONDecodeError:
                if "healthy" in output.lower():
                    emit(f"{service} is healthy.")
                    return True

        time.sleep(2)

    emit(f"{service} did not become healthy within {timeout} seconds.")
    return False


def run_in_service(service: str, command: list[str]) -> str:
    """
    Run: docker compose exec {service} {command}
    Return stdout. Raise RuntimeError on non-zero exit.
    """
    full_command = ["docker", "compose", "exec", service, *command]
    result = run_command(full_command)

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed in service {service}: {' '.join(command)}\n"
            f"{result.stderr or result.stdout or ''}"
        )

    return result.stdout.strip()


def print_stack_status() -> None:
    """
    Run: docker compose ps --format json
    Parse and print a formatted service status table:
      Service    | Status    | Health   | Ports
      pipeline   | running   | healthy  | -
      postgres   | running   | healthy  | 5432/tcp
      redis      | running   | healthy  | 6379/tcp
    """
    result = run_command(["docker", "compose", "ps", "--format", "json"])

    emit("\nService    | Status              | Health     | Ports")
    emit("-" * 62)

    if result.returncode != 0 or not (result.stdout or "").strip():
        emit("No Compose services found. Run compose_up() first.")
        return

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    rows: list[dict[str, object]] = []
    for line in lines:
        try:
            parsed = json.loads(line)
            if isinstance(parsed, list):
                rows.extend(parsed)
            else:
                rows.append(parsed)
        except json.JSONDecodeError:
            continue

    if not rows:
        try:
            parsed = json.loads(result.stdout)
            rows = parsed if isinstance(parsed, list) else [parsed]
        except json.JSONDecodeError:
            emit("Could not parse docker compose ps output.")
            return

    for row in rows:
        service = str(row.get("Service", row.get("Name", "-")))
        state = str(row.get("State", row.get("Status", "-")))
        health = str(row.get("Health", "-") or "-")
        publishers = row.get("Publishers", [])
        ports = "-"

        if isinstance(publishers, list) and publishers:
            port_chunks = []
            for publisher in publishers:
                if isinstance(publisher, dict):
                    published = publisher.get("PublishedPort")
                    target = publisher.get("TargetPort")
                    if published and target:
                        port_chunks.append(f"{published}->{target}")
            ports = ", ".join(port_chunks) if port_chunks else "-"

        emit(f"{service:10} | {state:19} | {health:10} | {ports}")


def main() -> int:
    emit("Docker for Data Engineers - Bundle 03A: Compose Data Stack")

    if shutil.which("docker") is None:
        emit("Docker CLI was not found in PATH. Install Docker Desktop and retry.")
        return 1

    version = run_command(["docker", "version", "--format", "{{.Server.Version}}"])
    if version.returncode != 0:
        emit("Docker Engine is not reachable. Start Docker Desktop and retry.")
        return 1

    if not validate_required_files():
        return 1

    emit("\nThis script starts a small data-engineering Compose stack:")
    emit("- pipeline: your Python pipeline image")
    emit("- postgres: database container with a health check")
    emit("- redis: cache container with a health check")
    emit("\nIt uses docker compose up --build -d so your terminal stays free.")

    if not compose_up(detach=True):
        emit("docker compose up failed. Review output above.")
        return 1

    wait_for_healthy("postgres", timeout=90)
    wait_for_healthy("redis", timeout=60)
    print_stack_status()

    emit("\nTry these next:")
    emit("  docker compose logs -f")
    emit("  docker compose ps")
    emit("  docker compose exec postgres psql -U pipeline -d studybook")
    emit("  docker compose down")
    emit("  docker compose down --volumes   # destroys database volume too")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
