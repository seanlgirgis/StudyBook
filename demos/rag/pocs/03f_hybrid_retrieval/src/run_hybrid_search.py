"""CLI runner for 03f hybrid retrieval sample generation.

This runner intentionally stays thin and delegates retrieval logic to
`hybrid_retrieval.py`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hybrid_retrieval import hybrid_search
from schemas import HybridRetrievalConfig

SAMPLE_QUERIES = [
    "ac blowing warm air",
    "ac blwoing warm air",
    "maintenance plan pricing",
    "maintenence plan prising",
    "water heater leaking",
    "watter heater leakng",
]


def resolve_project_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current.parent, *current.parents]:
        if (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not resolve project root (AGENTS.md not found).")


def get_default_paths(project_root: Path) -> tuple[Path, Path, Path]:
    word_index = project_root / "pocs" / "03d_word_tfidf_index" / "outputs" / "tfidf_index.joblib"
    char_index = project_root / "pocs" / "03e_char_tfidf_typo_search" / "outputs" / "char_tfidf_index.joblib"
    output_path = project_root / "pocs" / "03f_hybrid_retrieval" / "outputs" / "sample_hybrid_search_results.json"
    return word_index, char_index, output_path


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
    default_word, default_char, default_output = get_default_paths(project_root)

    parser = argparse.ArgumentParser(description="Run 03f hybrid retrieval sample queries.")
    parser.add_argument(
        "--word-index-path",
        default=default_word.relative_to(project_root).as_posix(),
        help="Word TF-IDF index path (absolute or repo-relative)",
    )
    parser.add_argument(
        "--char-index-path",
        default=default_char.relative_to(project_root).as_posix(),
        help="Char TF-IDF index path (absolute or repo-relative)",
    )
    parser.add_argument(
        "--output-path",
        default=default_output.relative_to(project_root).as_posix(),
        help="Output JSON path (absolute or repo-relative)",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--word-weight", type=float, default=0.65)
    parser.add_argument("--char-weight", type=float, default=0.35)
    return parser.parse_args()


def main() -> None:
    project_root = resolve_project_root()
    args = parse_args(project_root)

    word_index_path = resolve_cli_path(project_root, args.word_index_path).resolve()
    char_index_path = resolve_cli_path(project_root, args.char_index_path).resolve()
    output_path = resolve_cli_path(project_root, args.output_path).resolve()

    config = HybridRetrievalConfig(
        word_weight=args.word_weight,
        char_weight=args.char_weight,
        top_k=args.top_k,
    )

    queries_payload: list[dict[str, object]] = []
    for query in SAMPLE_QUERIES:
        response = hybrid_search(
            query=query,
            word_index_path=word_index_path,
            char_index_path=char_index_path,
            config=config,
        )
        queries_payload.append(
            {
                "query": response.query,
                "normalized_query": response.normalized_query,
                "results": [item.model_dump(mode="json") for item in response.results],
            }
        )

    payload = {
        "poc": "03f_hybrid_retrieval",
        "description": "Hybrid retrieval sample output combining word TF-IDF and char TF-IDF results.",
        "word_index_path": display_path(word_index_path, project_root),
        "char_index_path": display_path(char_index_path, project_root),
        "config": config.model_dump(mode="json"),
        "queries": queries_payload,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Word index path: {word_index_path}")
    print(f"Char index path: {char_index_path}")
    print(f"Output path: {output_path}")
    print(f"Queries run: {len(SAMPLE_QUERIES)}")
    print("PASS")


if __name__ == "__main__":
    main()
