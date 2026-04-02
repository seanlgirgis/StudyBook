from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from _env_loader import first_non_empty, load_env_file


def normalize_host(host: str | None) -> str | None:
    if not host:
        return None
    value = host.strip()
    if not value:
        return None
    if not value.startswith("http://") and not value.startswith("https://"):
        value = f"https://{value}"
    return value.rstrip("/")


def is_placeholder(value: str | None) -> bool:
    if not value:
        return True
    normalized = value.strip().lower()
    return normalized in {
        "<databricks_token>",
        "<fill>",
        "replace_me",
        "replace-me",
        "changeme",
        "change_me",
    }


def probe_current_user(host: str, token: str, timeout_sec: int) -> dict[str, object]:
    url = f"{host}/api/2.0/current-user/me"
    headers = {"Authorization": f"Bearer {token}"}

    start = time.perf_counter()
    try:
        response = requests.get(url, headers=headers, timeout=max(timeout_sec, 1))
    except requests.RequestException as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": False,
            "endpoint": url,
            "latency_ms": elapsed_ms,
            "error": str(exc),
        }

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    result: dict[str, object] = {
        "ok": response.ok,
        "endpoint": url,
        "status_code": response.status_code,
        "latency_ms": elapsed_ms,
    }

    if response.ok:
        payload = response.json()
        result.update(
            {
                "user_name": payload.get("userName"),
                "display_name": payload.get("displayName"),
                "active": payload.get("active"),
            }
        )
    else:
        result["body"] = response.text[:500]
    return result


def probe_clusters(host: str, token: str, timeout_sec: int) -> dict[str, object]:
    url = f"{host}/api/2.0/clusters/list"
    headers = {"Authorization": f"Bearer {token}"}

    start = time.perf_counter()
    try:
        response = requests.get(url, headers=headers, timeout=max(timeout_sec, 1))
    except requests.RequestException as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": False,
            "endpoint": url,
            "latency_ms": elapsed_ms,
            "error": str(exc),
        }

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    result: dict[str, object] = {
        "ok": response.ok,
        "endpoint": url,
        "status_code": response.status_code,
        "latency_ms": elapsed_ms,
    }

    if response.ok:
        payload = response.json()
        clusters = payload.get("clusters") or []
        result.update(
            {
                "cluster_count": len(clusters),
                "cluster_sample": [c.get("cluster_name") for c in clusters[:5]],
            }
        )
    else:
        result["body"] = response.text[:500]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Databricks workspace connection proof.")
    parser.add_argument("--host", help="Databricks workspace host override.")
    parser.add_argument("--token", help="Databricks PAT override.")
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to local env file with DATABRICKS_HOST and DATABRICKS_TOKEN.",
    )
    parser.add_argument("--timeout-sec", type=int, default=15, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    host = normalize_host(
        first_non_empty(
            args.host,
            os.getenv("DATABRICKS_HOST"),
            env_map.get("DATABRICKS_HOST"),
        )
    )
    token = first_non_empty(
        args.token,
        os.getenv("DATABRICKS_TOKEN"),
        env_map.get("DATABRICKS_TOKEN"),
    )

    result: dict[str, object] = {
        "ok": False,
        "proof": "databricks_read_only",
        "env_file_checked": str(env_file),
        "host_resolved": host,
        "token_present": bool(token),
        "token_looks_placeholder": is_placeholder(token),
    }

    if requests is None:
        result["error"] = "Missing dependency: requests"
        result["hint"] = "Install with: pip install requests"
        print(json.dumps(result, indent=2))
        return 2

    if not host:
        result["error"] = "Missing workspace host. Provide --host or DATABRICKS_HOST."
        print(json.dumps(result, indent=2))
        return 2

    if is_placeholder(token):
        result["error"] = "Missing Databricks PAT. Provide --token or DATABRICKS_TOKEN with a real token."
        result["hint"] = (
            "Create token in Databricks: User Settings -> Developer -> Access Tokens -> Generate new token"
        )
        print(json.dumps(result, indent=2))
        return 2

    current_user_probe = probe_current_user(host, token, args.timeout_sec)
    result["current_user_probe"] = current_user_probe

    clusters_probe: dict[str, object] | None = None
    if not current_user_probe.get("ok"):
        clusters_probe = probe_clusters(host, token, args.timeout_sec)
        result["clusters_probe"] = clusters_probe

    probes = [current_user_probe]
    if clusters_probe is not None:
        probes.append(clusters_probe)

    result["ok"] = any(bool(p.get("ok")) for p in probes)

    if result["ok"]:
        ok_probe = next((p for p in probes if p.get("ok")), None)
        result["workspace_host_confirmed"] = host
        if ok_probe:
            result["proof_endpoint"] = ok_probe.get("endpoint")
    else:
        for probe in probes:
            body = str(probe.get("body", "")).lower()
            if probe.get("status_code") in (401, 403) or "invalid access token" in body:
                result["hint"] = "Token appears invalid or lacks scope. Generate a fresh PAT and retry."
                break

    print(json.dumps(result, indent=2, default=str))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
