SET search_path TO joining_data_lab;

-- 1. Basic INNER JOIN
SELECT c.code,
       c.name,
       p.year,
       p.size
FROM countries AS c
INNER JOIN populations AS p
  ON c.code = p.country_code
ORDER BY c.code, p.year;

-- 2. USING when the key name matches
SELECT code,
       c.name,
       e.year,
       e.gdp_percapita
FROM countries AS c
INNER JOIN economies AS e
  USING (code);

-- 3. Three-table join with a complete key
SELECT c.name,
       p.year,
       p.size,
       e.gdp_percapita
FROM countries AS c
INNER JOIN populations AS p
  ON c.code = p.country_code
INNER JOIN economies AS e
  ON c.code = e.country_code
 AND p.year = e.year
ORDER BY c.code, p.year;

-- 4. LEFT JOIN preserves every country
SELECT c.code,
       c.name,
       e.year,
       e.gdp_percapita
FROM countries AS c
LEFT JOIN economies AS e
  ON c.code = e.country_code
ORDER BY c.code, e.year;

-- 5. WHERE removes unmatched rows
SELECT c.code,
       c.name,
       e.year
FROM countries AS c
LEFT JOIN economies AS e
  ON c.code = e.country_code
WHERE e.year = 2015
ORDER BY c.code;

-- 6. ON preserves unmatched rows while restricting matches
SELECT c.code,
       c.name,
       e.year
FROM countries AS c
LEFT JOIN economies AS e
  ON c.code = e.country_code
 AND e.year = 2015
ORDER BY c.code;

-- 7. FULL JOIN reconciliation
SELECT c.code AS country_code,
       c.name,
       e.country_code AS economy_code,
       e.year
FROM countries AS c
FULL JOIN economies AS e
  ON c.code = e.country_code
ORDER BY COALESCE(c.code, e.country_code), e.year;

-- 8. Find unmatched rows from either side
SELECT c.code AS country_code,
       e.country_code AS economy_code
FROM countries AS c
FULL JOIN economies AS e
  ON c.code = e.country_code
WHERE c.code IS NULL
   OR e.country_code IS NULL;
