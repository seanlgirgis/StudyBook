-- 04_window_functions.sql
-- SELECT-only window function practice queries.

-- 1) ROW_NUMBER by service
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    ROW_NUMBER() OVER (
        PARTITION BY s.service_name
        ORDER BY t.sampled_at
    ) AS row_number_within_service
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    row_number_within_service
LIMIT 50;

-- 2) RANK overall CPU
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    RANK() OVER (
        ORDER BY t.cpu_utilization_pct DESC
    ) AS cpu_rank_overall
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY cpu_rank_overall
LIMIT 25;

-- 3) DENSE_RANK overall CPU
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    DENSE_RANK() OVER (
        ORDER BY t.cpu_utilization_pct DESC
    ) AS dense_cpu_rank_overall
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY dense_cpu_rank_overall
LIMIT 25;

-- 4) RANK within service
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    RANK() OVER (
        PARTITION BY s.service_name
        ORDER BY t.cpu_utilization_pct DESC
    ) AS cpu_rank_within_service
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    cpu_rank_within_service
LIMIT 50;

-- 5) CTE to select top CPU sample per service
WITH ranked_samples AS (
    SELECT
        s.service_name,
        t.host_id,
        t.sampled_at,
        t.cpu_utilization_pct,
        RANK() OVER (
            PARTITION BY s.service_name
            ORDER BY t.cpu_utilization_pct DESC
        ) AS cpu_rank_within_service
    FROM telemetry_samples t
    JOIN services s
        ON s.service_id = t.service_id
)
SELECT
    service_name,
    host_id,
    sampled_at,
    cpu_utilization_pct,
    cpu_rank_within_service
FROM ranked_samples
WHERE cpu_rank_within_service = 1
ORDER BY service_name;

-- 6) LAG previous CPU
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    LAG(t.cpu_utilization_pct) OVER (
        PARTITION BY s.service_name, t.host_id
        ORDER BY t.sampled_at
    ) AS previous_cpu_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;

-- 7) CPU change from previous sample
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    LAG(t.cpu_utilization_pct) OVER (
        PARTITION BY s.service_name, t.host_id
        ORDER BY t.sampled_at
    ) AS previous_cpu_pct,
    ROUND(
        t.cpu_utilization_pct
        - LAG(t.cpu_utilization_pct) OVER (
            PARTITION BY s.service_name, t.host_id
            ORDER BY t.sampled_at
        ),
        2
    ) AS cpu_change_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;

-- 8) LEAD next CPU
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    LEAD(t.cpu_utilization_pct) OVER (
        PARTITION BY s.service_name, t.host_id
        ORDER BY t.sampled_at
    ) AS next_cpu_pct
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;

-- 9) Moving average CPU
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    ROUND(
        AVG(t.cpu_utilization_pct) OVER (
            PARTITION BY s.service_name, t.host_id
            ORDER BY t.sampled_at
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cpu_moving_avg_3_samples
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;

-- 10) Moving average sampled P95 latency
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.p95_latency_ms,
    ROUND(
        AVG(t.p95_latency_ms) OVER (
            PARTITION BY s.service_name, t.host_id
            ORDER BY t.sampled_at
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS p95_latency_moving_avg_3_samples
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;

-- 11) Running total requests by service
SELECT
    s.service_name,
    t.sampled_at,
    t.requests_per_min,
    SUM(t.requests_per_min) OVER (
        PARTITION BY s.service_name
        ORDER BY t.sampled_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_requests_per_min_total
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.sampled_at
LIMIT 50;

-- 12) Window function versus GROUP BY example
SELECT
    s.service_name,
    t.host_id,
    t.sampled_at,
    t.cpu_utilization_pct,
    ROUND(
        AVG(t.cpu_utilization_pct) OVER (
            PARTITION BY s.service_name
        ),
        2
    ) AS service_avg_cpu_visible_on_each_row
FROM telemetry_samples t
JOIN services s
    ON s.service_id = t.service_id
ORDER BY
    s.service_name,
    t.host_id,
    t.sampled_at
LIMIT 50;
