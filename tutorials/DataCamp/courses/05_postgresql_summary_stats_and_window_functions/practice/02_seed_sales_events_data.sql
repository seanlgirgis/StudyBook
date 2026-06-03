-- 02_seed_sales_events_data.sql
-- Seed realistic practice data (100 rows) with 4 events per day, mixed revenue patterns, and same-day ties.

INSERT INTO course05_sales_events (
    event_id,
    sale_date,
    region,
    store_id,
    salesperson,
    product_category,
    revenue,
    units_sold,
    customer_score
)
SELECT
    gs AS event_id,
    DATE '2025-01-01' + ((gs - 1) % 25) AS sale_date,
    CASE ((gs - 1) % 4)
        WHEN 0 THEN 'North'
        WHEN 1 THEN 'South'
        WHEN 2 THEN 'East'
        ELSE 'West'
    END AS region,
    CASE ((gs - 1) % 4)
        WHEN 0 THEN (101 + ((gs - 1) % 3))
        WHEN 1 THEN (201 + ((gs - 1) % 3))
        WHEN 2 THEN (301 + ((gs - 1) % 3))
        ELSE (401 + ((gs - 1) % 3))
    END AS store_id,
    (ARRAY['Alex Kim','Sam Patel','Jordan Lee','Taylor Chen','Morgan Diaz','Riley Brooks'])[((gs - 1) % 6) + 1] AS salesperson,
    (ARRAY['Electronics','Home','Clothing','Sports','Beauty'])[((gs - 1) % 5) + 1] AS product_category,
    (
        CASE
            -- Keep one clear teaching day: 900, 700, 700, 400 on 2025-01-01
            WHEN ((gs - 1) % 25) = 0 AND ((gs - 1) % 4) = 0 THEN 900
            WHEN ((gs - 1) % 25) = 0 AND ((gs - 1) % 4) IN (1, 2) THEN 700
            WHEN ((gs - 1) % 25) = 0 AND ((gs - 1) % 4) = 3 THEN 400
            -- Mixed pattern by date + region + event to avoid smooth trends and keep ties within each day
            WHEN ((gs - 1) % 4) = 0 THEN (430 + ((((gs - 1) % 25) * 73 + 17) % 48) * 10)
            WHEN ((gs - 1) % 4) IN (1, 2) THEN (380 + ((((gs - 1) % 25) * 61 + 29) % 44) * 10)
            ELSE (260 + ((((gs - 1) % 25) * 47 + 11) % 38) * 10)
        END
    )::numeric AS revenue,
    (2 + ((gs * 2) % 14)) AS units_sold,
    (62 + ((gs * 7) % 37)) AS customer_score
FROM generate_series(1, 100) AS gs;