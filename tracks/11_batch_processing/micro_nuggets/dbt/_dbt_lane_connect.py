"""
dbt Lane Connection & Configuration Hub.

Auto-detects backend (PostgreSQL → Snowflake → Databricks → DuckDB),
generates profiles.yml, and provides helpers for running dbt commands
programmatically via subprocess.

Credential resolution order (first non-empty wins):
  1. Environment variables
  2. _infra/env/.env.local
  3. Hardcoded defaults for local dev

Usage in any nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _dbt_lane_connect import (
        detect_backend, write_profiles_yml, run_dbt, check_dbt_installed,
        LANE_DIR, DBT_PROJECT_DIR, LAB_SCHEMA
    )

    backend, reason = detect_backend()
    write_profiles_yml()
    rc, stdout, stderr = run_dbt(["debug"])
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Optional

# ── Constants ─────────────────────────────────────────────────────────────────
LANE_DIR: Path = Path(__file__).parent.resolve()
DBT_PROJECT_DIR: Path = LANE_DIR / "lab_dbt_project"
PROFILES_DIR: Path = DBT_PROJECT_DIR          # profiles.yml lives next to dbt_project.yml
ENV_FILE: Path = Path(r"D:\StudyBook\_infra\env\.env.local")

LAB_SCHEMA = "dbt_lab"
LAB_DB = "dbt_lab_db"

# UTF-8 stdout for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ── Env file loader ───────────────────────────────────────────────────────────

def load_env_file(path: Path) -> dict[str, str]:
    """Load KEY=VALUE pairs from .env file, stripping quotes and comments."""
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


def _env(key: str, default: str = "") -> str:
    """
    Resolve a key from env var → .env.local → POSTGRES_* alias → default.

    Also resolves PG_* short-form keys to POSTGRES_* equivalents, because
    the StudyBook .env.local uses POSTGRES_* naming conventions.

    PG_HOST     → POSTGRES_HOST
    PG_PORT     → POSTGRES_PORT
    PG_USER     → POSTGRES_USER
    PG_PASSWORD → POSTGRES_PASSWORD
    PG_DB       → POSTGRES_DB
    """
    # Direct env var check first
    env_val = os.environ.get(key, "")
    if env_val:
        return env_val

    file_map = load_env_file(ENV_FILE)

    # Direct file key
    if key in file_map:
        return file_map[key]

    # PG_* → POSTGRES_* aliasing
    pg_alias = {
        "PG_HOST":     "POSTGRES_HOST",
        "PG_PORT":     "POSTGRES_PORT",
        "PG_USER":     "POSTGRES_USER",
        "PG_PASSWORD": "POSTGRES_PASSWORD",
        "PG_DB":       "POSTGRES_DB",
    }
    if key in pg_alias:
        alias = pg_alias[key]
        # Check env var alias
        if os.environ.get(alias, ""):
            return os.environ[alias]
        # Check file alias
        if alias in file_map:
            return file_map[alias]

    return default


# ── Backend auto-detection ─────────────────────────────────────────────────────

def _check_tcp(host: str, port: int, timeout: float = 2.0) -> bool:
    """Return True if TCP connect succeeds within timeout."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def detect_backend() -> tuple[str, str]:
    """
    Auto-detect the best available dbt backend.

    Priority:
      1. PostgreSQL  — if PG_HOST:PG_PORT is reachable via TCP
      2. Snowflake   — if SNOWFLAKE_ACCOUNT + _USER + _PASSWORD all present
      3. Databricks  — if DATABRICKS_HOST + _TOKEN + _HTTP_PATH all present
      4. DuckDB      — always available (pure-Python, no server needed)

    Returns (backend_name, reason_string).
    """
    # 1. PostgreSQL
    pg_host = _env("PG_HOST", "localhost")
    pg_port = int(_env("PG_PORT", "5432"))
    if _check_tcp(pg_host, pg_port):
        reason = f"TCP connect to {pg_host}:{pg_port} succeeded"
        print(f"[dbt-connect] backend=postgres  | {reason}")
        return "postgres", reason

    # 2. Snowflake
    sf_keys = ["SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD"]
    if all(_env(k) for k in sf_keys):
        reason = "SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD all set"
        print(f"[dbt-connect] backend=snowflake | {reason}")
        return "snowflake", reason

    # 3. Databricks
    db_keys = ["DATABRICKS_HOST", "DATABRICKS_TOKEN", "DATABRICKS_HTTP_PATH"]
    if all(_env(k) for k in db_keys):
        reason = "DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_HTTP_PATH all set"
        print(f"[dbt-connect] backend=databricks | {reason}")
        return "databricks", reason

    # 4. DuckDB fallback — always available
    reason = "No remote backend reachable; DuckDB local file selected"
    print(f"[dbt-connect] backend=duckdb    | {reason}")
    return "duckdb", reason


# ── profiles.yml generation ───────────────────────────────────────────────────

def _duckdb_path() -> str:
    """Absolute path to the DuckDB database file."""
    return str(DBT_PROJECT_DIR / "lab_dbt.duckdb")


def generate_profiles_yml(backend: str) -> str:
    """
    Generate profiles.yml YAML content for the given backend.

    The dbt_lab profile always has a 'dev' target.  The actual adapter
    section is swapped out based on backend detection.

    DuckDB note: dbt-duckdb supports multiple schemas via schema config
    in dbt_project.yml; no extra setup required.
    """
    duckdb_path = _duckdb_path()

    # ── DuckDB ──────────────────────────────────────────────────────────────
    if backend == "duckdb":
        return textwrap.dedent(f"""\
            # profiles.yml — auto-generated by _dbt_lane_connect.py
            # Backend: DuckDB (local file, no server required)
            # Edit _dbt_lane_connect.py to change backend or credentials.

            dbt_lab:
              target: dev
              outputs:
                dev:
                  type: duckdb
                  # Path to the local DuckDB database file.
                  # All schemas (dbt_lab, staging, raw, etc.) live inside this one file.
                  path: "{duckdb_path}"
                  schema: dbt_lab
                  threads: 4
        """)

    # ── PostgreSQL ───────────────────────────────────────────────────────────
    if backend == "postgres":
        pg_host = _env("PG_HOST", "localhost")
        pg_port = _env("PG_PORT", "5432")
        pg_user = _env("PG_USER", "de_admin")
        pg_pass = _env("PG_PASSWORD", "")
        pg_db   = _env("PG_DB", "de_telemetry")
        return textwrap.dedent(f"""\
            # profiles.yml — auto-generated by _dbt_lane_connect.py
            # Backend: PostgreSQL

            dbt_lab:
              target: dev
              outputs:
                dev:
                  type: postgres
                  host: {pg_host}
                  port: {pg_port}
                  user: {pg_user}
                  password: {pg_pass}
                  dbname: {pg_db}
                  schema: dbt_lab
                  threads: 4
                  keepalives_idle: 0
        """)

    # ── Snowflake ────────────────────────────────────────────────────────────
    if backend == "snowflake":
        sf_account  = _env("SNOWFLAKE_ACCOUNT")
        sf_user     = _env("SNOWFLAKE_USER")
        sf_password = _env("SNOWFLAKE_PASSWORD")
        sf_role     = _env("SNOWFLAKE_ROLE", "SYSADMIN")
        sf_warehouse= _env("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
        sf_database = _env("SNOWFLAKE_DATABASE", "DBT_LAB")
        return textwrap.dedent(f"""\
            # profiles.yml — auto-generated by _dbt_lane_connect.py
            # Backend: Snowflake

            dbt_lab:
              target: dev
              outputs:
                dev:
                  type: snowflake
                  account: {sf_account}
                  user: {sf_user}
                  password: {sf_password}
                  role: {sf_role}
                  warehouse: {sf_warehouse}
                  database: {sf_database}
                  schema: dbt_lab
                  threads: 4
                  client_session_keep_alive: False
        """)

    # ── Databricks ───────────────────────────────────────────────────────────
    if backend == "databricks":
        db_host      = _env("DATABRICKS_HOST")
        db_token     = _env("DATABRICKS_TOKEN")
        db_http_path = _env("DATABRICKS_HTTP_PATH")
        db_catalog   = _env("DATABRICKS_CATALOG", "hive_metastore")
        return textwrap.dedent(f"""\
            # profiles.yml — auto-generated by _dbt_lane_connect.py
            # Backend: Databricks SQL

            dbt_lab:
              target: dev
              outputs:
                dev:
                  type: databricks
                  host: {db_host}
                  http_path: {db_http_path}
                  token: {db_token}
                  catalog: {db_catalog}
                  schema: dbt_lab
                  threads: 4
        """)

    raise ValueError(f"Unknown backend: {backend!r}")


def write_profiles_yml() -> Path:
    """
    Detect backend, generate profiles.yml, and write it to DBT_PROJECT_DIR.

    Returns the Path of the written file.
    """
    backend, _ = detect_backend()
    content = generate_profiles_yml(backend)
    out_path = PROFILES_DIR / "profiles.yml"
    out_path.write_text(content, encoding="utf-8")
    print(f"[dbt-connect] profiles.yml written → {out_path}")
    return out_path


# ── Python executable resolution ──────────────────────────────────────────────

def _find_dbt_python() -> str:
    """
    Find a Python executable that has dbt installed.

    Resolution order:
      1. .venv_dbt/Scripts/python.exe  (lane-local venv, created by uv)
      2. DBT_PYTHON env var (user override)
      3. sys.executable (current Python, works if dbt is installed here)

    Returns the path to the Python executable as a string.
    """
    # 1. Lane-local venv (created by `uv venv .venv_dbt --python 3.13`)
    venv_python = LANE_DIR / ".venv_dbt" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)

    # 2. User-specified override
    user_python = os.environ.get("DBT_PYTHON", "")
    if user_python and Path(user_python).exists():
        return user_python

    # 3. Fallback to current Python
    return sys.executable


# ── dbt runner ────────────────────────────────────────────────────────────────

def run_dbt(
    args: list[str],
    cwd: Optional[Path] = None,
    timeout: int = 300,
) -> tuple[int, str, str]:
    """
    Run a dbt command as a subprocess.

    Args:
        args:    dbt sub-command + flags, e.g. ["run", "--select", "staging"]
        cwd:     Working directory; defaults to DBT_PROJECT_DIR
        timeout: Seconds before subprocess is killed

    Returns:
        (returncode, stdout, stderr)

    The --profiles-dir flag is automatically injected so that profiles.yml
    is always found next to dbt_project.yml inside lab_dbt_project/.

    Uses _find_dbt_python() to locate a Python that has dbt installed.
    On Python 3.14 (not yet supported by dbt), the lane-local .venv_dbt/
    with Python 3.13 is used automatically.
    """
    cwd = cwd or DBT_PROJECT_DIR

    # Inject --profiles-dir so dbt finds profiles.yml in lab_dbt_project/
    if "--profiles-dir" not in args:
        args = list(args) + ["--profiles-dir", str(PROFILES_DIR)]

    python_exe = _find_dbt_python()
    # Use dbt.cli.main as the module entry point (dbt has no __main__ module)
    cmd = [python_exe, "-W", "ignore::RuntimeWarning", "-m", "dbt.cli.main"] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "").strip() if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "").strip() if isinstance(exc.stderr, str) else ""
        return 124, stdout, f"dbt timed out after {timeout}s\n{stderr}"
    except FileNotFoundError:
        return 1, "", f"dbt not found via {python_exe}. Install: pip install dbt-core dbt-duckdb"


# ── dbt installation checks ───────────────────────────────────────────────────

def check_dbt_installed() -> bool:
    """Return True if dbt-core is importable via the resolved Python."""
    python_exe = _find_dbt_python()
    try:
        result = subprocess.run(
            [python_exe, "-c", "import dbt.version"],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def get_adapter_package(backend: str) -> str:
    """
    Return the pip package name for a given backend adapter.

    duckdb    → dbt-duckdb
    postgres  → dbt-postgres
    snowflake → dbt-snowflake
    databricks→ dbt-databricks
    """
    mapping = {
        "duckdb":     "dbt-duckdb",
        "postgres":   "dbt-postgres",
        "snowflake":  "dbt-snowflake",
        "databricks": "dbt-databricks",
    }
    return mapping.get(backend, f"dbt-{backend}")


def check_adapter_installed(backend: str) -> bool:
    """Return True if the adapter package for backend is importable via resolved Python."""
    adapter_modules = {
        "duckdb":     "dbt.adapters.duckdb",
        "postgres":   "dbt.adapters.postgres",
        "snowflake":  "dbt.adapters.snowflake",
        "databricks": "dbt.adapters.databricks",
    }
    module = adapter_modules.get(backend, f"dbt.adapters.{backend}")
    python_exe = _find_dbt_python()
    try:
        result = subprocess.run(
            [python_exe, "-c", f"import {module}"],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# ── Health check ──────────────────────────────────────────────────────────────

def health_check() -> bool:
    """
    Run a full health check and print a status table.
    Returns True if everything is ready to run dbt commands.
    """
    print("\n=== dbt Lane Health Check ===")
    ok = True

    # Python version
    py_ok = sys.version_info >= (3, 9)
    print(f"  Python >= 3.9   : {'OK' if py_ok else 'FAIL'} ({sys.version.split()[0]})")
    ok = ok and py_ok

    # dbt-core
    dbt_ok = check_dbt_installed()
    try:
        import dbt.version
        dbt_ver = dbt.version.__version__
    except Exception:
        dbt_ver = "not installed"
    print(f"  dbt-core        : {'OK' if dbt_ok else 'FAIL'} ({dbt_ver})")
    ok = ok and dbt_ok

    # backend + adapter
    backend, reason = detect_backend()
    adapter_ok = check_adapter_installed(backend)
    adapter_pkg = get_adapter_package(backend)
    print(f"  Backend         : {backend} ({reason})")
    print(f"  Adapter ({backend:10s}): {'OK' if adapter_ok else 'FAIL'} (pip install {adapter_pkg})")
    ok = ok and adapter_ok

    # profiles.yml writeable
    try:
        write_profiles_yml()
        profiles_ok = True
    except Exception as e:
        profiles_ok = False
        print(f"  profiles.yml    : FAIL ({e})")
    if profiles_ok:
        print(f"  profiles.yml    : OK ({PROFILES_DIR / 'profiles.yml'})")
    ok = ok and profiles_ok

    print(f"\n  Overall: {'READY' if ok else 'NOT READY'}")
    print("=" * 30)
    return ok


if __name__ == "__main__":
    sys.exit(0 if health_check() else 1)
