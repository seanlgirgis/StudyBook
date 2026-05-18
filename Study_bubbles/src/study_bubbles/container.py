from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

MISSING_BUBBLES_INI_ERROR = (
    "ERROR: No bubbles.ini found in the current folder.\n"
    "Run this command from a StudyBubble project folder, or create bubbles.ini first."
)


@dataclass(frozen=True)
class ContainerConfig:
    root: Path
    config_path: Path
    name: str
    mode: str
    default_topic: str | None
    topics_dir: Path
    layouts_dir: Path
    outputs_dir: Path
    assets_dir: Path
    downloads_dir: Path
    engine_path: Path


def _resolve_dir(root: Path, raw_value: str, fallback: str) -> Path:
    value = raw_value.strip() or fallback
    candidate = Path(value)
    return (candidate if candidate.is_absolute() else (root / candidate)).resolve()


def load_container_config(*, cwd: Path | None = None) -> ContainerConfig:
    root = (cwd or Path.cwd()).resolve()
    config_path = root / "bubbles.ini"
    if not config_path.exists():
        raise FileNotFoundError(MISSING_BUBBLES_INI_ERROR)

    parser = configparser.ConfigParser()
    parser.read(config_path, encoding="utf-8")

    name = parser.get("studybubble", "name", fallback=root.name).strip() or root.name
    mode = parser.get("studybubble", "mode", fallback="single-file").strip() or "single-file"
    default_topic = parser.get("studybubble", "default_topic", fallback="").strip() or None

    topics_dir = _resolve_dir(root, parser.get("studybubble", "topics_dir", fallback="topics"), "topics")
    layouts_dir = _resolve_dir(root, parser.get("studybubble", "layouts_dir", fallback="layouts"), "layouts")
    outputs_dir = _resolve_dir(root, parser.get("studybubble", "outputs_dir", fallback="outputs"), "outputs")
    assets_dir = _resolve_dir(root, parser.get("studybubble", "assets_dir", fallback="assets"), "assets")
    downloads_dir = _resolve_dir(
        root,
        parser.get("studybubble", "downloads_dir", fallback=str(Path.home() / "Downloads")),
        str(Path.home() / "Downloads"),
    )

    engine_raw = parser.get("engine", "path", fallback=".")
    engine_path = _resolve_dir(root, engine_raw, ".")

    return ContainerConfig(
        root=root,
        config_path=config_path.resolve(),
        name=name,
        mode=mode,
        default_topic=default_topic,
        topics_dir=topics_dir,
        layouts_dir=layouts_dir,
        outputs_dir=outputs_dir,
        assets_dir=assets_dir,
        downloads_dir=downloads_dir,
        engine_path=engine_path,
    )
