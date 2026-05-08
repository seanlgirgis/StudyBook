def sql_list_public_tables() -> str:
    return """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""


def sql_preview_telemetry(limit: int = 20) -> str:
    limit = max(1, int(limit))
    return f"""
SELECT
    sample_id,
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct,
    p95_latency_ms,
    requests_per_min,
    error_rate_pct,
    allocated_cpu_cores,
    allocated_memory_gb,
    actual_cpu_cores,
    actual_memory_gb,
    forecast_cpu_pct,
    forecast_memory_pct,
    cloud_cost_usd,
    tags
FROM telemetry_samples
ORDER BY sampled_at
LIMIT {limit};
"""


def sql_service_average_cpu_memory() -> str:
    return """
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_cpu_pct DESC;
"""


def sql_threshold_risk_samples(limit: int = 50) -> str:
    """
        The fixed telemetry metrics like CPU, memory, latency, and cost live in normal columns. 
        The flexible metadata lives in a JSONB tags column. I can keep the full JSON for traceability, 
        but also extract keys like team, environment, and region into readable derived columns 
        using the JSONB operator ->>. That lets me filter, group, and report by ownership or 
        location without needing a separate physical column for every tag.
    """

    
    limit = max(1, int(limit))
    return f"""
SELECT
    t.sampled_at,
    s.service_name,
    t.host_id,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.p95_latency_ms,
    t.error_rate_pct,
    t.forecast_cpu_pct,
    t.forecast_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
WHERE t.cpu_utilization_pct >= 85
   OR t.memory_utilization_pct >= 85
   OR t.p95_latency_ms >= 500
   OR t.error_rate_pct >= 2
   OR t.forecast_cpu_pct >= 85
   OR t.forecast_memory_pct >= 85
ORDER BY
    t.sampled_at,
    s.service_name,
    t.host_id
LIMIT {limit};
"""


def sql_hourly_service_rollup() -> str:
    return """
SELECT
    DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
    s.service_name,

    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,2
    ) AS p95_cpu_pct,

    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.memory_utilization_pct)::NUMERIC,
        2
    ) AS p95_memory_pct,

    ROUND(AVG(t.p95_latency_ms), 2) AS avg_sampled_p95_latency_ms,
    MAX(t.p95_latency_ms) AS max_sampled_p95_latency_ms,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.p95_latency_ms)::NUMERIC,
        2
    ) AS p95_of_sampled_p95_latency_ms,

    ROUND(AVG(t.requests_per_min), 0) AS avg_requests_per_min,
    MAX(t.requests_per_min) AS max_requests_per_min,

    ROUND(AVG(t.error_rate_pct), 3) AS avg_error_rate_pct,
    ROUND(MAX(t.error_rate_pct), 3) AS max_error_rate_pct,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.error_rate_pct)::NUMERIC,
        3
    ) AS p95_error_rate_pct,

    ROUND(SUM(t.cloud_cost_usd), 2) AS hourly_cloud_cost_usd

FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    sample_hour,
    s.service_name;
"""


def sql_jsonb_tag_preview(limit: int = 20) -> str:
    limit = max(1, int(limit))
    return f"""
SELECT
    sample_id,
    sampled_at,
    tags,
    tags ->> 'team' AS tag_team,
    tags ->> 'env' AS tag_env,
    tags ->> 'region' AS tag_region
FROM telemetry_samples
ORDER BY sampled_at
LIMIT {limit};
"""


def sql_service_capacity_detail() -> str:
    """
    Return service-level telemetry detail used for Pandas capacity analysis.

    This query keeps one row per telemetry sample, but adds service_name
    so downstream Pandas code can group by service.
    """
    return """
SELECT
    s.service_name,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.p95_latency_ms,
    t.error_rate_pct,
    t.cloud_cost_usd
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY t.sampled_at;
"""

def sql_service_capacity_detail(limit: int | None = 500) -> str:
    """
    Return service-level telemetry rows used for Pandas capacity analysis.

    This keeps one row per telemetry sample, but adds service_name so
    downstream Pandas code can group and summarize by service.
    """
    limit_clause = "" if limit is None else f"LIMIT {max(1, int(limit))}"

    return f"""
SELECT
    s.service_name,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.p95_latency_ms,
    t.error_rate_pct,
    t.cloud_cost_usd
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY t.sampled_at
{limit_clause};
"""