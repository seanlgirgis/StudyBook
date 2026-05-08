-- 01_basic_selects.sql
-- Beginner ramp-up SELECT queries for telemetry lab.

-- 1) List tables in public schema
SELECT
    table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 2) Preview telemetry_samples
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
    cloud_cost_usd,
    tags
FROM telemetry_samples
ORDER BY sampled_at
LIMIT 20;

-- 3) Select only CPU/memory columns
SELECT
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct
FROM telemetry_samples
ORDER BY sampled_at
LIMIT 20;

-- 4) Filter high CPU
SELECT
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct
FROM telemetry_samples
WHERE cpu_utilization_pct >= 80
ORDER BY cpu_utilization_pct DESC
LIMIT 20;

-- 5) Filter high memory
SELECT
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct
FROM telemetry_samples
WHERE memory_utilization_pct >= 80
ORDER BY memory_utilization_pct DESC
LIMIT 20;

-- 6) Filter high latency
SELECT
    sampled_at,
    service_id,
    host_id,
    p95_latency_ms,
    requests_per_min,
    error_rate_pct
FROM telemetry_samples
WHERE p95_latency_ms >= 400
ORDER BY p95_latency_ms DESC
LIMIT 20;

-- 7) AND/OR filter example
SELECT
    sampled_at,
    service_id,
    host_id,
    cpu_utilization_pct,
    memory_utilization_pct,
    p95_latency_ms,
    error_rate_pct
FROM telemetry_samples
WHERE cpu_utilization_pct >= 75
   OR memory_utilization_pct >= 75
   OR p95_latency_ms >= 400
ORDER BY sampled_at
LIMIT 30;

-- 8) Preview services lookup
SELECT
    service_id,
    service_name
FROM services
ORDER BY service_id;

-- 9) Simple JOIN telemetry_samples + services
SELECT
    t.sampled_at,
    s.service_name,
    t.host_id,
    t.cpu_utilization_pct,
    t.memory_utilization_pct,
    t.p95_latency_ms
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    t.sampled_at,
    s.service_name
LIMIT 20;

-- 10) Preview JSONB tags
SELECT
    sample_id,
    sampled_at,
    tags
FROM telemetry_samples
ORDER BY sampled_at
LIMIT 20;

-- 11) Extract JSONB tags
SELECT
    sample_id,
    sampled_at,
    tags,
    tags ->> 'team' AS tag_team,
    tags ->> 'env' AS tag_env,
    tags ->> 'region' AS tag_region
FROM telemetry_samples
ORDER BY sampled_at
LIMIT 20;

-- 12) Simple GROUP BY avg CPU/memory by service
SELECT
    s.service_name,
    ROUND(AVG(t.cpu_utilization_pct), 2) AS avg_cpu_pct,
    ROUND(AVG(t.memory_utilization_pct), 2) AS avg_memory_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
GROUP BY s.service_name
ORDER BY avg_cpu_pct DESC;
