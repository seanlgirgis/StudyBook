-- 02_joins_and_group_by.sql
-- Beginner-friendly SELECT-only JOIN and GROUP BY practice queries.

-- 1) Average CPU/memory/error by service
SELECT
    s.service_name,
    COUNT(DISTINCT t.host_id) AS host_count,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_mem,
    ROUND(AVG(t.error_rate_pct), 2) AS avg_error_rate
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_cpu DESC;

-- 2) P95 of sampled P95 latency by service
SELECT
    s.service_name,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY t.p95_latency_ms) AS p95_of_p95_latency
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY p95_of_p95_latency DESC;

-- 3) Daily service rollup
SELECT
    DATE_TRUNC('day', t.sampled_at) AS sample_day,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu,
    ROUND(AVG(t.requests_per_min), 0) AS avg_rpm
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('day', t.sampled_at),
    s.service_name
ORDER BY
    sample_day,
    s.service_name;

-- 4) Hourly service rollup
SELECT
    DATE_TRUNC('hour', t.sampled_at) AS hour_bucket,
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY
    DATE_TRUNC('hour', t.sampled_at),
    s.service_name
ORDER BY
    hour_bucket,
    s.service_name
LIMIT 40;

-- 5) Service + host rollup
SELECT
    s.service_name,
    h.hostname,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu,
    ROUND(MAX(t.cpu_utilization_pct), 2) AS max_cpu,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory,
    ROUND(MAX(t.memory_utilization_pct), 2) AS max_memory
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
JOIN hosts h
    ON h.host_id = t.host_id
GROUP BY
    s.service_name,
    h.hostname
ORDER BY
    avg_cpu DESC,
    s.service_name,
    h.hostname;

-- 6) Service + environment rollup
-- Skipped in this lab because hosts table does not include an environment column.
-- If hosts.environment exists later, add a GROUP BY query using s.service_name, h.environment.
