"""
Shared Databricks connection helper for all micro-nuggets.

Credential resolution order (first non-empty wins):
  1. Environment variables  DATABRICKS_*      (set by env_setter.ps1)
  2. Encrypted secrets file                   (StudyBook secrets system)
  3. D:\\StudyBook\\_infra\\env\\.env.local

Sources 1 and 3 require no external calls.
Source 2 shells out to PowerShell to decrypt the project's .enc.json files —
the same mechanism used by the connection proof in poc/connection_proofs/.

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _db_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
    conn.close()
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# ── Lab constants ─────────────────────────────────────────────────────────────
# Every nugget targets this Unity Catalog catalog and schema.
# Created by 01_workspace_and_catalog/01_create_catalog_schema.py — run that first.
# Default is 'workspace' because it exists on all Databricks workspaces.
# The nugget script creates 'nugget_lab' as a dedicated study catalog.
LAB_CATALOG = "nugget_lab"
LAB_SCHEMA = "default"

_ENV_FILE = Path(r"D:\StudyBook\_infra\env\.env.local")

_KEYS = [
    "DATABRICKS_HOST",
    "DATABRICKS_TOKEN",
    "DATABRICKS_HTTP_PATH",
]


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
    """Walk up from start until we find CONTROL_PROTOCOL.md."""
    for candidate in [start, *start.parents]:
        if (candidate / "CONTROL_PROTOCOL.md").exists():
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
    Decrypt the StudyBook .enc.json secret files via PowerShell and return
    a dict of DATABRICKS_* values found inside them.  Returns {} on any failure
    so callers can silently fall through to the next credential source.
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
                foreach ($k in @('DATABRICKS_HOST','DATABRICKS_TOKEN','DATABRICKS_HTTP_PATH')) {{
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

    # The script may print warnings before the JSON line — grab the last valid JSON object
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


def get_creds() -> dict[str, str | None]:
    """
    Return resolved Databricks credentials as a plain dict.
    Resolution order: env vars → encrypted secrets → .env.local
    """
    # Source 2: encrypted secrets (only attempt if project root is found)
    project_root = _find_project_root(Path(__file__).resolve())
    enc_map = _load_encrypted_secrets(project_root) if project_root else {}

    # Source 3: plain .env.local file
    file_map = _load_env_file(_ENV_FILE)

    return {
        k: _first(os.getenv(k), enc_map.get(k), file_map.get(k))
        for k in _KEYS
    }


def _discover_http_path(host: str, token: str) -> Optional[str]:
    """
    Best-effort auto-discovery of SQL warehouse HTTP path.
    Returns '/sql/1.0/warehouses/<id>' when a warehouse is found.
    """
    try:
        import requests  # type: ignore
    except ImportError:
        return None

    clean_host = host.strip().rstrip("/")
    if not clean_host.startswith("http://") and not clean_host.startswith("https://"):
        clean_host = f"https://{clean_host}"

    headers = {"Authorization": f"Bearer {token}"}
    urls = [
        f"{clean_host}/api/2.0/sql/warehouses",
        f"{clean_host}/api/2.0/sql/endpoints",
    ]

    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if not resp.ok:
                continue
            payload = resp.json()
            if not isinstance(payload, dict):
                continue

            items = []
            for key in ("warehouses", "endpoints"):
                value = payload.get(key)
                if isinstance(value, list):
                    items = value
                    break
            if not items:
                continue

            # Prefer running warehouse/endpoint, else first available
            chosen = None
            for item in items:
                state = str(item.get("state") or item.get("status") or "").upper()
                if "RUNNING" in state:
                    chosen = item
                    break
            if chosen is None:
                chosen = items[0]

            warehouse_id = (
                chosen.get("id")
                or chosen.get("warehouse_id")
                or chosen.get("endpoint_id")
            )
            if warehouse_id:
                return f"/sql/1.0/warehouses/{warehouse_id}"
        except Exception:
            continue

    return None


def get_connection(_bootstrap: bool = False, **overrides):
    """
    Open and return a databricks.sql.Connection.

    Normal mode (default):
        Connects to LAB_CATALOG / LAB_SCHEMA — the nugget study workspace.
        Ignores the catalog/schema in your credentials; always targets
        nugget_lab.default so nuggets work regardless of what's in your secrets.

    Bootstrap mode (_bootstrap=True):
        Connects at hive_metastore level (no catalog/schema) so that
        00_prereq_check.py can CREATE CATALOG nugget_lab freely.
        Only 00_prereq_check.py should pass _bootstrap=True.

    Any keyword argument overrides a resolved value, e.g.:
        conn = get_connection(catalog="sandbox")
    """
    try:
        import databricks.sql  # type: ignore
    except ImportError:
        raise EnvironmentError(
            "Missing dependency: databricks-sql-connector\n"
            "Fix: pip install databricks-sql-connector"
        )

    creds = get_creds()

    host  = overrides.pop("host",  creds.get("DATABRICKS_HOST"))
    token = overrides.pop("token", creds.get("DATABRICKS_TOKEN"))
    http_path = overrides.pop("http_path", creds.get("DATABRICKS_HTTP_PATH"))

    # SQL connector needs an HTTP path to a SQL warehouse.
    # If not provided, try best-effort auto-discovery via REST API.
    if not http_path and host and token:
        http_path = _discover_http_path(str(host), str(token))

    missing = [
        k for k, v in {"host": host, "token": token, "http_path": http_path}.items() if not v
    ]
    if missing:
        raise EnvironmentError(
            f"Missing Databricks credentials: {missing}\n"
            f"Fix:\n"
            f"  0. Auto-discovery already attempted for HTTP path and found none.\n"
            f"  1. Open Databricks UI → SQL Warehouses → your warehouse → Connection Details\n"
            f"  2. Copy the HTTP Path (looks like: /sql/1.0/warehouses/<id>)\n"
            f"  3. Add to encrypted secrets:\n"
            f"     .\\scripts\\env\\set_secret.ps1 -Machine asuspc -PromptSecretKey DATABRICKS_HTTP_PATH\n"
            f"  4. Or add to _infra/env/.env.local:\n"
            f"     DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/<your-warehouse-id>"
        )

    kwargs: dict = dict(
        server_hostname=host.replace("https://", ""),
        access_token=token,
        http_path=http_path,
        **overrides,
    )

    # Bootstrap connects without catalog/schema so it can CREATE CATALOG.
    # All other nuggets always target LAB_CATALOG / LAB_SCHEMA — stable, predictable.
    if not _bootstrap:
        kwargs["catalog"] = overrides.pop("catalog", LAB_CATALOG)
        kwargs["schema"]  = overrides.pop("schema",  LAB_SCHEMA)

    return databricks.sql.connect(**kwargs)


def get_workspace_info():
    """
    Return a dict with workspace metadata (host, user, org, etc.)
    Uses the REST API — useful for diagnostics and connection proofs.
    """
    import requests  # type: ignore

    creds = get_creds()
    host  = creds.get("DATABRICKS_HOST", "").replace("https://", "")
    token = creds.get("DATABRICKS_TOKEN", "")

    if not host or not token:
        return {}

    headers = {"Authorization": f"Bearer {token}"}

    # Some Databricks workspaces (especially certain editions/configurations)
    # do not expose /api/2.0/current-user/me and return ENDPOINT_NOT_FOUND.
    # Treat clusters/list as an auth + workspace reachability fallback probe.
    probes = [
        ("current-user/me", f"https://{host}/api/2.0/current-user/me"),
        ("clusters/list", f"https://{host}/api/2.0/clusters/list"),
    ]

    for probe_name, url in probes:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if not resp.ok:
                continue
            payload = resp.json()
            if probe_name == "current-user/me":
                payload["_probe"] = probe_name
                return payload
            return {
                "_probe": probe_name,
                "active": True,
                "workspace_reachable": True,
                "cluster_count": len(payload.get("clusters", [])) if isinstance(payload, dict) else None,
            }
        except Exception:
            continue

    return {}
