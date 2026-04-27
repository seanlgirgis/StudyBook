# ============================================================
# Topic   : Docker for Data Engineers
# File    : 02_multi_stage_builds.py
# Covers  : Multi-stage builds, builder/runtime separation, dev vs prod workflows
# Prereqs : Docker Desktop installed and running
# Run     : python 02_multi_stage_builds.py
# ============================================================

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class CommandResult:
    """Small value object for Docker command output."""

    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a shell command safely and print stdout/stderr."""
    print(f"\n$ {' '.join(command)}")

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
        print(stdout)

    if stderr.strip():
        print(stderr)

    return completed


def docker_available() -> bool:
    """Return True if Docker CLI is available and Docker Desktop is running."""
    result = run_command(["docker", "version", "--format", "{{.Server.Version}}"])
    if result.returncode != 0:
        print(
            "\nDocker is not available. Start Docker Desktop, then run this script again."
        )
        return False
    print(f"\nDocker server version: {result.stdout.strip()}")
    return True


def build_image(tag: str, dockerfile: str, target: str | None = None) -> bool:
    """Build a Docker image and return True when Docker exits successfully."""
    command = ["docker", "build", "-f", dockerfile, "-t", tag]
    if target:
        command.extend(["--target", target])
    command.append(".")
    result = run_command(command)
    return result.returncode == 0


def get_image_size(tag: str) -> str:
    """Read the human-friendly size for a Docker image tag."""
    result = run_command(
        ["docker", "images", tag, "--format", "{{.Repository}}:{{.Tag}}\t{{.Size}}"]
    )
    if result.returncode != 0 or not result.stdout.strip():
        return "not built"
    return result.stdout.strip().split("\t")[-1]


def build_and_compare_stages() -> None:
    """
    Build both single-stage and multi-stage images and compare image sizes.

    Expected rough sizes vary by Docker cache, platform, and base image updates:
      python:3.11 base image        -> around 1 GB
      Dockerfile.base               -> large because it uses full python:3.11
      Dockerfile.optimized          -> smaller because it uses slim + cache-aware layers
      Dockerfile.multistage runtime -> smaller runtime because builder tools are discarded

    Key idea:
      The builder stage can contain compilers and headers.
      The final runtime stage receives only files copied with COPY --from=builder.
    """
    required_paths = [
    "Dockerfile.base",
    "Dockerfile.optimized",
    "Dockerfile.multistage",
    "Dockerfile.dev",
    "requirements.txt",
    "app",
    ]

    missing = [path for path in required_paths if not Path(path).exists()]
    if missing:
        print("\nMissing required files/folders:")
        for path in missing:
            print(f"  - {path}")
        print("\nRun this script from:")
        print(r"  D:\Workarea\StudyBook\tutorials\36_docker")
        print("\nNot from inside docker_bundle_02_multistage.")
        return
    print("\n=== Multi-stage build: build-time tools vs runtime image ===")
    print(
        "A multi-stage Dockerfile lets you use heavy build tools temporarily, "
        "then ship only the final runtime files."
    )

    images_to_build = [
        ("tutorial36-pipeline:base-1.0.0", "Dockerfile.base", None),
        ("tutorial36-pipeline:optimized-1.0.0", "Dockerfile.optimized", None),
        ("tutorial36-pipeline:multistage-1.0.0", "Dockerfile.multistage", "runtime"),
    ]

    for tag, dockerfile, target in images_to_build:
        print(f"\nBuilding {tag} from {dockerfile}")
        ok = build_image(tag=tag, dockerfile=dockerfile, target=target)
        if not ok:
            print(f"Build failed for {tag}. Continuing so you can inspect output.")

    print("\nImage size comparison:")
    print(f"{'Image':45} | {'Size'}")
    print("-" * 62)
    for tag, _, _ in images_to_build:
        print(f"{tag:45} | {get_image_size(tag)}")

    print(
        "\nWhy this matters:\n"
        "- Smaller images pull faster in CI/CD and cloud deployments.\n"
        "- Fewer build tools in runtime reduces security risk.\n"
        "- COPY --from is the bridge between stages: only explicitly copied files survive."
    )


def demonstrate_copy_from() -> None:
    """
    Show COPY --from patterns for multiple uses:
    1. Copy built artifacts from a builder stage
    2. Copy config from a dedicated config stage
    3. Copy a binary from an official image into a custom image
    """
    print("\n=== COPY --from patterns ===")

    examples = [
        (
            "1. Copy built artifacts from builder",
            """
FROM python:3.11.9-slim-bookworm AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11.9-slim-bookworm AS runtime
COPY --from=builder /install /usr/local
""".strip(),
            "Use this when dependencies need compilers during build but not at runtime.",
        ),
        (
            "2. Copy config from a dedicated config stage",
            """
FROM alpine:3.20 AS config
RUN mkdir /config && echo "log_level=INFO" > /config/app.conf

FROM python:3.11.9-slim-bookworm AS runtime
COPY --from=config /config/app.conf /etc/myapp/app.conf
""".strip(),
            "Use this when generated config should be separated from app code.",
        ),
        (
            "3. Copy a binary from an official image",
            """
FROM golang:1.22 AS gobuilder
WORKDIR /src
COPY . .
RUN go build -o /myapp .

FROM scratch AS final
COPY --from=gobuilder /myapp /myapp
ENTRYPOINT ["/myapp"]
""".strip(),
            "Use this for tiny compiled runtime images with no package manager.",
        ),
    ]

    for title, dockerfile_snippet, explanation in examples:
        print(f"\n{title}")
        print(dockerfile_snippet)
        print(f"Why: {explanation}")


def dev_vs_prod_workflow() -> None:
    """
    Print the two-command developer workflow.

    DEV:
      docker build -f Dockerfile.dev -t tutorial36-pipeline:dev-1.0.0 .
      docker run --rm -v ${PWD}/app:/app/app:ro tutorial36-pipeline:dev-1.0.0

    PROD:
      docker build --target runtime -f Dockerfile.multistage -t tutorial36-pipeline:prod-1.0.0 .
      docker run --rm tutorial36-pipeline:prod-1.0.0

    Explanation:
      Dev mounts source code for fast iteration.
      Prod bakes source code into an immutable image.
    """
    print("\n=== Dev vs Prod workflow ===")

    print(
        """
DEV image: optimize for feedback speed.
  docker build -f Dockerfile.dev -t tutorial36-pipeline:dev-1.0.0 .
  docker run --rm -v ${PWD}/app:/app/app:ro tutorial36-pipeline:dev-1.0.0

Why dev mounts code:
  You can edit files on the host and re-run quickly without rebuilding every time.

PROD image: optimize for repeatability and deployment safety.
  docker build --target runtime -f Dockerfile.multistage -t tutorial36-pipeline:prod-1.0.0 .
  docker run --rm tutorial36-pipeline:prod-1.0.0

Why prod bakes code in:
  The image is immutable. CI/CD, teammates, and cloud runtimes all execute the same artifact.
""".strip()
    )


def main() -> None:
    """Run the bundle 02 learning path."""
    print("Docker for Data Engineers - Bundle 02: Multi-stage Builds")

    if docker_available():
        build_and_compare_stages()
    else:
        print("\nSkipping live builds because Docker is not available.")

    demonstrate_copy_from()
    dev_vs_prod_workflow()


if __name__ == "__main__":
    main()
