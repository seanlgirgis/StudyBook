-- DataCamp Project: Analyzing Students' Mental Health
-- File: lab/sql/03_practice_queries.sql
--
-- Purpose:
--   Extra practice queries for understanding the students dataset
--   and reinforcing the SQL patterns used in the project.

-- ============================================================
-- 1. Inspect the table
-- ============================================================

SELECT *
FROM students
LIMIT 10;


-- ============================================================
-- 2. Count all rows
-- ============================================================

SELECT COUNT(*) AS total_students
FROM students;


-- ============================================================
-- 3. Count international and domestic students
-- ============================================================

SELECT
    inter_dom,
    COUNT(*) AS student_count
FROM students
GROUP BY inter_dom
ORDER BY student_count DESC;


-- ============================================================
-- 4. Check for missing values in the project columns
-- ============================================================

SELECT
    COUNT(*) FILTER (WHERE inter_dom IS NULL) AS missing_inter_dom,
    COUNT(*) FILTER (WHERE stay IS NULL) AS missing_stay,
    COUNT(*) FILTER (WHERE todep IS NULL) AS missing_todep,
    COUNT(*) FILTER (WHERE tosc IS NULL) AS missing_tosc,
    COUNT(*) FILTER (WHERE toas IS NULL) AS missing_toas
FROM students;


-- ============================================================
-- 5. Count international students by length of stay
-- ============================================================

SELECT
    stay,
    COUNT(*) AS international_students
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
GROUP BY stay
ORDER BY stay DESC;


-- ============================================================
-- 6. Reproduce the project averages without a CTE
-- ============================================================

SELECT
    stay,
    COUNT(*) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
  AND stay IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL
GROUP BY stay
ORDER BY stay DESC;


-- ============================================================
-- 7. Compare international and domestic students
-- ============================================================

SELECT
    inter_dom,
    COUNT(*) AS student_count,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL
GROUP BY inter_dom
ORDER BY inter_dom;


-- ============================================================
-- 8. Compare average scores by gender for international students
-- ============================================================

SELECT
    gender,
    COUNT(*) AS student_count,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
  AND gender IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL
GROUP BY gender
ORDER BY student_count DESC;


-- ============================================================
-- 9. Compare average scores by age group
-- ============================================================

SELECT
    age,
    COUNT(*) AS student_count,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
  AND age IS NOT NULL
  AND todep IS NOT NULL
  AND tosc IS NOT NULL
  AND toas IS NOT NULL
GROUP BY age
HAVING COUNT(*) >= 3
ORDER BY age;


-- ============================================================
-- 10. Find stay groups with above-average depression scores
-- ============================================================

WITH stay_scores AS (
    SELECT
        stay,
        COUNT(*) AS student_count,
        AVG(todep) AS average_phq
    FROM students
    WHERE inter_dom = 'Inter'
      AND stay IS NOT NULL
      AND todep IS NOT NULL
    GROUP BY stay
),
overall_score AS (
    SELECT AVG(todep) AS overall_average_phq
    FROM students
    WHERE inter_dom = 'Inter'
      AND todep IS NOT NULL
)
SELECT
    s.stay,
    s.student_count,
    ROUND(s.average_phq, 2) AS average_phq,
    ROUND(o.overall_average_phq, 2) AS overall_average_phq
FROM stay_scores AS s
CROSS JOIN overall_score AS o
WHERE s.average_phq > o.overall_average_phq
ORDER BY s.average_phq DESC;


-- ============================================================
-- 11. Rank stay groups by average acculturative stress
-- ============================================================

WITH stay_scores AS (
    SELECT
        stay,
        COUNT(*) AS student_count,
        ROUND(AVG(toas), 2) AS average_as
    FROM students
    WHERE inter_dom = 'Inter'
      AND stay IS NOT NULL
      AND toas IS NOT NULL
    GROUP BY stay
)
SELECT
    stay,
    student_count,
    average_as,
    DENSE_RANK() OVER (ORDER BY average_as DESC) AS stress_rank
FROM stay_scores
ORDER BY stress_rank, stay DESC;


-- ============================================================
-- 12. Practice task
-- ============================================================
--
-- Write a query that:
--   1. Filters to international students.
--   2. Groups by stay.
--   3. Returns only stay groups with at least 5 students.
--   4. Shows the average PHQ, SCS, and AS scores.
--   5. Orders the result by average PHQ from highest to lowest.
--
-- Write your answer below:

-- SELECT
-- FROM
-- WHERE
-- GROUP BY
-- HAVING
-- ORDER BY
