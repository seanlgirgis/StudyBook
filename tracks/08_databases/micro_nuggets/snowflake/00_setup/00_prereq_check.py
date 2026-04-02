"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NUGGET 00-00 · Prerequisites Check                                          ║
║  Run this FIRST before any other nugget.                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

PURPOSE
───────
Verifies your local environment is ready before you touch Snowflake.
Checks Python version, required packages, credential resolution, and
a live connection. Prints a ✓/✗ checklist so you know exactly what to fix.

CONCEPTS
────────
Snowflake connector for Python:
  - Package name : snowflake-connector-python
  - Maintained by Snowflake Inc.
  - Wraps Snowflake's REST API — you never write raw HTTP.

Snowpark:
  - Higher-level Python API (like PySpark, but native to Snowflake).
  - Optional for these nuggets but very important for real DE work.

pandas:
  - Used in nugget 11 to read/write DataFrames directly to Snowflake.

Credentials flow (these nuggets):
  env_setter.ps1  →  SNOWFLAKE_* env vars  →  _sf_connect.py  →  nuggets
  OR
  .env.local file →  _sf_connect.py  →  nuggets

USAGE
─────
    python 00_prereq_check.py

EXPECTED OUTPUT (when everything is fine)
─────────────────────────────────────────
    ── Python ──────────────────────────────────
      [✓] Python >= 3.10  — 3.11.4

    ── Packages ────────────────────────────────
      [✓] snowflake-connector-python (3.5.0)  min=3.0.0
      [✓] snowflake-snowpark-python (1.11.1)
      [✓] pandas (2.1.0)  min=1.5.0

    ── Credentials ─────────────────────────────
      [✓] SNOWFLAKE_ACCOUNT    — myaccount.us-east-1
      [✓] SNOWFLAKE_USER       — JOHN_DOE
      [✓] SNOWFLAKE_PASSWORD   — ***
      [✓] SNOWFLAKE_ROLE       — SYSADMIN
      [✓] SNOWFLAKE_WAREHOUSE  — COMPUTE_WH
      [✓] SNOWFLAKE_DATABASE   — DEMO_DB
      [✓] SNOWFLAKE_SCHEMA     — PUBLIC

    ── Live Connection ──────────────────────────
      [✓] Connected to Snowflake  — account=MYACCOUNT role=SYSADMIN wh=COMPUTE_WH

    ── Result: 11/11 checks passed ──────────────
      ✓  All good — you're ready to run any nugget!

EXPECTED OUTPUT (missing password example)
──────────────────────────────────────────
      [✗] SNOWFLAKE_PASSWORD   — MISSING
      ...
      [✗] Connected to Snowflake  — Missing Snowflake credentials: ['password']
      ── Result: 9/11 checks passed ────────────
      ✗  Fix the items above, then rerun this script.
"""
from __future__ import annotations

import sys
import importlib.metadata
from pathlib import Path

# ── Add the snowflake root to sys.path so _sf_connect is importable ──────────
# Every nugget does this one-liner. It points to the folder containing
# _sf_connect.py regardless of where you launch the script from.
ROOT = Path(__file__).parent.parent   # .../micro_nuggets/snowflake/
sys.path.insert(0, str(ROOT))

# Accumulate (label, passed, detail) tuples and print as we go
CHECKS: list[tuple[str, bool, str]] = []


def check(label: str, passed: bool, detail: str = "") -> None:
    CHECKS.append((label, passed, detail))
    icon = "✓" if passed else "✗"
    suffix = f"  — {detail}" if detail else ""
    print(f"  [{icon}] {label}{suffix}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. Python version
#    Snowflake connector requires Python 3.8+.
#    3.10+ gives us union type syntax (str | None) used in _sf_connect.
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Python ──────────────────────────────────")
py = sys.version_info
check(
    "Python >= 3.10",
    py >= (3, 10),
    f"{py.major}.{py.minor}.{py.micro}",
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. Required packages
#    importlib.metadata.version() reads installed package metadata without
#    importing the package itself — fast and side-effect-free.
#
#    Minimum versions chosen because:
#      snowflake-connector-python 3.0  — first version with arrow-based fetch
#      pandas 1.5                      — stable DataFrame.to_parquet on Windows
# ─────────────────────────────────────────────────────────────────────────────
REQUIRED = {
    "snowflake-connector-python": "3.0.0",   # mandatory
    "snowflake-snowpark-python":  None,       # optional — nugget 11 only
    "pandas":                     "1.5.0",   # optional — nugget 11 only
}

print("\n── Packages ────────────────────────────────")
for pkg, min_ver in REQUIRED.items():
    is_required = pkg == "snowflake-connector-python"
    try:
        installed_ver = importlib.metadata.version(pkg)
        label = f"{pkg} ({installed_ver})"
        if min_ver:
            # Compare versions properly using packaging.version if available,
            # else fall back to a simple tuple comparison on the first 3 parts.
            label += f"  min={min_ver}"
            try:
                from packaging.version import Version  # type: ignore
                passed = Version(installed_ver) >= Version(min_ver)
            except ImportError:
                # packaging not installed — do rough tuple compare
                def _tup(v: str) -> tuple:
                    return tuple(int(x) for x in v.split(".")[:3])
                passed = _tup(installed_ver) >= _tup(min_ver)
        else:
            passed = True  # optional package — any version is fine
    except importlib.metadata.PackageNotFoundError:
        installed_ver = "NOT INSTALLED"
        passed = not is_required   # only the connector is a hard requirement
        label = f"{pkg}  — {installed_ver}"
    check(label, passed)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Credential resolution
#    _sf_connect.get_creds() reads env vars then .env.local and returns a dict.
#    No connection is made here — just checks that values are present.
#
#    If credentials are missing:
#      Run:  . D:\StudyBook\env_setter.ps1    (in PowerShell)
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Credentials ─────────────────────────────")
try:
    from _sf_connect import get_creds
    creds = get_creds()
    # SNOWFLAKE_ROLE is optional — Snowflake defaults to the user's assigned
    # default role (e.g. ACCOUNTADMIN) when none is specified in the connection.
    OPTIONAL_KEYS = {"SNOWFLAKE_ROLE"}
    for key, val in creds.items():
        if key == "SNOWFLAKE_PASSWORD":
            display = "***" if val else "MISSING"
        elif key in OPTIONAL_KEYS and not val:
            display = "MISSING (optional — will use your default role)"
        else:
            display = val or "MISSING"
        # Optional keys never count as failures
        passed = bool(val) or key in OPTIONAL_KEYS
        check(key, passed, display)
except Exception as exc:
    check("_sf_connect import", False, str(exc))

# ─────────────────────────────────────────────────────────────────────────────
# 4. Live connection
#    Opens a real TCP connection to Snowflake's cloud endpoint.
#    On success, shows the active account / role / warehouse from
#    Snowflake's own CURRENT_* functions — these never lie.
#
#    Common failures:
#      "250001 (08001): Failed to connect"  → wrong account identifier
#      "390100 (08004): Incorrect username"  → wrong user/password
#      "Timeout"                             → firewall blocking 443
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Live Connection ──────────────────────────")
try:
    from _sf_connect import get_connection
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT CURRENT_ACCOUNT(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
        )
        acct, role, wh = cur.fetchone()
    conn.close()
    check(
        "Connected to Snowflake",
        True,
        f"account={acct}  role={role}  wh={wh}",
    )
except Exception as exc:
    check("Connected to Snowflake", False, str(exc))

# ─────────────────────────────────────────────────────────────────────────────
# 5. Summary
# ─────────────────────────────────────────────────────────────────────────────
total  = len(CHECKS)
passed = sum(1 for _, p, _ in CHECKS if p)

print(f"\n── Result: {passed}/{total} checks passed ───────────────")
if passed == total:
    print("  ✓  All good — you're ready to run any nugget!\n")
else:
    print("  ✗  Fix the items above, then rerun this script.\n")

sys.exit(0 if passed == total else 1)
