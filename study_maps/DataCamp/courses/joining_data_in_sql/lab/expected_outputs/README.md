# Expected Output Guide

Use these checks rather than memorizing every result row.

## Key checks

- `countries` contains 7 rows.
- `populations` contains 12 rows.
- `economies` contains 10 rows.
- The country × two-year CROSS JOIN should return 14 rows.
- The broad self join should return 24 rows because each country has two population years and therefore 2 × 2 combinations.
- The restricted 2010-to-2015 self join should return 6 rows.
- `INTERSECT` between city names and country names should return:
  - Canada
  - Mexico
  - Singapore
- The `NOT IN` query using unfiltered `economies.country_code` may return no rows because the subquery includes NULL.
- `NOT EXISTS` should correctly identify countries without economy rows.
