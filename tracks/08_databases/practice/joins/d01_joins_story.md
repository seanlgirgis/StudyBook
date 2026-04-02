# Joins — Story Map

## Story
You need customer names next to their orders. A simple JOIN works, but it gets slow as the tables grow.

## Scenario
You join `customers` and `orders` on `customer_id`.
Sometimes the database is fast, sometimes it is slow.

## Pain
The same query feels different in dev vs prod.
The join strategy changes as data grows.

## Diagnosis
A JOIN is how the database combines rows from two tables.
It picks a **join strategy** based on cost.

### Nested Loop
Good for small tables or when an index exists.
Mental model: **for each row → lookup**.

### Hash Join
Good for large sets without useful indexes.
Mental model: **build lookup table → match**.

## Fix
Add the right index when lookups are selective.
Accept hash joins when scanning big sets.

## Pattern
The planner chooses a join based on estimated cost.
An index does not automatically force Nested Loop.
Join shape and selectivity matter.
Tiny outer set means truly tiny, not a few hundred rows.

## System
Joins are not just “SQL syntax.”
They are physical strategies chosen by the planner.

## Run Order
1. c057_nested_loop_vs_hash_join.py
2. c058_join_with_index_vs_without.py
