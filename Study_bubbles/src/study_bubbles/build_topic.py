from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from study_bubbles.validate_topic import validate_topic_file


def _json_for_script(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def _is_external_ref(path_value: str) -> bool:
    lower = path_value.lower()
    return lower.startswith(("http://", "https://", "data:", "//"))


def _copy_single_file_image_assets(topic: dict, out_html_path: Path) -> list[str]:
    warnings: list[str] = []
    project_root = Path.cwd().resolve()
    out_dir = out_html_path.parent.resolve()

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
            continue
        if project_root not in source_path.parents and source_path != project_root:
            warnings.append(f"WARN: skipped out-of-project image path '{src}'")
            continue

        target_path = (out_dir / rel_src).resolve()
        if out_dir not in target_path.parents and target_path != out_dir:
            warnings.append(f"WARN: skipped unsafe output image path '{src}'")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)

    return warnings


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


def build_multifile(topic_path: Path, out_dir: Path) -> int:
    ok, topic, _passes, _errors = _validate_and_load_topic(topic_path)
    if not ok:
        print("Topic validation failed. Build aborted.")
        return 1

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


def build_single_file(topic_path: Path, out_html_path: Path) -> int:
    ok, topic, _passes, _errors = _validate_and_load_topic(topic_path)
    if not ok:
        print("Topic validation failed. Build aborted.")
        return 1

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
      <button id=\"clear-filters\" class=\"clear-btn\" type=\"button\">Reset</button>
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

    <aside class=\"side-panel\">
      <h2>Details</h2>
      <div id=\"node-details\" class=\"panel-card\">
        <p>Select a bubble to view details.</p>
      </div>

      <h2>Study Paths</h2>
      <ul id=\"study-paths\" class=\"path-list\"></ul>
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
    copy_warnings = _copy_single_file_image_assets(topic, out_html_path)

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
    for warning in copy_warnings:
        print(warning)
    print(f"PASS: proof file generated at {proof_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build StudyBubble topic outputs")
    parser.add_argument("--topic", required=True, help="Path to topic .studybubble.json file")
    parser.add_argument("--out", required=True, help="Output directory for multifile or output HTML for single-file")
    parser.add_argument("--mode", required=True, help="Build mode: multifile or single-file")
    args = parser.parse_args(argv)

    topic_path = Path(args.topic)
    mode = args.mode

    if mode == "multifile":
        return build_multifile(topic_path=topic_path, out_dir=Path(args.out))
    if mode == "single-file":
        return build_single_file(topic_path=topic_path, out_html_path=Path(args.out))

    print(
        f"FAIL: unsupported mode '{mode}'. Supported modes are: multifile, single-file"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
