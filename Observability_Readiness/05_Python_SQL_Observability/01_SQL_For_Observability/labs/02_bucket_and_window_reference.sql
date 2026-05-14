-- Reference queries: time buckets and rolling window

-- Q1: Hourly bucket average CPU by host
SELECT
  date_trunc('hour', sampled_at) AS hour_bucket,
  host,
  ROUND(AVG(cpu_pct), 2) AS avg_cpu
FROM lab.telemetry_cpu_raw
GROUP BY 1, 2
ORDER BY hour_bucket DESC, host
LIMIT 20;

-- Q2: Hourly CPU with rolling 6-hour average by host
WITH hourly AS (
  SELECT
    date_trunc('hour', sampled_at) AS hour_bucket,
    host,
    AVG(cpu_pct) AS avg_cpu
  FROM lab.telemetry_cpu_raw
  GROUP BY 1, 2
)
SELECT
  hour_bucket,
  host,
  ROUND(avg_cpu::numeric, 2) AS avg_cpu,
  ROUND(AVG(avg_cpu) OVER (
    PARTITION BY host
    ORDER BY hour_bucket
    ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
  )::numeric, 2) AS rolling_6h_avg
FROM hourly
ORDER BY host, hour_bucket
LIMIT 50;
