import pandas as pd

from src.capacity_analysis import (
    add_capacity_flags,
    summarize_by_service,
    add_capacity_status,
)


def _sample_df():
    return pd.DataFrame(
        [
            {
                "service_name": "svc-a",
                "cpu_utilization_pct": 92.0,
                "memory_utilization_pct": 65.0,
                "p95_latency_ms": 300.0,
                "error_rate_pct": 1.1,
                "cloud_cost_usd": 10.0,
            },
            {
                "service_name": "svc-a",
                "cpu_utilization_pct": 82.0,
                "memory_utilization_pct": 72.0,
                "p95_latency_ms": 320.0,
                "error_rate_pct": 0.9,
                "cloud_cost_usd": 11.5,
            },
            {
                "service_name": "svc-b",
                "cpu_utilization_pct": 20.0,
                "memory_utilization_pct": 30.0,
                "p95_latency_ms": 480.0,
                "error_rate_pct": 2.1,
                "cloud_cost_usd": 5.25,
            },
        ]
    )


def test_add_capacity_flags():
    df = add_capacity_flags(_sample_df())
    assert {"high_cpu", "high_memory", "high_latency", "high_error"}.issubset(df.columns)
    assert bool(df.loc[0, "high_cpu"]) is True
    assert bool(df.loc[2, "high_error"]) is True


def test_summarize_by_service():
    summary = summarize_by_service(_sample_df())
    assert set([
        "service_name",
        "sample_count",
        "avg_cpu_pct",
        "max_cpu_pct",
        "avg_memory_pct",
        "max_memory_pct",
        "avg_p95_latency_ms",
        "max_p95_latency_ms",
        "avg_error_rate_pct",
        "total_cloud_cost_usd",
    ]).issubset(summary.columns)
    assert len(summary) == 2


def test_add_capacity_status():
    summary = summarize_by_service(_sample_df())
    out = add_capacity_status(summary)
    assert "capacity_status" in out.columns
    assert out["capacity_status"].notna().all()
