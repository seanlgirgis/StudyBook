# 012 - New Companies

## Source

HackerRank SQL - Advanced Select

## Problem Summary

Given company hierarchy tables for `Company`, `Lead_Manager`, `Senior_Manager`, `Manager`, and `Employee`, output each `company_code`, `founder`, and the total number of distinct lead managers, senior managers, managers, and employees for each company. Sort output by `company_code`.

## Schemas

`Company`
- `company_code String`
- `founder String`

`Lead_Manager`
- `lead_manager_code String`
- `company_code String`

`Senior_Manager`
- `senior_manager_code String`
- `lead_manager_code String`
- `company_code String`

`Manager`
- `manager_code String`
- `senior_manager_code String`
- `lead_manager_code String`
- `company_code String`

`Employee`
- `employee_code String`
- `manager_code String`
- `senior_manager_code String`
- `lead_manager_code String`
- `company_code String`

## Accepted Solution

```sql
SELECT
    c.company_code,
    c.founder,
    COUNT(DISTINCT lm.lead_manager_code)    AS total_lead_managers,
    COUNT(DISTINCT sm.senior_manager_code)  AS total_senior_managers,
    COUNT(DISTINCT m.manager_code)          AS total_managers,
    COUNT(DISTINCT e.employee_code)         AS total_employees
FROM Company c
LEFT JOIN Lead_Manager   lm ON c.company_code = lm.company_code
LEFT JOIN Senior_Manager sm ON c.company_code = sm.company_code
LEFT JOIN Manager        m  ON c.company_code = m.company_code
LEFT JOIN Employee       e  ON c.company_code = e.company_code
GROUP BY c.company_code, c.founder
ORDER BY c.company_code;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `Company` is used as the starting table.
- `LEFT JOIN` keeps every company in the result.
- Each hierarchy table is joined by `company_code`.
- `COUNT(DISTINCT ...)` correctly counts unique codes.
- `DISTINCT` is important because joins can multiply rows.
- `GROUP BY c.company_code, c.founder` gives one row per company.
- `ORDER BY c.company_code` sorts the final output correctly.

## Plain-English Explanation

The task asks for one row per company with counts at each hierarchy level.

When multiple hierarchy tables are joined together, row combinations can multiply. That can inflate plain `COUNT(column)` results.

Using `COUNT(DISTINCT code)` ensures each person/code at that level is counted once per company.

## Important Learning Notes

- `LEFT JOIN` preserves parent rows even when child rows are missing.
- `COUNT(DISTINCT column)` counts unique non-null values.
- Joining hierarchy tables can multiply rows.
- `DISTINCT` protects counts from join multiplication.
- `GROUP BY` is needed because counts are per company.
- `ORDER BY company_code` is required by the problem.

## Mistakes / Reminders

- Do not use `COUNT(*)`; it counts joined rows, not unique people.
- Do not forget `DISTINCT` in each hierarchy count.
- Do not group only by `founder`; group by `company_code` and `founder`.
- Do not order by `founder`.
- Do not use `INNER JOIN` if companies could be missing lower-level records.
- Keep output columns in the required order.
