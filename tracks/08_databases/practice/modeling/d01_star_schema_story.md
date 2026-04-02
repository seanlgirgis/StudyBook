# Star Schema - Story Map

## 1. Story (hub and spokes)
A bike wheel has a hub in the middle and spokes reaching out. Facts sit in the hub. Dimensions sit on the spokes.

## 2. Core Concepts (street version)
- Fact table = central hub of measurable events.
- Dimension tables = spokes with descriptive details.
- Star schema = one fact joined to many dimensions.

## 3. Why It Exists
Analysts can ask questions quickly by joining one fact table to a few dimensions.

## 4. What It Looks Like
Fact Sales links to Customer, Product, and Date dimensions.

## 5. Example Question
"Total sales by product category and month."

## 6. Final Mental Model
Star schema is a hub-and-spoke design for fast analytics.

## 7. Run Order
1. c002_star_schema_demo.py
