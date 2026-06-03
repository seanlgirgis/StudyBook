# Video 4 Raw Transcript: Introducing Queries, SELECT, FROM, and Result Sets

## 1. Introducing queries
00:00 - 00:10

Welcome back. Now that we understand how data is organized in databases, we can
begin drawing insights using SQL queries!

## 2. What is SQL useful for?
00:10 - 00:41

Recall from the last chapter that SQL is used to answer questions both within
and across relational database tables. In the library database, we might use SQL
to find which books James checked out from the library in 2022. In an HR
database, we could query salaries for employees in Marketing and Accounting to
determine whether pay across departments is comparable.

## 3. Best for large datasets
00:41 - 01:11

In many organizations, SQL is used as a complement to other tools such as
spreadsheet applications. We can use SQL queries to uncover trends in website
traffic, customer reviews, and product sales. Which products had the highest
sales last week? Which products get the worst review scores from customers? How
did website traffic change when a feature was introduced?

## 4. Keywords
01:11 - 01:52

Let's write our first SQL code! To do that, we will need to learn a few
keywords. Keywords are reserved words used to indicate what operation we'd like
our code to perform. The two most common keywords are SELECT and FROM. Perhaps
we'd like a list of every patron's name. The SELECT keyword indicates which
fields should be selected - in this case, the name field. The FROM keyword
indicates the table in which these fields are located - in this case, the
patrons table.

## 5. Our first query
01:52 - 02:27

Let's put these parts together and write a query. The SELECT statement appears
first, followed by the FROM statement. We end the query with a semicolon to
indicate that the query is complete. Notice keywords are capitalized while
keeping table and field names all lowercase. Now let's take a look at the
results of our query, often called a result set. The result set lists all patron
names, just as we had hoped.

## 6. Selecting multiple fields
02:27 - 02:47

To select multiple fields, we can list multiple field names after the SELECT
keyword, separated by commas. For example, to select card number and name, we'd
list both field names in the order we'd like them to appear in our result set.

## 7. Selecting multiple fields
02:47 - 03:02

As you might expect, we can select three fields such as name, card_num, and
total_fine, by listing all three field names after the SELECT keyword and
separating them with commas.

## 8. Selecting all fields
03:02 - 03:25

What if we want to select all of the fields in the patrons table? We could type
out the four individual field names after the SELECT statement, but there's an
easier way: we can tell SQL to select all fields using an asterisk or star,
also known as a wildcard character, instead.

## 9. Let's practice!
03:25 - 03:31

Let's get some hands-on experience writing our own queries!

# Video 5 Raw Transcript: Aliasing, DISTINCT, and Views

## 1. Writing queries
00:00 - 00:08

It's time to level up on our SQL queries by learning a few more commonly used
keywords. Let's dive in.

## 2. Aliasing
00:08 - 00:51

Sometimes, it can be helpful to rename columns in our result set, whether for
clarity or brevity. We can do this using aliasing. For instance, let's consider
an employees table that includes a field for each employee's name and their hire
date. Because the name field only contains each employee's first name, we can
use the AS keyword to alias the name field as first_name. This changes the
field name to first_name in the result set, while the actual field name in the
table remains as name.

## 3. Selecting distinct records
00:51 - 01:34

Some SQL questions require a way to return a list of unique values. Let's
imagine we want to create a list of years when we hired our employees.
Selecting the year_hired field from the employees table shows some years
multiple times, which is not what we want. To get a list of years with no repeat
values, we can add the DISTINCT keyword before the year_hired field name in the
SELECT statement. Now, we can see that all of our employees were hired in just
four different years.

## 4. DISTINCT with multiple fields
01:34 - 02:11

It's possible to return the unique combinations of multiple field values by
listing multiple fields after the DISTINCT keyword. Take a look at the
employees table. Perhaps we'd like to know the years that different departments
hired employees. We could use this SQL query to look at this information,
selecting the dept_id and year_hired from the employees table. Looking at the
results, we see that department three hired two employees in 2021.

## 5. DISTINCT with multiple fields
02:11 - 02:33

To avoid repeating this information, we could add the DISTINCT keyword before
the fields to select. Notice that the department id and year_hired fields still
have repeat values individually, but none of the records are the same: they are
all unique combinations of the two fields.

## 6. Views
02:33 - 03:23

Finally, let's explore saving SQL result sets. A view is a saved SQL query that
acts like a virtual table. Views don't store data; they store the query,
ensuring the results are always up-to-date with the latest database changes. To
create a view, use CREATE VIEW, followed by the view name, and AS to define the
query. For example, employee_hire_years can be created by saving a query that
selects specific fields from the employees table. Note that creating a view
doesn't produce a result set, it only saves the query for reuse.

## 7. Using views
03:23 - 03:31

Once a view is created, we can query it just as we would a normal table by
selecting FROM the view.

## 8. Let's practice!
03:31 - 03:38

Time to practice refining and saving queries with these new keywords!

# Video 6 Raw Transcript: SQL Flavors

## 1. SQL flavors
00:00 - 00:03

Our last topic is SQL flavors.

## 2. SQL flavors
00:03 - 00:45

SQL has several different versions or flavors, ranging from free versions to
those designed for major databases like Microsoft SQL Server or Oracle
Database. All SQL flavors work with table-based relational databases and share a
majority of keywords. In fact, all SQL flavors must follow universal standards
set by the International Organization for Standards and the American National
Standards Institute. Only additional features on top of these standards result
in different SQL flavors.

1 Table flatlay photo created by freepik www.freepik.com

## 3. Two popular SQL flavors
00:45 - 01:45

Let's take a look at two of the most popular SQL flavors. First is PostgreSQL,
a free and open-source relational database system which was originally created
at the University of California, Berkeley, and was sponsored by America's famous
Defense Advanced Research Projects Agency, or DARPA. The name "PostgreSQL"
refers to both the database system itself and the SQL flavor used with it. Next
is SQL Server. It is a relational database system available in both free and
enterprise versions. It was created by Microsoft, so it pairs well with other
Microsoft products. T-SQL is Microsoft's proprietary flavor of SQL, used with
SQL Server databases.

## 4. Comparing PostgreSQL and SQL Server
01:45 - 02:36

While there are many similarities between SQL Server and PostgreSQL, there are
some small differences worth noting. For example, if we want to limit the number
of employee names and IDs selected to only the first two records, PostgreSQL
uses the LIMIT keyword. In contrast, SQL Server achieves the same result using
the TOP keyword. Notice that this keyword is the only difference between the two
queries! Limiting results is useful when testing code since many result sets can
have thousands of results. It's best to write and test code using just a few
results before removing the LIMIT for the final query.

## 5. Choosing a flavor
02:36 - 03:15

New SQL learners often wonder which flavor to start with. The decision is
straightforward if an employer uses a specific system like Microsoft SQL
Server. For job seekers or students unsure about future tools, the differences
between flavors are minor. Don't worry too much about what flavor to learn. A
PostgreSQL expert can quickly adapt to SQL Server by learning just a few
additional keywords. Mastering the fundamentals builds versatility across any
SQL flavor.

## 6. Let's practice!
03:15 - 03:21

Now that we've sampled a few SQL flavors, let's practice!

# Final Video Raw Transcript: Course Completion and Next Steps

## 1. Congratulations!
00:00 - 00:09

You did it! Congratulations on completing this course. You've now got a strong
understanding of the foundations of SQL.

## 2. What you've learned
00:09 - 00:13

You've learned when and why databases are useful,

## 3. What you've learned
00:13 - 00:18

you've navigated the organization of relational databases,

## 4. What you've learned
00:18 - 00:23

and you've written your own SQL queries to extract insight from a database.

## 5. Where to go next
00:23 - 01:07

From here, it's only a matter of learning more keywords before you're writing
complex SQL queries! As we discussed, the keywords you learned in this course
are shared between SQL flavors, and that is true of most keywords. However,
given the small differences between flavors, the next course you take will be
specific to a SQL flavor. Here are a few DataCamp courses that you may want to
take next.

## 6. Thank you!
00:00 - 01:07

No matter where you take your new SQL knowledge, thanks for taking this course
all the way to the end! And congratulations again on a successful start to your
SQL journey!
