import pandas as pd


def build_demo_dataframe() -> pd.DataFrame:
    # Small in-memory telemetry sample (no database, no file writes)
    rows = [
        {"sampled_at": "2026-05-01 09:03:00", "service_name": "payments-api", "cpu_utilization_pct": 62, "memory_utilization_pct": 68, "p95_latency_ms": 250},
        {"sampled_at": "2026-05-01 09:21:00", "service_name": "payments-api", "cpu_utilization_pct": 74, "memory_utilization_pct": 71, "p95_latency_ms": 280},
        {"sampled_at": "2026-05-01 09:47:00", "service_name": "payments-api", "cpu_utilization_pct": 81, "memory_utilization_pct": 76, "p95_latency_ms": 320},
        {"sampled_at": "2026-05-01 10:08:00", "service_name": "payments-api", "cpu_utilization_pct": 77, "memory_utilization_pct": 74, "p95_latency_ms": 300},
        {"sampled_at": "2026-05-01 10:42:00", "service_name": "payments-api", "cpu_utilization_pct": 69, "memory_utilization_pct": 70, "p95_latency_ms": 270},
        {"sampled_at": "2026-05-01 09:12:00", "service_name": "risk-engine", "cpu_utilization_pct": 55, "memory_utilization_pct": 60, "p95_latency_ms": 340},
        {"sampled_at": "2026-05-01 09:56:00", "service_name": "risk-engine", "cpu_utilization_pct": 63, "memory_utilization_pct": 64, "p95_latency_ms": 380},
        {"sampled_at": "2026-05-01 10:14:00", "service_name": "risk-engine", "cpu_utilization_pct": 66, "memory_utilization_pct": 66, "p95_latency_ms": 410},
        {"sampled_at": "2026-05-02 09:06:00", "service_name": "payments-api", "cpu_utilization_pct": 71, "memory_utilization_pct": 72, "p95_latency_ms": 290},
        {"sampled_at": "2026-05-02 09:31:00", "service_name": "risk-engine", "cpu_utilization_pct": 60, "memory_utilization_pct": 62, "p95_latency_ms": 360},
    ]
    df = pd.DataFrame(rows)

    # Convert sampled_at text into datetime type.
    df["sampled_at"] = pd.to_datetime(df["sampled_at"])

    # .dt.floor("h") is the Pandas equivalent of SQL DATE_TRUNC('hour', sampled_at)
    df["sample_hour"] = df["sampled_at"].dt.floor("h")

    # .dt.floor("D") is the Pandas equivalent of SQL DATE_TRUNC('day', sampled_at)
    df["sample_day"] = df["sampled_at"].dt.floor("D")
    return df


def build_hourly_summary(df: pd.DataFrame) -> pd.DataFrame:
    # quantile(0.95) is the Pandas equivalent of calculating P95.
    # If p95_latency_ms is already a sampled P95 metric, this is
    # P95 of sampled P95 values, not raw request-level P95.
    hourly = (
        df.groupby(["sample_hour", "service_name"], as_index=False)
        .agg(
            avg_cpu_pct=("cpu_utilization_pct", "mean"),
            p95_cpu_pct=("cpu_utilization_pct", lambda x: x.quantile(0.95)),
            max_cpu_pct=("cpu_utilization_pct", "max"),
            avg_memory_pct=("memory_utilization_pct", "mean"),
            p95_memory_pct=("memory_utilization_pct", lambda x: x.quantile(0.95)),
            max_memory_pct=("memory_utilization_pct", "max"),
            p95_of_sampled_p95_latency_ms=("p95_latency_ms", lambda x: x.quantile(0.95)),
        )
        .sort_values(["sample_hour", "service_name"])
        .reset_index(drop=True)
    )

    num_cols = [
        "avg_cpu_pct",
        "p95_cpu_pct",
        "max_cpu_pct",
        "avg_memory_pct",
        "p95_memory_pct",
        "max_memory_pct",
        "p95_of_sampled_p95_latency_ms",
    ]
    hourly[num_cols] = hourly[num_cols].round(2)
    return hourly


def build_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby(["sample_day", "service_name"], as_index=False)
        .agg(
            avg_cpu_pct=("cpu_utilization_pct", "mean"),
            p95_cpu_pct=("cpu_utilization_pct", lambda x: x.quantile(0.95)),
            max_cpu_pct=("cpu_utilization_pct", "max"),
            avg_memory_pct=("memory_utilization_pct", "mean"),
            p95_memory_pct=("memory_utilization_pct", lambda x: x.quantile(0.95)),
            max_memory_pct=("memory_utilization_pct", "max"),
        )
        .sort_values(["sample_day", "service_name"])
        .reset_index(drop=True)
    )

    num_cols = [
        "avg_cpu_pct",
        "p95_cpu_pct",
        "max_cpu_pct",
        "avg_memory_pct",
        "p95_memory_pct",
        "max_memory_pct",
    ]
    daily[num_cols] = daily[num_cols].round(2)
    return daily


def main() -> None:
    df = build_demo_dataframe()

    print("=== Raw Data ===")
    print(df.to_string(index=False))

    hourly = build_hourly_summary(df)
    print("\n=== Hourly Summary ===")
    print(hourly.to_string(index=False))

    daily = build_daily_summary(df)
    print("\n=== Daily Summary ===")
    print(daily.to_string(index=False))


if __name__ == "__main__":
    main()
