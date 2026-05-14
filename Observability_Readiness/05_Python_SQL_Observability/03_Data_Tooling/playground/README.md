# Playground Guide

This folder is the hands-on sandbox for telemetry bucketing, rolling features, risk bands, and forecast validation across SQL, Pandas, and PySpark.

## Notebook Files (This Folder)

- `00_time_buckets_scratch.ipynb`
  - Early scratchpad for PostgreSQL time buckets and window query checks.

- `01_pyspark_time_buckets_scratch.ipynb`
  - Early PySpark scratchpad for JDBC load + bucket/window tests.

- `02_pandas_native_bucketing_demo.ipynb`
  - Pandas-native bucketing demo (`dt.floor`) and grouped metrics.

- `03_pyspark_native_bucketing_demo.ipynb`
  - PySpark-native bucketing and window demo in Spark DataFrames.

- `04_sql_pandas_time_buckets_grouping.ipynb`
  - SQL + Pandas coverage for hour/day buckets and grouping by ownership keys.

- `05_sql_pandas_rolling_trend_peak.ipynb`
  - SQL + Pandas coverage for rolling trend and rolling peak features.

- `06_sql_pandas_headroom_risk_bands.ipynb`
  - SQL + Pandas coverage for headroom, breach flags, and risk bands.

- `07_sql_pandas_forecast_vs_actual.ipynb`
  - SQL + Pandas coverage for predicted vs actual comparison and error metrics.

- `08_pyspark_time_buckets_grouping.ipynb`
  - PySpark coverage for time buckets and ownership-level grouping.

- `09_pyspark_rolling_trend_peak.ipynb`
  - PySpark coverage for rolling average and rolling peak features.

- `10_pyspark_headroom_risk_bands.ipynb`
  - PySpark coverage for headroom, breach flags, and risk labels.

- `11_pyspark_forecast_vs_actual.ipynb`
  - PySpark coverage for predicted vs actual validation metrics.

## SQL Files (Different Folder)

SQL scripts are stored in:
- `D:\Workarea\StudyBook\Observability_Readiness\05_Python_SQL_Observability\01_SQL_For_Observability\labs`

Coverage files:
- `03_sql_time_buckets_grouping.sql`
  - Bucket telemetry by hour/day and aggregate by host/application/service.

- `04_sql_rolling_trend_peak.sql`
  - Build rolling 24-hour average and rolling 24-hour peak.

- `05_sql_headroom_risk_bands.sql`
  - Convert utilization to headroom, breach flags, and risk bands.

- `06_sql_forecast_vs_actual.sql`
  - Compare predicted vs actual peaks and compute error metrics.

## Suggested Run Order

1. `04_sql_pandas_time_buckets_grouping.ipynb`
2. `05_sql_pandas_rolling_trend_peak.ipynb`
3. `06_sql_pandas_headroom_risk_bands.ipynb`
4. `07_sql_pandas_forecast_vs_actual.ipynb`
5. `08_pyspark_time_buckets_grouping.ipynb`
6. `09_pyspark_rolling_trend_peak.ipynb`
7. `10_pyspark_headroom_risk_bands.ipynb`
8. `11_pyspark_forecast_vs_actual.ipynb`

## Runtime Notes

- PostgreSQL container/profile used in these notebooks:
  - host: `host.docker.internal`
  - port: `5432`
  - db: `observability`
  - user: `obs_user`

- PySpark notebooks require PostgreSQL JDBC driver loading in Spark session (already configured in setup cells).
