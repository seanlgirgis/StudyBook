from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

try:
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
except ImportError:  # pragma: no cover
    padding = None
    Cipher = None

from _env_loader import first_non_empty, load_env_file


DPAPI_ENTROPY = b"StudyBook.SecretSeed.v1"


class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_byte)),
    ]


def _bytes_to_blob(data: bytes) -> tuple[DATA_BLOB, ctypes.Array[ctypes.c_char]]:
    buf = ctypes.create_string_buffer(data, len(data))
    blob = DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))
    return blob, buf


def dpapi_unprotect(ciphertext: bytes, entropy: bytes | None = None) -> bytes:
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32

    in_blob, in_buf = _bytes_to_blob(ciphertext)
    ent_blob_ptr = None
    ent_buf = None
    if entropy:
        ent_blob, ent_buf = _bytes_to_blob(entropy)
        ent_blob_ptr = ctypes.byref(ent_blob)

    out_blob = DATA_BLOB()
    if not crypt32.CryptUnprotectData(
        ctypes.byref(in_blob),
        None,
        ent_blob_ptr,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise ctypes.WinError()

    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        if out_blob.pbData:
            kernel32.LocalFree(out_blob.pbData)


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


def normalize_machine_name(name: str | None) -> str:
    base = (name or "").strip().lower()
    base = re.sub(r"[^a-z0-9\-_. ]", "", base)
    base = re.sub(r"[\s_]+", "-", base)
    return base


def find_project_root(start_path: Path) -> Path | None:
    for candidate in [start_path, *start_path.parents]:
        if (candidate / "CONTROL_PROTOCOL.md").exists():
            return candidate
    return None


def resolve_seed_path(project_root: Path) -> Path:
    env_seed = os.getenv("STUDYBOOK_SECRET_SEED_PATH")
    if env_seed:
        expanded = Path(os.path.expandvars(env_seed))
        if expanded.is_absolute():
            return expanded
        return (project_root / expanded).resolve()
    return (project_root / "config" / "secrets" / ".local" / "studybook.secret.seed.dpapi.json").resolve()


def decrypt_secret_payload(payload: dict[str, object], passphrase: str) -> dict[str, str]:
    if padding is None or Cipher is None:
        return {}

    try:
        salt = base64.b64decode(str(payload.get("salt", "")))
        iv = base64.b64decode(str(payload.get("iv", "")))
        ciphertext = base64.b64decode(str(payload.get("ciphertext", "")))
        iterations = int(payload.get("iterations", 150000))
    except Exception:
        return {}

    if not salt or not iv or not ciphertext or not passphrase:
        return {}

    key = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, iterations, dklen=32)

    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded_plain = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain_bytes = unpadder.update(padded_plain) + unpadder.finalize()

    try:
        data = json.loads(plain_bytes.decode("utf-8"))
    except Exception:
        return {}

    if not isinstance(data, dict):
        return {}

    out: dict[str, str] = {}
    for key_name, value in data.items():
        if value is None:
            continue
        out[str(key_name)] = str(value)
    return out


def load_databricks_secrets_python(project_root: Path) -> tuple[dict[str, str], str | None]:
    try:
        passphrase = os.getenv("STUDYBOOK_SECRET_PASSPHRASE")
        if not passphrase:
            seed_path = resolve_seed_path(project_root)
            if seed_path.exists():
                seed_payload = json.loads(seed_path.read_text(encoding="utf-8"))
                ciphertext_b64 = str(seed_payload.get("ciphertext", ""))
                if ciphertext_b64:
                    seed_cipher = base64.b64decode(ciphertext_b64)
                    passphrase = dpapi_unprotect(seed_cipher, DPAPI_ENTROPY).decode("utf-8")

        if not passphrase:
            return {}, "no_passphrase_source"

        machine = normalize_machine_name(os.getenv("STUDYBOOK_MACHINE") or os.getenv("COMPUTERNAME"))
        secret_files = [
            project_root / "config" / "secrets" / "shared.secrets.enc.json",
            project_root / "config" / "secrets" / f"{machine}.secrets.enc.json",
        ]

        merged: dict[str, str] = {}
        for secret_file in secret_files:
            if not secret_file.exists():
                continue
            try:
                payload = json.loads(secret_file.read_text(encoding="utf-8"))
                decrypted = decrypt_secret_payload(payload, passphrase)
                merged.update(decrypted)
            except Exception:
                continue

        out: dict[str, str] = {}
        for key in ("DATABRICKS_HOST", "DATABRICKS_TOKEN"):
            val = merged.get(key)
            if val and val.strip():
                out[key] = val.strip()

        return out, None
    except Exception as exc:
        return {}, str(exc)


def pick_powershell_exe() -> str | None:
    for name in ("pwsh", "powershell"):
        found = shutil.which(name)
        if found:
            return found

    known_paths = [
        r"C:\Program Files\PowerShell\7\pwsh.exe",
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
    ]
    for known in known_paths:
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


def load_databricks_secrets_from_encrypted_powershell(project_root: Path, timeout_sec: int) -> dict[str, str]:
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
                if ($data.ContainsKey('DATABRICKS_HOST')) {{
                    $out['DATABRICKS_HOST'] = [string]$data['DATABRICKS_HOST']
                }}
                if ($data.ContainsKey('DATABRICKS_TOKEN')) {{
                    $out['DATABRICKS_TOKEN'] = [string]$data['DATABRICKS_TOKEN']
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
    filtered: dict[str, str] = {}
    for key in ("DATABRICKS_HOST", "DATABRICKS_TOKEN"):
        value = parsed.get(key)
        if value and value.strip():
            filtered[key] = value.strip()
    return filtered


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

    project_root = find_project_root(Path(__file__).resolve())
    encrypted_secret_map: dict[str, str] = {}
    secret_loader = "none"
    secret_loader_error: str | None = None

    if project_root:
        python_map, python_err = load_databricks_secrets_python(project_root)
        if python_map:
            encrypted_secret_map = python_map
            secret_loader = "python_dpapi"
        else:
            secret_loader_error = python_err
            powershell_map = load_databricks_secrets_from_encrypted_powershell(project_root, args.timeout_sec)
            if powershell_map:
                encrypted_secret_map = powershell_map
                secret_loader = "powershell_fallback"

    host = normalize_host(
        first_non_empty(
            args.host,
            os.getenv("DATABRICKS_HOST"),
            encrypted_secret_map.get("DATABRICKS_HOST"),
            env_map.get("DATABRICKS_HOST"),
        )
    )
    token = first_non_empty(
        args.token,
        os.getenv("DATABRICKS_TOKEN"),
        encrypted_secret_map.get("DATABRICKS_TOKEN"),
        env_map.get("DATABRICKS_TOKEN"),
    )

    result: dict[str, object] = {
        "ok": False,
        "proof": "databricks_read_only",
        "env_file_checked": str(env_file),
        "project_root_detected": str(project_root) if project_root else None,
        "encrypted_secret_loader": secret_loader,
        "encrypted_secret_keys_loaded": sorted([k for k, v in encrypted_secret_map.items() if bool(v)]),
        "host_resolved": host,
        "token_present": bool(token),
        "token_looks_placeholder": is_placeholder(token),
    }

    if secret_loader_error and secret_loader == "none":
        result["encrypted_secret_loader_error"] = secret_loader_error

    if requests is None:
        result["error"] = "Missing dependency: requests"
        result["hint"] = "Install with: pip install requests"
        print(json.dumps(result, indent=2))
        return 2

    if not host:
        result["error"] = "Missing workspace host. Provide --host, DATABRICKS_HOST, or encrypted secret value."
        print(json.dumps(result, indent=2))
        return 2

    if is_placeholder(token):
        result["error"] = "Missing Databricks PAT. Provide --token, DATABRICKS_TOKEN, or encrypted secret value."
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
