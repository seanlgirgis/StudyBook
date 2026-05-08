BEGIN;

INSERT INTO services (service_name, team_name, environment, criticality) VALUES
('payments-api','Payments','prod','high'),
('risk-engine','Risk','prod','high'),
('customer-profile','Retail','prod','medium'),
('analytics-batch','Data','prod','medium')
ON CONFLICT (service_name) DO NOTHING;

INSERT INTO hosts (hostname, cluster_name, namespace_name, cloud_provider, instance_type, vcpu_allocated, memory_gb_allocated) VALUES
('eks-prod-a1','eks-prod-cluster-a','payments','AWS','m6i.2xlarge',8,32),
('eks-prod-a2','eks-prod-cluster-a','risk','AWS','m6i.2xlarge',8,32),
('eks-prod-b1','eks-prod-cluster-b','retail','AWS','m5.2xlarge',8,32),
('eks-prod-b2','eks-prod-cluster-b','data','AWS','m5.4xlarge',16,64)
ON CONFLICT (hostname) DO NOTHING;

INSERT INTO capacity_thresholds (service_id, cpu_warn_pct, cpu_crit_pct, mem_warn_pct, mem_crit_pct, p95_latency_warn_ms, p95_latency_crit_ms, max_error_rate_pct)
SELECT service_id,
       CASE service_name
         WHEN 'payments-api' THEN 70 WHEN 'risk-engine' THEN 72
         WHEN 'customer-profile' THEN 68 ELSE 65 END,
       CASE service_name
         WHEN 'payments-api' THEN 85 WHEN 'risk-engine' THEN 88
         WHEN 'customer-profile' THEN 82 ELSE 80 END,
       75, 90,
       CASE service_name
         WHEN 'payments-api' THEN 280 WHEN 'risk-engine' THEN 320
         WHEN 'customer-profile' THEN 250 ELSE 400 END,
       CASE service_name
         WHEN 'payments-api' THEN 400 WHEN 'risk-engine' THEN 450
         WHEN 'customer-profile' THEN 350 ELSE 600 END,
       2.50
FROM services s
WHERE NOT EXISTS (
  SELECT 1 FROM capacity_thresholds c WHERE c.service_id = s.service_id
);

INSERT INTO deployments (service_id, deployed_at, version, change_type, expected_impact, initiated_by)
SELECT service_id, '2026-05-01 14:00:00+00',
       CASE service_name
         WHEN 'payments-api' THEN 'v2.3.0'
         WHEN 'risk-engine' THEN 'v1.18.4'
         WHEN 'customer-profile' THEN 'v3.2.1'
         ELSE 'v4.0.0' END,
       'release',
       'performance and stability updates',
       'release-bot'
FROM services;

INSERT INTO incidents (service_id, host_id, started_at, ended_at, severity, summary, capacity_related)
SELECT s.service_id, h.host_id,
       '2026-05-02 10:00:00+00', '2026-05-02 10:30:00+00',
       'SEV2', 'CPU saturation caused request latency spike', TRUE
FROM services s JOIN hosts h ON s.service_name = 'payments-api' AND h.hostname = 'eks-prod-a1'
WHERE NOT EXISTS (SELECT 1 FROM incidents i WHERE i.summary = 'CPU saturation caused request latency spike');

WITH series AS (
  SELECT generate_series('2026-05-01 00:00:00+00'::timestamptz,
                         '2026-05-03 23:00:00+00'::timestamptz,
                         interval '1 hour') AS sampled_at
),
svc AS (
  SELECT s.service_id, s.service_name,
         CASE s.service_name
           WHEN 'payments-api' THEN 1
           WHEN 'risk-engine' THEN 2
           WHEN 'customer-profile' THEN 3
           ELSE 4 END AS host_pick
  FROM services s
),
h AS (
  SELECT host_id, ROW_NUMBER() OVER (ORDER BY host_id) AS rn FROM hosts
)
INSERT INTO telemetry_samples (
  service_id, host_id, sampled_at, cpu_utilization_pct, memory_utilization_pct,
  p95_latency_ms, requests_per_min, error_rate_pct,
  allocated_cpu_cores, allocated_memory_gb,
  actual_cpu_cores, actual_memory_gb,
  forecast_cpu_pct, forecast_memory_pct, cloud_cost_usd, tags
)
SELECT
  svc.service_id,
  h.host_id,
  series.sampled_at,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 62 + 14 * SIN(EXTRACT(EPOCH FROM series.sampled_at)/43200)
      WHEN 'risk-engine' THEN 58 + 18 * SIN(EXTRACT(EPOCH FROM series.sampled_at)/43200)
      WHEN 'customer-profile' THEN 46 + 10 * SIN(EXTRACT(EPOCH FROM series.sampled_at)/43200)
      ELSE 40 + 8 * SIN(EXTRACT(EPOCH FROM series.sampled_at)/43200)
    END
    + CASE WHEN series.sampled_at BETWEEN '2026-05-02 10:00:00+00' AND '2026-05-02 11:00:00+00'
           AND svc.service_name='payments-api' THEN 20 ELSE 0 END
  )::numeric, 2) AS cpu_utilization_pct,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 64 + 11 * COS(EXTRACT(EPOCH FROM series.sampled_at)/57600)
      WHEN 'risk-engine' THEN 60 + 9 * COS(EXTRACT(EPOCH FROM series.sampled_at)/57600)
      WHEN 'customer-profile' THEN 52 + 8 * COS(EXTRACT(EPOCH FROM series.sampled_at)/57600)
      ELSE 48 + 7 * COS(EXTRACT(EPOCH FROM series.sampled_at)/57600)
    END
  )::numeric, 2) AS memory_utilization_pct,
  (
    CASE svc.service_name
      WHEN 'payments-api' THEN 220
      WHEN 'risk-engine' THEN 270
      WHEN 'customer-profile' THEN 190
      ELSE 300
    END
    + (ABS(SIN(EXTRACT(EPOCH FROM series.sampled_at)/36000)) * 100)::int
    + CASE WHEN series.sampled_at BETWEEN '2026-05-02 10:00:00+00' AND '2026-05-02 11:00:00+00'
           AND svc.service_name='payments-api' THEN 130 ELSE 0 END
  ) AS p95_latency_ms,
  (
    CASE svc.service_name
      WHEN 'payments-api' THEN 980
      WHEN 'risk-engine' THEN 760
      WHEN 'customer-profile' THEN 840
      ELSE 420
    END
    + (ABS(COS(EXTRACT(EPOCH FROM series.sampled_at)/21600))*120)::int
  ) AS requests_per_min,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 0.60
      WHEN 'risk-engine' THEN 0.80
      WHEN 'customer-profile' THEN 0.45
      ELSE 0.70
    END
    + (ABS(SIN(EXTRACT(EPOCH FROM series.sampled_at)/43200)) * 0.6)
    + CASE WHEN series.sampled_at BETWEEN '2026-05-02 10:00:00+00' AND '2026-05-02 11:00:00+00'
           AND svc.service_name='payments-api' THEN 1.30 ELSE 0 END
  )::numeric, 2) AS error_rate_pct,
  CASE svc.service_name
    WHEN 'analytics-batch' THEN 10 ELSE 6 END AS allocated_cpu_cores,
  CASE svc.service_name
    WHEN 'analytics-batch' THEN 40 ELSE 24 END AS allocated_memory_gb,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 3.8
      WHEN 'risk-engine' THEN 3.5
      WHEN 'customer-profile' THEN 2.6
      ELSE 3.0
    END
    + ABS(SIN(EXTRACT(EPOCH FROM series.sampled_at)/64800))
  )::numeric,2) AS actual_cpu_cores,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 12.5
      WHEN 'risk-engine' THEN 11.8
      WHEN 'customer-profile' THEN 9.4
      ELSE 13.1
    END
    + ABS(COS(EXTRACT(EPOCH FROM series.sampled_at)/64800))*2
  )::numeric,2) AS actual_memory_gb,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 66
      WHEN 'risk-engine' THEN 63
      WHEN 'customer-profile' THEN 50
      ELSE 45
    END
  )::numeric,2) AS forecast_cpu_pct,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 67
      WHEN 'risk-engine' THEN 62
      WHEN 'customer-profile' THEN 54
      ELSE 50
    END
  )::numeric,2) AS forecast_memory_pct,
  ROUND((
    CASE svc.service_name
      WHEN 'payments-api' THEN 8.5
      WHEN 'risk-engine' THEN 7.3
      WHEN 'customer-profile' THEN 6.2
      ELSE 9.4
    END
    + ABS(SIN(EXTRACT(EPOCH FROM series.sampled_at)/86400))
  )::numeric,2) AS cloud_cost_usd,
  jsonb_build_object(
    'team', (SELECT team_name FROM services s2 WHERE s2.service_id = svc.service_id),
    'env', 'prod',
    'region', 'us-west-2'
  )
FROM series
JOIN svc ON TRUE
JOIN h ON h.rn = svc.host_pick
WHERE NOT EXISTS (
  SELECT 1 FROM telemetry_samples t
  WHERE t.service_id = svc.service_id AND t.sampled_at = series.sampled_at
);

COMMIT;
