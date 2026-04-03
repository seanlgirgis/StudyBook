"""
Shared connection helper for all Databricks Bridge micro-nuggets.

This module re-exports all credential/connection machinery from the existing
_db_connect.py in the sibling databricks/ directory, avoiding code duplication.
It overrides LAB_SCHEMA to 'bridge_lab' so bridge nuggets run in their own
namespace without touching the baseline databricks/ nugget tables.

Credential resolution order (first non-empty wins):
  1. Environment variables  DATABRICKS_*          (set by env_setter.ps1)
  2. Encrypted secrets file                        (StudyBook DPAPI system)
  3. D:\\StudyBook\\_infra\\env\\.env.local

Usage in any bridge nugget:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from _db_bridge_connect import get_connection, LAB_CATALOG, LAB_SCHEMA

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT CURRENT_USER()")
    conn.close()

Why a separate schema?
    bridge_lab nuggets teach transfer concepts from PostgreSQL/Snowflake.
    Keeping them in 'bridge_lab' means they can be reset independently
    without disturbing the 'default' schema used by the baseline nuggets.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# ── Re-use the existing databricks/_db_connect.py machinery ──────────────────
# The bridge module lives at micro_nuggets/databricks_bridge/
# The base module lives at micro_nuggets/databricks/
_BASE_DIR = Path(__file__).resolve().parent.parent / "databricks"
if str(_BASE_DIR) not in sys.path:
    sys.path.insert(0, str(_BASE_DIR))

import _db_connect as _base  # noqa: E402  (import after path manipulation)

# Re-export helpers that nuggets may need directly
get_creds = _base.get_creds
get_workspace_info = _base.get_workspace_info

# ── Bridge-specific lab constants ─────────────────────────────────────────────
# Same catalog as the baseline nuggets (nugget_lab is already created by them).
# Separate SCHEMA so bridge tables don't collide with 'default' schema tables.
LAB_CATALOG: str = "nugget_lab"
LAB_SCHEMA:  str = "bridge_lab"


def get_connection(_bootstrap: bool = False, **overrides):
    """
    Open and return a databricks.sql.Connection targeting bridge_lab.

    Normal mode (default):
        Connects to nugget_lab.bridge_lab — the bridge study workspace.

    Bootstrap mode (_bootstrap=True):
        Connects without catalog/schema so 00_prereq_check.py can
        CREATE CATALOG / SCHEMA freely.  Only setup scripts use this.

    Any keyword argument overrides a resolved value, e.g.:
        conn = get_connection(schema="sandbox_lab")
    """
    if not _bootstrap:
        # Inject bridge defaults — callers can still override with explicit kwargs
        overrides.setdefault("catalog", LAB_CATALOG)
        overrides.setdefault("schema", LAB_SCHEMA)
    return _base.get_connection(_bootstrap=_bootstrap, **overrides)
