# Query Optimization — Story Map

## Story
A simple lookup was fast at 1,000 rows. Six months later at 1,000,000 rows it is slow and expensive.

## Scenario
The app needs to find a customer order by email.
The query works, but the database scans the whole table each time.

## Pain
Scanning everything gets slower as data grows.
The system feels “fine” in dev and “broken” in prod.

## Diagnosis
Use EXPLAIN or EXPLAIN ANALYZE to see the execution plan.
If you see a **Seq Scan**, the database is reading many rows.

## Fix
Make the database find rows directly:
- use a clean predicate
- add the right index

## Pattern
Optimization = help the database do less work.
Prefer targeted lookup over full table scans.

## System
The database is choosing a path.
Optimization = giving it a better path or better structure.

## Cost-Based Planning
- The database does not blindly use indexes
- It estimates cost of different strategies
- It may choose a full scan if many rows match

Mental model:
The database is a planner choosing the cheapest path.

## When Indexes Are Ignored
- Cost-based decisions can favor a scan
- Low selectivity means too many rows match
- Predicate shape can block index use
- Tiny tables can be cheaper to scan than to use an index
- Planner decisions depend on real table size, so demos must reset data correctly

## Mental Model
Table scan = check every shelf.
Index scan = go straight to the right shelf.

## Run Order
1. c050_query_optimization_bad_vs_good.py
2. c051_explain_plan_reading.py
