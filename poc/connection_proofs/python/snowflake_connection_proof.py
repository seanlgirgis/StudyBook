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


def find_project_root(start_path: Path) -> Path | None:
    for candidate in [start_path, *start_path.parents]:
        if (candidate / "CONTROL_PROTOCOL.md").exists():
            return candidate
    return None


def pick_powershell_exe() -> str | None:
    for name in ("pwsh", "powershell"):
        found = shutil.which(name)
        if found:
            return found

    for known in (
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    ):
        if Path(known).exists():
            return known
    return None


def parse_json_object_from_stdout(stdout: str) -> dict[str, str]:
    if not stdout:
        return {}

    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    for line in reversed(lines):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items() if v is not None}
    return {}


def load_snowflake_secrets_from_encrypted(project_root: Path, timeout_sec: int) -> dict[str, str]:
    pwsh_exe = pick_powershell_exe()
    if not pwsh_exe:
        return {}

    project_root_escaped = str(project_root).replace("'", "''")
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$WarningPreference = 'SilentlyContinue'
$projectRoot = '{project_root_escaped}'
$coreScript = Join-Path $projectRoot 'scripts\\env\\env_core.ps1'
if (-not (Test-Path -LiteralPath $coreScript)) {{
    '{{}}'
    exit 0
}}
. $coreScript
$machine = $env:STUDYBOOK_MACHINE
if ([string]::IsNullOrWhiteSpace($machine)) {{
    $machine = $env:COMPUTERNAME
}}
$machine = $machine.Trim().ToLowerInvariant()
$machine = $machine -replace '[^a-z0-9\\-_. ]', ''
$machine = $machine -replace '[\\s_]+', '-'
$secretFiles = @(
    (Join-Path $projectRoot 'config\\secrets\\shared.secrets.enc.json'),
    (Join-Path $projectRoot ("config\\secrets\\{{0}}.secrets.enc.json" -f $machine))
)
$passphrase = Get-SecretPassphrase -NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {{
    '{{}}'
    exit 0
}}
$out = @{{}}
foreach ($secretFile in $secretFiles) {{
    if (Test-Path -LiteralPath $secretFile) {{
        try {{
            $raw = Unprotect-StudyBookSecretFile -EncryptedPath $secretFile -Passphrase $passphrase
            if (-not [string]::IsNullOrWhiteSpace($raw)) {{
                $data = $raw | ConvertFrom-Json -AsHashtable
                foreach($k in @('SNOWFLAKE_ACCOUNT','SNOWFLAKE_USER','SNOWFLAKE_PASSWORD','SNOWFLAKE_ROLE','SNOWFLAKE_WAREHOUSE','SNOWFLAKE_DATABASE','SNOWFLAKE_SCHEMA')) {{
                    if ($data.ContainsKey($k)) {{
                        $out[$k] = [string]$data[$k]
                    }}
                }}
            }}
        }} catch {{}}
    }}
}}
$out | ConvertTo-Json -Compress
""".strip()

    try:
        completed = subprocess.run(
            [pwsh_exe, "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=max(timeout_sec, 3),
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {}

    if completed.returncode != 0:
        return {}

    parsed = parse_json_object_from_stdout(completed.stdout)
    out: dict[str, str] = {}
    for key in (
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ROLE",
        "SNOWFLAKE_WAREHOUSE",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
    ):
        value = parsed.get(key)
        if value and value.strip():
            out[key] = value.strip()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Snowflake connection proof.")
    parser.add_argument("--account")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--role")
    parser.add_argument("--warehouse")
    parser.add_argument("--database")
    parser.add_argument("--schema")
    parser.add_argument("--query", default=(
        "SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_ROLE(), "
        "CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_REGION()"
    ))
    parser.add_argument("--timeout-sec", type=int, default=20)
    parser.add_argument(
        "--env-file",
        default=r"D:\StudyBook\_infra\env\.env.local",
        help="Path to env file with SNOWFLAKE_* values.",
    )
    args = parser.parse_args()

    env_file = Path(args.env_file)
    env_map = load_env_file(env_file)

    project_root = find_project_root(Path(__file__).resolve())
    enc_map = load_snowflake_secrets_from_encrypted(project_root, args.timeout_sec) if project_root else {}

    account = first_non_empty(args.account, os.getenv("SNOWFLAKE_ACCOUNT"), enc_map.get("SNOWFLAKE_ACCOUNT"), env_map.get("SNOWFLAKE_ACCOUNT"))
    user = first_non_empty(args.user, os.getenv("SNOWFLAKE_USER"), enc_map.get("SNOWFLAKE_USER"), env_map.get("SNOWFLAKE_USER"))
    password = first_non_empty(args.password, os.getenv("SNOWFLAKE_PASSWORD"), enc_map.get("SNOWFLAKE_PASSWORD"), env_map.get("SNOWFLAKE_PASSWORD"))
    role = first_non_empty(args.role, os.getenv("SNOWFLAKE_ROLE"), enc_map.get("SNOWFLAKE_ROLE"), env_map.get("SNOWFLAKE_ROLE"))
    warehouse = first_non_empty(args.warehouse, os.getenv("SNOWFLAKE_WAREHOUSE"), enc_map.get("SNOWFLAKE_WAREHOUSE"), env_map.get("SNOWFLAKE_WAREHOUSE"))
    database = first_non_empty(args.database, os.getenv("SNOWFLAKE_DATABASE"), enc_map.get("SNOWFLAKE_DATABASE"), env_map.get("SNOWFLAKE_DATABASE"))
    schema = first_non_empty(args.schema, os.getenv("SNOWFLAKE_SCHEMA"), enc_map.get("SNOWFLAKE_SCHEMA"), env_map.get("SNOWFLAKE_SCHEMA"))

    result: dict[str, object] = {
        "ok": False,
        "proof": "snowflake_read_only",
        "env_file_checked": str(env_file),
        "project_root_detected": str(project_root) if project_root else None,
        "encrypted_secret_keys_loaded": sorted([k for k, v in enc_map.items() if bool(v)]),
        "account_resolved": account,
        "user_resolved": user,
        "password_present": bool(password),
        "role_resolved": role,
        "warehouse_resolved": warehouse,
        "database_resolved": database,
        "schema_resolved": schema,
        "query": args.query,
    }

    required = {
        "SNOWFLAKE_ACCOUNT": account,
        "SNOWFLAKE_USER": user,
        "SNOWFLAKE_PASSWORD": password,
        "SNOWFLAKE_WAREHOUSE": warehouse,
        "SNOWFLAKE_DATABASE": database,
        "SNOWFLAKE_SCHEMA": schema,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        result["error"] = f"Missing required Snowflake settings: {', '.join(missing)}"
        print(json.dumps(result, indent=2))
        return 2

    try:
        import snowflake.connector
    except ImportError:
        result["error"] = "Missing dependency: snowflake-connector-python"
        result["hint"] = "Install with: pip install snowflake-connector-python"
        print(json.dumps(result, indent=2))
        return 2

    connect_kwargs = {
        "account": account,
        "user": user,
        "password": password,
        "warehouse": warehouse,
        "database": database,
        "schema": schema,
        "login_timeout": max(args.timeout_sec, 5),
        "network_timeout": max(args.timeout_sec, 5),
    }
    if role:
        connect_kwargs["role"] = role

    start = time.perf_counter()
    try:
        conn = snowflake.connector.connect(**connect_kwargs)
        try:
            with conn.cursor() as cur:
                cur.execute(args.query)
                row = cur.fetchone()
                cols = [d[0] for d in cur.description] if cur.description else []
        finally:
            conn.close()
    except Exception as exc:  # noqa: BLE001
        result["latency_ms"] = int((time.perf_counter() - start) * 1000)
        result["error"] = str(exc)
        print(json.dumps(result, indent=2, default=str))
        return 1

    result["latency_ms"] = int((time.perf_counter() - start) * 1000)
    result["ok"] = True
    result["result_columns"] = cols
    result["result_row"] = row
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
