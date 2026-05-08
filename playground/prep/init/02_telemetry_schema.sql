BEGIN;

CREATE TABLE IF NOT EXISTS services (
  service_id SERIAL PRIMARY KEY,
  service_name TEXT UNIQUE NOT NULL,
  team_name TEXT NOT NULL,
  environment TEXT NOT NULL,
  criticality TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hosts (
  host_id SERIAL PRIMARY KEY,
  hostname TEXT UNIQUE NOT NULL,
  cluster_name TEXT NOT NULL,
  namespace_name TEXT NOT NULL,
  cloud_provider TEXT NOT NULL,
  instance_type TEXT NOT NULL,
  vcpu_allocated INTEGER NOT NULL,
  memory_gb_allocated NUMERIC(6,2) NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS deployments (
  deployment_id SERIAL PRIMARY KEY,
  service_id INTEGER NOT NULL REFERENCES services(service_id),
  deployed_at TIMESTAMPTZ NOT NULL,
  version TEXT NOT NULL,
  change_type TEXT NOT NULL,
  expected_impact TEXT,
  initiated_by TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incidents (
  incident_id SERIAL PRIMARY KEY,
  service_id INTEGER NOT NULL REFERENCES services(service_id),
  host_id INTEGER REFERENCES hosts(host_id),
  started_at TIMESTAMPTZ NOT NULL,
  ended_at TIMESTAMPTZ,
  severity TEXT NOT NULL,
  summary TEXT NOT NULL,
  capacity_related BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS capacity_thresholds (
  threshold_id SERIAL PRIMARY KEY,
  service_id INTEGER NOT NULL REFERENCES services(service_id),
  cpu_warn_pct NUMERIC(5,2) NOT NULL,
  cpu_crit_pct NUMERIC(5,2) NOT NULL,
  mem_warn_pct NUMERIC(5,2) NOT NULL,
  mem_crit_pct NUMERIC(5,2) NOT NULL,
  p95_latency_warn_ms INTEGER NOT NULL,
  p95_latency_crit_ms INTEGER NOT NULL,
  max_error_rate_pct NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS telemetry_samples (
  sample_id BIGSERIAL PRIMARY KEY,
  service_id INTEGER NOT NULL REFERENCES services(service_id),
  host_id INTEGER NOT NULL REFERENCES hosts(host_id),
  sampled_at TIMESTAMPTZ NOT NULL,
  cpu_utilization_pct NUMERIC(5,2) NOT NULL,
  memory_utilization_pct NUMERIC(5,2) NOT NULL,
  p95_latency_ms INTEGER NOT NULL,
  requests_per_min INTEGER NOT NULL,
  error_rate_pct NUMERIC(5,2) NOT NULL,
  allocated_cpu_cores NUMERIC(6,2) NOT NULL,
  allocated_memory_gb NUMERIC(6,2) NOT NULL,
  actual_cpu_cores NUMERIC(6,2) NOT NULL,
  actual_memory_gb NUMERIC(6,2) NOT NULL,
  forecast_cpu_pct NUMERIC(5,2),
  forecast_memory_pct NUMERIC(5,2),
  cloud_cost_usd NUMERIC(10,2) NOT NULL,
  tags JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_telemetry_service_time ON telemetry_samples(service_id, sampled_at);
CREATE INDEX IF NOT EXISTS idx_telemetry_host_time ON telemetry_samples(host_id, sampled_at);

COMMIT;
