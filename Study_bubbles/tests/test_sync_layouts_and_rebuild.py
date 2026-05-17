from __future__ import annotations

from pathlib import Path

from tools.sync_layouts_and_rebuild import rebuild_topics_for_layouts, topic_ids_from_updated_layouts


def test_updated_layout_triggers_topic_id_resolution() -> None:
    files = [Path("layouts/case_capacity_feature_table.layout.json")]
    assert topic_ids_from_updated_layouts(files) == ["case_capacity_feature_table"]


def test_missing_topic_file_is_skipped_with_warning() -> None:
    report = rebuild_topics_for_layouts(["definitely_missing_topic_abcxyz"], dry_run=False)
    assert report.rebuilt_topics == []
    assert report.skipped_topics == ["definitely_missing_topic_abcxyz"]
    assert any("topic source missing" in e for e in report.errors)


def test_no_downloaded_layouts_means_no_rebuild() -> None:
    report = rebuild_topics_for_layouts([], dry_run=False)
    assert report.rebuilt_topics == []
    assert report.skipped_topics == []
    assert report.errors == []


def test_dry_run_marks_rebuild_without_running_builder() -> None:
    report = rebuild_topics_for_layouts(["case_capacity_feature_table"], dry_run=True)
    assert report.rebuilt_topics == ["case_capacity_feature_table"]
    assert report.skipped_topics == []
