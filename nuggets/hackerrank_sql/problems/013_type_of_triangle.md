# 013 - Type of Triangle

## Source

HackerRank SQL - Advanced Select

## Problem Summary

Given a `TRIANGLES` table with side lengths `A`, `B`, and `C`, classify each row as `Equilateral`, `Isosceles`, `Scalene`, or `Not A Triangle`.

## Schema

`TRIANGLES`
- `A Integer`
- `B Integer`
- `C Integer`

## Accepted Solution

```sql
SELECT
    CASE
        WHEN A + B <= C OR A + C <= B OR B + C <= A THEN 'Not A Triangle'
        WHEN A = B AND B = C THEN 'Equilateral'
        WHEN A = B OR B = C OR A = C THEN 'Isosceles'
        ELSE 'Scalene'
    END AS TRIANGLE_TYPE
FROM TRIANGLES;
```

## Provided Solution Reviewed

The provided SQL solution is almost correct and should pass because the `CASE` order protects the classifications.

Provided solution:

```sql
SELECT
    CASE
        WHEN A + B <= C OR A + C <= B OR B + C <= A THEN  'Not A Triangle'
        WHEN A = B AND B = C             THEN 'Equilateral'
        WHEN A = B OR B = C OR A = C     THEN 'Isosceles'
        WHEN A <> B AND B <> C OR A <> C THEN 'Scalene'
    END AS TRIANGLE_TYPE
FROM TRIANGLES;
```

### What is good

- The triangle inequality failure is checked first.
- Invalid triangles are classified as `Not A Triangle` before any equality checks.
- `Equilateral` is checked before `Isosceles`.
- `Isosceles` is checked before `Scalene`.
- `CASE` is the right SQL tool for conditional classification.

## Small Improvement

The final `Scalene` condition in the provided query is harder to read and relies on operator precedence. Since earlier branches already handle all other cases, `ELSE 'Scalene'` is the cleanest final branch.

## Plain-English Explanation

A triangle is valid only if the sum of any two sides is greater than the third side.

So a row is `Not A Triangle` if:
- `A + B <= C`
- or `A + C <= B`
- or `B + C <= A`

After confirming it is valid:
- `Equilateral`: all three sides equal
- `Isosceles`: two sides equal
- `Scalene`: all sides different

Order matters:
1. Not A Triangle
2. Equilateral
3. Isosceles
4. Scalene

## Important Learning Notes

- `CASE` returns labels from ordered conditions.
- Triangle validity should be checked before triangle type.
- `Equilateral` must be checked before `Isosceles`.
- `ELSE` is useful when remaining rows all map to one class.
- SQL uses `<>` for not equal.

## Sample Input Idea

`A  B  C`
`20 20 23`
`20 20 20`
`20 21 22`
`13 14 30`

## Sample Output

`Isosceles`
`Equilateral`
`Scalene`
`Not A Triangle`

## Mistakes / Reminders

- Do not check `Isosceles` before `Equilateral`.
- Do not forget the triangle inequality check.
- Do not use only `A + B <= C`; all three combinations must be checked.
- Do not overcomplicate the `Scalene` branch when `ELSE` works cleanly.
- Keep exact output text: `Equilateral`, `Isosceles`, `Scalene`, `Not A Triangle`.
