-- ============================================================
-- 06_server_5min_capacity_rollup_practice.sql
--
-- Purpose:
-- Create a practice table with one metric sample every 5 minutes
-- for every server, then calculate hourly AVG, MAX, and P95.
--
-- This is for capacity / telemetry SQL interview practice.
-- ============================================================

-- ------------------------------------------------------------
-- 1) Drop only the practice tables
-- ------------------------------------------------------------

DROP TABLE IF EXISTS server_metric_samples_5min;
DROP TABLE IF EXISTS server_inventory_practice;

-- ------------------------------------------------------------
-- 2) Create a small server inventory table
-- ------------------------------------------------------------

CREATE TABLE server_inventory_practice (
    server_id       SERIAL PRIMARY KEY,
    hostname        TEXT NOT NULL UNIQUE,
    service_name    TEXT NOT NULL,
    environment     TEXT NOT NULL,
    region          TEXT NOT NULL,
    cpu_cores       NUMERIC(6,2) NOT NULL,
    memory_gb       NUMERIC(8,2) NOT NULL
);

-- ------------------------------------------------------------
-- 3) Create the 5-minute telemetry sample table
-- ------------------------------------------------------------

CREATE TABLE server_metric_samples_5min (
    sample_id               BIGSERIAL PRIMARY KEY,
    server_id               INTEGER NOT NULL REFERENCES server_inventory_practice(server_id),
    sampled_at              TIMESTAMPTZ NOT NULL,

    cpu_utilization_pct      NUMERIC(6,2) NOT NULL,
    memory_utilization_pct   NUMERIC(6,2) NOT NULL,
    disk_utilization_pct     NUMERIC(6,2) NOT NULL,

    p95_latency_ms           INTEGER NOT NULL,
    requests_per_min         INTEGER NOT NULL,
    error_rate_pct           NUMERIC(6,3) NOT NULL,

    actual_cpu_cores         NUMERIC(6,2) NOT NULL,
    actual_memory_gb         NUMERIC(8,2) NOT NULL,
    cloud_cost_usd           NUMERIC(10,4) NOT NULL,

    tags                     JSONB NOT NULL DEFAULT '{}'::jsonb,

    CONSTRAINT uq_server_sample_time UNIQUE (server_id, sampled_at)
);

-- ------------------------------------------------------------
-- 4) Seed fake servers
-- ------------------------------------------------------------

INSERT INTO server_inventory_practice
    (hostname, service_name, environment, region, cpu_cores, memory_gb)
VALUES
    ('checkout-api-01',  'checkout-api',  'prod', 'us-east-1',  8, 32),
    ('checkout-api-02',  'checkout-api',  'prod', 'us-east-1',  8, 32),
    ('payment-api-01',   'payment-api',   'prod', 'us-east-1', 16, 64),
    ('payment-api-02',   'payment-api',   'prod', 'us-east-1', 16, 64),
    ('search-api-01',    'search-api',    'prod', 'us-west-2',  8, 32),
    ('search-api-02',    'search-api',    'prod', 'us-west-2',  8, 32),
    ('inventory-api-01', 'inventory-api', 'prod', 'us-east-1',  4, 16),
    ('inventory-api-02', 'inventory-api', 'prod', 'us-east-1',  4, 16),
    ('reporting-01',     'reporting',     'prod', 'us-east-1', 16, 128),
    ('batch-worker-01',  'batch-worker',  'prod', 'us-west-2', 32, 128);

-- ------------------------------------------------------------
-- 5) Generate one row every 5 minutes for every server
--    Here we generate 24 hours of samples.
--
--    24 hours * 12 samples/hour * 10 servers = 2,880 rows
-- ------------------------------------------------------------

WITH sample_times AS (
    SELECT generate_series(
        TIMESTAMPTZ '2026-05-01 00:00:00+00',
        TIMESTAMPTZ '2026-05-01 23:55:00+00',
        INTERVAL '5 minutes'
    ) AS sampled_at
),
server_time_grid AS (
    SELECT
        s.server_id,
        s.hostname,
        s.service_name,
        s.environment,
        s.region,
        s.cpu_cores,
        s.memory_gb,
        st.sampled_at,

        -- hour of day helps create busier daytime patterns
        EXTRACT(HOUR FROM st.sampled_at) AS hour_of_day
    FROM server_inventory_practice s
    CROSS JOIN sample_times st
),
generated_metrics AS (
    SELECT
        server_id,
        sampled_at,

        -- CPU pattern:
        -- base differs by service, daytime is busier, random adds noise
        LEAST(
            99.00,
            GREATEST(
                5.00,
                CASE
                    WHEN service_name = 'payment-api' THEN 55
                    WHEN service_name = 'checkout-api' THEN 48
                    WHEN service_name = 'search-api' THEN 42
                    WHEN service_name = 'reporting' THEN 35
                    WHEN service_name = 'batch-worker' THEN 30
                    ELSE 25
                END
                + CASE WHEN hour_of_day BETWEEN 13 AND 21 THEN 18 ELSE 0 END
                + (random() * 18)
            )
        )::NUMERIC(6,2) AS cpu_utilization_pct,

        -- Memory pattern:
        -- less spiky than CPU, but reporting and batch are heavier
        LEAST(
            99.00,
            GREATEST(
                10.00,
                CASE
                    WHEN service_name = 'reporting' THEN 68
                    WHEN service_name = 'batch-worker' THEN 62
                    WHEN service_name = 'payment-api' THEN 58
                    WHEN service_name = 'checkout-api' THEN 50
                    ELSE 42
                END
                + (random() * 12)
            )
        )::NUMERIC(6,2) AS memory_utilization_pct,

        -- Disk utilization
        LEAST(
            95.00,
            GREATEST(
                15.00,
                CASE
                    WHEN service_name = 'reporting' THEN 72
                    WHEN service_name = 'batch-worker' THEN 65
                    ELSE 38
                END
                + (random() * 10)
            )
        )::NUMERIC(6,2) AS disk_utilization_pct,

        -- Requests per minute
        GREATEST(
            20,
            (
                CASE
                    WHEN service_name = 'checkout-api' THEN 2200
                    WHEN service_name = 'payment-api' THEN 1600
                    WHEN service_name = 'search-api' THEN 2800
                    WHEN service_name = 'inventory-api' THEN 900
                    WHEN service_name = 'reporting' THEN 250
                    WHEN service_name = 'batch-worker' THEN 120
                    ELSE 100
                END
                + CASE WHEN hour_of_day BETWEEN 13 AND 21 THEN 700 ELSE 0 END
                + (random() * 500)
            )::INTEGER
        ) AS requests_per_min,

        -- P95 latency in ms
        GREATEST(
            25,
            (
                CASE
                    WHEN service_name = 'payment-api' THEN 220
                    WHEN service_name = 'checkout-api' THEN 180
                    WHEN service_name = 'search-api' THEN 140
                    WHEN service_name = 'inventory-api' THEN 110
                    WHEN service_name = 'reporting' THEN 350
                    WHEN service_name = 'batch-worker' THEN 300
                    ELSE 100
                END
                + CASE WHEN hour_of_day BETWEEN 13 AND 21 THEN 80 ELSE 0 END
                + (random() * 120)
            )::INTEGER
        ) AS p95_latency_ms,

        -- Error rate percentage
        LEAST(
            8.000,
            GREATEST(
                0.000,
                CASE
                    WHEN service_name = 'payment-api' THEN 0.400
                    WHEN service_name = 'checkout-api' THEN 0.300
                    WHEN service_name = 'search-api' THEN 0.200
                    ELSE 0.100
                END
                + (random() * 0.700)
                + CASE WHEN hour_of_day BETWEEN 18 AND 20 THEN random() * 1.500 ELSE 0 END
            )
        )::NUMERIC(6,3) AS error_rate_pct,

        cpu_cores,
        memory_gb,
        service_name,
        environment,
        region
    FROM server_time_grid
)
INSERT INTO server_metric_samples_5min (
    server_id,
    sampled_at,
    cpu_utilization_pct,
    memory_utilization_pct,
    disk_utilization_pct,
    p95_latency_ms,
    requests_per_min,
    error_rate_pct,
    actual_cpu_cores,
    actual_memory_gb,
    cloud_cost_usd,
    tags
)
SELECT
    server_id,
    sampled_at,
    cpu_utilization_pct,
    memory_utilization_pct,
    disk_utilization_pct,
    p95_latency_ms,
    requests_per_min,
    error_rate_pct,

    ROUND((cpu_cores * cpu_utilization_pct / 100.0)::NUMERIC, 2) AS actual_cpu_cores,
    ROUND((memory_gb * memory_utilization_pct / 100.0)::NUMERIC, 2) AS actual_memory_gb,

    -- fake cost per 5-minute sample
    ROUND(
        (
            (cpu_cores * 0.0025)
            + (memory_gb * 0.0008)
            + (requests_per_min * 0.00001)
        )::NUMERIC,
        4
    ) AS cloud_cost_usd,

    jsonb_build_object(
        'service', service_name,
        'environment', environment,
        'region', region,
        'sample_grain', '5_minutes',
        'source', 'synthetic_capacity_lab'
    ) AS tags
FROM generated_metrics;
