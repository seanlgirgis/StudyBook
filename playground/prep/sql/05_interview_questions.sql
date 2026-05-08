-- 05_interview_questions.sql
-- SELECT-only interview-style telemetry and capacity SQL practice.

-- 1) Highest average CPU by service
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    COUNT(*) AS sample_count
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_cpu_pct DESC;

-- 2) Highest memory pressure by service
SELECT
    s.service_name,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
    COUNT(*) AS sample_count
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_memory_pct DESC;

-- 3) Risky sampled P95 latency by service
SELECT
    s.service_name,
    ROUND(AVG(t.p95_latency_ms), 2) AS avg_sampled_p95_latency_ms,
    MAX(t.p95_latency_ms) AS max_sampled_p95_latency_ms,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.p95_latency_ms)::NUMERIC,
        2
    ) AS p95_of_sampled_p95_latency_ms
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY p95_of_sampled_p95_latency_ms DESC;

-- 4) Threshold breach samples
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
    t.host_id;

-- 5) Daily service capacity trend
SELECT
    DATE_TRUNC('day', t.sampled_at) AS sample_day,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
    ROUND(AVG(t.error_rate_pct), 3) AS avg_error_rate_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('day', t.sampled_at),
    s.service_name
ORDER BY
    sample_day,
    s.service_name;

-- 6) Hourly service capacity trend
SELECT
    DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
    ROUND(AVG(t.requests_per_min), 0) AS avg_requests_per_min,
    ROUND(AVG(t.error_rate_pct), 3) AS avg_error_rate_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    sample_hour,
    s.service_name;

-- 7) Over-allocation / rightsizing query
SELECT
    t.sampled_at,
    s.service_name,
    t.host_id,
    t.allocated_cpu_cores,
    t.actual_cpu_cores,
    ROUND(t.allocated_cpu_cores - t.actual_cpu_cores, 2) AS unused_cpu_cores,
    t.allocated_memory_gb,
    t.actual_memory_gb,
    ROUND(t.allocated_memory_gb - t.actual_memory_gb, 2) AS unused_memory_gb,
    t.cloud_cost_usd
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
WHERE t.allocated_cpu_cores > t.actual_cpu_cores
   OR t.allocated_memory_gb > t.actual_memory_gb
ORDER BY
    t.cloud_cost_usd DESC,
    t.sampled_at
LIMIT 50;

-- 8) Cost by service
SELECT
    s.service_name,
    ROUND(SUM(t.cloud_cost_usd), 2) AS total_cloud_cost_usd,
    ROUND(AVG(t.cloud_cost_usd), 4) AS avg_sample_cloud_cost_usd,
    COUNT(*) AS sample_count
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY total_cloud_cost_usd DESC;

-- 9) Risky hourly windows using CTE
WITH hourly_service_rollup AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
        ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,
            2
        ) AS p95_cpu_pct,
        ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
        ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.memory_utilization_pct)::NUMERIC,
            2
        ) AS p95_memory_pct,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.p95_latency_ms)::NUMERIC,
            2
        ) AS p95_of_sampled_p95_latency_ms,
        ROUND(AVG(t.error_rate_pct), 3) AS avg_error_rate_pct
    FROM telemetry_samples t
    JOIN services s
        ON s.service_id = t.service_id
    GROUP BY
        DATE_TRUNC('hour', t.sampled_at),
        s.service_name
)
SELECT *
FROM hourly_service_rollup
WHERE p95_cpu_pct >= 85
   OR p95_memory_pct >= 85
   OR p95_of_sampled_p95_latency_ms >= 450
   OR avg_error_rate_pct >= 1.0
ORDER BY
    sample_hour,
    p95_cpu_pct DESC,
    p95_of_sampled_p95_latency_ms DESC;

-- 10) Rank hourly CPU risk with RANK
WITH hourly_service_rollup AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,
            2
        ) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s
        ON s.service_id = t.service_id
    GROUP BY
        DATE_TRUNC('hour', t.sampled_at),
        s.service_name
),
ranked AS (
    SELECT
        sample_hour,
        service_name,
        p95_cpu_pct,
        RANK() OVER (
            PARTITION BY sample_hour
            ORDER BY p95_cpu_pct DESC
        ) AS cpu_risk_rank
    FROM hourly_service_rollup
)
SELECT *
FROM ranked
WHERE cpu_risk_rank = 1
ORDER BY sample_hour;

-- 11) Compare service CPU to previous hour with LAG
WITH hourly_service_rollup AS (
    SELECT
        DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
        s.service_name,
        ROUND(
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.cpu_utilization_pct)::NUMERIC,
            2
        ) AS p95_cpu_pct
    FROM telemetry_samples t
    JOIN services s
        ON s.service_id = t.service_id
    GROUP BY
        DATE_TRUNC('hour', t.sampled_at),
        s.service_name
),
with_previous AS (
    SELECT
        sample_hour,
        service_name,
        p95_cpu_pct,
        LAG(p95_cpu_pct) OVER (
            PARTITION BY service_name
            ORDER BY sample_hour
        ) AS previous_hour_p95_cpu_pct
    FROM hourly_service_rollup
)
SELECT
    sample_hour,
    service_name,
    p95_cpu_pct,
    previous_hour_p95_cpu_pct,
    ROUND(
        p95_cpu_pct - previous_hour_p95_cpu_pct,
        2
    ) AS p95_cpu_change
FROM with_previous
ORDER BY
    service_name,
    sample_hour;

-- 12) JSONB tag filter
SELECT
    t.sampled_at,
    s.service_name,
    t.host_id,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.tags,
    t.tags ->> 'region' AS tag_region,
    t.tags ->> 'service' AS tag_service
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
WHERE t.tags ? 'region'
ORDER BY
    t.sampled_at,
    s.service_name
LIMIT 50;

-- 13) Optional incidents query (included because incidents table and columns exist)
SELECT
    i.incident_id,
    s.service_name,
    i.started_at,
    i.ended_at,
    t.sampled_at,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.p95_latency_ms,
    t.error_rate_pct
FROM incidents i
JOIN services s
    ON s.service_id = i.service_id
JOIN telemetry_samples t
    ON t.service_id = i.service_id
WHERE t.sampled_at BETWEEN i.started_at - INTERVAL '2 hour'
                      AND COALESCE(i.ended_at, i.started_at + INTERVAL '30 min') + INTERVAL '2 hour'
ORDER BY
    i.incident_id,
    t.sampled_at;

-- 14) Optional deployments query (included because deployments table and columns exist)
WITH latest_deploy AS (
    SELECT service_id, MAX(deployed_at) AS deployed_at
    FROM deployments
    GROUP BY service_id
)
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct) FILTER (
        WHERE t.sampled_at >= d.deployed_at - INTERVAL '12 hour'
          AND t.sampled_at < d.deployed_at
    ), 2) AS cpu_before,
    ROUND(AVG(t.cpu_utilization_pct) FILTER (
        WHERE t.sampled_at >= d.deployed_at
          AND t.sampled_at < d.deployed_at + INTERVAL '12 hour'
    ), 2) AS cpu_after,
    ROUND(AVG(t.p95_latency_ms) FILTER (
        WHERE t.sampled_at >= d.deployed_at - INTERVAL '12 hour'
          AND t.sampled_at < d.deployed_at
    ), 2) AS latency_before,
    ROUND(AVG(t.p95_latency_ms) FILTER (
        WHERE t.sampled_at >= d.deployed_at
          AND t.sampled_at < d.deployed_at + INTERVAL '12 hour'
    ), 2) AS latency_after
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
JOIN latest_deploy d
    ON d.service_id = s.service_id
GROUP BY s.service_name
ORDER BY s.service_name;
