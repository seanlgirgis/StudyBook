"""
Shared PostgreSQL connection helper for all micro-nuggets.

Credential resolution order (first non-empty wins):
  1. Environment variables  POSTGRES_*       (set by env_setter.ps1)
  2. _infra/env/.env.local
  3. Hardcoded defaults for local Docker dev

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _pg_connect import get_connection, LAB_SCHEMA

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

# ── Lab schema — all nuggets create objects here ──────────────────────────────
LAB_SCHEMA = "de_lab"

_KEYS = [
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
]

# Sensible defaults for local Docker PostgreSQL
_DEFAULTS = {
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
    "POSTGRES_USER": "de_admin",
    "POSTGRES_DB": "de_telemetry",
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
    a dict of POSTGRES_* values found inside them.  Returns {} on any failure
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
                foreach ($k in @('POSTGRES_HOST','POSTGRES_PORT','POSTGRES_USER',
                                  'POSTGRES_PASSWORD','POSTGRES_DB')) {{
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
    Return resolved PostgreSQL credentials as a plain dict.
    Resolution order: env vars → encrypted secrets → .env.local → defaults
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
    """
    Return where primary POSTGRES credentials are being resolved from.
    """
    project_root = _find_project_root(Path(__file__).resolve())
    env_file = (
        project_root / "_infra" / "env" / ".env.local"
        if project_root
        else Path("_infra/env/.env.local")
    )
    enc_map = _load_encrypted_secrets(project_root) if project_root else {}
    file_map = _load_env_file(env_file)

    if os.getenv("POSTGRES_HOST"):
        return "environment_variables"
    if enc_map.get("POSTGRES_HOST"):
        return "encrypted_secrets"
    if file_map.get("POSTGRES_HOST"):
        return "env_file"
    if _DEFAULTS.get("POSTGRES_HOST"):
        return "defaults"
    return "unknown"


def get_connection(dbname: Optional[str] = None, **overrides):
    """
    Open and return a psycopg2 connection.

    Normal mode (default):
        Connects to POSTGRES_DB and targets LAB_SCHEMA for all objects.

    Any keyword argument overrides a resolved value, e.g.:
        conn = get_connection(dbname="postgres")
    """
    try:
        import psycopg2  # type: ignore
        import psycopg2.extras  # type: ignore
    except ImportError:
        raise EnvironmentError(
            "Missing dependency: psycopg2-binary\n"
            "Fix: pip install psycopg2-binary"
        )

    creds = get_creds()

    host     = overrides.pop("host",     creds.get("POSTGRES_HOST"))
    port     = overrides.pop("port",     creds.get("POSTGRES_PORT"))
    user     = overrides.pop("user",     creds.get("POSTGRES_USER"))
    password = overrides.pop("password", creds.get("POSTGRES_PASSWORD"))
    dbname   = overrides.pop("dbname",   dbname or creds.get("POSTGRES_DB"))

    missing = [
        k for k, v in {"host": host, "port": port, "user": user,
                        "password": password, "dbname": dbname}.items() if not v
    ]
    if missing:
        raise EnvironmentError(
            f"Missing PostgreSQL credentials: {missing}\n"
            f"Fix: ensure POSTGRES_* vars are set in _infra/env/.env.local\n"
            f"     or start the Docker stack: .\\_infra\\scripts\\infra_up.ps1"
        )

    return psycopg2.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        dbname=dbname,
        **overrides,
    )


def ensure_lab_schema(conn):
    """
    Create the LAB_SCHEMA if it doesn't exist.
    Call this at the start of every nugget that creates objects.
    """
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {LAB_SCHEMA}")
        conn.commit()
