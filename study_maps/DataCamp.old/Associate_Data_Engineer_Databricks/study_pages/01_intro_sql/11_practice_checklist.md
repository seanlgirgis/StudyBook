# Course 1 Practice Checklist: Introduction to SQL

Use this checklist to decide whether Course 1 is truly understood.

## Database Foundations

Sean should be able to explain:

* [ ] what a database is
* [ ] what a table is
* [ ] what a row/record is
* [ ] what a column/field is
* [ ] why relational databases use multiple related tables
* [ ] why one giant table can create duplicate data problems

## Table Design Basics

Sean should be able to explain:

* [ ] why naming tables clearly matters
* [ ] why naming fields clearly matters
* [ ] why field names are usually singular
* [ ] why primary keys are important
* [ ] why names are usually not good unique identifiers
* [ ] how related tables can connect through shared fields

## Data Types and Schema

Sean should be able to explain:

* [ ] what a data type is
* [ ] what VARCHAR is used for
* [ ] what INT is used for
* [ ] what NUMERIC is used for
* [ ] why data types affect operations
* [ ] what a schema is
* [ ] why schema awareness matters in data engineering

## Basic Querying

Sean should be able to write:

* [ ] SELECT one field from a table
* [ ] SELECT multiple fields from a table
* [ ] SELECT all fields with *
* [ ] use AS to alias a field
* [ ] use DISTINCT on one field
* [ ] use DISTINCT on multiple fields
* [ ] create a basic view
* [ ] query a view
* [ ] limit rows in PostgreSQL with LIMIT
* [ ] recognize SQL Server TOP syntax

## Practice Prompts

Write SQL for each prompt.

### Prompt 1

Return all names from the patrons table.

Expected pattern:

```sql
SELECT name
FROM patrons;
```

### Prompt 2

Return card numbers and names from the patrons table.

Expected pattern:

```sql
SELECT card_num, name
FROM patrons;
```

### Prompt 3

Return all fields from the patrons table.

Expected pattern:

```sql
SELECT *
FROM patrons;
```

### Prompt 4

Return employee names but display the output column as first_name.

Expected pattern:

```sql
SELECT name AS first_name
FROM employees;
```

### Prompt 5

Return each hire year only once.

Expected pattern:

```sql
SELECT DISTINCT year_hired
FROM employees;
```

### Prompt 6

Return each unique department and hire-year combination.

Expected pattern:

```sql
SELECT DISTINCT dept_id, year_hired
FROM employees;
```

### Prompt 7

Create a view named employee_hire_years from the year_hired field.

Expected pattern:

```sql
CREATE VIEW employee_hire_years AS
SELECT year_hired
FROM employees;
```

### Prompt 8

Query all fields from the employee_hire_years view.

Expected pattern:

```sql
SELECT *
FROM employee_hire_years;
```

## Ready To Move On When

Sean can:

* [ ] explain the database/table/record/field model in plain English
* [ ] write basic SELECT/FROM queries without looking
* [ ] explain what DISTINCT does
* [ ] explain what AS does
* [ ] explain what a view is
* [ ] explain why schemas and data types matter
* [ ] say what is beginner-level versus what comes later
