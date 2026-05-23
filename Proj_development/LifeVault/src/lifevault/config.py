from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_json_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_paths_example() -> Dict[str, Any]:
    return load_json_config(project_root() / "config" / "paths.example.json")


def load_rclone_remotes_example() -> Dict[str, Any]:
    return load_json_config(project_root() / "config" / "rclone_remotes.example.json")