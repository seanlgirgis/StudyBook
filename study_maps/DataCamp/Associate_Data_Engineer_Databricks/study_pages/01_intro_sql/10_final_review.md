# Course 1 Final Review: Introduction to SQL

## One-Minute Review

SQL is the language used to query structured data in relational databases.

A database contains tables.

A table contains records and fields.

A record is a row.

A field is a column.

A schema describes the database structure.

A primary key uniquely identifies a record.

A SQL query uses keywords such as SELECT and FROM to return a result set.

## Must-Know Terms

### Database

An organized system for storing data.

### Table

A structured collection of rows and columns inside a database.

### Record

One row in a table.

### Field

One column in a table.

### Primary Key

A field that uniquely identifies each record.

### Data Type

The kind of value a field can store.

### Schema

The blueprint of a database, including tables, fields, data types, and
relationships.

### Query

A SQL command that asks the database to return data.

### Result Set

The output returned by a query.

### View

A saved SQL query that acts like a virtual table.

## Must-Know SQL Patterns

### Select one field

```sql
SELECT name
FROM patrons;
```

### Select multiple fields

```sql
SELECT card_num, name
FROM patrons;
```

### Select all fields

```sql
SELECT *
FROM patrons;
```

### Alias a field

```sql
SELECT name AS first_name
FROM employees;
```

### Select unique values

```sql
SELECT DISTINCT year_hired
FROM employees;
```

### Select unique combinations

```sql
SELECT DISTINCT dept_id, year_hired
FROM employees;
```

### Create a view

```sql
CREATE VIEW employee_hire_years AS
SELECT year_hired
FROM employees;
```

### Query a view

```sql
SELECT *
FROM employee_hire_years;
```

### Limit rows in PostgreSQL

```sql
SELECT name, id
FROM employees
LIMIT 2;
```

### Limit rows in SQL Server

```sql
SELECT TOP 2 name, id
FROM employees;
```

## Common Traps

### Trap 1: Confusing a database with a table

A database can contain many tables.

### Trap 2: Confusing records and fields

A record is a row.
A field is a column.

### Trap 3: Thinking a name is always a safe unique identifier

Names can repeat. IDs or card numbers are usually safer.

### Trap 4: Thinking DISTINCT always makes each column unique

DISTINCT with multiple fields returns unique row combinations.

### Trap 5: Overusing SELECT *

SELECT * is useful for quick exploration, but specific field selection is better
for repeatable work.

### Trap 6: Assuming all SQL flavors use identical syntax

Core SQL transfers, but syntax details can differ.

## What Sean Should Know Cold

* what SELECT does
* what FROM does
* what a result set is
* what a primary key is
* what a schema is
* what data types are
* what DISTINCT does
* what a view is
* why SQL dialects differ

## Final Course 1 Confidence Statement

I understand the basic structure of relational databases and can write simple
SQL queries using SELECT and FROM. I also understand basic table structure,
data types, schemas, aliases, DISTINCT, views, and SQL flavor differences.
