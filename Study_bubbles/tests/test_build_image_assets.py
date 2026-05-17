from __future__ import annotations

import importlib.util
from pathlib import Path

from src.study_bubbles.build_topic import _copy_single_file_image_assets


def _topic_with_image(src: str) -> dict:
    return {
        "nodes": [
            {
                "id": "n1",
                "note": {"image": {"src": src}},
            }
        ]
    }


def test_svg_copied_as_is(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "assets" / "diagram.svg"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text("<svg><rect width='10' height='10'/></svg>", encoding="utf-8")
    out = tmp_path / "outputs" / "single_file" / "topic.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8")

    warnings, stats = _copy_single_file_image_assets(_topic_with_image("assets/diagram.svg"), out)
    copied = out.parent / "assets" / "diagram.svg"
    assert copied.exists()
    assert copied.read_text(encoding="utf-8") == src.read_text(encoding="utf-8")
    assert warnings == []
    assert stats["copied"] == 1


def test_external_and_unsafe_paths_skipped(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "outputs" / "single_file" / "topic.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8")
    topic = {"nodes": [{"id": "a", "note": {"image": {"src": "https://example.com/a.png"}}}, {"id": "b", "note": {"image": {"src": "../secret.png"}}}]}
    warnings, stats = _copy_single_file_image_assets(topic, out)
    assert stats["skipped_external"] == 1
    assert any("unsafe image path" in w for w in warnings)


def test_missing_image_warns_and_continues(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "outputs" / "single_file" / "topic.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8")
    warnings, stats = _copy_single_file_image_assets(_topic_with_image("assets/missing.png"), out)
    assert any("image source not found" in w for w in warnings)
    assert stats["missing"] == 1


def test_large_raster_resized_within_bounds_if_pillow(tmp_path: Path, monkeypatch) -> None:
    if not importlib.util.find_spec("PIL"):
        return
    from PIL import Image

    monkeypatch.chdir(tmp_path)
    src = tmp_path / "assets" / "big.png"
    src.parent.mkdir(parents=True, exist_ok=True)
    with Image.new("RGB", (2000, 1200), color=(200, 100, 50)) as img:
        img.save(src)
    out = tmp_path / "outputs" / "single_file" / "topic.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("", encoding="utf-8")

    _warnings, stats = _copy_single_file_image_assets(_topic_with_image("assets/big.png"), out, image_max_width=900, image_max_height=700)
    copied = out.parent / "assets" / "big.png"
    assert copied.exists()
    with Image.open(copied) as img2:
        assert img2.width <= 900
        assert img2.height <= 700
    assert stats["resized"] == 1
