# 014 - The Blunder

## Source

HackerRank SQL - Aggregation

## Problem Summary

Samantha calculated the average monthly salary from the `EMPLOYEES` table, but her keyboard's zero key was broken, so all zero digits were removed from salaries before her mistaken calculation. Find the difference between the actual average salary and the miscalculated average salary, then round the result up to the next integer.

## Schema

`EMPLOYEES`
- `ID Integer`
- `Name String`
- `Salary Integer`

## Accepted Solution

```sql
SELECT CEIL(
    AVG(Salary) - AVG(CAST(REPLACE(Salary, '0', '') AS UNSIGNED))
) AS difference
FROM EMPLOYEES;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `AVG(Salary)` calculates the actual average salary.
- `REPLACE(Salary, '0', '')` removes all zero digits from each salary.
- `CAST(... AS UNSIGNED)` converts the zero-removed salary back into a number.
- `AVG(CAST(...))` calculates Samantha's miscalculated average.
- Subtracting the two averages gives the error.
- `CEIL(...)` rounds the result up to the next integer.

## Plain-English Explanation

The required value is:

`actual average salary - miscalculated average salary`

The actual average uses the original `Salary` values.
The miscalculated average uses salaries after removing every `0` digit.

Example conversions:
- `1420 -> 142`
- `2006 -> 26`
- `2210 -> 221`
- `3000 -> 3`

Then average both versions, subtract, and round up.

## Important Learning Notes

- `REPLACE(text, old, new)` performs text replacement.
- `REPLACE(Salary, '0', '')` strips zero digits.
- MySQL handles numeric-to-text conversion for `REPLACE`.
- `CAST(... AS UNSIGNED)` converts back to numeric.
- `AVG()` calculates mean values.
- `CEIL()` rounds up.
- Final output is one number.

## Sample Input Idea

`1420`
`2006`
`2210`
`3000`

Actual average: `2159`
Miscalculated average: `98`
Difference: `2061`

Sample output: `2061`

## Mistakes / Reminders

- Do not remove rows containing zero; remove zero digits inside each salary.
- Do not use `ROUND()`; this problem requires round-up via `CEIL()`.
- Do not subtract in the wrong order.
- Do not forget to cast replaced salary back to numeric.
- In MySQL, `CAST(... AS UNSIGNED)` is a safe cast for this case.
