# 015 - Top Earners

## Source

HackerRank SQL - Aggregation

## Problem Summary

For each employee, total earnings are calculated as monthly salary multiplied by months worked. Find the maximum total earnings and count how many employees have that maximum earnings value. Output both values as two space-separated integers.

## Schema

`Employee`
- `employee_id Integer`
- `name String`
- `months Integer`
- `salary Integer`

## Accepted Solution

```sql
SELECT (months * salary) AS earnings, COUNT(*)
FROM Employee
GROUP BY earnings
ORDER BY earnings DESC
LIMIT 1;
```

## Alternative Explicit Solution

```sql
SELECT months * salary, COUNT(*)
FROM Employee
GROUP BY months * salary
ORDER BY months * salary DESC
LIMIT 1;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass in MySQL.

### What is good

- `months * salary` correctly calculates total earnings for each employee.
- `GROUP BY earnings` groups employees by the same total earnings value.
- `COUNT(*)` counts how many employees have each earnings value.
- `ORDER BY earnings DESC` sorts highest earnings first.
- `LIMIT 1` returns only the maximum earnings group.
- Output shape matches the problem: maximum earnings and count.

## Plain-English Explanation

First compute each employee's earnings:
`earnings = months * salary`

Then group by that earnings value, count employees in each group, sort from highest earnings to lowest, and keep the top row.

That top row gives:
1. maximum earnings
2. number of employees with that maximum

## Important Learning Notes

- Multiplication uses `*`.
- `COUNT(*)` counts rows in each group.
- `GROUP BY` is required for per-earnings counts.
- `ORDER BY ... DESC` puts max first.
- `LIMIT 1` keeps the top row only.
- MySQL allows alias use in `GROUP BY` and `ORDER BY`.

## Sample Input Idea

For Kimberly:
`months = 16`, `salary = 4372`

Earnings:
`16 * 4372 = 69952`

Sample output:
`69952 1`

## Mistakes / Reminders

- Do not use plain `MAX(months * salary), COUNT(*)` without isolating max earners correctly.
- Do not count all employees; count only those in the maximum earnings group.
- Do not order ascending.
- Do not forget `LIMIT 1`.
- Keep output as two values: maximum earnings and count.
