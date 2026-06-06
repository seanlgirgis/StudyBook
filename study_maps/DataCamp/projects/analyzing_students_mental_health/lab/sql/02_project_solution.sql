-- DataCamp Project: Analyzing Students' Mental Health
-- File: lab/sql/02_project_solution.sql
--
-- Goal:
--   Analyze how length of stay affects average mental-health scores
--   for international students.
--
-- Expected result:
--   9 rows and 5 columns, ordered by stay descending.

WITH clean_students AS (
    SELECT *
    FROM students
    WHERE inter_dom IS NOT NULL
      AND stay IS NOT NULL
      AND todep IS NOT NULL
      AND tosc IS NOT NULL
      AND toas IS NOT NULL
)
SELECT
    stay,
    COUNT(*) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM clean_students
WHERE inter_dom = 'Inter'
GROUP BY stay
ORDER BY stay DESC;

-- Validation checks

-- Count international-student rows used by the project.
SELECT COUNT(*) AS international_rows
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL;

-- Confirm the number of stay groups returned.
SELECT COUNT(DISTINCT stay) AS stay_groups
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL;
