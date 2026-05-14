WITH hourly AS (
  SELECT date_trunc('hour', sampled_at) AS hour_bucket, host, region AS application, env AS service,
         AVG(cpu_pct) AS avg_cpu, MAX(cpu_pct) AS peak_cpu
  FROM lab.telemetry_cpu_raw
  GROUP BY 1,2,3,4
)
SELECT hour_bucket, host, application, service,
       ROUND(avg_cpu::numeric, 2) AS avg_cpu,
       ROUND(AVG(avg_cpu) OVER (PARTITION BY host, application, service ORDER BY hour_bucket ROWS BETWEEN 23 PRECEDING AND CURRENT ROW)::numeric, 2) AS cpu_24h_rolling_avg,
       ROUND(MAX(peak_cpu) OVER (PARTITION BY host, application, service ORDER BY hour_bucket ROWS BETWEEN 23 PRECEDING AND CURRENT ROW)::numeric, 2) AS cpu_24h_rolling_peak
FROM hourly
ORDER BY host, application, service, hour_bucket
LIMIT 400;
