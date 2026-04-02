# Cost Model — Story Map

## 1. Story
You are choosing a route before traffic happens. You do not know the future, so you pick the route that looks cheapest on paper.

## 2. Core Concepts (street version)
- Planner = the brain that picks a plan before running.
- Cost = a relative score, not real milliseconds.
- Stats = the planner's map of the data.

## 3. What The Cost Model Is
The planner compares possible paths and picks the one with the lowest estimated cost.
It is guessing the cheapest path before it runs.

## 4. What Inputs The Planner Uses
- Row counts and selectivity estimates.
- Indexes and their expected payoff.
- Basic I/O + CPU cost assumptions.

## 5. Why Estimates Can Be Wrong
If stats are stale or too weak, the planner guesses the wrong row counts.
Wrong guesses lead to wrong plans.

## 6. Why ANALYZE Matters
ANALYZE refreshes stats so the planner can estimate selectivity correctly.
Better estimates usually mean better plans.

## 7. Final Mental Model
Planner = a cost-based gambler.
Stats = the odds sheet.
Bad odds = bad bets.

## 8. Run Order
1. c063_cost_model_demo.py
