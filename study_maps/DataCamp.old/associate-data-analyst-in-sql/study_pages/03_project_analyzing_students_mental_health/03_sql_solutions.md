## Local PostgreSQL SQL Analysis Ladder - First Pass

### 1) Select sample rows
```sql
SELECT *
FROM students
LIMIT 10;
```

### 2) Count rows
```sql
SELECT COUNT(*) AS total_rows
FROM students;
```

### 3) Inspect columns via information_schema
```sql
SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'students'
ORDER BY ordinal_position;
```

### 4) Missing-value checks
```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN inter_dom IS NULL THEN 1 ELSE 0 END) AS null_inter_dom,
    SUM(CASE WHEN stay IS NULL THEN 1 ELSE 0 END) AS null_stay,
    SUM(CASE WHEN todep IS NULL THEN 1 ELSE 0 END) AS null_todep,
    SUM(CASE WHEN tosc IS NULL THEN 1 ELSE 0 END) AS null_tosc,
    SUM(CASE WHEN toas IS NULL THEN 1 ELSE 0 END) AS null_toas
FROM students;
```

### 5) Category counts
```sql
SELECT inter_dom, COUNT(*) AS row_count
FROM students
GROUP BY inter_dom
ORDER BY row_count DESC;

SELECT academic, COUNT(*) AS row_count
FROM students
GROUP BY academic
ORDER BY row_count DESC;
```

### 6) Score ranges
```sql
SELECT
    MIN(todep) AS min_todep,
    MAX(todep) AS max_todep,
    MIN(tosc) AS min_tosc,
    MAX(tosc) AS max_tosc,
    MIN(toas) AS min_toas,
    MAX(toas) AS max_toas
FROM students;
```

### 7) Averages by inter_dom
```sql
SELECT
    inter_dom,
    ROUND(AVG(todep), 2) AS avg_todep,
    ROUND(AVG(tosc), 2) AS avg_tosc,
    ROUND(AVG(toas), 2) AS avg_toas,
    COUNT(*) AS row_count
FROM students
GROUP BY inter_dom
ORDER BY inter_dom;
```

### 8) Averages by stay
```sql
SELECT
    stay,
    ROUND(AVG(todep), 2) AS avg_todep,
    ROUND(AVG(tosc), 2) AS avg_tosc,
    ROUND(AVG(toas), 2) AS avg_toas,
    COUNT(*) AS row_count
FROM students
GROUP BY stay
ORDER BY stay;
```

### 9) International-only stay analysis
```sql
SELECT
    stay,
    COUNT(*) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
GROUP BY stay
ORDER BY stay;
```

### 10) Final project-style query
```sql
SELECT
    stay,
    COUNT(*) AS count_int,
    ROUND(AVG(todep), 2) AS average_phq,
    ROUND(AVG(tosc), 2) AS average_scs,
    ROUND(AVG(toas), 2) AS average_as
FROM students
WHERE inter_dom = 'Inter'
GROUP BY stay
ORDER BY stay DESC;
```
