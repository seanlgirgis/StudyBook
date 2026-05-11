# 010 - Occupations

## Source

HackerRank SQL - Advanced Select

## Problem Summary

Pivot the `Occupation` column in the `OCCUPATIONS` table so names are displayed under four columns in this exact order: `Doctor`, `Professor`, `Singer`, `Actor`. Names under each occupation must be sorted alphabetically. If an occupation has fewer names than another occupation, output `NULL` for the missing cells.

## Schema

`OCCUPATIONS`
- `Name String`
- `Occupation String`

## Accepted Solution

```sql
WITH Doc AS (
    SELECT ROW_NUMBER() OVER (ORDER BY Name) AS rn, Name
    FROM OCCUPATIONS
    WHERE Occupation = 'Doctor'
),
Prof AS (
    SELECT ROW_NUMBER() OVER (ORDER BY Name) AS rn, Name
    FROM OCCUPATIONS
    WHERE Occupation = 'Professor'
),
Singer AS (
    SELECT ROW_NUMBER() OVER (ORDER BY Name) AS rn, Name
    FROM OCCUPATIONS
    WHERE Occupation = 'Singer'
),
Actor AS (
    SELECT ROW_NUMBER() OVER (ORDER BY Name) AS rn, Name
    FROM OCCUPATIONS
    WHERE Occupation = 'Actor'
),
AllRows AS (
    SELECT rn FROM Doc
    UNION
    SELECT rn FROM Prof
    UNION
    SELECT rn FROM Singer
    UNION
    SELECT rn FROM Actor
)
SELECT
    Doc.Name AS Doctor,
    Prof.Name AS Professor,
    Singer.Name AS Singer,
    Actor.Name AS Actor
FROM AllRows
LEFT JOIN Doc    ON AllRows.rn = Doc.rn
LEFT JOIN Prof   ON AllRows.rn = Prof.rn
LEFT JOIN Singer ON AllRows.rn = Singer.rn
LEFT JOIN Actor  ON AllRows.rn = Actor.rn
ORDER BY AllRows.rn;
```

## Provided Solution Reviewed

The provided SQL solution is correct for MySQL 8+ and should pass if the HackerRank runtime supports CTEs and `ROW_NUMBER()`.

### What is good

- Each occupation is isolated into its own CTE.
- `ROW_NUMBER() OVER (ORDER BY Name)` gives each name a rank inside its occupation.
- The names are ranked alphabetically.
- `AllRows` creates the full set of row numbers needed for the final output.
- `LEFT JOIN` keeps rows even when a specific occupation has no name for that `rn`.
- Missing values naturally appear as `NULL`.
- The final `SELECT` outputs columns in the required order: `Doctor`, `Professor`, `Singer`, `Actor`.
- `ORDER BY AllRows.rn` keeps the rows aligned from first alphabetic name to last.

## Plain-English Explanation

The table starts in vertical form:

`Name | Occupation`

The task wants pivoted form:

`Doctor | Professor | Singer | Actor`

The solution creates four alphabetically ranked occupation lists, then joins them by row number (`rn`).

So row 1 contains first doctor, first professor, first singer, first actor.
Row 2 contains second doctor, second professor, second singer, second actor.
If a list is shorter, that cell is `NULL`.

## Important Learning Notes

- `ROW_NUMBER()` assigns sequence numbers to rows.
- `ORDER BY Name` inside `ROW_NUMBER()` ensures alphabetical ranking.
- CTEs can make complex pivot logic easier to read.
- `UNION` builds a complete row-number list.
- `LEFT JOIN` preserves all `rn` values from `AllRows`.
- This is a pivot-style SQL problem.

## Alternative Compact Pivot Solution

```sql
WITH Ranked AS (
    SELECT
        Name,
        Occupation,
        ROW_NUMBER() OVER (PARTITION BY Occupation ORDER BY Name) AS rn
    FROM OCCUPATIONS
)
SELECT
    MAX(CASE WHEN Occupation = 'Doctor' THEN Name END) AS Doctor,
    MAX(CASE WHEN Occupation = 'Professor' THEN Name END) AS Professor,
    MAX(CASE WHEN Occupation = 'Singer' THEN Name END) AS Singer,
    MAX(CASE WHEN Occupation = 'Actor' THEN Name END) AS Actor
FROM Ranked
GROUP BY rn
ORDER BY rn;
```

## Mistakes / Reminders

- Do not only `GROUP BY Occupation`; that gives one row per occupation, not the required pivot.
- Do not forget alphabetical sorting within each occupation.
- Do not forget required column order: `Doctor`, `Professor`, `Singer`, `Actor`.
- Do not use `INNER JOIN`, because missing rows would disappear instead of showing `NULL`.
- Do not order final output by name; order by row number.
- If using conditional aggregation, `GROUP BY rn` is required.
- If HackerRank runtime is older, verify `ROW_NUMBER()` support.
