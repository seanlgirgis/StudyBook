from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from _env_loader import first_non_empty, load_env_file

READ_ONLY_SCOPE = "https://www.googleapis.com/auth/cloud-platform.read-only"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only GCP connection proof.")
    parser.add_argument("--credentials-path", help="Service account JSON path override.")
    parser.add_argument("--project-id", help="GCP project ID override.")
    parser.add_argument(
        "--require-project-lookup",
        action="store_true",
        help="Strict mode: require Cloud Resource Manager project lookup to succeed.",
    )
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to local env file with GOOGLE_APPLICATION_CREDENTIALS_PATH and GCP_PROJECT_ID.",
    )
    parser.add_argument("--timeout-sec", type=int, default=10, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    credentials_path = first_non_empty(
        args.credentials_path,
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS_PATH"),
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        env_map.get("GOOGLE_APPLICATION_CREDENTIALS_PATH"),
    )

    project_id = first_non_empty(
        args.project_id,
        os.getenv("GCP_PROJECT_ID"),
        env_map.get("GCP_PROJECT_ID"),
    )

    result: dict[str, object] = {
        "ok": False,
        "proof": "gcp_read_only",
        "env_file_checked": str(env_file),
        "project_id": project_id,
    }

    if not credentials_path:
        result["error"] = "Missing credential path. Provide --credentials-path or GOOGLE_APPLICATION_CREDENTIALS_PATH."
        print(json.dumps(result, indent=2))
        return 2

    credentials_file = Path(credentials_path)
    if not credentials_file.exists():
        result["error"] = f"Credential file not found: {credentials_file}"
        print(json.dumps(result, indent=2))
        return 2

    if not project_id:
        result["error"] = "Missing project ID. Provide --project-id or GCP_PROJECT_ID."
        print(json.dumps(result, indent=2))
        return 2

    try:
        creds = service_account.Credentials.from_service_account_file(
            str(credentials_file),
            scopes=[READ_ONLY_SCOPE],
        )
        creds.refresh(Request())

        headers = {"Authorization": f"Bearer {creds.token}"}
        project_url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{project_id}"
        project_resp = requests.get(project_url, headers=headers, timeout=args.timeout_sec)

        project_payload: dict[str, object]
        if project_resp.ok:
            project_payload = {
                "ok": True,
                "status_code": project_resp.status_code,
                "project": project_resp.json(),
            }
        else:
            project_payload = {
                "ok": False,
                "status_code": project_resp.status_code,
                "body": project_resp.text,
            }

        # Optional: sample bucket listing if Storage API is enabled and IAM allows it.
        buckets_url = f"https://storage.googleapis.com/storage/v1/b?project={project_id}&maxResults=5"
        buckets_resp = requests.get(buckets_url, headers=headers, timeout=args.timeout_sec)
        if buckets_resp.ok:
            bucket_names = [item.get("name") for item in buckets_resp.json().get("items", [])]
            buckets_payload: dict[str, object] = {
                "ok": True,
                "status_code": buckets_resp.status_code,
                "bucket_sample": bucket_names,
            }
        else:
            buckets_payload = {
                "ok": False,
                "status_code": buckets_resp.status_code,
                "body": buckets_resp.text,
            }

        overall_ok = project_resp.ok if args.require_project_lookup else (project_resp.ok or buckets_resp.ok)
        warnings: list[str] = []
        if not project_resp.ok and buckets_resp.ok:
            warnings.append(
                "Cloud Resource Manager lookup failed, but Storage probe succeeded. "
                "Enable cloudresourcemanager.googleapis.com for project metadata checks."
            )
        if project_resp.ok and not buckets_resp.ok:
            warnings.append(
                "Project lookup succeeded, but Storage probe failed. "
                "Storage API may be disabled or IAM may not allow bucket listing."
            )

        result.update(
            {
                "ok": overall_ok,
                "strict_mode": args.require_project_lookup,
                "token_expiry": str(creds.expiry),
                "project_lookup": project_payload,
                "storage_bucket_probe": buckets_payload,
                "warnings": warnings,
            }
        )

        print(json.dumps(result, indent=2, default=str))
        return 0 if overall_ok else 1
    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)
        print(json.dumps(result, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
