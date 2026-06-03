-- 06_seed_support_tickets.sql
-- Seeds support tickets (300 rows) for lag/lead/ranking/percentiles.

INSERT INTO course05_muscle.support_tickets (
    ticket_id, opened_ts, customer_segment, product_area, priority, status, assigned_team, resolution_minutes
)
SELECT
    gs AS ticket_id,
    TIMESTAMP '2026-03-01 08:00:00' + ((gs - 1) * INTERVAL '3 hour') AS opened_ts,
    (ARRAY['Enterprise','Midmarket','SMB'])[((gs - 1) % 3) + 1] AS customer_segment,
    (ARRAY['Login','Billing','Data Pipeline','Reporting','Security'])[((gs - 1) % 5) + 1] AS product_area,
    (ARRAY['P1','P2','P3','P4'])[((gs - 1) % 4) + 1] AS priority,
    (ARRAY['Resolved','Escalated','Closed'])[((gs - 1) % 3) + 1] AS status,
    (ARRAY['L1 Support','Platform','Data Engineering','Security Ops'])[((gs - 1) % 4) + 1] AS assigned_team,
    CASE ((gs - 1) % 4)
      WHEN 0 THEN 20 + ((gs * 7) % 180)
      WHEN 1 THEN 45 + ((gs * 9) % 280)
      WHEN 2 THEN 90 + ((gs * 11) % 420)
      ELSE 150 + ((gs * 13) % 720)
    END AS resolution_minutes
FROM generate_series(1, 300) AS gs;
