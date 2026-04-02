from __future__ import annotations

from pathlib import Path
from typing import Dict


def load_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def first_non_empty(*values: str | None) -> str | None:
    for value in values:
        if value and str(value).strip():
            return str(value).strip()
    return None
