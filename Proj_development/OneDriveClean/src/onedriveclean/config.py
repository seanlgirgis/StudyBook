from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


def infer_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_json(local_path: Path, example_path: Path) -> Dict[str, Any]:
    selected = local_path if local_path.exists() else example_path
    if not selected.exists():
        raise FileNotFoundError(f"Missing config file: {local_path} or {example_path}")
    with selected.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a JSON object: {selected}")
    return data


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    paths: Dict[str, Any]
    remotes: Dict[str, Any]
    batches: Dict[str, Any]
    local_sources: Dict[str, Any]
    staging_batches: Dict[str, Any]

    @property
    def lab_root(self) -> Path:
        value = self.paths.get("lab_root")
        if not value:
            raise ValueError("paths config missing 'lab_root'")
        return Path(value)

    def lab_path(self, key: str) -> Path:
        value = self.paths.get(key)
        if not value:
            raise ValueError(f"paths config missing '{key}'")
        return self.lab_root / str(value)

    @property
    def dirty_remote(self) -> str:
        value = self.remotes.get("dirty_remote")
        if not value:
            raise ValueError("rclone remotes config missing 'dirty_remote'")
        return str(value)

    @property
    def clean_remote(self) -> str:
        value = self.remotes.get("clean_remote")
        if not value:
            raise ValueError("rclone remotes config missing 'clean_remote'")
        return str(value)

    def batch_remote_path(self, batch_name: str) -> str:
        batches = self.batches.get("batches", {})
        batch = batches.get(batch_name)
        if not batch:
            raise ValueError(f"Batch '{batch_name}' not found")
        remote_path = batch.get("remote_path")
        if not remote_path:
            raise ValueError(f"Batch '{batch_name}' missing remote_path")
        return str(remote_path)

    @property
    def excluded_remote_paths(self) -> list[str]:
        raw = self.remotes.get("excluded_remote_paths", [])
        if raw is None:
            return []
        return [str(item) for item in raw if str(item).strip()]

    @property
    def large_file_threshold_bytes(self) -> int:
        raw = self.paths.get("large_file_threshold_bytes", 100 * 1024 * 1024)
        return int(raw)


def load_config(project_root: Path | None = None) -> AppConfig:
    root = project_root or infer_project_root()
    config_dir = root / "config"

    paths = _read_json(config_dir / "paths.local.json", config_dir / "paths.example.json")
    remotes = _read_json(config_dir / "rclone_remotes.local.json", config_dir / "rclone_remotes.example.json")
    batches = _read_json(config_dir / "batches.local.json", config_dir / "batches.example.json")
    local_sources = _read_json(config_dir / "local_sources.local.json", config_dir / "local_sources.example.json")
    staging_batches = _read_json(config_dir / "staging_batches.local.json", config_dir / "staging_batches.example.json")

    return AppConfig(
        project_root=root,
        paths=paths,
        remotes=remotes,
        batches=batches,
        local_sources=local_sources,
        staging_batches=staging_batches,
    )
