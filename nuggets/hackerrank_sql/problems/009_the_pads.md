# 009 - The PADS

## Source

HackerRank SQL - Advanced Select

## Problem Summary

Generate two result sets from the `OCCUPATIONS` table.

First result set:
Query all names alphabetically, immediately followed by the first letter of the occupation in parentheses.

Second result set:
Query the number of occurrences of each occupation and print each count in this sentence format:
`There are a total of [occupation_count] [occupation]s.`

The second result set should be ordered by occupation count ascending, then by occupation name alphabetically.

## Schema

`OCCUPATIONS`
- `Name String`
- `Occupation String`

## Accepted Solution

```sql
SELECT CONCAT(NAME, '(', LEFT(Occupation, 1), ')')
FROM OCCUPATIONS
ORDER BY NAME;

SELECT CONCAT('There are a total of ', COUNT(*), ' ', LOWER(Occupation), 's.')
FROM OCCUPATIONS
GROUP BY Occupation
ORDER BY COUNT(*), Occupation;
```

## Provided Solution Reviewed

The provided solution was very close.

Provided first query:

```sql
SELECT CONCAT(NAME ,'(', Left(Occupation,1),')')
FROM OCCUPATIONS
ORDER BY NAME;
```

This first query is correct.

### What is good

- `CONCAT` builds the required output string.
- `LEFT(Occupation, 1)` gets the first letter of the occupation.
- `ORDER BY NAME` sorts the names alphabetically.

Provided second query:

```sql
WITH TAB as (
SELECT COUNT(*) AS CNT, Occupation FROM OCCUPATIONS
GROUp BY Occupation
ORDER BY CNT ASC, Occupation ASC)
SELECT
CONCAT ('There are a total of ', CNT, ' ', lower(Occupation) , 's.')
FROM TAB;
```

The logic is correct, but for HackerRank MySQL it is safer and simpler to avoid the CTE and put the `ORDER BY` in the final grouped query.

Cleaner version:

```sql
SELECT CONCAT('There are a total of ', COUNT(*), ' ', LOWER(Occupation), 's.')
FROM OCCUPATIONS
GROUP BY Occupation
ORDER BY COUNT(*), Occupation;
```

## Plain-English Explanation

The first query formats each person as:
`Name(first occupation letter)`

Example:
`Samantha is a Doctor`

becomes:
`Samantha(D)`

The second query counts how many people have each occupation.

Example:
`Doctor appears 2 times`

becomes:
`There are a total of 2 doctors.`

## Important Learning Notes

- `CONCAT` joins strings together in MySQL.
- `LEFT(text, 1)` returns the first character.
- `LOWER(text)` converts text to lowercase.
- `COUNT(*)` counts rows.
- `GROUP BY Occupation` groups rows by occupation.
- `ORDER BY COUNT(*), Occupation` sorts by count first and occupation name second.
- Multiple `SELECT` statements are allowed for this HackerRank problem.

## Mistakes / Reminders

- Do not forget the parentheses around the occupation initial.
- Do not forget `ORDER BY NAME` in the first query.
- Do not forget `GROUP BY Occupation` in the second query.
- Do not forget `LOWER(Occupation)`, because the sentence requires lowercase occupation names.
- Put `ORDER BY` in the final grouped query.
- Avoid unnecessary CTEs for this HackerRank problem.
