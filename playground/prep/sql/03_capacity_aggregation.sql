-- 03_capacity_aggregation.sql
-- SELECT-only capacity aggregation practice queries.

-- 1) Service-level average CPU and memory
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_cpu_pct DESC;

-- 2) Service-level AVG and MAX capacity
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY max_cpu_pct DESC;

-- 3) P95 sampled latency by service
SELECT
    s.service_name,
    ROUND(
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.p95_latency_ms)::NUMERIC,
        2
    ) AS p95_of_sampled_p95_latency_ms
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY p95_of_sampled_p95_latency_ms DESC;

-- 4) Daily service rollup
SELECT
    DATE_TRUNC('day', t.sampled_at) AS sample_day,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(AVG(t.requests_per_min), 0) AS avg_requests_per_min,
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

-- 5) Hourly service rollup
SELECT
    DATE_TRUNC('hour', t.sampled_at) AS sample_hour,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory_pct,
    ROUND(AVG(t.requests_per_min), 0) AS avg_requests_per_min
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    sample_hour,
    s.service_name;

-- 6) Hourly AVG / MAX / P95 for CPU and memory
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
    ) AS p95_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    sample_hour,
    p95_cpu_pct DESC;

-- 7) Capacity waste / over-allocation check
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

-- 8) Threshold-style capacity risk
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

-- 9) Cost rollup by service
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
