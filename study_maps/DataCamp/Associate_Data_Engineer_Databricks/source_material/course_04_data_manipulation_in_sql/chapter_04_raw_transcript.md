# Course 4: Data Manipulation in SQL - Chapter 4 Raw Transcript

Status: raw transcript captured

## Transcript Section: Window Functions Intro

1. Window Functions
00:00 - 00:12
Great job! You now have experience transforming data using simple subqueries, correlated subqueries, and common table expressions.

2. Working with aggregate values
00:12 - 00:36
Let's tackle another limitation you've likely encountered in SQL -- the fact that you have to group results when using aggregate functions. If you try to retrieve additional information without grouping by every single non-aggregate value, your query will return an error. Thus, you can't compare aggregate values to non-aggregate data.

3. Introducing window functions!
00:36 - 01:12
You can work around this limitation using a window function. Window functions are a class of functions that perform calculations on a result set that has already been generated, also referred to as a "window". You can use window functions to perform aggregate calculations without having to group your data, just as you did with a subquery in SELECT. You can also use them to calculate information such as running totals, rankings, and moving averages.

4. What's a window function?
01:12 - 01:40
So what's a window function? How do you use it? Let's start with a query from chapter 2, where we answered the question, "how many goals were scored in each match in 2011/2012, and how did that compare to the average?" This query selects two columns from match table, and then used a subquery in SELECT to pass the overall average along the data set without aggregating the results.

5. What's a window function?
01:40 - 02:15
The same results can be generated using the clause common to all window functions -- the OVER clause. Instead of writing a subquery, calculate the AVG of home_goal and away_goal, and follow it with the OVER clause. This clause tells SQL to "pass this aggregate value over this existing result set." The results are identical to the previous statement that used a subquery in SELECT, with a simpler syntax and faster processing time.

6. Generate a RANK
02:15 - 02:46
Another simple type of column you can generate with a window function is a RANK. A RANK simply creates a column numbering your data set from highest to lowest, or lowest to highest, based on a column that you specify. Let's take the same query as the previous example, without the window function, and use it to answer the question -- what is the RANK of matches based on the number of goals scored?

7. Generate a RANK
02:46 - 03:27
We can answer this using the RANK window function. In order to set this up, let's add a new column in SELECT as you see here. To create the rank, you start with the RANK function, using parentheses, followed by the OVER clause. Inside the OVER clause, include the ORDER BY clause, and the column or columns you want to use to generate the rank. By default, the RANK function orders the results and ranking from smallest to largest values. In the case of our data set here, this isn't particularly informative.

8. Generate a RANK
03:27 - 03:51
You can easily correct this by adding the DESC function to reverse the order of the rank, just as you would if you were using ORDER BY at the end of your query. You'll notice that the RANK function automatically ties identical values, such as the first 2 results, and then skips the next value in the rank.

9. Key differences
03:51 - 04:26
There are a few key considerations when using window functions. First, window functions are processed after the entire query except the final ORDER BY statement. Thus, the window function uses the result set to calculate information, as opposed to using the database directly. Second, it's important to know that window functions are available in PostgreSQL, Oracle, MySQL, but not in SQLite.

10. Let's practice!
04:26 - 04:34
Okay, let's practice some simple window functions using the OVER clause!

## Transcript Section: Window Partitions

1. Window Partitions
00:00 - 00:14
You've done a great job working with the OVER clause so far! The real bread and butter of window functions that differentiates them from subqueries in select, are in the functions you can add within the OVER clause.

2. OVER and PARTITION BY
00:14 - 01:08
One important statement you can add to your OVER clause is PARTITION BY. A partition allows you to calculate separate values for different categories established in a partition. This is one way to calculate different aggregate values within one column of data, and pass them down a data set, instead of having to calculate them in different columns. The syntax for a partition is fairly simple. Just like before, use an aggregate function to compute a calculation, such as the AVG of the home_goal column. You then add the OVER clause afterward, and inside the parentheses, state PARTITION BY, followed by the column you want to partition the average by. This will then return the overall average for, or PARTITIONed BY each season.

3. Partition your data
01:08 - 01:33
Let's take a look at how this works in a query. This is the example query from the previous lesson, answering the question, "How many goals were scored in each match, and how did that compare to the overall average?" This is accomplished using the OVER clause, and the query returns the date, goals scored, and overall average.

4. Partition your data
01:33 - 02:24
Let's expand on the previous question, and instead ask, "How many goals were scored in each match, and how did that compare to the season's average?" We can do this by adding a PARTITION BY clause to the OVER clause from the previous slide. Specifying, "PARTITION BY season" returns each season's average on each row, in accordance to the season that each record belongs to. As you can see, rows 1 and 2 are matches played in the 2011/2012 season, and the season_avg column contains the 2011/2012 season average. Rows 3 and 4 are part of the 2012/2013 season, and return the 2012/2013 season average.

5. PARTITION by Multiple Columns
02:24 - 03:05
You can also use PARTITION to calculate values broken out by multiple columns. In the query you see here, the OVER clause contains two columns to partition the AVG goals scored--season, and country. The result set returns the average goals scored broken out by season and country. In row 1, a match was played in Belgium in the 2011/2012 season, and had 1 goal scored throughout the match. This is compared to the 2.88, which is the average goals scored in Belgium in the 2011/2012 season.

6. PARTITION BY considerations
03:05 - 03:29
PARTITION BY is a pretty straight forward addition to the OVER clause. You can partition calculations by 1 or more columns as necessary to answer a question you may have. Additionally, you can use a PARTITION with any kind of window function -- calculation, rank, or others that we will discuss further in the following lesson.

7. Let's practice!
03:29 - 03:38
For now, let's practice calculating window partitions on our match data.

## Transcript Section: Sliding Windows

1. Sliding windows
00:00 - 00:13
In addition to calculating aggregate and rank information, window functions can also be used to calculate information that changes with each subsequent row in a data set.

2. Sliding windows
00:13 - 00:48
These types of window functions are called sliding windows. Sliding windows are functions that perform calculations relative to the current row of a data set. You can use sliding windows to calculate a wide variety of information that aggregates one row at a time down your data set -- running totals, sums, counts, and averages in any order you need. A sliding window calculation can also be partitioned by one or more columns, just like a non-sliding window.

3. Sliding window keywords
00:48 - 01:54
A sliding window function contains specific functions within the OVER clause to specify the data you want to use in your calculations. The general syntax looks like this -- you use the phrase ROWS BETWEEN to indicate that you plan on slicing information in your window function for each row in the data set, and then you specify the starting and finishing point of the calculation. For the start and finish in your ROWS BETWEEN statement, you can specify a number of keywords as shown here. PRECEDING and FOLLOWING are used to specify the number of rows before, or after, the current row that you want to include in a calculation. UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING tell SQL that you want to include every row since the beginning, or the end, of the data set in your calculations. Finally, CURRENT ROW tells SQL that you want to stop your calculation at the current row.

4. Sliding window example
01:54 - 02:39
For example, the sliding window in this query includes several key pieces of information in its calculation. It first states that the goal is to calculate a sum of goals scored when Manchester City played as the home team during the 2011/2012 season. It then tells you that you want to turn this calculation into a running total, ordered by the date of the match from oldest to most recent and calculated from the beginning of the data set to the current row. Your resulting data set looks like this, with a column calculating the total number of goals scored across the season, with a final total listed in the last row.

5. Sliding window frame
02:39 - 03:21
Using the PRECEDING statement, you also have the ability to calculate sliding windows with a more limited frame. For example, the query you see here is similar to the previous one, with a slightly modified sliding window. The phrase UNBOUNDED PRECEDING is replaced here with the phrase 1 PRECEDING, which calculates the sum of Manchester City's goals in the current and previous match. As you see in the data set here, the two rows in red are used to calculate the sum on the second row, and the two rows in green are used to calculate the sum on the third row.

6. Let's practice!
03:21 - 03:35
There are a wide variety of sliding windows you can use to calculate information in your query. Let's practice here with some examples based on what we've reviewed so far.

## Transcript Section: Bringing It All Together

1. Bringing it all Together
00:00 - 00:06
Congratulations! You've made it to the final lesson of the course.

2. What you've learned so far
00:06 - 00:50
Throughout the course we've covered a wide variety of methods for transforming, manipulating, and calculating data to answer a wide variety of questions in SQL. Specifically, you've learned how to use CASE statements for categorizing, aggregating, and calculating information, and how to use simple subqueries in SELECT, FROM, and WHERE clauses. You also learned how to use nested and correlated subqueries, and common table expressions to extract, match, and organize large amounts of data in order to generate a final table. Finally, you learned how to use some of the many window functions available to you in SQL.

3. Let's do a case study!
00:50 - 01:02
Let's put several of these topics together to answer one question about your data set -- Who defeated Manchester United in the 2013/2014 season?

4. Steps to construct the query
01:02 - 01:38
In the following exercises, you will generate a data set that tackles one of the issues we've explored during this course -- namely, that it's difficult to retrieve the names of teams who played in a given match. Since this isn't feasible with joins, we will accomplish it with common table expressions. We'll also be using CASE statements to categorize the outcomes of matches based on whether or not Manchester United won a particular match. Finally, we'll be ranking matches by the number of goals they lost the match using a window function.

5. Getting the database for yourself
01:38 - 01:56
If Manchester United happens to be a team that you favor, or if there are other European teams you consider a rival to your favorite team, I encourage you to explore the European Soccer Database for yourself and create similar, or completely different queries to answer your questions.

6. Let's practice!
01:56 - 02:02
Okay! Let's get to it!
