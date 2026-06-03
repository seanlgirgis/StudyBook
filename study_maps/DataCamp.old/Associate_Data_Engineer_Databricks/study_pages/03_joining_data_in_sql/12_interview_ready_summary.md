# Course 3: Joining Data in SQL - Interview Ready Summary

Status: draft interview summary started

Interview-safe summary:

In this course, I practiced several ways to combine and compare relational data.
I used INNER, LEFT, RIGHT, FULL, CROSS, and SELF joins for different table
relationship problems. I also practiced set operations such as UNION,
UNION ALL, INTERSECT, and EXCEPT, which combine or compare SELECT results
vertically. Finally, I practiced subqueries inside WHERE, SELECT, and FROM,
including semi join and anti join patterns for filtering rows based on another
query.

A safe practical framing:
I choose the SQL pattern based on the business question. If I need matching
records only, I use INNER JOIN. If I need to preserve a main list, I use
LEFT JOIN. If I need reconciliation, I use FULL JOIN. If I need to compare
complete result sets, I use set operations. If I need one query to filter or
calculate from another query, I use subqueries.
