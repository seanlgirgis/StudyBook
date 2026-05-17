from __future__ import annotations

import json
from pathlib import Path

from tools.sync_downloaded_layouts import resolve_paths, sync_downloaded_layouts


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def test_valid_downloaded_layout_updates_target_and_deletes_source(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    layouts = tmp_path / "layouts"
    src = downloads / "case_capacity_feature_table.layout.json"
    _write_json(
        src,
        {
            "topicId": "case_capacity_feature_table",
            "version": 1,
            "nodes": {"feature_table": {"x": 600, "y": 260}},
        },
    )

    report = sync_downloaded_layouts(downloads, layouts)

    target = layouts / "case_capacity_feature_table.layout.json"
    assert report.found_count == 1
    assert target.exists()
    assert not src.exists()
    assert len(report.updated_files) == 1
    assert report.errors == []


def test_existing_target_is_backed_up(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    layouts = tmp_path / "layouts"
    target = layouts / "case_capacity_feature_table.layout.json"
    _write_json(
        target,
        {"topicId": "case_capacity_feature_table", "version": 1, "nodes": {"a": {"x": 1, "y": 2}}},
    )
    src = downloads / "new.layout.json"
    _write_json(
        src,
        {"topicId": "case_capacity_feature_table", "version": 1, "nodes": {"b": {"x": 3, "y": 4}}},
    )

    report = sync_downloaded_layouts(downloads, layouts)
    backups = list((layouts / "backups").glob("case_capacity_feature_table.layout.*.bak.json"))

    assert len(backups) == 1
    assert len(report.backups_created) == 1
    assert not src.exists()


def test_bad_json_is_skipped_and_not_deleted(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    layouts = tmp_path / "layouts"
    bad = downloads / "broken.layout.json"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text("{not-json", encoding="utf-8")

    report = sync_downloaded_layouts(downloads, layouts)

    assert bad.exists()
    assert len(report.updated_files) == 0
    assert any("invalid json" in e for e in report.errors)


def test_missing_topic_id_is_skipped_and_not_deleted(tmp_path: Path) -> None:
    downloads = tmp_path / "Downloads"
    layouts = tmp_path / "layouts"
    src = downloads / "missing-topic.layout.json"
    _write_json(src, {"version": 1, "nodes": {"n": {"x": 1, "y": 1}}})

    report = sync_downloaded_layouts(downloads, layouts)

    assert src.exists()
    assert len(report.updated_files) == 0
    assert any("topicId" in e for e in report.errors)


def test_resolve_paths_reads_downloads_and_layouts_from_ini(tmp_path: Path) -> None:
    cfg = tmp_path / "studybubble.ini"
    cfg.write_text("[paths]\ndownloads_dir = D:\\Data\\DL\nlayouts_dir = layouts\n", encoding="utf-8")
    downloads, layouts, warnings, used = resolve_paths(config_path=cfg, downloads_override=None)
    assert warnings == []
    assert used == cfg.resolve()
    assert str(downloads).lower().endswith(str(Path("D:/Data/DL")).lower())
    assert layouts == (Path.cwd().resolve() / "layouts")


def test_downloads_override_wins_over_ini(tmp_path: Path) -> None:
    cfg = tmp_path / "studybubble.ini"
    cfg.write_text("[paths]\ndownloads_dir = D:\\Data\\DL\nlayouts_dir = layouts\n", encoding="utf-8")
    override = tmp_path / "my_downloads"
    downloads, _layouts, _warnings, _used = resolve_paths(
        config_path=cfg,
        downloads_override=str(override),
    )
    assert downloads == override.resolve()


def test_missing_config_falls_back(tmp_path: Path) -> None:
    cfg = tmp_path / "missing.ini"
    downloads, layouts, warnings, used = resolve_paths(config_path=cfg, downloads_override=None)
    assert used is None
    assert any("config file not found" in w for w in warnings)
    assert layouts == Path.cwd().resolve() / "layouts"
    assert downloads == (Path.home() / "Downloads").resolve()
