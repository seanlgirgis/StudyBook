# Video 1: What Are Databases and SQL?

Status: FAST REVIEW

SQL stands for Structured Query Language. It is used to communicate with data
stored in databases. A SQL query gives instructions to the database and returns
data based on those instructions.

A database stores and organizes data. Inside a relational database, data is
usually organized into tables. A table is made of rows and columns.

Rows represent individual records. Columns represent specific fields or
attributes about those records.

Example:
A library database might contain separate tables for books, patrons, and
checkouts. These tables can be connected through shared columns, such as a
patron card number or a book ID.

The key idea is that relational databases use multiple related tables to store
structured data. SQL lets users ask questions about that data.

Important distinction:
A basic SELECT query reads and returns data. It does not change the data stored
inside the database.

# Video 2: Tables, Records, Fields, and Unique Identifiers

Status: NORMAL STUDY / INTERVIEW IMPORTANT

A table is the main building block inside a database. A table should have a clear
name that describes the data it contains, such as books, products, inventory, or
patrons.

Good table names are usually:
- lowercase
- clear
- descriptive
- written with underscores instead of spaces

Example:
Use checked_out_books instead of Checked Out Books.

Tables contain rows and columns. In database language, rows are often called
records, and columns are often called fields.

A record contains the data for one individual observation. For example, in a
patrons table, each record represents one library patron.

A field contains one specific piece of information for every record in the
table. For example, a name field contains the name value for each patron.

Good field names are important because SQL queries must refer to fields by
name. Field names should usually be:
- lowercase
- singular
- descriptive
- written with underscores instead of spaces
- unique within the table

A field name should usually be singular because it describes one value for one
record. For example, use name instead of names.

Two fields in the same table should not have the same name. A field should also
not have the same name as the table, because that makes queries harder to read.

Tables often include a special field that uniquely identifies each record. This
is often called a primary key. A primary key value must be unique for every
record in the table.

Example:
In a patrons table, card_num may be a better unique identifier than name,
because two patrons can have the same name but should not have the same library
card number.

A key data-modeling idea from this video is that several well-organized related
tables are often better than one giant table. One large table can create
duplicate information, confusion, and fields that are no longer unique.

Keeping data in separate related tables makes it easier to query, connect, and
analyze the data with SQL.

# Video 3: Data Types, Database Storage, and Schemas

Status: NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

A database must be physically stored somewhere. In many systems, database data
is stored on a server. A server is a powerful computer that stores information
and responds to requests made over a network.

For databases, the server provides access to stored data. Many users or
applications can send requests to the server at the same time.

When creating a table, each field needs a name and a data type. The data type
defines what kind of value can be stored in that field.

Common data categories include:
- text
- whole numbers
- decimal numbers
- dates

The data type matters because it affects what operations make sense. For
example, multiplying two numbers makes sense. Multiplying a person's name does
not.

A string is a sequence of characters. Strings can contain letters, numbers, or
punctuation. In SQL, VARCHAR is a common data type used for text because it can
store flexible string values.

An integer is a whole number. INT is a common SQL data type used for whole
numbers.

A float is a number with a decimal or fractional part. In this course example,
NUMERIC is used for decimal values such as money amounts or fines.

A schema is like a blueprint of a database. It shows the database design,
including:
- what tables exist
- what fields exist in each table
- what data type each field can hold
- how tables relate to each other

The key idea is that table structure is not random. A table's fields and data
types are part of the database design.

# Video 4: Introducing Queries, SELECT, FROM, and Result Sets

Status: NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

SQL queries are used to ask questions of data stored in relational database
tables. After learning how databases are organized, this video introduces the
first practical SQL syntax.

SQL is useful for answering questions within one table or across multiple
related tables. Examples include:
- Which books did a patron check out?
- Which employees belong to a department?
- Which products had the highest sales?
- How did website traffic change after a feature launch?

SQL is especially useful with larger datasets where spreadsheets may become
limited or difficult to manage.

A SQL keyword is a reserved word that tells SQL what operation to perform. The
two first keywords introduced are SELECT and FROM.

SELECT tells SQL which field or fields to return.

FROM tells SQL which table contains those fields.

Basic query pattern:

SELECT name
FROM patrons;

In this example:
- SELECT name means return the name field
- FROM patrons means read from the patrons table
- the semicolon marks the end of the query

The output of a query is called a result set. A result set is the data returned
by the database after the query runs.

To select multiple fields, list the field names after SELECT and separate them
with commas.

Example:

SELECT card_num, name
FROM patrons;

To select all fields from a table, SQL can use the asterisk wildcard:

SELECT *
FROM patrons;

The asterisk means all fields.

Important style note:
SQL keywords are often written in uppercase, while table and field names are
often written in lowercase.

# Video 5: Aliasing, DISTINCT, and Views

Status: NORMAL STUDY / PRACTICE REQUIRED / INTERVIEW IMPORTANT

This video introduces several useful SQL keywords that make queries cleaner,
more focused, and more reusable.

Aliasing means renaming a column in the result set. Aliasing changes the output
column name shown in the query result. It does not rename the actual field in
the source table.

The AS keyword is commonly used for aliases.

Example:

SELECT name AS first_name
FROM employees;

In this example, the original field is still called name in the employees
table, but the result set displays it as first_name.

DISTINCT is used to return unique values.

Example:

SELECT DISTINCT year_hired
FROM employees;

This returns each hire year once, instead of repeating the same year for every
employee hired in that year.

DISTINCT can also work with multiple fields. When multiple fields are listed,
SQL returns unique combinations of those field values.

Example:

SELECT DISTINCT dept_id, year_hired
FROM employees;

In this example, dept_id values may repeat and year_hired values may repeat,
but each combination of dept_id and year_hired appears only once.

A view is a saved SQL query that acts like a virtual table. A view does not
store a separate copy of the data. It stores the query definition.

Because a view stores the query, the results can stay current with the
underlying tables when the view is queried.

Basic view pattern:

CREATE VIEW employee_hire_years AS
SELECT year_hired
FROM employees;

Creating a view saves the query. It does not directly return a result set.

After a view exists, it can be queried like a table:

SELECT *
FROM employee_hire_years;

The key ideas:
- AS makes result column names clearer.
- DISTINCT removes repeated values or repeated combinations.
- Views save reusable query logic.

# Video 6: SQL Flavors, PostgreSQL, SQL Server, LIMIT, and TOP

Status: NORMAL STUDY / FAST REVIEW / INTERVIEW USEFUL

SQL has several versions, often called flavors. Different database systems may
support slightly different SQL syntax or extra features.

Most SQL flavors share the same core ideas and many of the same keywords because
they are based on common SQL standards.

Examples of SQL database systems and flavors:
- PostgreSQL
- Microsoft SQL Server
- Oracle Database
- T-SQL for Microsoft SQL Server

PostgreSQL is a free and open-source relational database system. The name
PostgreSQL can refer to both the database system and its SQL flavor.

SQL Server is Microsoft's relational database system. T-SQL is Microsoft's SQL
flavor used with SQL Server.

Most beginner SQL knowledge transfers across database systems. The differences
usually appear in specific keywords, functions, or vendor-specific features.

Example difference:

PostgreSQL uses LIMIT:

SELECT name, id
FROM employees
LIMIT 2;

SQL Server uses TOP:

SELECT TOP 2 name, id
FROM employees;

Both examples limit the result to two records, but the keyword placement is
different.

Limiting results is useful when testing a query because real tables may contain
many rows. It is often safer to test with a small result set before running or
reviewing a larger query.

The key idea:
Do not worry too much about choosing the perfect SQL flavor at the beginning.
Learn the fundamentals first. Strong SQL fundamentals transfer across tools.

# Final Video: Course Completion and Next Steps

Status: FAST REVIEW / COURSE WRAP-UP

This final video summarizes the course.

The course covered:
- why databases are useful
- how relational databases are organized
- how SQL queries extract insight from database tables
- how SQL fundamentals transfer across SQL flavors

The instructor notes that the next step is learning more SQL keywords and
continuing into a specific SQL flavor.

Sean study decision:
Keep this as a course wrap-up only. Do not spend heavy study time here.
