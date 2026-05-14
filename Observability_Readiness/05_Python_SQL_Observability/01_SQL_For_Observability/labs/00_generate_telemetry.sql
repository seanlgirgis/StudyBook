-- Generate synthetic telemetry data for bucketing/window labs
CREATE SCHEMA IF NOT EXISTS lab;

DROP TABLE IF EXISTS lab.telemetry_cpu_raw;
CREATE TABLE lab.telemetry_cpu_raw (
  id BIGSERIAL PRIMARY KEY,
  sampled_at TIMESTAMPTZ NOT NULL,
  host TEXT NOT NULL,
  cpu_pct NUMERIC(5,2) NOT NULL,
  mem_pct NUMERIC(5,2) NOT NULL,
  region TEXT NOT NULL,
  env TEXT NOT NULL
);

-- About 371k rows across ~43 days at 10-second intervals
INSERT INTO lab.telemetry_cpu_raw (sampled_at, host, cpu_pct, mem_pct, region, env)
SELECT
  gs.ts + (random() * interval '59 seconds'),
  'host' || lpad(((1 + floor(random() * 80))::int)::text, 2, '0'),
  round((25 + random() * 70)::numeric, 2),
  round((30 + random() * 60)::numeric, 2),
  (ARRAY['us-east-1', 'us-west-2', 'eu-west-1'])[1 + floor(random() * 3)::int],
  (ARRAY['prod', 'stage'])[1 + floor(random() * 2)::int]
FROM generate_series(
  '2026-04-01 00:00:00+00'::timestamptz,
  '2026-05-14 00:00:00+00'::timestamptz,
  interval '10 seconds'
) AS gs(ts);

CREATE INDEX idx_telemetry_sampled_at ON lab.telemetry_cpu_raw(sampled_at);
CREATE INDEX idx_telemetry_host_sampled_at ON lab.telemetry_cpu_raw(host, sampled_at);
