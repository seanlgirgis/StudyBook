# SQL Progress Log

## 2026-05-10

- Solved `001` - Revising the Select Query I
- Notes:
  - SELECT specific columns
  - WHERE filters
  - AND combines conditions
  - quoted strings vs numeric comparisons

- Solved `003` - Weather Observation Station 4
- Notes:
  - COUNT(column) counts non-null rows
  - COUNT(DISTINCT column) counts unique non-null values
  - direct aggregate subtraction can be done in one SELECT
  - no GROUP BY needed for one overall result

- Solved `004` - Weather Observation Station 5
- Notes:
  - ORDER BY supports multi-column tie-break logic
  - shortest uses LENGTH(CITY) ASC, CITY ASC
  - longest uses LENGTH(CITY) DESC, CITY ASC
  - LIMIT 1 picks a single row per query

- Solved `005` - Weather Observation Station 6
- Notes:
  - DISTINCT removes duplicate city names
  - extract first character before vowel check
  - UPPER supports case-insensitive matching
  - IN list checks vowel membership

- Solved `006` - Weather Observation Station 7
- Notes:
  - RIGHT(CITY, 1) extracts final character
  - LOWER supports case-insensitive vowel check
  - DISTINCT removes duplicate city names
  - IN list checks vowel membership

- Solved `007` - Weather Observation Station 8
- Notes:
  - both first and last character must be vowels
  - LEFT and RIGHT target first/last character checks
  - each vowel comparison must include IN (...)
  - AND requires both conditions to pass

- Solved `008` - Higher Than 75 Marks
- Notes:
  - Marks > 75 is strict (not >=)
  - RIGHT(NAME, 3) drives primary ordering
  - ID provides ascending tie-break for matching suffixes
  - select only NAME per prompt

- Solved `009` - The PADS
- Notes:
  - first query formats Name(initial) sorted by NAME
  - second query groups by Occupation and counts rows
  - LOWER(Occupation) matches required sentence format
  - ORDER BY COUNT(*), Occupation applies required ranking

- Solved `010` - Occupations
- Notes:
  - rank names alphabetically within each occupation using ROW_NUMBER()
  - align occupations by rn to create pivoted rows
  - LEFT JOIN preserves rows and yields NULL for missing occupation slots
  - final output column order must be Doctor, Professor, Singer, Actor

- Solved `011` - Binary Tree Nodes
- Notes:
  - CASE classifies node type by root/leaf/inner rules
  - leaf detection uses N NOT IN parent list
  - subquery must filter NULL parents to protect NOT IN logic
  - ORDER BY N enforces required ascending output

- Solved `012` - New Companies
- Notes:
  - start from Company as parent table
  - LEFT JOIN keeps companies even when lower levels are missing
  - COUNT(DISTINCT code) prevents overcount from join multiplication
  - GROUP BY company_code, founder gives one row per company

- Solved `013` - Type of Triangle
- Notes:
  - check triangle inequality first to catch invalid rows
  - check Equilateral before Isosceles
  - use ELSE Scalene for clean final classification
  - CASE order determines correctness

- Solved `014` - The Blunder
- Notes:
  - REPLACE(Salary, '0', '') strips zero digits from each salary
  - CAST(... AS UNSIGNED) converts stripped text back to number
  - compare AVG(real) minus AVG(miscalculated)
  - CEIL rounds the final difference up

- Solved `015` - Top Earners
- Notes:
  - earnings formula is months * salary
  - GROUP BY earnings clusters equal totals
  - COUNT(*) gives number of employees at each earnings total
  - ORDER BY DESC + LIMIT 1 returns max earnings row

- Solved `016` - Weather Observation Station 15
- Notes:
  - filter LAT_N values below threshold first
  - sort LAT_N descending to bring largest valid latitude to top
  - return that row's LONG_W and round to 4 decimals
  - pattern: fetch value from row that satisfies a max-under-constraint

- Solved `017` - Weather Observation Station 16
- Notes:
  - filter LAT_N values above threshold first
  - sort LAT_N ascending to bring smallest valid latitude to top
  - return that row's LONG_W and round to 4 decimals
  - pattern: fetch value from row that satisfies a min-over-constraint

- Solved `018` - Draw The Triangle 1
- Notes:
  - MySQL variable @rownum generates sequence 1..20
  - information_schema.columns is used as a convenient row source
  - REPEAT('* ', 21 - n) prints decreasing star counts 20..1
  - LIMIT 20 guarantees exactly 20 output rows

- Solved `019` - Draw The Triangle 2
- Notes:
  - MySQL variable @rownum generates sequence 1..20
  - REPEAT('* ', n) prints increasing stars from 1 to 20
  - information_schema.columns is a row source helper, not challenge data
  - LIMIT 20 enforces exactly 20 printed rows

- Solved `020` - Weather Observation Station 18
- Notes:
  - use min and max bounds for both LAT_N and LONG_W
  - Manhattan distance is sum of absolute coordinate differences
  - ABS keeps each component non-negative
  - ROUND(..., 4) formats final distance

- Solved `021` - Weather Observation Station 19
- Notes:
  - use min/max bounds to define two endpoint coordinates
  - square each coordinate delta with POW(..., 2)
  - sum squared deltas and apply SQRT for Euclidean distance
  - ROUND(..., 4) formats final result
