# JSON / Array Functions - Story Map

## 1. Story
You ingest event payloads with nested JSON and arrays. The analytics team wants clean columns and per-item rows for reporting.

## 2. Core Concepts (street version)
- JSON functions pull fields out of nested structures.
- Array functions expand lists into rows.
- After expansion, you regroup to summarize.

## 3. Why plain SELECT is not enough
Nested data hides the fields you need and lists bundle many items into one cell.

## 4. What JSON functions do
Extract or cast specific fields from nested objects (for example, customer.city).

## 5. What array functions do
Turn a list into one row per item (often called UNNEST or EXPLODE).

## 6. The typical flow
Extract fields -> explode arrays -> aggregate results.

## 7. Example
Orders stored inside a customer record:
- Extract customer name and city
- Explode orders into rows
- Group to get total spend per customer

## 8. What json / array functions are great at
- Semi-structured logs and events
- Flattening API payloads
- Building fact tables from nested sources

## 9. What json / array functions are bad at
- Ambiguous schemas
- Deep nesting without clear paths
- Heavy use without indexing or pruning

## 10. Final mental model
JSON functions find the fields. Array functions make them rows.

## 11. Run Order
1. c103_json_array_functions_demo.py
