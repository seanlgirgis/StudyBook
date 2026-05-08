import pandas as pd


def add_capacity_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
            I add boolean risk flags so raw telemetry becomes easier to act on. 
            Instead of repeatedly writing threshold logic everywhere, I create columns
            like high_cpu, high_memory, high_latency, and high_error. 
            Then the rest of the pipeline can filter, summarize, test, and report 
            capacity risks more cleanly.
    """
    out = df.copy()
    out["high_cpu"] = out["cpu_utilization_pct"] >= 85
    out["high_memory"] = out["memory_utilization_pct"] >= 85
    out["high_latency"] = out["p95_latency_ms"] >= 500
    out["high_error"] = out["error_rate_pct"] >= 2
    return out


def summarize_by_service(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("service_name", as_index=False)
        .agg(
            sample_count=("service_name", "count"),
            avg_cpu_pct=("cpu_utilization_pct", "mean"),
            max_cpu_pct=("cpu_utilization_pct", "max"),
            avg_memory_pct=("memory_utilization_pct", "mean"),
            max_memory_pct=("memory_utilization_pct", "max"),
            avg_p95_latency_ms=("p95_latency_ms", "mean"),
            max_p95_latency_ms=("p95_latency_ms", "max"),
            avg_error_rate_pct=("error_rate_pct", "mean"),
            total_cloud_cost_usd=("cloud_cost_usd", "sum"),
        )
        .sort_values("avg_cpu_pct", ascending=False)
        .reset_index(drop=True)
    )

    round_cols = [
        "avg_cpu_pct",
        "max_cpu_pct",
        "avg_memory_pct",
        "max_memory_pct",
        "avg_p95_latency_ms",
        "max_p95_latency_ms",
        "avg_error_rate_pct",
        "total_cloud_cost_usd",
    ]
    grouped[round_cols] = grouped[round_cols].round(2)
    grouped["sample_count"] = grouped["sample_count"].astype(int)
    return grouped


def classify_capacity_status(row) -> str:
    if row["max_cpu_pct"] >= 90 or row["max_memory_pct"] >= 90:
        return "high_capacity_risk"
    if row["avg_cpu_pct"] < 35 and row["avg_memory_pct"] < 45:
        return "rightsizing_candidate"
    if row["avg_p95_latency_ms"] >= 450:
        return "latency_watch"
    return "normal"


def add_capacity_status(summary_df: pd.DataFrame) -> pd.DataFrame:
    out = summary_df.copy()
    out["capacity_status"] = out.apply(classify_capacity_status, axis=1)
    return out
