# Capacity Summary Report

- Generated from local PostgreSQL telemetry lab
- AVG shows typical usage across samples
- MAX shows highest observed pressure
- P95 is useful for sustained high-load context
- Flags/status help prioritize capacity risk and rightsizing opportunities

## Top Service Rows

| service_name     |   sample_count |   avg_cpu_pct |   max_cpu_pct |   avg_memory_pct |   max_memory_pct |   avg_p95_latency_ms |   max_p95_latency_ms |   avg_error_rate_pct |   total_cloud_cost_usd | capacity_status    |
|:-----------------|---------------:|--------------:|--------------:|-----------------:|-----------------:|---------------------:|---------------------:|---------------------:|-----------------------:|:-------------------|
| payments-api     |             72 |         63.01 |         92.87 |            67.72 |               75 |               291.39 |                  450 |                 1.02 |                 658.73 | high_capacity_risk |
| risk-engine      |             72 |         58.59 |         76    |            63.04 |               69 |               337.78 |                  370 |                 1.18 |                 572.33 | normal             |
| customer-profile |             72 |         46.33 |         56    |            54.71 |               60 |               257.78 |                  290 |                 0.83 |                 493.13 | normal             |
| analytics-batch  |             72 |         40.26 |         48    |            50.37 |               55 |               367.78 |                  400 |                 1.08 |                 723.53 | normal             |