# Recursive CTEs - Story Map

## 1. Story
You need to show an org chart: CEO, their direct reports, and all levels below. A single SELECT can only see one level at a time.

## 2. Core Concepts (street version)
- Recursive CTEs walk a tree level by level.
- The anchor is the starting set.
- The recursive part keeps adding children until it runs out.

## 3. Why a normal JOIN is not enough
One JOIN gives you only one hop. You need repeated hops without writing endless self-joins.

## 4. What a recursive CTE is
A named query that contains:
- an anchor query (level 0)
- a recursive query (level 1, 2, 3...) that references itself

## 5. Anchor vs recursive intuition
Anchor = seed nodes.  
Recursive = "given what we already found, find the next layer."

## 6. Termination
Recursion stops when the recursive query returns no new rows.

## 7. Hierarchy example
Start at the CEO, then add direct reports, then their reports, and so on.

## 8. What recursive CTEs are great at
- Org charts and reporting lines
- Bill of materials / parts explosion
- Graph or tree traversal inside SQL

## 9. What recursive CTEs are bad at
- Cycles without protection
- Very deep trees without limits
- Extremely large graphs without careful pruning

## 10. Final mental model
Recursive CTEs are "loops in SQL": seed a set, then keep expanding it until nothing new appears.

## 11. Run Order
1. c101_recursive_ctes_demo.py
