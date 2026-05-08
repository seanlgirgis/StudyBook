from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def ensure_output_dirs() -> None:
    """
    Create standard output folders.

    parents=True creates missing parent folders, similar to mkdir -p.
    exist_ok=True avoids an error if the folder already exists.
    """
    for rel in ["csv", "reports", "logs"]:
        (OUTPUTS_DIR / rel).mkdir(parents=True, exist_ok=True)


def build_output_path(folder: str, filename: str) -> Path:
    """
    Build a safe output path under the project outputs folder.

    Example:
        build_output_path("csv", "capacity_summary.csv")
        -> outputs/csv/capacity_summary.csv
    """
    return OUTPUTS_DIR / folder / filename


def export_dataframe(df: pd.DataFrame, path) -> None:
    """
    Write a DataFrame to CSV.

    Pathlib makes file paths cleaner and safer. The parent folder is created
    if needed. index=False avoids writing the Pandas index as an extra column.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)


def write_text_report(text: str, path) -> None:
    """
    Write a text or Markdown report to disk.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")