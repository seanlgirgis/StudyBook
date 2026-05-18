from __future__ import annotations

from pathlib import Path

import pytest

from study_bubbles.container import MISSING_BUBBLES_INI_ERROR, load_container_config


def test_bubbles_ini_discovery_from_cwd(tmp_path: Path) -> None:
    (tmp_path / "bubbles.ini").write_text(
        "\n".join(
            [
                "[studybubble]",
                "name = LearnTerraform",
                "mode = single-file",
                "default_topic = terraform_1000_foot_view",
                "topics_dir = topics",
                "layouts_dir = layouts",
                "outputs_dir = outputs",
                "assets_dir = assets",
                "",
                "[engine]",
                "path = ../../Study_bubbles",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    config = load_container_config(cwd=tmp_path)
    assert config.config_path == (tmp_path / "bubbles.ini").resolve()
    assert config.default_topic == "terraform_1000_foot_view"
    assert config.topics_dir == (tmp_path / "topics").resolve()
    assert config.downloads_dir == (Path.home() / "Downloads").resolve()


def test_missing_bubbles_ini_fails_fast(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="No bubbles.ini found"):
        load_container_config(cwd=tmp_path)

    with pytest.raises(FileNotFoundError) as exc:
        load_container_config(cwd=tmp_path)
    assert str(exc.value) == MISSING_BUBBLES_INI_ERROR


def test_relative_paths_resolve_from_container_root(tmp_path: Path) -> None:
    nested = tmp_path / "project"
    nested.mkdir(parents=True)
    (nested / "bubbles.ini").write_text(
        "\n".join(
            [
                "[studybubble]",
                "topics_dir = data/topics",
                "layouts_dir = data/layouts",
                "outputs_dir = data/outputs",
                "assets_dir = data/assets",
                "downloads_dir = data/downloads",
                "",
                "[engine]",
                "path = ../engine",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    config = load_container_config(cwd=nested)
    assert config.topics_dir == (nested / "data/topics").resolve()
    assert config.layouts_dir == (nested / "data/layouts").resolve()
    assert config.outputs_dir == (nested / "data/outputs").resolve()
    assert config.assets_dir == (nested / "data/assets").resolve()
    assert config.downloads_dir == (nested / "data/downloads").resolve()
    assert config.engine_path == (nested / "../engine").resolve()
