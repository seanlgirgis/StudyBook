from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from study_bubbles.validate_topic import validate_topic_file

try:
    from PIL import Image
except Exception:  # pragma: no cover - graceful fallback when Pillow is unavailable
    Image = None


def _json_for_script(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def _is_external_ref(path_value: str) -> bool:
    lower = path_value.lower()
    return lower.startswith(("http://", "https://", "data:", "//"))


def _copy_single_file_image_assets(
    topic: dict,
    out_html_path: Path,
    *,
    image_max_width: int = 900,
    image_max_height: int = 700,
) -> tuple[list[str], dict[str, int]]:
    warnings: list[str] = []
    stats = {
        "copied": 0,
        "resized": 0,
        "skipped_external": 0,
        "missing": 0,
    }
    project_root = Path.cwd().resolve()
    out_dir = out_html_path.parent.resolve()
    raster_exts = {".png", ".jpg", ".jpeg", ".webp"}

    for node in topic.get("nodes", []):
        if not isinstance(node, dict):
            continue
        note = node.get("note")
        if not isinstance(note, dict):
            continue
        image = note.get("image")
        if not isinstance(image, dict):
            continue
        src = image.get("src")
        if not isinstance(src, str) or not src.strip():
            continue
        src = src.strip()
        if _is_external_ref(src):
            stats["skipped_external"] += 1
            continue

        rel_src = Path(src)
        if rel_src.is_absolute():
            warnings.append(f"WARN: skipped absolute image path '{src}'")
            continue
        if ".." in rel_src.parts:
            warnings.append(f"WARN: skipped unsafe image path '{src}'")
            continue

        source_path = (project_root / rel_src).resolve()
        if not source_path.exists():
            warnings.append(f"WARN: image source not found '{src}'")
            stats["missing"] += 1
            continue
        if project_root not in source_path.parents and source_path != project_root:
            warnings.append(f"WARN: skipped out-of-project image path '{src}'")
            continue

        target_path = (out_dir / rel_src).resolve()
        if out_dir not in target_path.parents and target_path != out_dir:
            warnings.append(f"WARN: skipped unsafe output image path '{src}'")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        ext = source_path.suffix.lower()
        resized = False

        if ext in raster_exts and Image is not None:
            try:
                with Image.open(source_path) as img:
                    w, h = img.size
                    if w > image_max_width or h > image_max_height:
                        img.thumbnail((image_max_width, image_max_height), Image.Resampling.LANCZOS)
                        save_args = {}
                        if ext in {".jpg", ".jpeg", ".webp"}:
                            save_args["quality"] = 85
                            save_args["optimize"] = True
                        img.save(target_path, **save_args)
                        resized = True
                    else:
                        shutil.copyfile(source_path, target_path)
            except Exception as exc:
                warnings.append(f"WARN: image resize failed for '{src}', copied original ({exc})")
                shutil.copyfile(source_path, target_path)
        else:
            if ext in raster_exts and Image is None:
                warnings.append("WARN: Pillow unavailable; raster images copied without resizing")
            shutil.copyfile(source_path, target_path)

        stats["copied"] += 1
        if resized:
            stats["resized"] += 1

    return warnings, stats


def _validate_and_load_topic(topic_path: Path) -> tuple[bool, dict, list[str], list[str]]:
    ok, passes, errors = validate_topic_file(topic_path)
    for line in passes:
        print(line)
    for line in errors:
        print(line)

    if not ok:
        return False, {}, passes, errors

    with topic_path.open("r", encoding="utf-8") as f:
        topic = json.load(f)
    return True, topic, passes, errors


def _load_layout(layout_path: Path, topic_id: str | None) -> tuple[dict | None, list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []

    try:
        raw = layout_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, warnings, [f"FAIL: layout file not found: {layout_path}"]
    except OSError as exc:
        return None, warnings, [f"FAIL: could not read layout file '{layout_path}': {exc}"]

    try:
        layout = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, warnings, [f"FAIL: invalid layout JSON '{layout_path}': {exc}"]

    if not isinstance(layout, dict):
        return None, warnings, [f"FAIL: layout root must be an object: {layout_path}"]

    nodes = layout.get("nodes")
    if not isinstance(nodes, dict):
        return None, warnings, [f"FAIL: layout nodes must be an object: {layout_path}"]

    layout_topic_id = layout.get("topicId")
    if topic_id and isinstance(layout_topic_id, str) and layout_topic_id.strip() and layout_topic_id != topic_id:
        warnings.append(
            f"WARN: layout topicId '{layout_topic_id}' does not match topic id '{topic_id}'"
        )

    return layout, warnings, errors


def _apply_layout_to_topic(topic: dict, layout: dict) -> tuple[int, int]:
    nodes = layout.get("nodes", {})
    if not isinstance(nodes, dict):
        return 0, 0

    applied = 0
    skipped = 0
    for node in topic.get("nodes", []):
        if not isinstance(node, dict):
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str):
            continue
        entry = nodes.get(node_id)
        if not isinstance(entry, dict):
            continue
        x = entry.get("x")
        y = entry.get("y")
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            node["x"] = float(x)
            node["y"] = float(y)
            applied += 1
        else:
            skipped += 1
    return applied, skipped


def build_multifile(topic_path: Path, out_dir: Path, layout_path: Path | None = None) -> int:
    ok, topic, _passes, _errors = _validate_and_load_topic(topic_path)
    if not ok:
        print("Topic validation failed. Build aborted.")
        return 1
    if layout_path is not None:
        layout, layout_warnings, layout_errors = _load_layout(layout_path, topic.get("id"))
        for warning in layout_warnings:
            print(warning)
        for error in layout_errors:
            print(error)
        if layout_errors:
            return 1
        if layout is not None:
            applied, skipped = _apply_layout_to_topic(topic, layout)
            print(f"PASS: applied layout positions to {applied} node(s)")
            if skipped:
                print(f"WARN: skipped {skipped} layout node position(s) with invalid x/y")

    out_dir.mkdir(parents=True, exist_ok=True)

    viewer_dir = Path("viewer")
    html_src = viewer_dir / "bubble_viewer.html"
    css_src = viewer_dir / "bubble_viewer.css"
    js_src = viewer_dir / "bubble_viewer.js"

    file_map = [
        (html_src, out_dir / "index.html"),
        (css_src, out_dir / "bubble_viewer.css"),
        (js_src, out_dir / "bubble_viewer.js"),
        (topic_path, out_dir / "topic.studybubble.json"),
    ]

    for src, dst in file_map:
        if not src.exists():
            print(f"FAIL: required source file missing: {src}")
            return 1
        shutil.copyfile(src, dst)
    if layout_path is not None:
        (out_dir / "topic.studybubble.json").write_text(
            json.dumps(topic, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    generated_files = [
        "index.html",
        "bubble_viewer.css",
        "bubble_viewer.js",
        "topic.studybubble.json",
        "run_proof.txt",
    ]

    proof_path = out_dir / "run_proof.txt"
    proof_lines = [
        f"timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"source topic path: {topic_path}",
        f"output folder: {out_dir}",
        "mode: multifile",
        "generated files:",
    ]
    proof_lines.extend([f"- {name}" for name in generated_files])
    proof_lines.extend(
        [
            f"topic id: {topic.get('id')}",
            f"title: {topic.get('title')}",
            f"node count: {len(topic.get('nodes', []))}",
            f"link count: {len(topic.get('links', []))}",
            f"path count: {len(topic.get('paths', []))}",
            "validation result: PASS",
            "summary: PASS",
            "manual smoke steps:",
            "1. Open index.html in browser.",
            "2. Confirm title/header and three bubbles are visible.",
            "3. Confirm two relationship lines are visible.",
            "4. Click each bubble and verify side panel content updates.",
            "5. Confirm study path list shows 'Telemetry to Forecast'.",
        ]
    )
    proof_path.write_text("\n".join(proof_lines) + "\n", encoding="utf-8")

    print(f"PASS: build output generated at {out_dir}")
    return 0


def build_single_file(
    topic_path: Path,
    out_html_path: Path,
    layout_path: Path | None = None,
    *,
    image_max_width: int = 900,
    image_max_height: int = 700,
) -> int:
    ok, topic, _passes, _errors = _validate_and_load_topic(topic_path)
    if not ok:
        print("Topic validation failed. Build aborted.")
        return 1
    if layout_path is not None:
        layout, layout_warnings, layout_errors = _load_layout(layout_path, topic.get("id"))
        for warning in layout_warnings:
            print(warning)
        for error in layout_errors:
            print(error)
        if layout_errors:
            return 1
        if layout is not None:
            applied, skipped = _apply_layout_to_topic(topic, layout)
            print(f"PASS: applied layout positions to {applied} node(s)")
            if skipped:
                print(f"WARN: skipped {skipped} layout node position(s) with invalid x/y")

    viewer_dir = Path("viewer")
    css_src = viewer_dir / "bubble_viewer.css"
    js_src = viewer_dir / "bubble_viewer.js"

    if not css_src.exists() or not js_src.exists():
        print("FAIL: viewer source files are missing (bubble_viewer.css/js).")
        return 1

    css_text = css_src.read_text(encoding="utf-8")
    js_text = js_src.read_text(encoding="utf-8")
    topic_json = _json_for_script(topic)

    build_metadata = {
        "generatedAtUtc": datetime.now(timezone.utc).isoformat(),
        "mode": "single-file",
        "sourceTopicPath": str(topic_path),
        "topicId": topic.get("id"),
        "title": topic.get("title"),
        "nodeCount": len(topic.get("nodes", [])),
        "linkCount": len(topic.get("links", [])),
        "pathCount": len(topic.get("paths", [])),
    }

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <!-- SECTION: Metadata -->
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{topic.get('title', 'StudyBubble')}</title>

  <!-- SECTION: Styles -->
  <style>
{css_text}
  </style>
</head>
<body>
  <!-- SECTION: App Shell -->
  <header class=\"app-header\">
    <div class=\"header-top\">
      <h1 id=\"topic-title\">Loading topic...</h1>
      <p id=\"topic-subtitle\"></p>
    </div>
    <div class=\"toolbar\">
      <input id=\"search-input\" type=\"text\" placeholder=\"Search label, definition, safe sentence...\" autocomplete=\"off\" />
      <span id=\"search-count\" class=\"search-count\"></span>
      <div id=\"group-filters\" class=\"group-filters\"></div>
      <button id=\"drag-toggle\" class=\"clear-btn\" type=\"button\" title=\"Toggle drag mode\">Drag Mode</button>
      <button id=\"focus-toggle\" class=\"clear-btn\" type=\"button\" title=\"Focus selected node connections\">Focus</button>
      <button id=\"fit-view\" class=\"clear-btn\" type=\"button\" title=\"Fit map\">Fit</button>
      <button id=\"reset-view\" class=\"clear-btn\" type=\"button\" title=\"Reset map view\">Reset View</button>
      <button id=\"export-layout\" class=\"clear-btn\" type=\"button\" title=\"Export current node layout as JSON\">Export Layout</button>
      <button id=\"clear-filters\" class=\"clear-btn\" type=\"button\">Reset</button>
      <span id=\"layout-export-status\" class=\"search-count\"></span>
    </div>
  </header>

  <main class=\"layout\">
    <section class=\"map-area\">
      <svg id=\"map-svg\" viewBox=\"0 0 1000 520\" role=\"img\" aria-label=\"Study bubble map\"></svg>
      <div id=\"zoom-hud\" class=\"zoom-hud\">100%</div>
      <div id=\"mode-hud\" class=\"mode-hud\">Pan mode</div>
      <div class=\"minimap-wrap\">
        <svg id=\"minimap-svg\" viewBox=\"0 0 1200 700\" role=\"img\" aria-label=\"Map minimap\"></svg>
      </div>
      <div class=\"keyboard-hints\">Keys: <span>Arrows</span> move selection <span>Enter</span> select <span>Esc</span> clear <span>F</span> focus</div>
    </section>
    <div id=\"panel-resizer\" class=\"panel-resizer\" role=\"separator\" aria-orientation=\"vertical\" aria-label=\"Resize study panel\"></div>
    <aside class=\"side-panel\">
      <div class=\"side-panel-body\">
        <h2>Details</h2>
        <div id=\"node-details\" class=\"panel-card\">
          <p>Select a bubble to view details.</p>
        </div>
      </div>
      <div class=\"side-panel-footer\">
        <h2>Study Paths</h2>
        <ul id=\"study-paths\" class=\"path-list\"></ul>
      </div>
    </aside>
  </main>

  <div id=\"context-menu\" class=\"context-menu\" aria-hidden=\"true\">
    <button type=\"button\" class=\"ctx-item\" data-action=\"pin\">Pin details</button>
    <button type=\"button\" class=\"ctx-item\" data-action=\"focus\">Focus connections</button>
    <button type=\"button\" class=\"ctx-item\" data-action=\"filter\">Filter to group</button>
    <button type=\"button\" class=\"ctx-item\" data-action=\"reset\">Reset view</button>
  </div>

  <!-- SECTION: Embedded Topic Data -->
  <script id=\"studybubble-topic-data\" type=\"application/json\">
{topic_json}
  </script>

  <!-- SECTION: JavaScript -->
  <script>
{js_text}
  </script>

  <!-- SECTION: Build Metadata -->
  <script id=\"studybubble-build-metadata\" type=\"application/json\">
{_json_for_script(build_metadata)}
  </script>
</body>
</html>
"""

    out_html_path.parent.mkdir(parents=True, exist_ok=True)
    out_html_path.write_text(html, encoding="utf-8")
    copy_warnings, image_stats = _copy_single_file_image_assets(
        topic,
        out_html_path,
        image_max_width=image_max_width,
        image_max_height=image_max_height,
    )

    proof_dir = out_html_path.parent / "run_proofs"
    proof_dir.mkdir(parents=True, exist_ok=True)
    proof_path = proof_dir / "iteration7_single_file_proof.txt"

    html_size = out_html_path.stat().st_size
    proof_lines = [
        f"timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"source topic path: {topic_path}",
        f"output HTML path: {out_html_path}",
        "mode: single-file",
        f"topic id: {topic.get('id')}",
        f"topic title: {topic.get('title')}",
        f"node count: {len(topic.get('nodes', []))}",
        f"link count: {len(topic.get('links', []))}",
        f"path count: {len(topic.get('paths', []))}",
        "validation result: PASS",
        f"generated HTML byte size: {html_size}",
        "manual smoke test steps:",
        "1. Open outputs/single_file/tiny_capacity_demo.html directly from File Explorer.",
        "2. Confirm title and subtitle render.",
        "3. Confirm 3 bubbles render (Telemetry, Baseline, Forecast).",
        "4. Confirm 2 relationship lines render.",
        "5. Click Telemetry and confirm side panel updates.",
        "6. Click Baseline and confirm side panel updates.",
        "7. Click Forecast and confirm side panel updates.",
        "8. Confirm no 'Failed to fetch' message appears.",
        "summary: PASS",
    ]
    if copy_warnings:
        proof_lines.append("asset copy warnings:")
        proof_lines.extend(copy_warnings)
    proof_path.write_text("\n".join(proof_lines) + "\n", encoding="utf-8")

    print(f"PASS: single-file output generated at {out_html_path}")
    print(
        "PASS: image asset handling copied={copied} resized={resized} skipped_external={skipped_external}".format(
            **image_stats
        )
    )
    for warning in copy_warnings:
        print(warning)
    print(f"PASS: proof file generated at {proof_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build StudyBubble topic outputs")
    parser.add_argument("--topic", required=True, help="Path to topic .studybubble.json file")
    parser.add_argument("--out", required=True, help="Output directory for multifile or output HTML for single-file")
    parser.add_argument("--mode", required=True, help="Build mode: multifile or single-file")
    parser.add_argument("--layout", required=False, help="Optional layout JSON file with saved node x/y positions")
    parser.add_argument("--image-max-width", type=int, default=900, help="Max raster image width for copied note assets")
    parser.add_argument("--image-max-height", type=int, default=700, help="Max raster image height for copied note assets")
    args = parser.parse_args(argv)

    topic_path = Path(args.topic)
    mode = args.mode

    if mode == "multifile":
        return build_multifile(topic_path=topic_path, out_dir=Path(args.out), layout_path=Path(args.layout) if args.layout else None)
    if mode == "single-file":
        return build_single_file(
            topic_path=topic_path,
            out_html_path=Path(args.out),
            layout_path=Path(args.layout) if args.layout else None,
            image_max_width=args.image_max_width,
            image_max_height=args.image_max_height,
        )

    print(
        f"FAIL: unsupported mode '{mode}'. Supported modes are: multifile, single-file"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
