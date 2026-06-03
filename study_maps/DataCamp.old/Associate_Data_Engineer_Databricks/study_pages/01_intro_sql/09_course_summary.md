# Course 1 Summary: Introduction to SQL

## Course Status

Course 1 transcript processing is complete.

This course introduced the foundations of relational databases and basic SQL
querying.

## Big Picture

SQL is used to communicate with structured data stored in relational databases.
A SQL query tells the database what data to return.

At this stage, the focus is not advanced SQL. The focus is understanding the
basic mental model:

```text
database -> tables -> rows/records -> columns/fields -> queries -> result sets
```

## What This Course Covered

### 1. Database Foundations

Key ideas:

* databases store and organize data
* tables are the main building blocks inside databases
* tables contain rows and columns
* rows are also called records
* columns are also called fields
* relational databases can connect tables through shared fields
* databases may be hosted on servers that respond to network requests

### 2. Table Structure

Key ideas:

* table names should be clear and descriptive
* field names should be clear and descriptive
* lowercase and underscores are common naming conventions
* fields should usually be singular
* each record should often have a unique identifier
* a primary key uniquely identifies a record
* several related tables are usually better than one giant duplicated table

### 3. Data Types and Schemas

Key ideas:

* every field has a data type
* VARCHAR is commonly used for text
* INT is commonly used for whole numbers
* NUMERIC is commonly used for decimal values
* data types affect what operations make sense
* a schema is the blueprint of a database
* schemas show tables, fields, data types, and relationships

### 4. Basic SQL Querying

Key ideas:

* SELECT chooses fields
* FROM chooses the table
* a result set is the output returned by a query
* a semicolon marks the end of a query
* multiple fields are separated with commas
* SELECT * returns all fields

Basic pattern:

```sql
SELECT field_name
FROM table_name;
```

### 5. Useful SQL Keywords

Key ideas:

* AS creates an alias in the result set
* DISTINCT returns unique values
* DISTINCT with multiple fields returns unique combinations
* CREATE VIEW saves a reusable SQL query as a virtual table
* views can be queried like tables

### 6. SQL Flavors

Key ideas:

* SQL has multiple dialects or flavors
* core SQL fundamentals transfer across systems
* PostgreSQL uses LIMIT
* SQL Server uses TOP
* Databricks SQL and Spark SQL will have their own details later
* always check the target SQL dialect

## Sean Study Decision

This course is beginner-level, but it is worth keeping because it establishes
the vocabulary and basic query model needed for the rest of the Databricks Data
Engineer track.

Do not over-study the orientation sections.

Spend more attention on:

* primary keys
* schemas
* data types
* SELECT and FROM
* DISTINCT
* views
* SQL flavor differences

## Completion Judgment

Course 1 should be considered:

```text
Foundation complete.
Practice still useful.
Ready to move forward after map/review package is created.
```
