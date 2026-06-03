SELECT COUNT(*) AS total_rows FROM students;

SELECT inter_dom, COUNT(*) AS row_count
FROM students
GROUP BY inter_dom
ORDER BY inter_dom;

SELECT MIN(stay) AS min_stay, MAX(stay) AS max_stay
FROM students;

SELECT stay, COUNT(*) AS count_international
FROM students
WHERE inter_dom = 'Inter'
GROUP BY stay
ORDER BY stay;

SELECT
    inter_dom,
    ROUND(AVG(todep)::numeric, 2) AS avg_todep,
    ROUND(AVG(tosc)::numeric, 2) AS avg_tosc,
    ROUND(AVG(toas)::numeric, 2) AS avg_toas
FROM students
GROUP BY inter_dom
ORDER BY inter_dom;

SELECT
    SUM(CASE WHEN inter_dom IS NULL THEN 1 ELSE 0 END) AS null_inter_dom,
    SUM(CASE WHEN stay IS NULL THEN 1 ELSE 0 END) AS null_stay,
    SUM(CASE WHEN todep IS NULL THEN 1 ELSE 0 END) AS null_todep,
    SUM(CASE WHEN tosc IS NULL THEN 1 ELSE 0 END) AS null_tosc,
    SUM(CASE WHEN toas IS NULL THEN 1 ELSE 0 END) AS null_toas
FROM students;

SELECT DISTINCT inter_dom FROM students ORDER BY inter_dom;
SELECT DISTINCT academic FROM students ORDER BY academic;
SELECT DISTINCT japanese_cate FROM students ORDER BY japanese_cate;
SELECT DISTINCT english_cate FROM students ORDER BY english_cate;
