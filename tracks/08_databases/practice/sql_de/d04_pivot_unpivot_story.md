# Pivot / Unpivot - Story Map

## 1. Story
You get daily sales as rows (store, day, amount). Your manager wants a spreadsheet-style view: days as columns, stores as rows. Later, you need to turn it back into rows for analysis.

## 2. Core Concepts (street version)
- Pivot turns rows into columns.
- Unpivot turns columns back into rows.
- They are shape changes, not new data.

## 3. Why a normal GROUP BY is not enough
GROUP BY aggregates rows, but it does not rotate them into new columns.

## 4. What pivot is
Take one column's values and turn them into multiple columns, usually with an aggregate.

## 5. What unpivot is
Take multiple columns and turn them into a single value column with a label column.

## 6. Pivot vs unpivot intuition
Pivot = "wide table for humans."  
Unpivot = "tall table for machines."

## 7. Example
Rows: (store, day, sales)  
Pivot: one row per store, columns Mon/Tue/Wed  
Unpivot: back to (store, day, sales)

## 8. What pivot / unpivot are great at
- Cross-tab reporting
- Spreadsheet-style summaries
- Normalizing wide data for analytics

## 9. What pivot / unpivot are bad at
- Dynamic columns without clear definitions
- Extremely wide outputs
- Losing detail if you aggregate incorrectly

## 10. Final mental model
Pivot and unpivot rotate the same data between wide and tall shapes.

## 11. Run Order
1. c102_pivot_unpivot_demo.py
