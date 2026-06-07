<a id="top"></a>

# PostgreSQL Functions Quick Lookup Cheat Sheet

Fast syntax lookup for DataCamp Functions for Manipulating Data in PostgreSQL.

## Contents

- [How to Use This Cheat Sheet](#1-how-to-use-this-cheat-sheet)
- [A-Z Function and Operator Index](#2-a-z-function-and-operator-index)
- [Problem-Based Lookup Index](#3-problem-based-lookup-index)
- [Tiny Examples by Category](#4-tiny-examples-by-category)
- [Direction Rules: Higher vs Lower vs True/False](#5-direction-rules-higher-vs-lower-vs-truefalse)
- [Common Mistake Flash Table](#6-common-mistake-flash-table)
- [Links Back to Main Guides](#7-links-back-to-main-guides)

## 1. How to Use This Cheat Sheet

- Use browser find with `Ctrl+F`.
- Search by function name, problem phrase, or mistake.
- This page gives the smallest useful example.
- For deeper explanation, use the Field Guide.
- For worked lab evidence, use the Lab Guide.

[Back to top](#top)

## 2. A-Z Function and Operator Index

| Search keywords | Function / Operator | Tiny syntax | Use when | Trap |
|---|---|---|---|---|
| elapsed timestamp gap | `AGE()` | `SELECT AGE(end_ts, start_ts);` | want readable timestamp difference | returns interval, not number |
| array has one value | `ANY()` | `SELECT 'sql' = ANY(tags);` | search array for one value | not for multi-value required match |
| array contains requested values | `@>` | `SELECT tags @> ARRAY['sql'];` | check array contains one or more values | right side must be an array |
| count array items | `CARDINALITY()` | `SELECT CARDINALITY(tags);` | count values inside array | arrays start at 1, not 0 |
| standard cast | `CAST()` | `SELECT CAST(ts AS date);` | convert data type with standard SQL | more verbose than `::` |
| postgres cast shorthand | `::` | `SELECT ts::date;` | quick PostgreSQL cast | PostgreSQL-specific syntax |
| label with conditions | `CASE` | `SELECT CASE WHEN x > 0 THEN 'Y' END;` | build business labels | order matters, first match wins |
| null fallback | `COALESCE()` | `SELECT COALESCE(return_date, NOW());` | replace NULL with fallback | argument types must be compatible |
| join strings function-style | `CONCAT()` | `SELECT CONCAT(first, ' ', last);` | build full name or label | null handling differs from `||` |
| today date | `CURRENT_DATE` | `SELECT CURRENT_DATE;` | get today's date | no time part |
| current clock time | `CURRENT_TIME` | `SELECT CURRENT_TIME;` | get current time only | no date part |
| current timestamp | `CURRENT_TIMESTAMP` | `SELECT CURRENT_TIMESTAMP;` | get current timestamp | includes fractional seconds |
| timestamp no milliseconds | `CURRENT_TIMESTAMP(0)` | `SELECT CURRENT_TIMESTAMP(0);` | get whole-second timestamp | `(0)` is precision, not zero time |
| date part alternative | `DATE_PART()` | `SELECT DATE_PART('month', ts);` | get numeric month or quarter | returns number, not bucket |
| month bucket | `DATE_TRUNC()` | `SELECT DATE_TRUNC('month', ts);` | group by month or week | better than month number across years |
| numeric date part | `EXTRACT()` | `SELECT EXTRACT(month FROM ts);` | get month, quarter, year number | returns number, not timestamp |
| weekday, day of week, Sunday zero, ISO weekday, dow | `EXTRACT(dow)` | `SELECT EXTRACT(dow FROM rental_date);` | get PostgreSQL weekday number | Sunday = 0 |
| ISO weekday, Monday one, Sunday seven, isodow | `EXTRACT(isodow)` | `SELECT EXTRACT(isodow FROM rental_date);` | get ISO weekday number | Monday = 1, Sunday = 7 |
| total interval hours | `EXTRACT(EPOCH FROM interval)` | `SELECT EXTRACT(EPOCH FROM gap) / 3600;` | get total hours from interval | `EXTRACT(hour ...)` is only hour component |
| case-insensitive match | `ILIKE` | `SELECT * FROM t WHERE txt ILIKE '%case%';` | search ignoring case | not the same as full-text search |
| title case | `INITCAP()` | `SELECT INITCAP(TRIM(txt));` | standardize names or labels | clean first, then format |
| relative time offset | `INTERVAL` | `SELECT NOW() + INTERVAL '5 days';` | add hours or days | avoid mixing with date-only assumptions |
| left prefix | `LEFT()` | `SELECT LEFT(txt, 3);` | extract first characters | fixed-width only |
| count characters | `LENGTH()` | `SELECT LENGTH(txt);` | measure text length | useful for hidden spaces |
| fuzzy typo distance | `levenshtein()` | `SELECT levenshtein(a, b);` | measure edit distance | lower is better |
| starts with or contains | `LIKE` | `SELECT * FROM t WHERE txt LIKE 'G%';` | character-pattern search | case-sensitive in PostgreSQL |
| lowercase | `LOWER()` | `SELECT LOWER(TRIM(txt));` | normalize case | clean first if padding exists |
| left pad zeros | `LPAD()` | `SELECT LPAD(code, 4, '0');` | make fixed-width code | can truncate if target is shorter |
| trim left spaces | `LTRIM()` | `SELECT LTRIM(txt);` | remove left padding | only left side |
| current timestamp shorthand | `NOW()` | `SELECT NOW();` | get current timestamp | may include timezone detail |
| substring position | `POSITION()` | `SELECT POSITION('ELF' IN txt);` | find substring index | returns 0 if not found |
| collapse repeated spaces | `REGEXP_REPLACE()` | `SELECT REGEXP_REPLACE(txt, '\s+', ' ', 'g');` | clean internal whitespace | without `'g'`, only first match |
| exact text swap | `REPLACE()` | `SELECT REPLACE(txt, 'ELF', 'ORC');` | replace exact matching text | not fuzzy replacement |
| reverse characters | `REVERSE()` | `SELECT REVERSE(txt);` | reverse text | niche, not general cleanup |
| right suffix | `RIGHT()` | `SELECT RIGHT(txt, 3);` | extract last characters | fixed-width only |
| round result | `ROUND()` | `SELECT ROUND(x, 2);` | round numeric output | use numeric expression first |
| right pad text | `RPAD()` | `SELECT RPAD(code, 8, '.');` | pad label or code to width | can truncate if target is shorter |
| trim right spaces | `RTRIM()` | `SELECT RTRIM(txt);` | remove right padding | only right side |
| trigram score | `similarity()` | `SELECT similarity(a, b);` | fuzzy trigram score | higher is better |
| phonetic code | `soundex()` | `SELECT soundex('Smith');` | sound-alike matching | phonetic, not edit distance |
| split by delimiter | `SPLIT_PART()` | `SELECT SPLIT_PART(txt, ' ', 1);` | pull nth piece of text | part numbers start at 1 |
| substring position alt | `STRPOS()` | `SELECT STRPOS(txt, 'ELF');` | find substring index | returns 0 if not found |
| substring standard form | `SUBSTRING()` | `SELECT SUBSTRING(txt FROM 2 FOR 3);` | extract middle text | positions are 1-based |
| substring short form | `SUBSTR()` | `SELECT SUBSTR(txt, 2, 3);` | extract middle text | positions are 1-based |
| build searchable document | `to_tsvector()` | `SELECT to_tsvector('english', txt);` | prepare text for full-text search | tokens get normalized |
| build tsquery manually | `to_tsquery()` | `SELECT to_tsquery('english', 'elf & search');` | use full-text operators | not ideal for raw user text |
| build tsquery from plain words | `plainto_tsquery()` | `SELECT plainto_tsquery('english', 'postgres database');` | convert plain words safely | stop words may disappear |
| full-text match | `@@` | `SELECT doc @@ query;` | test tsvector against tsquery | both sides should be full-text objects |
| trim both sides | `TRIM()` | `SELECT TRIM(txt);` | clean outside spaces | does not fix internal repeated spaces |
| uppercase | `UPPER()` | `SELECT UPPER(TRIM(txt));` | normalize case | clean first if needed |
| embedded fuzzy match | `word_similarity()` | `SELECT word_similarity(a, phrase);` | match inside longer sentence | higher is better |
| trigram pass fail | `pg_trgm %` | `SELECT title % 'POSTGRES HER0';` | filter similar-enough match | not percent math |
| trigram distance | `pg_trgm <->` | `SELECT title <-> 'POSTGRES HER0';` | rank closest trigram matches | lower is better |
| current trigram threshold | `show_limit()` | `SELECT show_limit();` | inspect active pg_trgm threshold | threshold affects `%`, not score |
| set trigram threshold | `set_limit()` | `SELECT set_limit(0.3);` | change pg_trgm threshold | reset temporary changes |
| sound similarity score | `difference()` | `SELECT difference('Smith', 'Smyth');` | compare phonetic closeness | higher is better |

[Back to top](#top)

## 3. Problem-Based Lookup Index

| I want to... | Use this | Tiny SQL | Watch out |
|---|---|---|---|
| get today’s date | `CURRENT_DATE` | `SELECT CURRENT_DATE;` | date only, no time |
| get current time | `CURRENT_TIME` | `SELECT CURRENT_TIME;` | time only, no date |
| get current timestamp | `CURRENT_TIMESTAMP` | `SELECT CURRENT_TIMESTAMP;` | includes fractional seconds |
| get current timestamp with no milliseconds | `CURRENT_TIMESTAMP(0)` | `SELECT CURRENT_TIMESTAMP(0);` | precision argument, not zero time |
| add 5 days to now | `INTERVAL` | `SELECT CURRENT_TIMESTAMP(0)::timestamp + INTERVAL '5 days';` | timestamp math returns timestamp |
| add rental duration days to rental date | `INTERVAL` | `SELECT rental_date + INTERVAL '1 day' * rental_duration;` | duration must be numeric days |
| subtract two timestamps | timestamp subtraction | `SELECT return_date - rental_date;` | returns interval |
| subtract two dates | date subtraction | `SELECT return_date::date - rental_date::date;` | returns integer days |
| get total hours from an interval | `EXTRACT(EPOCH)` | `SELECT EXTRACT(EPOCH FROM gap) / 3600;` | `EXTRACT(hour ...)` is not total hours |
| round numeric result | `ROUND()` | `SELECT ROUND(total_hours, 2);` | round after computing |
| group by month | `DATE_TRUNC()` | `SELECT DATE_TRUNC('month', rental_date);` | safer than month number alone |
| get month number | `EXTRACT()` | `SELECT EXTRACT(month FROM rental_date);` | numeric part only |
| get quarter number | `EXTRACT()` or `DATE_PART()` | `SELECT EXTRACT(quarter FROM rental_date);` | numeric part only |
| get day of week with Sunday as 0 | `EXTRACT(dow)` | `SELECT EXTRACT(dow FROM rental_date);` | `0 = Sunday, 6 = Saturday` |
| get ISO day of week | `EXTRACT(isodow)` | `SELECT EXTRACT(isodow FROM rental_date);` | `1 = Monday, 7 = Sunday` |
| get the day number within the month | `EXTRACT(day)` | `SELECT EXTRACT(day FROM rental_date);` | this is day of month, not weekday |
| cast timestamp to date | `::` or `CAST()` | `SELECT rental_date::date;` | drops time detail |
| replace NULL with fallback | `COALESCE()` | `SELECT COALESCE(return_date, NOW());` | types must match |
| label rows with business logic | `CASE` | `SELECT CASE WHEN x > 72 THEN 'Long' END;` | order from most specific to least |
| build a full name | `CONCAT()` or `||` | `SELECT CONCAT(first_name, ' ', last_name);` | `||` can null out whole result |
| clean outside spaces | `TRIM()` | `SELECT TRIM(raw_text);` | not internal spaces |
| clean left spaces only | `LTRIM()` | `SELECT LTRIM(raw_text);` | left side only |
| clean right spaces only | `RTRIM()` | `SELECT RTRIM(raw_text);` | right side only |
| title-case text | `INITCAP()` | `SELECT INITCAP(TRIM(raw_text));` | trim first |
| uppercase text | `UPPER()` | `SELECT UPPER(TRIM(raw_text));` | trim first |
| lowercase text | `LOWER()` | `SELECT LOWER(TRIM(raw_text));` | trim first |
| pad code with zeros | `LPAD()` | `SELECT LPAD(raw_code, 4, '0');` | target shorter can truncate |
| collapse repeated internal spaces | `REGEXP_REPLACE()` | `SELECT REGEXP_REPLACE(raw_text, '\s+', ' ', 'g');` | need `'g'` |
| find substring position | `POSITION()` or `STRPOS()` | `SELECT STRPOS(comparison_text, 'ELF');` | returns 0 if not found |
| extract left characters | `LEFT()` | `SELECT LEFT(comparison_text, 3);` | fixed-width slice |
| extract right characters | `RIGHT()` | `SELECT RIGHT(comparison_text, 3);` | fixed-width slice |
| extract middle text | `SUBSTRING()` or `SUBSTR()` | `SELECT SUBSTR(comparison_text, 2, 3);` | positions start at 1 |
| split text by delimiter | `SPLIT_PART()` | `SELECT SPLIT_PART(clean_text, ' ', 1);` | part numbers start at 1 |
| search text starts with | `LIKE` | `SELECT * FROM t WHERE txt LIKE 'G%';` | case-sensitive |
| search text contains | `LIKE` | `SELECT * FROM t WHERE txt LIKE '%BO%';` | character search only |
| search case-insensitive | `ILIKE` | `SELECT * FROM t WHERE txt ILIKE '%case%';` | not full-text search |
| search array for one value | `ANY()` | `SELECT * FROM t WHERE 'sql' = ANY(tags);` | one searched value |
| check array contains multiple values | `@>` | `SELECT * FROM t WHERE tags @> ARRAY['sql','postgres'];` | right side must be array |
| count array items | `CARDINALITY()` | `SELECT CARDINALITY(tags);` | arrays are 1-based |
| full-text searchable document | `to_tsvector()` | `SELECT to_tsvector('english', description);` | tokens normalize |
| full-text query from plain words | `plainto_tsquery()` | `SELECT plainto_tsquery('english', 'postgres database');` | stop words may be removed |
| full-text match | `@@` | `SELECT doc @@ query;` | use tsvector plus tsquery |
| fuzzy typo distance | `levenshtein()` | `SELECT levenshtein('POSTGRES HERO', 'POSTGRES HER0');` | lower is better |
| fuzzy sound match | `soundex()` / `difference()` | `SELECT difference('Smith', 'Smyth');` | `difference()` higher is better |
| fuzzy trigram score | `similarity()` | `SELECT similarity('POSTGRES HERO', 'POSTGRES HER0');` | higher is better |
| fuzzy trigram pass/fail | `pg_trgm %` | `SELECT title % 'POSTGRES HER0';` | threshold-based true/false |
| fuzzy match inside longer sentence | `word_similarity()` | `SELECT word_similarity('POSTGRES HERO', 'please find POSTGRES HER0 for me');` | higher is better |
| rank closest trigram matches | `pg_trgm <->` | `SELECT title <-> 'POSTGRES HER0' FROM lab_films ORDER BY 1 ASC;` | sort ascending |

[Back to top](#top)

## 4. Tiny Examples by Category

### Date/time quick examples

```sql
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;
SELECT CURRENT_TIMESTAMP;
SELECT CURRENT_TIMESTAMP(0);
SELECT CURRENT_TIMESTAMP(0)::timestamp;
SELECT CURRENT_TIMESTAMP(0)::timestamp + INTERVAL '5 days';
SELECT rental_date + INTERVAL '1 day' * rental_duration AS expected_return_date;
SELECT return_date - rental_date AS rental_duration;
SELECT return_date::date - rental_date::date AS rental_days;
SELECT DATE_TRUNC('month', rental_date) AS rental_month;
SELECT EXTRACT(day FROM rental_date) AS day_of_month;
SELECT EXTRACT(dow FROM rental_date) AS postgres_day_of_week;
SELECT EXTRACT(isodow FROM rental_date) AS iso_day_of_week;
SELECT DATE_PART('dow', rental_date) AS postgres_day_of_week;
SELECT DATE_PART('isodow', rental_date) AS iso_day_of_week;
SELECT EXTRACT(month FROM rental_date) AS rental_month_number;
SELECT EXTRACT(EPOCH FROM return_date - rental_date) / 3600 AS total_hours;
```

### Text cleanup quick examples

```sql
SELECT TRIM(raw_text);
SELECT LTRIM(raw_text);
SELECT RTRIM(raw_text);
SELECT INITCAP(TRIM(raw_text));
SELECT UPPER(TRIM(raw_text));
SELECT LOWER(TRIM(raw_text));
SELECT LPAD(raw_code, 4, '0');
SELECT REGEXP_REPLACE(raw_text, '\s+', ' ', 'g');
```

### Text parsing quick examples

```sql
SELECT POSITION('ELF' IN comparison_text);
SELECT STRPOS(comparison_text, 'ELF');
SELECT LEFT(comparison_text, 3);
SELECT RIGHT(comparison_text, 3);
SELECT SUBSTRING(comparison_text FROM 2 FOR 3);
SELECT SUBSTR(comparison_text, 2, 3);
SELECT SPLIT_PART(clean_text, ' ', 1);
```

### Pattern search quick examples

```sql
SELECT * FROM lab_dirty_text WHERE comparison_text LIKE 'G%';
SELECT * FROM lab_dirty_text WHERE comparison_text LIKE '%BO%';
SELECT * FROM lab_dirty_text WHERE comparison_text LIKE 'G_MBO';
SELECT * FROM lab_dirty_text WHERE comparison_text ILIKE '%case%';
```

### ARRAY quick examples

```sql
SELECT favorite_tags[1] AS first_tag FROM lab_customers;
SELECT * FROM lab_customers WHERE 'sql' = ANY(favorite_tags);
SELECT * FROM lab_customers WHERE favorite_tags @> ARRAY['sql'];
SELECT * FROM lab_customers WHERE favorite_tags @> ARRAY['sql', 'postgres'];
SELECT CARDINALITY(favorite_tags) AS tag_count FROM lab_customers;
```

### Full-text search quick examples

```sql
SELECT to_tsvector('english', description) FROM lab_films;

SELECT *
FROM lab_films
WHERE to_tsvector('english', description)
      @@ to_tsquery('english', 'elf');

SELECT *
FROM lab_films
WHERE to_tsvector('english', title || ' ' || description)
      @@ plainto_tsquery('english', 'postgres database');
```

### Fuzzy search quick examples

```sql
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
SELECT levenshtein('POSTGRES HERO', 'POSTGRES HER0');
SELECT soundex('Smith'), soundex('Smyth');
SELECT difference('Smith', 'Smyth');

CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT similarity('POSTGRES HERO', 'POSTGRES HER0');
SELECT word_similarity('POSTGRES HERO', 'please find POSTGRES HER0 for me');
SELECT show_limit();
SELECT set_limit(0.3);

SELECT *
FROM lab_films
WHERE title % 'POSTGRES HER0';

SELECT
  title,
  title <-> 'POSTGRES HER0' AS trigram_distance
FROM lab_films
ORDER BY trigram_distance ASC;
```

[Back to top](#top)

## 5. Direction Rules: Higher vs Lower vs True/False

| Function / Operator | Direction | Best value | Memory |
|---|---|---|---|
| `levenshtein()` | lower is better | `0` exact | edit distance |
| `similarity()` | higher is better | `1` exact/high | trigram score |
| `word_similarity()` | higher is better | `1` exact/high | match inside longer text |
| `difference()` | higher is better | `4` strongest | sound similarity |
| `title % search` | true/false | `true` | passes pg_trgm threshold |
| `title <-> search` | lower is better | `0` exact/close | trigram distance |
| `LIKE` / `ILIKE` | true/false | `true` | character pattern match |
| `@@` | true/false | `true` | full-text match |
| `@>` | true/false | `true` | array contains requested array |
| `ANY()` | true/false | `true` | searched value appears in array |

[Back to top](#top)

## 6. Common Mistake Flash Table

| Mistake | Correct memory |
|---|---|
| `CURRENT_TIMESTAMP(___)` syntax error | replace blank with precision like `CURRENT_TIMESTAMP(0)` |
| expecting `DATE - DATE` to return interval | it returns integer days |
| expecting `TIMESTAMP - TIMESTAMP` to return number | it returns `INTERVAL` |
| using `EXTRACT(hour FROM interval)` for total hours | use `EXTRACT(EPOCH FROM interval) / 3600` |
| grouping by `EXTRACT(month)` across years | use `DATE_TRUNC('month', timestamp)` |
| using `EXTRACT(day FROM date)` for weekday | `day` means day of month; use `dow` or `isodow` for weekday |
| forgetting PostgreSQL `dow` numbering | `dow`: Sunday = 0 through Saturday = 6 |
| forgetting ISO weekday numbering | `isodow`: Monday = 1 through Sunday = 7 |
| expecting arrays to start at 0 | PostgreSQL arrays start at 1 |
| expecting `TRIM()` to fix internal spaces | use `REGEXP_REPLACE(text, '\s+', ' ', 'g')` |
| forgetting `'g'` in `REGEXP_REPLACE()` | without `g`, only first match is replaced |
| expecting `LIKE` to ignore case | use `ILIKE` |
| treating `levenshtein()` bigger as better | lower is better |
| treating `similarity()` lower as better | higher is better |
| reading `pg_trgm %` as percent math | it means similar enough |
| sorting `<->` descending | use ascending because lower distance is better |
| pasting result table text into psql | paste only SQL or comment text with `--` |

[Back to top](#top)

## 7. Links Back to Main Guides

- [Field Guide HTML](field_guide.html)
- [Lab Guide HTML](../lab/lab_guide.html)

- Field Guide = concept explanation
- Lab Guide = worked practice and evidence
- Quick Lookup = fastest syntax reminder

[Back to top](#top)
