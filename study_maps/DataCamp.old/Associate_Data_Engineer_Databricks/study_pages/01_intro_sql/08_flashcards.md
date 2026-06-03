# Flashcards

## Video 1: Databases and SQL

Q: What does SQL stand for?
A: Structured Query Language.

Q: What is SQL used for?
A: SQL is used to communicate with data stored in databases.

Q: What is a database?
A: A database is an organized system for storing data.

Q: What is a table?
A: A table is a structured collection of rows and columns inside a database.

Q: What is a row?
A: A row is one individual record in a table.

Q: What is a column?
A: A column is one field or attribute about each record.

Q: What is a relational database?
A: A relational database stores data in multiple tables that can relate through
shared columns.

Q: Does a basic SELECT query change stored data?
A: No. A basic SELECT query reads and returns data without changing the stored
data.

## Video 2: Tables, Records, Fields, and Keys

Q: What is a table?
A: A table is a structured collection of data inside a database.

Q: What is another name for a row?
A: A record.

Q: What is another name for a column?
A: A field.

Q: What does one record represent?
A: One individual observation or item in the table.

Q: What does one field represent?
A: One specific piece of information for every record in the table.

Q: How should table and field names usually be written?
A: In lowercase with underscores instead of spaces.

Q: Should field names usually be singular or plural?
A: Singular, because the field refers to one value for one record.

Q: Can two fields in the same table have the same name?
A: No. Field names should be unique within a table.

Q: What is a primary key?
A: A field that uniquely identifies each record in a table.

Q: Why is name usually not a good primary key?
A: Because two records can have the same name.

Q: Why are several related tables often better than one giant table?
A: Separate related tables reduce duplication and make the data easier to query,
connect, and analyze.

## Video 3: Data Types and Schemas

Q: Where is database data often stored?
A: On a server.

Q: What is a server?
A: A powerful computer that stores information and responds to network
requests.

Q: What is a data type?
A: A data type defines what kind of value can be stored in a field.

Q: Why do data types matter?
A: They determine what values are allowed and what operations make sense.

Q: What is a string?
A: A sequence of characters such as letters, numbers, or punctuation.

Q: What SQL data type is commonly used for strings?
A: VARCHAR.

Q: What is an integer?
A: A whole number.

Q: What SQL data type is commonly used for whole numbers?
A: INT.

Q: What is a float or decimal value?
A: A number with a fractional part or decimal point.

Q: What SQL data type can store decimal values in this course example?
A: NUMERIC.

Q: What is a schema?
A: A blueprint of a database that shows tables, fields, data types, and
relationships.

Q: Why is schema awareness important for data engineers?
A: Pipelines and queries depend on stable field names, correct data types, and
clear relationships between tables.

## Video 4: Introducing Queries

Q: What is a SQL query?
A: A command that asks the database to return data according to instructions.

Q: What does SELECT do?
A: SELECT chooses which field or fields to return.

Q: What does FROM do?
A: FROM chooses which table SQL should read from.

Q: What is a SQL keyword?
A: A reserved word that tells SQL what operation to perform.

Q: What are the two first SQL keywords introduced in this video?
A: SELECT and FROM.

Q: What is a result set?
A: The output returned by a query.

Q: How do you select multiple fields?
A: List the field names after SELECT and separate them with commas.

Q: What does SELECT * mean?
A: Select all fields from the table.

Q: What does the semicolon do?
A: It marks the end of the query.

Q: Why should SELECT * be used carefully?
A: It returns all fields, which can be unnecessary or risky in repeatable
queries.

## Video 5: Aliasing, DISTINCT, and Views

Q: What is aliasing in SQL?
A: Renaming a column in the result set.

Q: Which keyword is commonly used for aliasing?
A: AS.

Q: Does aliasing rename the actual field in the table?
A: No. It only changes the column name shown in the result set.

Q: What does DISTINCT do?
A: It returns unique values or unique combinations.

Q: What does DISTINCT return when used with one field?
A: Each unique value from that field.

Q: What does DISTINCT return when used with multiple fields?
A: Each unique combination of the selected fields.

Q: What is a view?
A: A saved SQL query that acts like a virtual table.

Q: Does a normal view store a separate copy of the data?
A: No. It stores the query definition.

Q: What keyword pattern creates a view?
A: CREATE VIEW view_name AS followed by a SELECT query.

Q: Does CREATE VIEW directly return a result set?
A: No. It saves the query for later reuse.

Q: How can a view be queried after it is created?
A: With SELECT and FROM, like a normal table.

## Video 6: SQL Flavors

Q: What is a SQL flavor?
A: A version or dialect of SQL used by a specific database system.

Q: Do SQL flavors share the same core ideas?
A: Yes. Most SQL flavors share many keywords and core relational database
concepts.

Q: What is PostgreSQL?
A: A free and open-source relational database system and SQL flavor.

Q: What is SQL Server?
A: Microsoft's relational database system.

Q: What is T-SQL?
A: Microsoft's proprietary SQL flavor used with SQL Server.

Q: Which keyword does PostgreSQL use to limit rows?
A: LIMIT.

Q: Which keyword does SQL Server use to limit rows?
A: TOP.

Q: Why is limiting results useful?
A: It helps test and inspect queries without returning too many rows.

Q: Should beginners worry too much about choosing one SQL flavor?
A: No. It is better to learn SQL fundamentals first.

Q: What should data engineers check when moving between SQL platforms?
A: The specific SQL dialect and any syntax differences.

## Final Video: Course Wrap-Up

Q: Did the final video introduce new SQL syntax?
A: No. It summarized the course and suggested next steps.

Q: What did the course introduce?
A: Databases, relational database organization, and basic SQL querying.

Q: What is the next learning step after this course?
A: Learn more SQL keywords and continue practicing in a specific SQL flavor.

Q: How should Sean treat this video?
A: As a fast-review course wrap-up.
