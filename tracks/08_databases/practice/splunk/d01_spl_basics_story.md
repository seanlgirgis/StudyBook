# SPL Basics - Story Map

## 1. Story (searching a toolbox)
You open the toolbox (index), filter by tool type, then count how many of each you have.

## 2. Core Concepts (street version)
- `index=` selects the dataset.
- Filters narrow results (e.g., `level=ERROR`).
- `stats count by field` summarizes events.

## 3. Typical Flow
Start broad with an index, filter to the signal, then aggregate.

## 4. Final Mental Model
SPL is a pipeline: search ? filter ? stats.

## 5. Run Order
1. c002_spl_basics_demo.py
