from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db import run_sql
from src.telemetry_queries import (
    sql_jsonb_tag_preview,
    sql_list_public_tables,
    sql_preview_telemetry,
    sql_service_average_cpu_memory,
    sql_threshold_risk_samples,
)


def print_section(title: str, df):
    print(f"\n=== {title} ===")
    print(df.to_string(index=False))


if __name__ == "__main__":
    print_section("Public Tables", run_sql(sql_list_public_tables()))
    print_section("Telemetry Preview", run_sql(sql_preview_telemetry(20)))
    print_section("Service Avg CPU/Memory", run_sql(sql_service_average_cpu_memory()))
    print_section("Threshold Risk Samples", run_sql(sql_threshold_risk_samples(50)))
    print_section("JSONB Tag Preview", run_sql(sql_jsonb_tag_preview(20)))
