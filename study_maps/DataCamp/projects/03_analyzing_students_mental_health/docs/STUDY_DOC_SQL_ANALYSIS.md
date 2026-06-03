# Study Doc: SQL Analysis of Students' Mental Health

## 1. Project question in plain English

This project asks a focused question:

For international students, does length of stay relate to average depression, social connectedness, and acculturative stress scores?

In this analysis, `stay` acts like a year-by-year bucket: 1 year, 2 years, 3 years, and so on.

## 2. Important fields

`inter_dom`
- student type
- `Inter` = international student
- `Dom` = domestic student

`stay`
- number of years the student stayed

`todep`
- total depression score
- higher means more depression symptoms

`tosc`
- total social connectedness score
- higher means stronger social connectedness

`toas`
- total acculturative stress score
- higher means more acculturative stress

## 3. Inspect the table fields

```sql
SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'students'
ORDER BY ordinal_position;
```

This query lists each column name and its data type so you can verify the table structure before analysis.

## 4. Count missing values in one field

```sql
SELECT
    COUNT(*) - COUNT(inter_dom) AS inter_dom_missing
FROM public.students;
```

How it works:
- `COUNT(*)` counts all rows.
- `COUNT(inter_dom)` counts only rows where `inter_dom` is not `NULL`.
- The difference is the number of missing values.

Known example:
- 286 total rows - 268 non-null `inter_dom` rows = 18 missing rows.

## 5. Count missing values across important fields

```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN inter_dom IS NULL THEN 1 ELSE 0 END) AS missing_inter_dom,
    SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS missing_region,
    SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS missing_gender,
    SUM(CASE WHEN academic IS NULL THEN 1 ELSE 0 END) AS missing_academic,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS missing_age,
    SUM(CASE WHEN stay IS NULL THEN 1 ELSE 0 END) AS missing_stay
FROM public.students;
```

`CASE` pattern explanation:
- If the field is `NULL`, count `1`.
- Otherwise count `0`.
- `SUM(...)` adds those 1s to get the number of missing rows.

## 6. Clean working data with a CTE

```sql
WITH clean_international_students AS (
    SELECT
        stay,
        todep,
        tosc,
        toas
    FROM public.students
    WHERE inter_dom = 'Inter'
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
FROM clean_international_students
GROUP BY stay
ORDER BY stay DESC;
```

Explanation:
- The CTE creates a clean temporary working table.
- It keeps only international students.
- It removes rows missing the fields needed for analysis.
- The outer query groups by `stay`.
- Each `stay` value is a bucket.
- The query calculates count and averages per bucket.

## 7. How the final query works line by line

- `WITH clean_international_students AS (...)`: builds a clean subset first.
- `SELECT stay`: returns the stay bucket in each output row.
- `COUNT(*) AS count_int`: counts international students in that stay bucket.
- `ROUND(AVG(todep), 2)`: computes average depression score and rounds to 2 decimals.
- `ROUND(AVG(tosc), 2)`: computes average social connectedness score and rounds to 2 decimals.
- `ROUND(AVG(toas), 2)`: computes average acculturative stress score and rounds to 2 decimals.
- `FROM clean_international_students`: uses only the cleaned dataset.
- `GROUP BY stay`: creates one result row per stay bucket.
- `ORDER BY stay DESC`: sorts from longest stay to shortest stay.

## 8. Final answer in plain English

The final result shows one row per length-of-stay group. For each group, it shows how many international students are in that group and the average depression, social connectedness, and acculturative stress scores.

## 9. SQL patterns learned

- Inspect table metadata with `information_schema.columns`
- `COUNT(*)` vs `COUNT(column)`
- Missing-value counting with `CASE WHEN`
- Cleaning records with a CTE
- Filtering with `WHERE`
- Grouping with `GROUP BY`
- Aggregating with `COUNT` and `AVG`
- Rounding numeric results with `ROUND`
- Sorting output with `ORDER BY`

## 10. Interview-safe summary

I started by inspecting the table structure and checking missing values. Then I created a clean working set of international student records using a CTE. After that, I grouped students by length of stay and calculated average depression, social connectedness, and acculturative stress scores for each stay group. This turned the raw student table into a clear year-by-year mental health analysis.

## 11. Practice extensions

### A. Table structure with nullable flag

```sql
SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'students'
ORDER BY ordinal_position;```
```


## 12. Local environment access (this project)

Use this command to connect to PostgreSQL from command line:

```bash
psql -h localhost -p 5432 -U obs_user -d observability
```

When prompted, enter the database password for `obs_user`.

After connecting, the main table for this project is:

- `public.students`

Quick check commands after login:

```sql
\dt
SELECT COUNT(*) FROM public.students;
SELECT * FROM public.students LIMIT 5;
```
