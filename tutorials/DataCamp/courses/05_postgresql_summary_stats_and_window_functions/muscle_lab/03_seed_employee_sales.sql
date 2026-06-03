-- 03_seed_employee_sales.sql
-- Seeds employee monthly sales (240 rows) for ranking/interview drills.

WITH months AS (
    SELECT generate_series(DATE '2025-01-01', DATE '2025-08-01', INTERVAL '1 month')::date AS sale_month
),
roster AS (
    SELECT * FROM (VALUES
      ('Data Engineering','Nora Diaz'),('Data Engineering','Avi Gupta'),('Data Engineering','Leah Kim'),('Data Engineering','Evan Stone'),('Data Engineering','Mila Tran'),('Data Engineering','Omar Ali'),
      ('Cloud Platform','Ivy Chen'),('Cloud Platform','Noah Park'),('Cloud Platform','Zoe Miller'),('Cloud Platform','Liam Cole'),('Cloud Platform','Maya Reed'),('Cloud Platform','Ian Flores'),
      ('Observability','Ella Ross'),('Observability','Kai Brooks'),('Observability','Rina Shah'),('Observability','Theo Ward'),('Observability','Asha Raman'),('Observability','Jules Kent'),
      ('Support','Ben Ortiz'),('Support','Nina Costa'),('Support','Ravi Singh'),('Support','Sara Moon'),('Support','Joel Price'),('Support','Tina Lowe'),
      ('Security','Aria Fox'),('Security','Mason Hale'),('Security','Priya Nair'),('Security','Gabe Hunt'),('Security','Lena Park'),('Security','Drew Bell')
    ) AS t(department, salesperson)
)
INSERT INTO course05_muscle.employee_sales (
    sale_id, sale_month, department, salesperson, sales_amount, deal_count
)
SELECT
    ROW_NUMBER() OVER (ORDER BY m.sale_month, r.department, r.salesperson) AS sale_id,
    m.sale_month,
    r.department,
    r.salesperson,
    ROUND(
      (
        22000
        + ((ROW_NUMBER() OVER (ORDER BY m.sale_month, r.department, r.salesperson) * 137) % 18000)
        + CASE WHEN EXTRACT(MONTH FROM m.sale_month) IN (3,6) THEN 2200 ELSE 0 END
        + CASE WHEN ROW_NUMBER() OVER (ORDER BY m.sale_month, r.department, r.salesperson) % 10 = 0 THEN 1000 ELSE 0 END
      )::numeric,
      2
    ) AS sales_amount,
    4 + ((ROW_NUMBER() OVER (ORDER BY m.sale_month, r.department, r.salesperson) * 5) % 22) AS deal_count
FROM months m
CROSS JOIN roster r;
