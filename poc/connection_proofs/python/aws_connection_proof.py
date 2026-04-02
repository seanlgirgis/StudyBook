from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List

from _env_loader import first_non_empty, load_env_file


def resolve_aws_cli(cli_override: str | None) -> str | None:
    candidates = [
        cli_override,
        os.getenv("AWS_CLI_PATH"),
        shutil.which("aws"),
        r"C:\Program Files\Amazon\AWSCLIV2\aws.exe",
    ]

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if path.exists():
            return str(path)
        if candidate == "aws":
            return candidate
    return None


def parse_aws_profiles(credentials_file: Path) -> List[str]:
    if not credentials_file.exists():
        return []

    profiles: List[str] = []
    for raw_line in credentials_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("[") and line.endswith("]"):
            profile = line[1:-1].strip()
            if profile and profile not in profiles:
                profiles.append(profile)
    return profiles


def choose_profile(explicit_profile: str | None, available_profiles: List[str]) -> str | None:
    if explicit_profile:
        return explicit_profile

    for preferred in ("study", "default", "de_learner"):
        if preferred in available_profiles:
            return preferred

    if available_profiles:
        return available_profiles[0]

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only AWS connection proof (STS GetCallerIdentity).")
    parser.add_argument("--profile", help="AWS profile override.")
    parser.add_argument("--region", help="AWS region override.")
    parser.add_argument("--aws-cli", help="Path to AWS CLI executable override.")
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to local env file with AWS_* values.",
    )
    parser.add_argument("--timeout-sec", type=int, default=12, help="AWS CLI timeout in seconds.")
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    explicit_profile = first_non_empty(
        args.profile,
        os.getenv("AWS_PROFILE"),
        os.getenv("AWS_DEFAULT_PROFILE"),
        env_map.get("AWS_PROFILE"),
        env_map.get("AWS_DEFAULT_PROFILE"),
    )
    region = first_non_empty(
        args.region,
        os.getenv("AWS_REGION"),
        os.getenv("AWS_DEFAULT_REGION"),
        env_map.get("AWS_REGION"),
        env_map.get("AWS_DEFAULT_REGION"),
    )

    credentials_file = first_non_empty(
        os.getenv("AWS_SHARED_CREDENTIALS_FILE"),
        env_map.get("AWS_SHARED_CREDENTIALS_FILE"),
        str(Path.home() / ".aws" / "credentials"),
    )
    config_file = first_non_empty(
        os.getenv("AWS_CONFIG_FILE"),
        env_map.get("AWS_CONFIG_FILE"),
        str(Path.home() / ".aws" / "config"),
    )

    aws_cli = resolve_aws_cli(args.aws_cli)
    credentials_path = Path(credentials_file)
    available_profiles = parse_aws_profiles(credentials_path)
    profile = choose_profile(explicit_profile, available_profiles)

    result: dict[str, object] = {
        "ok": False,
        "proof": "aws_sts_read_only",
        "env_file_checked": str(env_file),
        "profile_requested": profile,
        "profile_source": "explicit" if explicit_profile else "auto",
        "available_profiles": available_profiles,
        "region_requested": region,
        "aws_cli": aws_cli,
        "credentials_file": credentials_file,
        "credentials_file_exists": credentials_path.exists(),
        "config_file": config_file,
        "config_file_exists": Path(config_file).exists(),
    }

    if not aws_cli:
        result["error"] = "AWS CLI was not found. Install AWS CLI v2 or pass --aws-cli."
        print(json.dumps(result, indent=2))
        return 2

    if not profile:
        result["error"] = "No AWS profile resolved. Set AWS_PROFILE or pass --profile after running aws configure."
        print(json.dumps(result, indent=2))
        return 2

    command = [aws_cli, "sts", "get-caller-identity", "--output", "json", "--profile", profile]
    if region:
        command.extend(["--region", region])

    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=max(args.timeout_sec, 1),
            check=False,
        )
    except subprocess.TimeoutExpired:
        result["error"] = f"AWS CLI timed out after {args.timeout_sec} seconds."
        print(json.dumps(result, indent=2))
        return 1
    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)
        print(json.dumps(result, indent=2))
        return 1

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    result["latency_ms"] = elapsed_ms
    result["command"] = command

    if completed.returncode != 0:
        result["error"] = (completed.stderr or completed.stdout or "Unknown AWS CLI error.").strip()
        result["return_code"] = completed.returncode
        if available_profiles:
            result["hint"] = f"Available profiles: {', '.join(available_profiles)}"
        print(json.dumps(result, indent=2))
        return 1

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result["error"] = "AWS CLI returned non-JSON output."
        result["raw_output"] = completed.stdout.strip()
        print(json.dumps(result, indent=2))
        return 1

    result.update(
        {
            "ok": True,
            "account": payload.get("Account"),
            "arn": payload.get("Arn"),
            "user_id": payload.get("UserId"),
        }
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
