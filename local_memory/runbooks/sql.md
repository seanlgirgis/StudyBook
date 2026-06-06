# How do I set schema before running SQL?

Use when:
I need to choose the schema context before executing queries.

Command:

```sql
SET search_path TO <SchemaA, SchemaB>;
```

Known value:
- current search path: intermediate_sql, public

Current practice override:

```sql
SET search_path TO intermediate_sql, public;
```

Memory rule:
When asked for the current search path, return both:
- the general template command
- the current practice command for `intermediate_sql, public`

If no current override is active, fall back to the general template command.

Tags:
#postgresql #prompt #schema #sql #search_path

# How do I check the schema set for current session?

Use when:
I want to verify the active schema search path for the current session.

Command:

```sql
SHOW search_path;
```

Tags:
#postgresql #schema #search_path #sql #session

# PostgreSQL Nugget: Inspect table structure (column metadata)

Use when:
I need a quick, reliable view of a table's columns, types, nullability, and defaults.

Command:

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = '<table_name>'
ORDER BY ordinal_position;
```

Notes:
- Replace `<table_name>` with your target table name.
- Add `AND table_schema = '<schema_name>'` if you need schema-specific filtering.

Tags:
#postgresql #sql #table-structure #information_schema #metadata
# How to create a named window in PostgreSQL

Info nugget:
A named window is a shortcut name for the repeated part inside `OVER()`.

Instead of repeating this many times:

```sql
OVER (
  PARTITION BY region
  ORDER BY sale_date, sale_id
)
```

Define it once at the bottom of the query:

```sql
WINDOW
  region_ordered_window AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )
```

Then reuse it like this:

```sql
SUM(revenue) OVER region_ordered_window
COUNT(*)     OVER region_ordered_window
MAX(revenue) OVER region_ordered_window
MIN(revenue) OVER region_ordered_window
```

Important:
The named window does not store the function.
It stores only the window definition: which rows belong together, and in what order.

Mental model:
- `PARTITION BY` = choose the room
- `ORDER BY` = line people up inside the room
- `WINDOW` name = give that room/line setup a reusable name

Example:

```sql
SELECT
  sale_id,
  sale_date,
  region,
  revenue,
  SUM(revenue) OVER region_window AS region_total_revenue,
  SUM(revenue) OVER region_ordered_window AS running_region_revenue
FROM sales_events
WINDOW
  region_window AS (
    PARTITION BY region
  ),
  region_ordered_window AS (
    PARTITION BY region
    ORDER BY sale_date, sale_id
  )
ORDER BY
  region,
  sale_date,
  sale_id;
```

Memory rule:
Use named windows when several columns use the same `PARTITION BY` / `ORDER BY`.
It makes the query shorter, cleaner, and easier to verify.

Tags:
#postgresql #sql #window-functions #named-window #partition-by #order-by
