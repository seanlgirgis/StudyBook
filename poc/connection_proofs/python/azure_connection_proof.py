from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from _env_loader import first_non_empty, load_env_file

# Azure CLI known install paths on Windows
_AZ_CLI_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
    r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
]


def resolve_azure_cli() -> str | None:
    found = shutil.which("az")
    if found:
        return found
    for candidate in _AZ_CLI_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def probe_via_cli(az_cli: str, subscription_id: str | None, timeout_sec: int) -> dict:
    """Read-only proof: az account show (no writes, no resource creation)."""
    cmd = [az_cli, "account", "show", "--output", "json"]
    if subscription_id:
        cmd.extend(["--subscription", subscription_id])

    start = time.perf_counter()
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max(timeout_sec, 1),
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"az CLI timed out after {timeout_sec}s"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    if completed.returncode != 0:
        error_text = (completed.stderr or completed.stdout or "Unknown az error").strip()
        result: dict = {"ok": False, "error": error_text, "latency_ms": elapsed_ms}
        if "please run" in error_text.lower() or "login" in error_text.lower():
            result["hint"] = "Run 'az login' first, then retry."
        return result

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "az returned non-JSON output", "raw": completed.stdout[:500]}

    return {
        "ok": True,
        "latency_ms": elapsed_ms,
        "subscription_id": payload.get("id"),
        "subscription_name": payload.get("name"),
        "tenant_id": payload.get("tenantId"),
        "state": payload.get("state"),
        "user": payload.get("user", {}).get("name"),
        "auth_type": payload.get("user", {}).get("type"),
    }


def probe_via_sdk(subscription_id: str | None, timeout_sec: int) -> dict:
    """Read-only proof: DefaultAzureCredential + SubscriptionClient.list()."""
    try:
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.subscription import SubscriptionClient
    except ImportError as exc:
        return {
            "ok": False,
            "error": f"Missing Azure SDK package: {exc}",
            "hint": "pip install azure-identity azure-mgmt-resource",
        }

    start = time.perf_counter()
    try:
        cred = DefaultAzureCredential()
        sub_client = SubscriptionClient(cred)
        subs = list(sub_client.subscriptions.list())
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        if not subs:
            return {
                "ok": False,
                "error": "No subscriptions accessible with current credentials.",
                "latency_ms": elapsed_ms,
            }

        matched = None
        if subscription_id:
            for sub in subs:
                if sub.subscription_id == subscription_id:
                    matched = sub
                    break

        target = matched or subs[0]
        return {
            "ok": True,
            "latency_ms": elapsed_ms,
            "subscription_id": target.subscription_id,
            "subscription_name": target.display_name,
            "state": str(target.state),
            "total_accessible": len(subs),
            "requested_found": matched is not None if subscription_id else None,
        }
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        result = {"ok": False, "error": str(exc), "latency_ms": elapsed_ms}
        if "credential" in str(exc).lower() or "EnvironmentCredential" in str(exc):
            result["hint"] = "Run 'az login' so DefaultAzureCredential picks up the CLI token."
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Azure connection proof (no writes).")
    parser.add_argument("--subscription-id", help="Azure subscription ID override.")
    parser.add_argument("--tenant-id", help="Azure tenant ID override (informational).")
    parser.add_argument("--resource-group", help="Azure resource group override (informational).")
    parser.add_argument(
        "--mode",
        choices=["sdk", "cli", "both"],
        default="both",
        help="Which probe(s) to run. Default: both.",
    )
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to local env file with AZURE_* values.",
    )
    parser.add_argument("--timeout-sec", type=int, default=15, help="Per-probe timeout in seconds.")
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    subscription_id = first_non_empty(
        args.subscription_id,
        os.getenv("AZURE_SUBSCRIPTION_ID"),
        env_map.get("AZURE_SUBSCRIPTION_ID"),
    )
    tenant_id = first_non_empty(
        args.tenant_id,
        os.getenv("AZURE_TENANT_ID"),
        env_map.get("AZURE_TENANT_ID"),
    )
    resource_group = first_non_empty(
        args.resource_group,
        os.getenv("AZURE_RESOURCE_GROUP"),
        env_map.get("AZURE_RESOURCE_GROUP"),
    )

    az_cli = resolve_azure_cli()

    result: dict[str, object] = {
        "ok": False,
        "proof": "azure_read_only",
        "env_file_checked": str(env_file),
        "subscription_id_resolved": subscription_id,
        "tenant_id_resolved": tenant_id,
        "resource_group_resolved": resource_group,
        "az_cli": az_cli,
        "mode": args.mode,
    }

    cli_result: dict | None = None
    sdk_result: dict | None = None

    if args.mode in ("cli", "both"):
        if az_cli:
            cli_result = probe_via_cli(az_cli, subscription_id, args.timeout_sec)
        else:
            cli_result = {
                "ok": False,
                "error": "az CLI not found.",
                "hint": "Install Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows",
            }
        result["cli_probe"] = cli_result

    if args.mode in ("sdk", "both"):
        sdk_result = probe_via_sdk(subscription_id, args.timeout_sec)
        result["sdk_probe"] = sdk_result

    probes = [p for p in [cli_result, sdk_result] if p is not None]
    result["ok"] = any(p.get("ok") for p in probes) if probes else False

    if result["ok"]:
        successful = next((p for p in probes if p.get("ok")), None)
        if successful:
            result["subscription_id_confirmed"] = successful.get("subscription_id")
            result["subscription_name"] = successful.get("subscription_name")
            result["tenant_id_confirmed"] = successful.get("tenant_id")

    print(json.dumps(result, indent=2, default=str))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
