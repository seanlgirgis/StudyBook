-- Time bucket + window function starter queries

-- 1) Quick shape check
SELECT COUNT(*) AS rows, MIN(sampled_at) AS min_ts, MAX(sampled_at) AS max_ts, COUNT(DISTINCT host) AS hosts
FROM lab.telemetry_cpu_raw;

-- 2) Hourly bucket averages by host (prod only)
SELECT
  date_trunc('hour', sampled_at) AS hour_bucket,
  host,
  ROUND(AVG(cpu_pct), 2) AS avg_cpu,
  MAX(cpu_pct) AS peak_cpu
FROM lab.telemetry_cpu_raw
WHERE env = 'prod'
GROUP BY 1, 2
ORDER BY hour_bucket DESC, host
LIMIT 50;

-- 3) Daily bucket by region
SELECT
  date_trunc('day', sampled_at) AS day_bucket,
  region,
  ROUND(AVG(cpu_pct), 2) AS avg_cpu,
  ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY cpu_pct)::numeric, 2) AS p95_cpu
FROM lab.telemetry_cpu_raw
GROUP BY 1, 2
ORDER BY day_bucket DESC, region;

-- 4) Rolling 6-hour average per host (window)
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
LIMIT 200;
