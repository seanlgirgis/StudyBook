# Course 4: Data Manipulation in SQL - chapter_01_raw_transcript

Status: placeholder


## Transcript Section: Complex CASE Logic

1. In CASE things get more complex
00:00 - 00:09
Now that you understand the basics of CASE statements, let's set up some more complex logical tests.

2. Reviewing CASE WHEN
00:09 - 00:44
Previously, we covered CASE statements with one logical test in a WHEN statement, returning outcomes based on whether that test is TRUE or FALSE. This example tests whether home or away goals were higher, and identifies them as wins for the team that had a higher score. Everything ELSE is categorized as a tie. The resulting table has one column identifying matches as one of 3 possible outcomes.

3. CASE WHEN ... AND then some
00:44 - 01:53
If you want to test multiple logical conditions in a CASE statement, you can use AND inside your WHEN clause. For example, let's see if each match was played, and won, by the team Chelsea. Let's see the CASE statement in this query. Each WHEN clause contains two logical tests -- the first tests if a hometead_id identifies Chelsea, AND then it tests if the home team scored higher than the away team. If both conditions are TRUE, the new column output returns the phrase "Chelsea home win!". The opposite set of conditions are included in a second when statement -- if the awayteam_id belongs to Chelsea, AND scored higher, then the output returns "Chelsea away win!". All other matches are categorized as a loss or tie. Here's the resulting table.

4. What ELSE is being excluded?
01:53 - 02:40
When testing logical conditions, it's important to carefully consider which rows of your data are part of your ELSE clause, and if they're categorized correctly. Here's the same CASE statement from the previous slide, but the WHERE filter has been removed. Without this filter, your ELSE clause will categorize ALL matches played by anyone, who don't meet these first two conditions, as "Loss or tie :(". Here are the results of this query. A quick look at it shows that the first few matches are all categorized as "Loss or tie", but neither the hometeam_id or awayteam_id belong to Chelsea.

5. Correctly categorize your data with CASE
02:40 - 03:20
The easiest way to correct for this is to ensure you add specific filters in the WHERE clause that exclude all teams where Chelsea did not play. Here, we specify this by using an OR statement in WHERE, which retrieves only results where the id 8455 is present in the hometeam_id or awayteam_id columns. The resulting table from earlier, with the team IDs in bold here, clearly specifies whether Chelsea was home or away team.

6. What's NULL?
03:20 - 03:44
It's also important to consider what your ELSE clause is doing. These two queries here are identical, except for the ELSE NULL statement specified in the second. They both return identical results -- a table with quite a few null results. But what if you want to exclude them?

7. What are your NULL values doing?
03:44 - 04:04
Let's say we're only interested in viewing the results of games where Chelsea won, and we don't care if they lose or tie. Just like in the previous example, simply removing the ELSE clause will still retrieve those results -- and a lot of NULL values.

8. Where to place your CASE?
04:04 - 04:20
To correct for this, you can treat the entire CASE statement as a column to filter by in your WHERE clause, just like any other column. In order to filter a query by a CASE statement,

9. Where to place your CASE?
04:20 - 04:50
you include the entire CASE statement, except its alias, in WHERE. You then specify what you want to include, or exclude. For this query, I want to keep all rows where this CASE statement IS NOT NULL. My resulting table now only includes Chelsea's home and away wins -- and I don't need to filter by their team ID anymore!

10. Let's practice!
04:50 - 04:59
Okay! Let's practice some more complex CASE statements.

## Transcript Section: Complex CASE Logic

1. In CASE things get more complex
00:00 - 00:09
Now that you understand the basics of CASE statements, let's set up some more complex logical tests.

2. Reviewing CASE WHEN
00:09 - 00:44
Previously, we covered CASE statements with one logical test in a WHEN statement, returning outcomes based on whether that test is TRUE or FALSE. This example tests whether home or away goals were higher, and identifies them as wins for the team that had a higher score. Everything ELSE is categorized as a tie. The resulting table has one column identifying matches as one of 3 possible outcomes.

3. CASE WHEN ... AND then some
00:44 - 01:53
If you want to test multiple logical conditions in a CASE statement, you can use AND inside your WHEN clause. For example, let's see if each match was played, and won, by the team Chelsea. Let's see the CASE statement in this query. Each WHEN clause contains two logical tests -- the first tests if a hometead_id identifies Chelsea, AND then it tests if the home team scored higher than the away team. If both conditions are TRUE, the new column output returns the phrase "Chelsea home win!". The opposite set of conditions are included in a second when statement -- if the awayteam_id belongs to Chelsea, AND scored higher, then the output returns "Chelsea away win!". All other matches are categorized as a loss or tie. Here's the resulting table.

4. What ELSE is being excluded?
01:53 - 02:40
When testing logical conditions, it's important to carefully consider which rows of your data are part of your ELSE clause, and if they're categorized correctly. Here's the same CASE statement from the previous slide, but the WHERE filter has been removed. Without this filter, your ELSE clause will categorize ALL matches played by anyone, who don't meet these first two conditions, as "Loss or tie :(". Here are the results of this query. A quick look at it shows that the first few matches are all categorized as "Loss or tie", but neither the hometeam_id or awayteam_id belong to Chelsea.

5. Correctly categorize your data with CASE
02:40 - 03:20
The easiest way to correct for this is to ensure you add specific filters in the WHERE clause that exclude all teams where Chelsea did not play. Here, we specify this by using an OR statement in WHERE, which retrieves only results where the id 8455 is present in the hometeam_id or awayteam_id columns. The resulting table from earlier, with the team IDs in bold here, clearly specifies whether Chelsea was home or away team.

6. What's NULL?
03:20 - 03:44
It's also important to consider what your ELSE clause is doing. These two queries here are identical, except for the ELSE NULL statement specified in the second. They both return identical results -- a table with quite a few null results. But what if you want to exclude them?

7. What are your NULL values doing?
03:44 - 04:04
Let's say we're only interested in viewing the results of games where Chelsea won, and we don't care if they lose or tie. Just like in the previous example, simply removing the ELSE clause will still retrieve those results -- and a lot of NULL values.

8. Where to place your CASE?
04:04 - 04:20
To correct for this, you can treat the entire CASE statement as a column to filter by in your WHERE clause, just like any other column. In order to filter a query by a CASE statement,

9. Where to place your CASE?
04:20 - 04:50
you include the entire CASE statement, except its alias, in WHERE. You then specify what you want to include, or exclude. For this query, I want to keep all rows where this CASE statement IS NOT NULL. My resulting table now only includes Chelsea's home and away wins -- and I don't need to filter by their team ID anymore!

10. Let's practice!
04:50 - 04:59
Okay! Let's practice some more complex CASE statements.

## Transcript Section: CASE WHEN with Aggregate Functions

1. CASE WHEN with aggregate functions
00:00 - 00:08
Great job so far! Let's take a look at CASE statements with aggregate functions.

2. In CASE you need to aggregate
00:08 - 00:24
CASE statements can be used to create columns for categorizing data, and to filter your data in the WHERE clause. You can also use CASE statements to aggregate data based on the result of a logical test.

3. COUNTing CASES
00:24 - 00:48
Let's say you wanted to prepare a summary table counting the number of home and away games that Liverpool won in each season. If you've created summary tables in Spreadsheets, you can probably visualize the final table, here -- but how do you get a count of Liverpool's wins in each season?

4. CASE WHEN with COUNT
00:48 - 01:38
You guessed it -- a CASE statement. CASE statements are like any other column in your query, so you can include them inside an aggregate function. Take a look at the CASE statement. The WHEN clause includes a similar logical test to the previous lesson -- did Liverpool play as the home team, AND did the home team score higher than the away team? The difference begins in your THEN clause. Instead of returning a string of text, you return the column identifying the unique match id. When this CASE statement is inside the COUNT function, it COUNTS every id returned by this CASE statement.

5. CASE WHEN with COUNT
01:38 - 01:53
You then add a second CASE statement for the away team, and group the query by the season. When counting information in a CASE statement, you can return anything you'd like --

6. CASE WHEN with COUNT
01:53 - 02:05
a number, a string of text, or any column in the table, SQL is COUNTing the number of rows returned by the CASE statement.

7. CASE WHEN with SUM
02:05 - 02:41
Similarly, you can use the SUM function to calculate a total of any value. Let's say we're interested in the number of home and away goals that Liverpool scored in each season. This is fairly simple to set up -- if the hometeam_id is Liverpool's, return the home_goal value. The ELSE condition is assumed to be NULL, so the query returns the total home_goals scored by Liverpool in each season.

8. The CASE is fairly AVG...
02:41 - 03:11
You can also use the AVG function with CASE in two key ways. First, you can calculate an average of data. You can do this using CASE in the EXACT same way you used the SUM function. Just change out SUM for AVG in this query, and you instead get the AVG goals Liverpool scored in each season.

9. A ROUNDed AVG
03:11 - 03:23
You can make the results easier to read using ROUND. ROUND takes 2 arguments -- a numerical value, and the number of decimal points to round the value to.

10. A ROUNDed AVG
03:23 - 03:35
Place it outside your aggregate CASE statement, and include the number of decimal points at the end. There, that's much easier to read!

11. Percentages with CASE and AVG
03:35 - 04:36
The second key application of CASE with AVG is in the calculation of percentages. This requires a specific structure in order for your calculation to be accurate. The question we're answering here is, "What percentage of Liverpool's games did they win in each season?" The first component of this CASE statement is a WHEN clause identifying what you're calculating a percentage of -- in this case, how many games did they win? This is tested in the same way as previous slides, and your THEN clause returns a 1. The second component identifies Liverpool's games that they LOST, and returns the value 0. All other matches -- ties, games not involving Liverpool -- are excluded as NULLs. Here are the results of this query ...

12. Percentages with CASE and AVG
04:36 - 04:41
... and here's the ROUNDed, more readable version of the results.

13. Let's practice!
04:41 - 04:51
Now it's your turn to practice creating CASE statements with aggregate functions.
