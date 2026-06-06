SET search_path TO joining_data_lab;

-- 1. Semi join with IN
SELECT name
FROM countries
WHERE code IN (
    SELECT country_code
    FROM economies
    WHERE country_code IS NOT NULL
)
ORDER BY name;

-- 2. Semi join with EXISTS
SELECT c.name
FROM countries AS c
WHERE EXISTS (
    SELECT 1
    FROM economies AS e
    WHERE e.country_code = c.code
)
ORDER BY c.name;

-- 3. Anti join with NOT EXISTS
SELECT c.name
FROM countries AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM economies AS e
    WHERE e.country_code = c.code
)
ORDER BY c.name;

-- 4. Anti join with LEFT JOIN
SELECT c.name
FROM countries AS c
LEFT JOIN economies AS e
  ON c.code = e.country_code
WHERE e.country_code IS NULL
ORDER BY c.name;

-- 5. Demonstrate NOT IN / NULL trap
SELECT name
FROM countries
WHERE code NOT IN (
    SELECT country_code
    FROM economies
);

-- 6. Corrected NOT IN version
SELECT name
FROM countries
WHERE code NOT IN (
    SELECT country_code
    FROM economies
    WHERE country_code IS NOT NULL
)
ORDER BY name;

-- 7. Scalar subquery in WHERE
SELECT name,
       population
FROM cities
WHERE population > (
    SELECT AVG(population)
    FROM cities
)
ORDER BY population DESC;

-- 8. Correlated scalar subquery in SELECT
SELECT c.name,
       (
           SELECT COUNT(*)
           FROM cities AS ci
           WHERE ci.country_code = c.code
       ) AS city_count
FROM countries AS c
ORDER BY c.name;

-- 9. Subquery in FROM
SELECT region,
       AVG(country_population) AS average_population
FROM (
    SELECT region,
           population AS country_population
    FROM countries
    WHERE population IS NOT NULL
) AS country_data
GROUP BY region
ORDER BY region;
