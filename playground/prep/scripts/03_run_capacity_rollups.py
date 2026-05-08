from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capacity_analysis import add_capacity_status, summarize_by_service
from src.db import run_sql
from src.telemetry_queries import (
    sql_hourly_service_rollup,
    sql_service_capacity_detail,
)


def main() -> None:
    hourly_df = run_sql(sql_hourly_service_rollup())

    print("=== Hourly Service Rollup ===")
    print(hourly_df.to_string(index=False))

    base_df = run_sql(sql_service_capacity_detail(limit=500))
    summary_df = summarize_by_service(base_df)
    summary_df = add_capacity_status(summary_df)

    print("\n=== Service Summary (Pandas) ===")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()