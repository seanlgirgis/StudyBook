WITH hourly AS (
  SELECT date_trunc('hour', sampled_at) AS hour_bucket, host, region AS application, env AS service,
         AVG(cpu_pct) AS avg_cpu, MAX(cpu_pct) AS peak_cpu
  FROM lab.telemetry_cpu_raw GROUP BY 1,2,3,4
), features AS (
  SELECT hour_bucket, host, application, service,
         AVG(avg_cpu) OVER (PARTITION BY host, application, service ORDER BY hour_bucket ROWS BETWEEN 23 PRECEDING AND CURRENT ROW) AS cpu_24h_rolling_avg,
         MAX(peak_cpu) OVER (PARTITION BY host, application, service ORDER BY hour_bucket ROWS BETWEEN 23 PRECEDING AND CURRENT ROW) AS cpu_24h_rolling_peak
  FROM hourly
)
SELECT hour_bucket, host, application, service,
       ROUND(cpu_24h_rolling_avg::numeric,2) AS cpu_24h_rolling_avg,
       ROUND(cpu_24h_rolling_peak::numeric,2) AS cpu_24h_rolling_peak,
       ROUND((85 - cpu_24h_rolling_peak)::numeric,2) AS cpu_headroom_pct,
       (cpu_24h_rolling_peak >= 85) AS cpu_breach_flag,
       CASE WHEN cpu_24h_rolling_peak >= 85 THEN 'breached'
            WHEN 85 - cpu_24h_rolling_peak <= 5 THEN 'critical'
            WHEN 85 - cpu_24h_rolling_peak <= 15 THEN 'warning'
            ELSE 'healthy' END AS cpu_risk_band
FROM features
ORDER BY hour_bucket DESC, host
LIMIT 300;
