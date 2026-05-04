"""CLI runner for 03g retrieval decision sample generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from retrieval_decision import load_decision_config, load_hybrid_results, run_decision_batch


def resolve_project_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current.parent, *current.parents]:
        if (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not resolve project root (AGENTS.md not found).")


def get_default_paths(project_root: Path) -> tuple[Path, Path, Path]:
    input_path = project_root / "pocs" / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
    config_path = project_root / "pocs" / "03g_retrieval_decision" / "config" / "decision_config.json"
    output_path = project_root / "pocs" / "03g_retrieval_decision" / "outputs" / "sample_retrieval_decisions.json"
    return input_path, config_path, output_path


def resolve_cli_path(project_root: Path, path_text: str) -> Path:
    raw = Path(path_text)
    return raw if raw.is_absolute() else project_root / raw


def display_path(path: Path, project_root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def parse_args(project_root: Path) -> argparse.Namespace:
    default_input, default_config, default_output = get_default_paths(project_root)
    parser = argparse.ArgumentParser(description="Run 03g deterministic retrieval decisions.")
    parser.add_argument(
        "--input-path",
        default=default_input.relative_to(project_root).as_posix(),
        help="03f hybrid retrieval output path (absolute or repo-relative).",
    )
    parser.add_argument(
        "--config-path",
        default=default_config.relative_to(project_root).as_posix(),
        help="03g decision config path (absolute or repo-relative).",
    )
    parser.add_argument(
        "--output-path",
        default=default_output.relative_to(project_root).as_posix(),
        help="03g decision output path (absolute or repo-relative).",
    )
    return parser.parse_args()


def main() -> None:
    project_root = resolve_project_root()
    args = parse_args(project_root)

    input_path = resolve_cli_path(project_root, args.input_path).resolve()
    config_path = resolve_cli_path(project_root, args.config_path).resolve()
    output_path = resolve_cli_path(project_root, args.output_path).resolve()

    hybrid_batch = load_hybrid_results(input_path)
    config = load_decision_config(config_path)
    decision_batch = run_decision_batch(
        hybrid_batch=hybrid_batch,
        input_source=display_path(input_path, project_root),
        config=config,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(decision_batch.model_dump(mode="json"), indent=2), encoding="utf-8")

    print(f"Input path: {input_path}")
    print(f"Config path: {config_path}")
    print(f"Output path: {output_path}")
    print(f"Queries processed: {len(decision_batch.query_decisions)}")
    print("PASS")


if __name__ == "__main__":
    main()
