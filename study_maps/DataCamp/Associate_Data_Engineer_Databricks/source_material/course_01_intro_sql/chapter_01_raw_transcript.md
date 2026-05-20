# Video 1 Raw Transcript: Databases and SQL Orientation

Speaker 1 00:00

And welcome! My name is Kevin and I will be your SQL coach. We have two main
goals in this course. In chapter one, we will get to know databases which store
and organize data. We'll discuss what databases are and how they are structured
to store data. This context will prepare us for our second goal to interact with
data from databases using SQL code in chapter 2.

Let's get started with SQL. Sequel or structured query language is the most
widely used programming language for communicating with data in databases. It
lets us quickly access, organize, and analyze large amounts of data with direct
commands known as queries. These large amounts of data are stored in a
database.

Let's imagine that we are in charge of storing and organizing data for a
library. We need to keep track of the library's books as patrons. That is,
people who have joined the library and what books are checked out and by who?
Because of that, we need to create a database that contains a checkouts table,
a books table, and a patrons table.

These tables might look similar to the way data is organized in spreadsheets,
but databases are far more powerful. They can handle much more data and are
more secure due to encryption. The table is a component of a database. Oh,
patience. Table stores various data about our library's patrons, such as their
library card number name, the year they join, and the total fines they owe our
library.

Tables organized data into rows and columns. Rows contain individual data, and
each column describes a specific part of that data. For example, our patrons
table has a row for each Patron and a column for each part of their data, such
as the year they join. Several tables usually make up a database, and they work
together through relationships.

Relational databases include tables that share information. This creates
connections between them. For example, the checkouts table relates to the
Patriots and books tables through shared data. The card number column relates
checkouts to patrons. The book ID column relates checkouts to books. By
arranging information, this way we can answer questions, like, how many books
is he checked out?

These questions are asked in the form of SQL queries. Many users can write
queries to gather insights from the data within a database simultaneously. When
a database is query, the data stored inside the database does not change.
Rather, the database information is accessed and presented, according for
instructions in the query.

All right, let's use this newfound database knowledge in some exercises.

# Video 2 Raw Transcript: Tables, Records, Fields, and Unique Identifiers

Now that we know the basic organization of a database, let's examine its main
building block tables. Let's begin with table naming.

Speaker 1 00:09

The table name should be clear and refers to the data it contains, like
inventory products or books. Also, table names should be in lowercase and use
underscores instead of spaces. In the previous video, we saw that databases are
organized into tables, which are organized into rows and columns. In the world
of databases, rows are often referred to as Rebels and columns as Fields.

Each record contains the data for an individual observation. Here. The patrons
table contains four records, one for each Patron. The record for Yasmin
indicates that she became a member in 2022 and apparently owes two dollars and
five cents in fines. Fields contain one piece of information for every record in
a table.

For example, the name field in the patrons table contains all our library
patrons needs. Field naming is important because field names must be typed out
when querying a database with SQL. Similar to table names, field names should be
lowercase and use underscores instead of spaces. The field name should be
singular rather than plural because it refers to the information contained in
that field for a single record.

This is why our table has car to none and name Fields rather than cardinals and
names. Finally, two fields in a table cannot have the same name, and they should
never share a name with the table they are housed in so that it's clear whether
a field or table is being referred to.

Tables include a special field containing a unique identifier for each record,
sometimes called picky. The K value must be unique for every record. In the
patrons table, the Cardinal field is the unique identifier for each member, as
opposed to the name field because it's possible that two patrons might have the
same name as our little Library grows.

Using several well-organized tables is often better than putting everything
into one big table. For example, if we combine our patrons and checkouts tables,
the information can get confusing. It's the same data, but much less cooler
because it now contains duplicate information. While we can see that, Izzy has
two checkouts, and Mahan has none.

The card num column is no longer unique because of Izzy's multiple checkouts.
By keeping data in separate related tables and connecting them with SQL, we can
analyze and answer questions more easily than we could with spreadsheets. We'll
learn more about that soon. For now, it's time to practice your table
knowledge.

# Video 3 Raw Transcript: Data Types, Database Storage, and Schemas

## 1. Data types
00:00 - 00:08

Welcome to the final part of the databases chapter where we'll learn about
database storage and data types.

## 2. Database storage
00:08 - 00:45

Now that we know what a database is, we have to think about where it is housed.
All this data in our databases must be stored somewhere, right? Data is stored
on a server's hard disk. Servers are powerful computers that store information
and perform services via requests made over a network. In our case, the service
performed is data access. Servers can handle a large number of data requests
simultaneously, making them ideal for collaboration.

## 3. SQL data types
00:45 - 01:20

When creating a table, we name each field and decide what type of data will be
stored in it. The data type depends on the specific information stored in the
field, such as numbers, text, or dates. We also want to consider the type of
operations that we want to apply to that information. For example, it is logical
to multiply numbers together, but multiplying someone's name does not make
sense.

## 4. Strings
01:20 - 01:50

A "string" is a sequence of characters such as letters, numbers, or
punctuation. In the patrons table, the data in the name field is made up of
strings, such as "Maham" and "James". SQL has several different data types that
can hold strings. The VARCHAR data type is commonly used due to its flexibility
to store small or large strings.

## 5. Integers
01:50 - 02:11

Integer data types store whole numbers, such as the numbers in the card_num
field of the checkouts table. INT, a common SQL integer data type, can store
numbers from less than negative two billion to more than positive two billion!

## 6. Floats
02:11 - 02:42

In addition to whole numbers, we also have numbers that include a fractional
part or a decimal point, such as the $2.05 that one patron, Jasmin, owes in
fines. In programming, these numbers are referred to as floats. The NUMERIC
data type can store floats with up to 38 digits total, including those before
and after the decimal point.

## 7. Schemas
02:42 - 03:27

Now that we're familiar with data types, we can look at a database schema.
Schemas are often referred to as "blueprints" of databases. A schema shows a
database's design, such as what tables are included, any relationships between
its tables, and what data type each field can hold. The schema for our library
database shows the VARCHAR data type is used for strings like book title,
author, and genre. We can also see that the patrons table is related to the
checkouts table, but not the books table.

## 8. Let's practice!
03:27 - 03:33

Okay, let's get some practice with data!
