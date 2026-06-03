-- 02_seed_sales_events.sql
-- Seeds realistic sales events (360 rows) for window-function practice.

INSERT INTO course05_muscle.sales_events (
    sale_id, sale_date, region, salesperson, product_category, revenue, units, channel
)
SELECT
    gs AS sale_id,
    DATE '2026-01-01' + ((gs - 1) % 120) AS sale_date,
    (ARRAY['North','South','East','West'])[((gs - 1) % 4) + 1] AS region,
    (ARRAY['Alex Kim','Sam Patel','Jordan Lee','Taylor Chen','Morgan Diaz','Riley Brooks','Casey Nguyen','Jamie Clark'])[((gs - 1) % 8) + 1] AS salesperson,
    (ARRAY['Cloud','Database','Security','Analytics','Support'])[((gs - 1) % 5) + 1] AS product_category,
    ROUND(
      (
        550
        + ((gs * 41) % 900)
        + CASE WHEN ((gs - 1) % 30) BETWEEN 18 AND 24 THEN 180 ELSE 0 END
        + CASE WHEN gs % 53 = 0 THEN 700 ELSE 0 END
        - CASE WHEN gs % 47 = 0 THEN 260 ELSE 0 END
        + CASE WHEN gs % 9 = 0 THEN 25 ELSE 0 END
      )::numeric,
      2
    ) AS revenue,
    1 + ((gs * 3) % 18) AS units,
    (ARRAY['Direct','Partner','Online'])[((gs - 1) % 3) + 1] AS channel
FROM generate_series(1, 360) AS gs;
