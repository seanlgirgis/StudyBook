"""
Shared MongoDB connection helper for all micro-nuggets.

Credential resolution order (first non-empty wins):
  1. Environment variables  MONGODB_*        (set by env_setter.ps1)
  2. Encrypted secrets file                  (StudyBook secrets system)
  3. D:\\StudyBook\\_infra\\env\\.env.local

Sources 1 and 3 require no external calls.
Source 2 shells out to PowerShell to decrypt the project's .enc.json files —
the same mechanism used by the connection proof in poc/connection_proofs/.

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _mg_connect import get_client, get_lab_db, LAB_DB

    client = get_client()
    db     = get_lab_db()          # shortcut: client[LAB_DB]
    col    = db["my_collection"]
    col.find_one({})
    client.close()

MongoDB connection model vs SQL:
  - MongoClient is a connection POOL, not a single socket.
    It is thread-safe and meant to be shared (create once, reuse everywhere).
  - Unlike Snowflake/Databricks, there is no "cursor" in the SQL sense.
    Instead you work with Collection objects that return Cursor iterators.
  - client[db_name][collection_name] is the idiomatic access pattern.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ── UTF-8 stdout ──────────────────────────────────────────────────────────────
# Box-drawing characters in nugget headers require UTF-8 output encoding.
# Windows console defaults to cp1252 — reconfigure once here at import time.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import certifi
from pymongo import MongoClient
from pymongo.database import Database

# ── Lab constants ─────────────────────────────────────────────────────────────
# Every nugget creates/uses collections inside this database.
# A dedicated lab database keeps experiments isolated from de_telemetry.
LAB_DB = "nugget_lab"

_ENV_FILE = Path(r"D:\StudyBook\_infra\env\.env.local")

_KEYS = [
    "MONGODB_URI",
    "MONGODB_HOST",
    "MONGODB_USER",
    "MONGODB_PASSWORD",
    "MONGODB_DATABASE",
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
    Decrypt StudyBook .enc.json files via PowerShell and return MONGODB_* keys.
    Returns {} on any failure so callers fall through to the next source.
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
                foreach ($k in @('MONGODB_URI','MONGODB_HOST','MONGODB_USER',
                                  'MONGODB_PASSWORD','MONGODB_DATABASE')) {{
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


def get_creds() -> dict[str, str | None]:
    """
    Return resolved MongoDB credentials.
    Resolution order: env vars → encrypted secrets → .env.local
    """
    project_root = _find_project_root(Path(__file__).resolve())
    enc_map = _load_encrypted_secrets(project_root) if project_root else {}
    file_map = _load_env_file(_ENV_FILE)

    return {
        k: _first(os.getenv(k), enc_map.get(k), file_map.get(k))
        for k in _KEYS
    }


def _build_uri(creds: dict[str, str | None], cli_uri: str | None = None) -> str:
    """
    Build a MongoDB connection URI from credentials.

    Priority:
      1. cli_uri (explicit override)
      2. MONGODB_URI (full URI already stored as a secret)
      3. Constructed from MONGODB_HOST + USER + PASSWORD

    URI formats:
      mongodb://user:pass@host:port/database          ← standalone / replica set
      mongodb+srv://user:pass@cluster.mongodb.net/db  ← Atlas SRV (DNS-based)

    SRV format (mongodb+srv://) is the modern Atlas default:
      - No port needed — DNS SRV records resolve the cluster topology.
      - Supports automatic failover and read preference routing.
      - Requires retryWrites=true (default in pymongo 4+) and w=majority.
    """
    uri = _first(cli_uri, creds.get("MONGODB_URI"))
    if uri:
        return uri

    host = creds.get("MONGODB_HOST")
    user = creds.get("MONGODB_USER")
    password = creds.get("MONGODB_PASSWORD")
    database = _first(creds.get("MONGODB_DATABASE"), "admin")

    if not host:
        raise EnvironmentError(
            "Missing MongoDB connection details.\n"
            "Provide MONGODB_URI or MONGODB_HOST in env vars / .env.local / encrypted secrets.\n"
            r"Fix: run  . D:\StudyBook\env_setter.ps1  then retry."
        )

    # If host is already a full URI, use it directly.
    if host.startswith("mongodb://") or host.startswith("mongodb+srv://"):
        return host

    if user and password:
        # SRV cluster (no port in host) vs standalone (host:port)
        if ":" in host:
            return f"mongodb://{user}:{password}@{host}/{database}"
        return f"mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true&w=majority"

    if ":" in host:
        return f"mongodb://{host}/{database}"
    return f"mongodb+srv://{host}/{database}?retryWrites=true&w=majority"


def get_client(**overrides) -> MongoClient:
    """
    Build and return a MongoClient connected to Atlas (or any MongoDB host).

    TLS / certifi:
      Atlas always requires TLS. We pass certifi's CA bundle so the driver
      validates the server certificate against trusted roots — same approach
      as the connection proof in poc/connection_proofs/python/.

    serverSelectionTimeoutMS:
      How long the driver tries to find a suitable server before raising
      ServerSelectionTimeoutError. 8 s is comfortable for Atlas cold connections
      (first DNS SRV resolution + TLS handshake).

    MongoClient is a CONNECTION POOL:
      - Thread-safe. Create once per process.
      - Pool size defaults to 100 (maxPoolSize=100).
      - Connections are created lazily on first use.
      - Call client.close() at program exit to drain the pool cleanly.

    Any keyword argument overrides a driver option, e.g.:
        client = get_client(maxPoolSize=5, w="majority")
    """
    creds = get_creds()
    uri = _build_uri(creds, overrides.pop("uri", None))

    needs_tls = uri.startswith("mongodb+srv://") or ".mongodb.net" in uri

    kwargs: dict = dict(
        serverSelectionTimeoutMS=overrides.pop("serverSelectionTimeoutMS", 8_000),
        **overrides,
    )
    if needs_tls:
        kwargs.setdefault("tls", True)
        kwargs.setdefault("tlsCAFile", certifi.where())

    return MongoClient(uri, **kwargs)


def get_lab_db(**client_overrides) -> Database:
    """
    Return the lab Database object (client[LAB_DB]).

    Convenience wrapper — most nuggets only need a Database handle.
    The underlying MongoClient is NOT tracked here; call client.close()
    yourself if you need explicit cleanup (most short scripts can skip it).

    Pattern:
        db  = get_lab_db()
        col = db["my_collection"]
        col.insert_one({"key": "value"})
    """
    client = get_client(**client_overrides)
    return client[LAB_DB]
