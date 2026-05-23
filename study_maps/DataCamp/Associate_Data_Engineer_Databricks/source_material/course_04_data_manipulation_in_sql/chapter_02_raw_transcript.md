# Course 4: Data Manipulation in SQL - Chapter 2 Raw Transcript

Status: raw transcript captured

## Transcript Section: Simple Subqueries in WHERE

1. WHERE are the subqueries?
00:00 - 00:12
Welcome back! In this chapter, we will cover the use of simple subqueries to extract and transform your data.

2. What is a subquery?
00:12 - 00:53
A subquery is a query nested inside another query. You can tell that there is a subquery in your SQL statement if you have an additional SELECT statement contained inside parentheses, surrounded by another complete SQL statement. So why is this important? Often, in order to retrieve information you want, you have to perform some intermediary transformations to your data before selecting, filtering, or calculating information. Subqueries are a common way of performing this transformation.

3. What do you do with subqueries?
00:53 - 01:31
A subquery can be placed in any part of your query -- such as the SELECT, FROM, WHERE, or GROUP BY clause. Where you place it depends on what you want your final data to look like. A subquery can return a variety of information, such as scalar quantities, or numbers, like the ones listed here. A subquery can return a list to use for filtering or joining information, or it can return a table to extract and further transform data.

4. Why subqueries?
01:31 - 02:21
So why might you need to use a subquery? Subqueries allow you to compare summarized values to detailed data. For example, compare Liverpool's performance to the entire English Premier League. Subqueries also allow you to better structure or reshape your data for multiple purposes, such as determining the highest monthly average of goals scored in the Bundesliga. Finally, subqueries allow you to combine data from tables where you are unable to perform a join, such as getting both the home and away team names into your results table. We'll discuss all of these questions in the coming lessons.

5. Simple subqueries
02:21 - 02:50
Let's start with the definition of a simple subquery. A simple subquery is a query, nested inside another query, that can be run on its own. The example you see here has a subquery in the WHERE clause -- if you copy the entire inner query, "SELECT the average home goal FROM the match table", you can run it on its own and get a result.

6. Simple subqueries
02:50 - 03:30
A simple subquery is also evaluated once in the entire query. This means that SQL first processes the information inside the subquery, gets the information it needs, and then moves on to processing information in the OUTER query. Here is the same query you see above. The subquery in WHERE is processed first, generating the overall average of home goals scored. SQL then moves onto the main query, treating the subquery like the single, aggregate value it just generated.

7. Subqueries in the WHERE clause
03:30 - 04:03
The first type of simple subquery we'll explore is the subquery in the WHERE clause. These are useful for filtering results based on information you'd have to calculate separately beforehand. Let's generate a list of matches in the 2012/2013 season where the number of home goals scored was higher than overall average. You could calculate the average, and then include that number in the main query...

8. Subqueries in the WHERE clause
04:03 - 04:16
...or you could put the query directly into the WHERE clause, inside parentheses. This way, you have one less manual step to perform before getting the results you need.

9. Subquery filtering list with IN
04:16 - 04:54
Subqueries are also useful for generating a filtering list. This query answers the question, "Which teams are part of Poland's league?" The "team" table doesn't have the country IDs, but the "match" table has both country and team IDs. By querying a list of hometeam_id's from match where the country_id is 15722, which indicates "Poland", you can generate a list to compare to the team_api_id column IN the WHERE clause.

10. Practice time!
04:54 - 05:03
Great! Let's practice creating simple subqueries in the WHERE clause.

## Transcript Section: Subqueries in FROM

1. Subqueries in the FROM statement
00:00 - 00:13
Fantastic! You're really getting the hang of using subqueries. In this lesson, we will cover the use of subqueries in your FROM statement.

2. Subqueries in FROM
00:13 - 01:37
You probably noticed that subqueries in WHERE can only return a single column. But what if you want to return a more complex set of results? Subqueries in the FROM statement are a robust tool for restructuring and transforming your data. Often, the data you need to answer a question is not yet in the format necessary to query it directly, and requires some additional processing to prepare for analysis. For example, you may want to transform your data into a different shape, or pre-filter it before making calculations. Subqueries in a FROM statement are a common way of preparing that data. Subqueries in FROM are also useful when calculating aggregates of aggregate information. Let's say you're interested in getting the top 3 teams who scored the highest number of home_goals on average in the 2011/2012 season. You would first calculate the average for each team in the league, and THEN calculate the max value for any team overall. This can be easily accomplished with a subquery in FROM.

3. FROM subqueries...
01:37 - 02:23
Let's examine the home_goal average for every team in the database. First, you will create the query that will become your subquery. This query here selects the team's long name from the "team" table, and the AVG of home_goal column from the "match" table. The team table is left joined onto the "match" table using hometeam_id, which will give you the identity of the home team. The query is then filtered by season and grouped by team. The results look like this -- an average value calculated for each team in the table.

4. ...to main queries!
02:23 - 02:37
In order to get only the top team as a final result, place this ENTIRE query without the semicolon inside the FROM statement of an outer query,

5. ...to main queries!
02:37 - 02:40
...make sure to give it an alias...

6. ...to main queries!
02:40 - 02:53
...then add it to the main query, selecting the team, and home_avg columns from the subquery, just as you would with any other table in the database.

7. ...to main queries!
02:53 - 03:16
Finally, don't forget to order by home_avg, descending, and limit the query to 3 results. The final query returns your top 3 teams based on home_goals scored in the 2011/2012 season. And it seems our top team for that season is Barcelona!

8. Things to remember
03:16 - 04:05
There are a few key things to remember when using subqueries in the FROM statement. The first, is that you have the ability to create more than one subquery in the FROM statement of any main query. When you do so, make sure that you give each subquery an alias, and make sure that you are able to JOIN them to each other, just as you would when querying a table from your database. Second, you can join a subquery to any existing table in your database. Again, however, you need to make sure you have a column in the subquery that you can use with the JOIN you'd like to perform.

9. Let's practice!
04:05 - 04:14
Fantastic! It's time for you to practice using subqueries in the FROM clause.

## Transcript Section: Subqueries in SELECT

1. Subqueries in SELECT
00:00 - 00:16
So far, we've covered the use of simple subqueries in FROM and WHERE statements. Subqueries can also be included in a SELECT statement to bring summary values into a detailed data set.

2. SELECTing what?
00:16 - 00:57
Subqueries in SELECT are used to return a single, aggregate value. This can be fairly useful, since, as you'll recall, you cannot include an aggregate value in an ungrouped SQL query. Subqueries in SELECT are one way to get around that. Subqieries in SELECT are also useful when performing complex mathematical calculations on information in your data set. For example, you may want to see how much an individual score deviates from an average -- say, how higher than the average is this individual score?

3. Subqueries in SELECT
00:57 - 01:30
Including a subquery in SELECT is fairly simple, and is set up the same way you set up subqueries in the WHERE and FROM clauses. Let's say we want to create a column to compare the total number of matches played in each season to the total number of matches played OVERALL. We can first calculate the overall count of matches across all seasons, which is 12,837.

4. Subqueries in SELECT
01:30 - 01:36
We can then add that single number to the SELECT statement, which yields the following results...

5. Subqueries in SELECT
01:36 - 01:45
...or, we can skip that step, and add the subquery directly to the SELECT statement to get identical results.

6. SELECT subqueries for mathematical calculations
01:45 - 02:28
Subqueries in SELECT are also incredibly useful for calculations with the data you are querying. The single value returned by a subquery in select can be used to calculate information based on existing information in a database. For example, the overall average number of goals scored in a match across all seasons is 2.72. If you want to calculate the difference from the average in any given match, you can either calculate this number ahead of time in a separate query, and input the value into the SELECT statement...

7. Subqueries in SELECT
02:28 - 02:52
...or you can use a subquery that calculates this value for you in your SELECT statement, and subtract it from the total goals in that match. Overall, this second option can save you a lot of time and errors in your work, and the results you see here, are identical to calculating the result manually.

8. SELECT subqueries -- things to keep in mind
02:52 - 04:02
There are a few unique considerations when working with subqueries in SELECT. The first is that the subquery needs to return a single value. If your subquery result returns multiple rows, your entire query will generate an error. This is because the information retrieved in a SELECT query is applied identically to each row in the data set -- and that's not possible if there's more than one unit of information. The second thing to keep an eye out is the correct placement of your data's filters in both the main query and the subquery. Here is the query from the previous slide. Since the subquery is processed before the main query, you'll need to include relevant filters in the subquery as well as the main query. Without the WHERE clause you see here in the subquery, the number returned would have been the overall average across all seasons rather than in the 2011/2012 season.

9. Let's practice!
04:02 - 04:12
Okay! Let's practice a few examples of subqueries in the SELECT statement.

## Transcript Section: Subqueries Everywhere and Best Practices

1. Subqueries everywhere! And best practices!
00:00 - 00:20
Now that you've covered the ways in which you can use subqueries in the SELECT, FROM, and WHERE clauses, let's look at the use of multiple subqueries in one query, and some best practices for making sure your queries are as readable as possible.

2. As many subqueries as you want...
00:20 - 00:57
In SQL, you can include as many simple subqueries as you need within multiple clauses within your query. However, your queries can quickly become long, and difficult to read. For example, the query you see here includes a subquery in the SELECT, FROM, and WHERE statements. You don't have to read through this now, but it's worth getting a sense of how extensive SQL queries can get, and discuss some best practices for reading, and writing large queries.

3. Format your queries
00:57 - 01:28
The best practice you can start early on in your SQL journey is properly formatting your queries. It's important to properly line up your SELECT, FROM, GROUP BY, and WHERE statements, and all of the information contained in them. This way, you and others you work with can return to a saved query and easily tell if these statements are part of a main query, or a subquery.

4. Annotate your queries
01:28 - 01:48
It's also considered best practice to annotate your queries with comments in order to tell the user what it does -- using either a multiple line comment, inside a forward slash, star, and ending with a star, and a forward slash.

5. Annotate your queries
01:48 - 02:03
You can also use in-line comments using two dashes. Every piece of information after an in-line comment is treated as text, even if it's a recognized SQL command.

6. Indent your queries
02:03 - 02:29
Additionally, make sure that you properly indent all information contained within a subquery. That way, you can easily return to the query and understand what information is being processed first, where you need to apply changes, such as to a range of dates, and what you can expect from your results if you make those changes.

7. Indent your queries
02:29 - 03:08
Make sure that you clearly indent all information that's part of a single column, such as a long CASE statement, or a complicated subquery in SELECT. In order to best keep track of all the conditions necessary to set up each WHEN clause, each THEN clause, and how they create the column outcome, it's important to clearly indent each piece of information in the statement. Overall, I highly recommend you read Holywell's SQL Style Guide to get a sense of all the formatting conventions when working with SQL queries.

8. Is that subquery necessary?
03:08 - 03:41
When deciding whether or not you need a subquery, it's important to know that each subquery you add requires additional computing power to generate your results. Depending on the size of your database and the number of records you extract in your query, you may significantly increase the amount of time it takes to run your query. So it's always worth asking whether or not a specific subquery is necessary to get the results you need.

9. Properly filter each subquery!
03:41 - 04:21
Finally, when constructing a main query with multiple subquery, make sure that your filters are properly placed in every subquery, and the main query, in order to generate accurate results. The query here, for example, filters for the 2013/2014 season in 3 places -- once in the SELECT subquery, once in the WHERE subquery, and once in the main query. This ensures that all data returned is only about matches from the 2013/2014 season.

10. Let's practice!
04:21 - 04:31
Okay! Time to practice creating complex queries with multiple subqueries.
