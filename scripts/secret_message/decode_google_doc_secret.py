from __future__ import annotations

import argparse
from io import StringIO
from typing import Iterable

import pandas as pd
import requests


def _as_int(value: object) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _extract_points(df: pd.DataFrame) -> list[tuple[str, int, int]]:
    # Expected source columns are x-coordinate, Character, y-coordinate.
    # We still support fallback ordering for resilience.
    points: list[tuple[str, int, int]] = []

    candidates: Iterable[tuple[int, int, int]] = (
        (0, 1, 2),  # x, char, y (actual doc layout)
        (1, 0, 2),  # char, x, y (common mistaken layout)
        (0, 2, 1),  # x, y, char
    )

    for x_col, char_col, y_col in candidates:
        trial: list[tuple[str, int, int]] = []
        for _, row in df.iterrows():
            x = _as_int(row.iloc[x_col])
            y = _as_int(row.iloc[y_col])
            if x is None or y is None:
                continue
            char = str(row.iloc[char_col])
            if not char:
                continue
            trial.append((char, x, y))
        if trial:
            points = trial
            break

    return points


def decode_a_secret_message(doc_url: str, invert_y: bool = False) -> str:
    response = requests.get(doc_url, timeout=30)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))
    if not tables:
        raise ValueError("No table found in the document.")

    data = next((table.iloc[:, :3] for table in tables if table.shape[1] >= 3), None)
    if data is None:
        raise ValueError("No table found with at least 3 columns.")

    points = _extract_points(data)
    if not points:
        raise ValueError("No valid character coordinate rows found.")

    max_x = max(x for _, x, _ in points)
    max_y = max(y for _, _, y in points)
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for char, x, y in points:
        if 0 <= x <= max_x and 0 <= y <= max_y:
            draw_y = (max_y - y) if invert_y else y
            grid[draw_y][x] = char

    return "\n".join("".join(row) for row in grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode secret message from a published Google Doc table.")
    parser.add_argument(
        "doc_url",
        nargs="?",
        default="https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub",
        help="Published Google Doc URL.",
    )
    parser.add_argument(
        "--invert-y",
        action="store_true",
        help="Flip Y axis if your source coordinates are bottom-up.",
    )
    args = parser.parse_args()

    # Windows terminals often default to cp1252 and fail on block characters.
    try:
        import sys

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print(decode_a_secret_message(args.doc_url, invert_y=args.invert_y))


if __name__ == "__main__":
    main()
