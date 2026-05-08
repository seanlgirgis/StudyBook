from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pathlib import Path

from src.db import run_sql
from src.capacity_analysis import add_capacity_flags, add_capacity_status, summarize_by_service
from src.reporting import ensure_output_dirs, export_dataframe, write_text_report
from src.telemetry_queries import sql_service_capacity_detail

from src.reporting import (
    build_output_path,
    ensure_output_dirs,
    export_dataframe,
    write_text_report,
)

if __name__ == "__main__":
    ensure_output_dirs()

    df = run_sql(sql_service_capacity_detail())
    flagged_df = add_capacity_flags(df)
    summary_df = summarize_by_service(flagged_df)
    summary_df = add_capacity_status(summary_df)


    csv_path = build_output_path("csv", "capacity_summary.csv")
    report_path = build_output_path("reports", "capacity_summary.md")

    export_dataframe(summary_df, csv_path)

    report_text = """# Capacity Summary Report

- Generated from local PostgreSQL telemetry lab
- AVG shows typical usage across samples
- MAX shows highest observed pressure
- P95 is useful for sustained high-load context
- Flags/status help prioritize capacity risk and rightsizing opportunities

## Top Service Rows

""" + summary_df.head(20).to_markdown(index=False)

    write_text_report(report_text, report_path)

    print(f"Exported CSV: {csv_path}")
    print(f"Exported Report: {report_path}")
