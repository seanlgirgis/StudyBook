# SQL Pattern Notes

## Video 1: Read-Only Query Mindset

Pattern:
A basic SQL query asks a database to return data.

Plain English:
The query tells the database what information to show. The stored data does not
change just because it is queried.

Important distinction:
Reading data is different from changing data.

Beginner-safe example:

SELECT columns
FROM table;

Data engineer meaning:
Data engineers use SQL to inspect, validate, filter, join, aggregate, and move
structured data through pipelines. This video only introduces the read/query
idea.

# SQL Pattern Notes

## Video 2: Naming and Key Fields

Pattern:
Use clear table and field names so SQL queries are easier to read and maintain.

Good naming style:
- lowercase
- underscores instead of spaces
- singular field names
- descriptive table names
- no duplicate field names in the same table

Example table names:
books
patrons
checkouts
inventory_items

Example field names:
book_id
card_num
join_year
total_fines

Primary key pattern:
A table should usually have a field that uniquely identifies each record.

Example:
card_num can uniquely identify a patron.
book_id can uniquely identify a book.

Data engineer meaning:
Clean naming and unique identifiers make SQL queries, joins, validation checks,
and pipeline logic easier to build and troubleshoot.

# SQL Pattern Notes

## Video 3: Data Types and Schema Awareness

Pattern:
Every field in a SQL table has a data type.

Common examples:
- VARCHAR for text/string values
- INT for whole numbers
- NUMERIC for decimal values

Plain English:
The data type tells the database what kind of values are allowed in a field and
what operations make sense on those values.

Examples:
- name -> VARCHAR
- card_num -> INT
- total_fines -> NUMERIC
- checkout_date -> date-related type

Schema pattern:
Before querying or transforming data, inspect the schema.

Ask:
- What tables exist?
- What fields exist?
- What data type is each field?
- Which fields connect tables?
- Which fields are IDs, dates, measures, or descriptive attributes?

Data engineer meaning:
Schema awareness is critical for data validation, joins, transformations,
pipeline contracts, and preventing type-related bugs.

# SQL Pattern Notes

## Video 4: Basic SELECT FROM Query

Pattern:
Use SELECT to choose fields and FROM to choose the table.

Basic shape:

SELECT field_name
FROM table_name;

Multiple fields:

SELECT field_one, field_two, field_three
FROM table_name;

All fields:

SELECT *
FROM table_name;

Plain English:
Show me these columns from this table.

Example:

SELECT name
FROM patrons;

Meaning:
Return the name field from the patrons table.

Result set:
The result set is the output returned by the query.

Style convention:
- SQL keywords: uppercase
- table and field names: lowercase
- end the query with a semicolon

Data engineer meaning:
SELECT and FROM are the foundation for inspection queries, validation checks,
data profiling, debugging, and later transformation logic.

Common trap:
SELECT * is convenient for exploration, but in production-style work it is
usually safer to select only the fields needed.

# SQL Pattern Notes

## Video 5: Aliasing, DISTINCT, and Views

Pattern 1:
Use AS to rename a field in the result set.

Example:

SELECT name AS first_name
FROM employees;

Plain English:
Show the name field, but label it first_name in the result.

Important:
The source table field is not renamed. Only the result set label changes.

Pattern 2:
Use DISTINCT to return unique values.

Example:

SELECT DISTINCT year_hired
FROM employees;

Plain English:
Show each hire year only once.

Pattern 3:
Use DISTINCT with multiple fields to return unique combinations.

Example:

SELECT DISTINCT dept_id, year_hired
FROM employees;

Plain English:
Show each unique department-and-hire-year combination once.

Pattern 4:
Use CREATE VIEW to save a reusable SQL query.

Example:

CREATE VIEW employee_hire_years AS
SELECT year_hired
FROM employees;

Then query the view:

SELECT *
FROM employee_hire_years;

Data engineer meaning:
Aliases improve readability. DISTINCT helps profile unique values and remove
repeated result rows. Views can package reusable query logic for repeated
analysis or downstream use.

Common trap:
DISTINCT on multiple fields does not make each individual field unique. It
returns unique row combinations across the selected fields.

# SQL Pattern Notes

## Video 6: SQL Flavors and Limiting Results

Pattern:
SQL fundamentals transfer across database systems, but some keywords vary by
flavor.

PostgreSQL limiting pattern:

SELECT name, id
FROM employees
LIMIT 2;

SQL Server limiting pattern:

SELECT TOP 2 name, id
FROM employees;

Plain English:
Return only two rows so the query output is easier to inspect.

Data engineer meaning:
When working across platforms, always confirm the SQL dialect. Core SQL ideas
are portable, but syntax details may differ between PostgreSQL, SQL Server,
Oracle, Spark SQL, Databricks SQL, and other engines.

Common trap:
Assuming every SQL engine accepts the exact same syntax.

Practical habit:
Use small result limits when exploring large tables or testing early query
logic.
