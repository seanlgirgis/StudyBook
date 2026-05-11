# 008 - Higher Than 75 Marks

## Source

HackerRank SQL - Basic Select

## Problem Summary

Query the `Name` of students from `STUDENTS` who scored higher than `75` marks. Order the output by the last three characters of each name. If two or more students have names ending in the same last three characters, use ascending `ID` as the secondary sort.

## Schema

`STUDENTS`
- `ID Integer`
- `Name String`
- `Marks Integer`

## Accepted Solution

```sql
SELECT NAME
FROM STUDENTS
WHERE Marks > 75
ORDER BY RIGHT(NAME, 3), ID;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `SELECT NAME` returns only the requested column.
- `FROM STUDENTS` uses the correct table.
- `WHERE Marks > 75` filters only students with marks higher than `75`.
- `RIGHT(NAME, 3)` extracts the last three characters of each name.
- `ORDER BY RIGHT(NAME, 3), ID` applies the required primary and secondary sorting.
- `ID` defaults to ascending order, which matches the problem requirement.

## Plain-English Explanation

The problem asks for names of students whose `Marks` are greater than `75`.

After filtering, the results must be sorted by the last three characters of the name.

Example:
`Ashley -> ley`
`Julia -> lia`
`Belvet -> vet`

If two names have the same last three characters, then the student with the smaller `ID` comes first.

## Important Learning Notes

- `WHERE` filters rows.
- `Marks > 75` means strictly higher than `75`, not equal to `75`.
- `RIGHT(NAME, 3)` gets the last three characters in MySQL.
- `ORDER BY` can sort by calculated expressions.
- `ORDER BY expression, ID` means sort by expression first, then `ID`.
- `ASC` is the default sort direction.

## Mistakes / Reminders

- Do not use `Marks >= 75` because the problem says higher than `75`.
- Do not `SELECT *` because the problem asks only for `Name`.
- Do not sort by full `Name`.
- Do not forget the secondary sort by `ID`.
- Keep this MySQL-style for HackerRank.
