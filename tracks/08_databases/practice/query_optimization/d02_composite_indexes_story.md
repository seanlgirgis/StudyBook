# Composite Indexes — Story Map

## Story
Searches were fast when users filtered by last name. Then product added first-name search and performance got weird.

## Scenario
You store contacts. You add an index on `(last_name, first_name)` and expect all name searches to be fast.

## Pain
Some queries fly, some crawl, even though “the index exists.”

## Diagnosis
Composite index = one index over multiple columns.
It follows the **left-to-right rule**:
- index on `(col1, col2)` can use `col1`
- can use `col1 + col2`
- **cannot** use `col2` alone well

## Fix
Order columns by how queries filter.
Put the most common leading filter first.

## Pattern
Column order matters more than people think.
Design composite indexes around real query shapes.

## System
Indexes are sorted structures.
If the left side is missing, the database cannot jump to the right side.

## Mental Model
Composite index is like a book sorted by **last name, then first name**.
You can search by:
- last name
- last + first

First name alone is weak because the book is not sorted by first name first.

## When Composite Index Helps
- Queries filter by the leftmost column(s)
- Queries filter by full prefix of the index
- Helps most when each added column narrows the search further

## When It Does Not
- Query uses only the trailing column
- Query wraps the leading column in a function
- Most rows match (low selectivity)

## Run Order
1. c053_composite_index_left_to_right.py
2. c054_composite_index_good_vs_bad_queries.py
