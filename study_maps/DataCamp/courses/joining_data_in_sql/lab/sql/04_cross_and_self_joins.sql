SET search_path TO joining_data_lab;

-- 1. CROSS JOIN: every country-year combination
SELECT c.code,
       c.name,
       y.year
FROM countries AS c
CROSS JOIN (
    VALUES (2010), (2015)
) AS y(year)
ORDER BY c.code, y.year;

-- 2. Expected row count
SELECT
    (SELECT COUNT(*) FROM countries) AS country_rows,
    2 AS year_rows,
    (SELECT COUNT(*) FROM countries) * 2 AS expected_cross_join_rows;

-- 3. Broad self join showing row multiplication
SELECT p1.country_code,
       p1.year AS year_1,
       p2.year AS year_2,
       p1.size AS size_1,
       p2.size AS size_2
FROM populations AS p1
INNER JOIN populations AS p2
  ON p1.country_code = p2.country_code
ORDER BY p1.country_code, p1.year, p2.year;

-- 4. Correct self join for 2010 versus 2015
SELECT p1.country_code,
       p1.size AS size2010,
       p2.size AS size2015,
       p2.size - p1.size AS growth
FROM populations AS p1
INNER JOIN populations AS p2
  ON p1.country_code = p2.country_code
 AND p1.year = 2010
 AND p2.year = 2015
ORDER BY p1.country_code;

-- 5. Alternative using conditional aggregation
SELECT country_code,
       MAX(size) FILTER (WHERE year = 2010) AS size2010,
       MAX(size) FILTER (WHERE year = 2015) AS size2015,
       MAX(size) FILTER (WHERE year = 2015)
       - MAX(size) FILTER (WHERE year = 2010) AS growth
FROM populations
GROUP BY country_code
ORDER BY country_code;
