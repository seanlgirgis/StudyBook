"""
Shared Snowflake connection helper for all micro-nuggets.

Credential resolution order (first non-empty wins):
  1. Environment variables  SNOWFLAKE_*       (set by env_setter.ps1)
  2. Encrypted secrets file                   (StudyBook secrets system)
  3. D:\\StudyBook\\_infra\\env\\.env.local

Sources 1 and 3 require no external calls.
Source 2 shells out to PowerShell to decrypt the project's .enc.json files —
the same mechanism used by the connection proof in poc/connection_proofs/.

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _sf_connect import get_connection

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
# Every nugget targets this database and schema.
# Created by 00_setup/00_bootstrap.py — run that first.
LAB_DB     = "NUGGET_LAB"
LAB_SCHEMA = "PUBLIC"

_ENV_FILE = Path(r"D:\StudyBook\_infra\env\.env.local")

_KEYS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_SCHEMA",
]


# ── helpers ───────────────────────────────────────────────────────────────────

def _load_env_file(path: Path) -> dict[str, str]:
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
    a dict of SNOWFLAKE_* values found inside them.  Returns {} on any failure
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
                foreach ($k in @('SNOWFLAKE_ACCOUNT','SNOWFLAKE_USER','SNOWFLAKE_PASSWORD',
                                  'SNOWFLAKE_ROLE','SNOWFLAKE_WAREHOUSE',
                                  'SNOWFLAKE_DATABASE','SNOWFLAKE_SCHEMA')) {{
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
    Return resolved Snowflake credentials as a plain dict.
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


def get_connection(_bootstrap: bool = False, **overrides):
    """
    Open and return a snowflake.connector.SnowflakeConnection.

    Normal mode (default):
        Connects to LAB_DB / LAB_SCHEMA — the nugget study workspace.
        Ignores the database/schema in your credentials; always targets
        NUGGET_LAB so nuggets work regardless of what's in your secrets file.

    Bootstrap mode (_bootstrap=True):
        Connects at account level (no database/schema) so that
        00_bootstrap.py can CREATE DATABASE NUGGET_LAB freely.
        Only 00_bootstrap.py should pass _bootstrap=True.

    Any keyword argument overrides a resolved value, e.g.:
        conn = get_connection(warehouse="COMPUTE_WH_XL")
    """
    import snowflake.connector  # type: ignore

    creds = get_creds()

    account   = overrides.pop("account",   creds.get("SNOWFLAKE_ACCOUNT"))
    user      = overrides.pop("user",      creds.get("SNOWFLAKE_USER"))
    password  = overrides.pop("password",  creds.get("SNOWFLAKE_PASSWORD"))
    role      = overrides.pop("role",      creds.get("SNOWFLAKE_ROLE"))
    warehouse = overrides.pop("warehouse", creds.get("SNOWFLAKE_WAREHOUSE"))

    # Bootstrap connects without a database so it can create NUGGET_LAB.
    # All other nuggets always target LAB_DB / LAB_SCHEMA — stable, predictable.
    if _bootstrap:
        database = None
        schema   = None
    else:
        database = overrides.pop("database", LAB_DB)
        schema   = overrides.pop("schema",   LAB_SCHEMA)

    missing = [
        k for k, v in {
            "account": account, "user": user, "password": password,
            "warehouse": warehouse,
        }.items()
        if not v
    ]
    if missing:
        raise EnvironmentError(
            f"Missing Snowflake credentials: {missing}\n"
            r"Fix: run  . D:\StudyBook\env_setter.ps1  then retry."
        )

    kwargs: dict = dict(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        **overrides,
    )
    if role:
        kwargs["role"] = role
    if database:
        kwargs["database"] = database
    if schema:
        kwargs["schema"] = schema

    return snowflake.connector.connect(**kwargs)
