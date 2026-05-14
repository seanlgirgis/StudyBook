WITH base AS (
  SELECT sampled_at, host, cpu_pct, mem_pct, region AS application, env AS service
  FROM lab.telemetry_cpu_raw
)
SELECT date_trunc('hour', sampled_at) AS hour_bucket, date_trunc('day', sampled_at) AS day_bucket,
       host, application, service,
       ROUND(AVG(cpu_pct), 2) AS avg_cpu, MAX(cpu_pct) AS peak_cpu,
       ROUND(AVG(mem_pct), 2) AS avg_memory, MAX(mem_pct) AS peak_memory
FROM base
GROUP BY 1,2,3,4,5
ORDER BY hour_bucket DESC, host
LIMIT 200;
