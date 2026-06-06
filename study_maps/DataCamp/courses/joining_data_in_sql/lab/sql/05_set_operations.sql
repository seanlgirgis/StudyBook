SET search_path TO joining_data_lab;

-- 1. UNION removes duplicates
SELECT country_code
FROM populations

UNION

SELECT country_code
FROM economies
ORDER BY country_code;

-- 2. UNION ALL preserves duplicates
SELECT country_code
FROM populations

UNION ALL

SELECT country_code
FROM economies;

-- 3. Compare row counts
SELECT COUNT(*) AS union_count
FROM (
    SELECT country_code FROM populations
    UNION
    SELECT country_code FROM economies
) AS u;

SELECT COUNT(*) AS union_all_count
FROM (
    SELECT country_code FROM populations
    UNION ALL
    SELECT country_code FROM economies
) AS u;

-- 4. City names that are also country names
SELECT name
FROM cities

INTERSECT

SELECT name
FROM countries;

-- 5. Same logic with INNER JOIN
SELECT DISTINCT ci.name
FROM cities AS ci
INNER JOIN countries AS c
  ON ci.name = c.name;

-- 6. Economy keys missing from populations
SELECT country_code,
       year
FROM economies
WHERE country_code IS NOT NULL

EXCEPT

SELECT country_code,
       year
FROM populations;

-- 7. Reverse direction
SELECT country_code,
       year
FROM populations

EXCEPT

SELECT country_code,
       year
FROM economies
WHERE country_code IS NOT NULL;
