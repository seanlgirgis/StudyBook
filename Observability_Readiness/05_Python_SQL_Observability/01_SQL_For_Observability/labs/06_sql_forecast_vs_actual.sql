WITH daily_actual AS (
  SELECT date_trunc('day', sampled_at) AS day_bucket, host, region AS application, env AS service,
         MAX(cpu_pct) AS actual_peak_cpu
  FROM lab.telemetry_cpu_raw GROUP BY 1,2,3,4
), daily_forecast AS (
  SELECT day_bucket, host, application, service,
         LAG(actual_peak_cpu, 1) OVER (PARTITION BY host, application, service ORDER BY day_bucket) AS predicted_peak_cpu
  FROM daily_actual
)
SELECT a.day_bucket, a.host, a.application, a.service,
       ROUND(a.actual_peak_cpu::numeric,2) AS actual_peak_cpu,
       ROUND(f.predicted_peak_cpu::numeric,2) AS predicted_peak_cpu,
       ROUND((a.actual_peak_cpu - f.predicted_peak_cpu)::numeric,2) AS forecast_error,
       ROUND(ABS(a.actual_peak_cpu - f.predicted_peak_cpu)::numeric,2) AS absolute_error,
       (a.actual_peak_cpu >= 85) AS actual_breach,
       (f.predicted_peak_cpu >= 85) AS predicted_breach
FROM daily_actual a
LEFT JOIN daily_forecast f ON a.day_bucket=f.day_bucket AND a.host=f.host AND a.application=f.application AND a.service=f.service
WHERE f.predicted_peak_cpu IS NOT NULL
ORDER BY a.day_bucket DESC, a.host
LIMIT 300;
