# Fast Review Items

## Video 1: Databases and SQL

Fast review:
- SQL means Structured Query Language.
- Databases store organized data.
- Tables contain rows and columns.
- Rows are records.
- Columns are fields.
- Relational databases connect tables through shared columns.
- Queries can read data without changing stored data.

Reason:
This is foundation material and already familiar. Keep it as orientation but do
not spend heavy study time here.

## Video 2: Tables and Naming Rules

Classification:
NORMAL STUDY / INTERVIEW IMPORTANT

Fast review:
- Table names should be clear and descriptive.
- Table and field names usually use lowercase and underscores.
- Rows are also called records.
- Columns are also called fields.

Slow down:
- A primary key uniquely identifies each record.
- Names are usually not safe unique identifiers.
- Several related tables are often better than one giant table.
- Duplicated data can make analysis and joins confusing.

Reason:
This is still introductory, but it introduces important data modeling language
that appears later in SQL joins, relational databases, and data engineering
pipeline design.

## Video 3: Data Types, Servers, and Schemas

Classification:
NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

Fast review:
- Databases are stored on servers.
- Servers respond to requests over a network.
- Strings are character sequences.
- Integers are whole numbers.
- Floats/decimals have fractional parts.

Slow down:
- Every table field has a data type.
- Data types affect what operations make sense.
- VARCHAR is commonly used for text.
- INT is commonly used for whole numbers.
- NUMERIC can store decimal values.
- A schema is the database blueprint.
- Schema understanding is essential before joins, validation, or transformation.

Reason:
This video introduces vocabulary and habits that matter in real data
engineering work. Data type mismatches are a common source of pipeline bugs.

## Video 4: Introducing Queries

Classification:
NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

Fast review:
- SQL queries ask questions of database tables.
- SELECT chooses fields.
- FROM chooses the table.
- A result set is the returned output.
- Semicolon marks the end of a query.

Slow down:
- SELECT and FROM are the base pattern for almost every query.
- Multiple fields are separated by commas.
- SELECT * returns all fields.
- SELECT * is useful for quick exploration but should be used carefully.
- Keywords are often uppercase; table and field names are often lowercase.

Reason:
This is the first real SQL syntax section. It should be practiced, not just
read.

## Video 5: Aliasing, DISTINCT, and Views

Classification:
NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

Fast review:
- AS gives a result column an alias.
- Aliasing does not rename the source table field.
- DISTINCT removes repeated result values.
- A view is a saved query.

Slow down:
- DISTINCT with one field returns unique values.
- DISTINCT with multiple fields returns unique combinations.
- A view acts like a virtual table.
- CREATE VIEW saves a query definition.
- Creating a view does not directly return a result set.
- Views can be queried later with SELECT and FROM.

Reason:
This video introduces practical SQL features used for clearer outputs, basic
profiling, reusable query logic, and cleaner downstream SQL.

## Video 6: SQL Flavors

Classification:
NORMAL STUDY / FAST REVIEW / INTERVIEW USEFUL

Fast review:
- SQL has multiple flavors.
- SQL flavors share most core keywords.
- PostgreSQL is open-source.
- SQL Server is from Microsoft.
- T-SQL is Microsoft's SQL flavor.
- PostgreSQL uses LIMIT.
- SQL Server uses TOP.

Slow down:
- SQL fundamentals transfer across tools.
- Specific syntax can differ by platform.
- Always confirm the SQL dialect before copying syntax.
- Limiting rows is useful while testing queries on large tables.

Reason:
This video is not deeply technical, but it is useful for avoiding confusion
when moving between PostgreSQL, SQL Server, Databricks SQL, Spark SQL, and other
SQL engines.

## Final Video: Course Completion

Classification:
FAST REVIEW / COURSE WRAP-UP

Fast review:
- This video does not introduce new technical material.
- It summarizes the course.
- It points learners toward more SQL keywords and SQL-flavor-specific courses.

Reason:
This is a closing video, not a technical teaching section.
