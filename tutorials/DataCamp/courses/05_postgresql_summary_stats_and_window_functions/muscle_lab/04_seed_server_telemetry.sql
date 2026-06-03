-- 04_seed_server_telemetry.sql
-- Seeds server telemetry (1200 rows) for percentiles, NTILE, and time windows.

INSERT INTO course05_muscle.server_telemetry (
    sample_id, sample_ts, environment, service_name, host_name, cpu_pct, memory_pct, latency_ms, error_count
)
SELECT
    gs AS sample_id,
    TIMESTAMP '2026-02-01 00:00:00' + ((gs - 1) * INTERVAL '1 hour') AS sample_ts,
    (ARRAY['dev','qa','prod'])[((gs - 1) % 3) + 1] AS environment,
    (ARRAY['billing-api','customer-api','batch-loader','reporting','search'])[((gs - 1) % 5) + 1] AS service_name,
    ((ARRAY['billing-api','customer-api','batch-loader','reporting','search'])[((gs - 1) % 5) + 1]) || '-h' || (((gs - 1) % 4) + 1) AS host_name,
    ROUND(
      LEAST(99.00, GREATEST(2.00,
        (
          20
          + CASE WHEN ((gs - 1) % 3) = 2 THEN 18 ELSE 0 END
          + CASE WHEN ((gs - 1) % 5) = 2 AND ((gs - 1) % 24) BETWEEN 1 AND 4 THEN 26 ELSE 0 END
          + ((gs * 17) % 36)
          + CASE WHEN gs % 77 = 0 THEN 12 ELSE 0 END
        )
      ))::numeric,
      2
    ) AS cpu_pct,
    ROUND(
      LEAST(99.00, GREATEST(5.00,
        (
          28
          + CASE WHEN ((gs - 1) % 3) = 2 THEN 15 ELSE 0 END
          + CASE WHEN ((gs - 1) % 5) = 2 THEN 8 ELSE 0 END
          + ((gs * 11) % 32)
        )
      ))::numeric,
      2
    ) AS memory_pct,
    ROUND(
      (
        45
        + CASE WHEN ((gs - 1) % 3) = 2 THEN 28 ELSE 0 END
        + CASE WHEN ((gs - 1) % 5) = 2 THEN 36 ELSE 0 END
        + ((gs * 23) % 120)
        + CASE WHEN gs % 89 = 0 THEN 180 ELSE 0 END
      )::numeric,
      2
    ) AS latency_ms,
    GREATEST(0,
      CASE
        WHEN ((gs - 1) % 3) = 2 THEN ((gs * 7) % 6)
        ELSE ((gs * 5) % 4)
      END
    ) AS error_count
FROM generate_series(1, 1200) AS gs;
