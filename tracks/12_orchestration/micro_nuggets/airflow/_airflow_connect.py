"""
Shared Airflow connection helper for all micro-nuggets.

Credential resolution order (first non-empty wins):
  1. Environment variables  AIRFLOW_*  (set by env_setter.ps1)
  2. _infra/env/.env.local
  3. Hardcoded defaults for local Docker dev

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _airflow_connect import get_creds, get_airflow_session, LAB_PREFIX

    session, base_url = get_airflow_session()
    resp = session.get(f"{base_url}/api/v1/health")
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# ── Lab namespace — all nugget DAGs/variables/connections use this prefix ─────
LAB_PREFIX = "lab_airflow"
LAB_OUTPUT_DIR = os.getenv("LAB_AIRFLOW_OUTPUT_DIR", "/tmp/airflow_lab")
LAB_POSTGRES_HOST = os.getenv("LAB_POSTGRES_HOST", "host.docker.internal")

_KEYS = [
    "AIRFLOW_HOST",
    "AIRFLOW_PORT",
    "AIRFLOW_USER",
    "AIRFLOW_PASSWORD",
]

_DEFAULTS = {
    "AIRFLOW_HOST": "localhost",
    "AIRFLOW_PORT": "8082",
    "AIRFLOW_USER": "airflow",
    "AIRFLOW_PASSWORD": "airflow",
}

# DAG IDs created by the lab
LAB_DAG_IDS = [
    f"{LAB_PREFIX}_taskflow_basics",
    f"{LAB_PREFIX}_python_bash_operators",
    f"{LAB_PREFIX}_xcom_demo",
    f"{LAB_PREFIX}_fan_in_fan_out",
    f"{LAB_PREFIX}_scheduling_demo",
    f"{LAB_PREFIX}_sensor_demo",
    f"{LAB_PREFIX}_retries_demo",
    f"{LAB_PREFIX}_etl_pattern",
    f"{LAB_PREFIX}_branching",
    f"{LAB_PREFIX}_capstone",
]

# Airflow Variables created by the lab
LAB_VARIABLES = {
    f"{LAB_PREFIX}_environment": "local",
    f"{LAB_PREFIX}_batch_size": "100",
    f"{LAB_PREFIX}_output_dir": LAB_OUTPUT_DIR,
    f"{LAB_PREFIX}_watermark": "2024-01-01",
}

# Airflow Connections created by the lab (non-secret, local only)
LAB_CONNECTIONS = {
    f"{LAB_PREFIX}_postgres": {
        "conn_type": "postgres",
        "host": LAB_POSTGRES_HOST,
        "port": 5432,
        "schema": "de_telemetry",
        "login": "de_admin",
        "description": "Lab PostgreSQL connection (StudyBook; host configurable via LAB_POSTGRES_HOST)",
    },
    f"{LAB_PREFIX}_filesystem": {
        "conn_type": "fs",
        "extra": f'{{"path": "{LAB_OUTPUT_DIR}"}}',
        "description": "Lab filesystem connection",
    },
}


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE env file (no shell expansion)."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def _first(*values: Optional[str]) -> Optional[str]:
    """Return first non-None, non-empty string."""
    for v in values:
        if v and str(v).strip():
            return str(v).strip()
    return None


def _find_project_root(start: Path) -> Optional[Path]:
    """Walk up from start until we find _infra directory."""
    for candidate in [start, *start.parents]:
        if (candidate / "_infra").exists():
            return candidate
    return None


def _pick_powershell() -> Optional[str]:
    """Find pwsh (PowerShell 7) or powershell (Windows PowerShell 5.1)."""
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


def _load_encrypted_secrets(project_root: Path) -> dict[str, str]:
    """
    Decrypt StudyBook .enc.json secret files via PowerShell.
    Returns {} on any failure so callers can fall through to next source.
    """
    pwsh = _pick_powershell()
    if not pwsh:
        return {}

    root_escaped = str(project_root).replace("'", "''")
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$WarningPreference = 'SilentlyContinue'
$projectRoot = '{root_escaped}'
$coreScript = Join-Path $projectRoot 'scripts\\env\\env_core.ps1'
if (-not (Test-Path -LiteralPath $coreScript)) {{ '{{}}'; exit 0 }}
. $coreScript
$machine = $env:STUDYBOOK_MACHINE
if ([string]::IsNullOrWhiteSpace($machine)) {{ $machine = $env:COMPUTERNAME }}
$machine = $machine.Trim().ToLowerInvariant() -replace '[^a-z0-9\\-_. ]','' -replace '[\\s_]+','-'
$secretFiles = @(
    (Join-Path $projectRoot 'config\\secrets\\shared.secrets.enc.json'),
    (Join-Path $projectRoot ("config\\secrets\\{{0}}.secrets.enc.json" -f $machine))
)
$passphrase = Get-SecretPassphrase -NonInteractive -ProjectRoot $projectRoot
if (-not $passphrase) {{ '{{}}'; exit 0 }}
$out = @{{}}
foreach ($f in $secretFiles) {{
    if (Test-Path -LiteralPath $f) {{
        try {{
            $raw = Unprotect-StudyBookSecretFile -EncryptedPath $f -Passphrase $passphrase
            if (-not [string]::IsNullOrWhiteSpace($raw)) {{
                $data = $raw | ConvertFrom-Json -AsHashtable
                foreach ($k in @('AIRFLOW_HOST','AIRFLOW_PORT','AIRFLOW_USER','AIRFLOW_PASSWORD')) {{
                    if ($data.ContainsKey($k)) {{ $out[$k] = [string]$data[$k] }}
                }}
            }}
        }} catch {{}}
    }}
}}
$out | ConvertTo-Json -Compress
""".strip()

    try:
        result = subprocess.run(
            [pwsh, "-NoProfile", "-Command", ps_script],
            capture_output=True, text=True, timeout=20, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return {}

    if result.returncode != 0:
        return {}

    for line in reversed(result.stdout.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
            if isinstance(parsed, dict):
                return {str(k): str(v) for k, v in parsed.items() if v is not None}
        except json.JSONDecodeError:
            continue
    return {}


def get_creds() -> dict[str, str]:
    """
    Return resolved Airflow credentials as a plain dict.
    Resolution order: env vars -> encrypted secrets -> .env.local -> defaults
    """
    project_root = _find_project_root(Path(__file__).resolve())
    env_file = (
        project_root / "_infra" / "env" / ".env.local"
        if project_root
        else Path("_infra/env/.env.local")
    )
    enc_map = _load_encrypted_secrets(project_root) if project_root else {}
    file_map = _load_env_file(env_file)

    result = {}
    for k in _KEYS:
        val = _first(os.getenv(k), enc_map.get(k), file_map.get(k), _DEFAULTS.get(k))
        result[k] = val or ""
    return result


def get_creds_source() -> str:
    """Return where primary AIRFLOW credentials are being resolved from."""
    project_root = _find_project_root(Path(__file__).resolve())
    env_file = (
        project_root / "_infra" / "env" / ".env.local"
        if project_root
        else Path("_infra/env/.env.local")
    )
    enc_map = _load_encrypted_secrets(project_root) if project_root else {}
    file_map = _load_env_file(env_file)

    if os.getenv("AIRFLOW_HOST"):
        return "environment_variables"
    if enc_map.get("AIRFLOW_HOST"):
        return "encrypted_secrets"
    if file_map.get("AIRFLOW_HOST"):
        return "env_file"
    return "defaults"


def get_base_url() -> str:
    """Return the Airflow webserver base URL."""
    creds = get_creds()
    host = creds.get("AIRFLOW_HOST", "localhost")
    port = creds.get("AIRFLOW_PORT", "8082")
    return f"http://{host}:{port}"


def get_airflow_session():
    """
    Return (requests.Session, base_url) authenticated for the Airflow REST API.

    Usage:
        session, base_url = get_airflow_session()
        resp = session.get(f"{base_url}/api/v1/health")
    """
    try:
        import requests  # type: ignore
    except ImportError:
        raise EnvironmentError(
            "Missing dependency: requests\n"
            "Fix: pip install requests"
        )

    creds = get_creds()
    user = creds.get("AIRFLOW_USER", "airflow")
    password = creds.get("AIRFLOW_PASSWORD", "airflow")
    base_url = get_base_url()

    session = requests.Session()
    session.auth = (user, password)
    session.headers.update({"Content-Type": "application/json"})
    return session, base_url


def check_airflow_reachable(timeout: int = 10) -> tuple[bool, str]:
    """
    Probe Airflow API endpoints with fallback logic.
    Returns (reachable: bool, version_or_error: str).
    """
    try:
        session, base_url = get_airflow_session()

        # Primary probe
        resp = session.get(f"{base_url}/api/v1/version", timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            version = data.get("version", "unknown")
            return True, version

        # Fallback probe for deployments that gate /version differently
        health = session.get(f"{base_url}/api/v1/health", timeout=timeout)
        if health.status_code == 200:
            return True, "unknown"

        return False, f"HTTP {resp.status_code} (version), HTTP {health.status_code} (health)"
    except Exception as e:
        return False, str(e)


def trigger_dag(dag_id: str, conf: Optional[dict] = None) -> dict:
    """Trigger a DAG run via REST API. Returns the run response dict."""
    session, base_url = get_airflow_session()
    payload = {"conf": conf or {}}
    resp = session.post(
        f"{base_url}/api/v1/dags/{dag_id}/dagRuns",
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()


def get_dag_runs(dag_id: str, limit: int = 5) -> list:
    """Return recent DAG runs for the given dag_id."""
    session, base_url = get_airflow_session()
    resp = session.get(
        f"{base_url}/api/v1/dags/{dag_id}/dagRuns",
        params={"limit": limit, "order_by": "-execution_date"},
    )
    resp.raise_for_status()
    return resp.json().get("dag_runs", [])


def get_variables() -> dict[str, str]:
    """Return all Airflow Variables as {key: value} dict."""
    session, base_url = get_airflow_session()
    resp = session.get(f"{base_url}/api/v1/variables", params={"limit": 200})
    resp.raise_for_status()
    return {v["key"]: v["value"] for v in resp.json().get("variables", [])}


def set_variable(key: str, value: str) -> None:
    """Create or update an Airflow Variable."""
    session, base_url = get_airflow_session()
    # Try PATCH first (update), fall back to POST (create)
    resp = session.patch(
        f"{base_url}/api/v1/variables/{key}",
        json={"key": key, "value": value},
    )
    if resp.status_code == 404:
        resp = session.post(
            f"{base_url}/api/v1/variables",
            json={"key": key, "value": value},
        )
    resp.raise_for_status()


def delete_variable(key: str) -> None:
    """Delete an Airflow Variable (ignores 404)."""
    session, base_url = get_airflow_session()
    resp = session.delete(f"{base_url}/api/v1/variables/{key}")
    if resp.status_code not in (200, 204, 404):
        resp.raise_for_status()


def get_connections() -> list[dict]:
    """Return all Airflow Connections."""
    session, base_url = get_airflow_session()
    resp = session.get(f"{base_url}/api/v1/connections", params={"limit": 200})
    resp.raise_for_status()
    return resp.json().get("connections", [])


def upsert_connection(conn_id: str, conn_body: dict) -> None:
    """Create or update an Airflow Connection."""
    session, base_url = get_airflow_session()
    body = {"connection_id": conn_id, **conn_body}
    # Try PATCH first, then POST
    resp = session.patch(f"{base_url}/api/v1/connections/{conn_id}", json=body)
    if resp.status_code == 404:
        resp = session.post(f"{base_url}/api/v1/connections", json=body)
    resp.raise_for_status()


def delete_connection(conn_id: str) -> None:
    """Delete an Airflow Connection (ignores 404)."""
    session, base_url = get_airflow_session()
    resp = session.delete(f"{base_url}/api/v1/connections/{conn_id}")
    if resp.status_code not in (200, 204, 404):
        resp.raise_for_status()
