# Fact vs Dimension Tables - Story Map

## 1. Story (receipt + catalog)
A store keeps receipts for every purchase and a catalog for product details. Receipts tell you what happened. The catalog tells you what the items are.

## 2. Core Concepts (street version)
- Fact table = measurable events (sales, clicks, shipments).
- Dimension table = descriptive context (who, what, where).

## 3. Fact Table (what it contains)
Facts store numeric measures and foreign keys to dimensions: amount, quantity, date, customer_id, product_id.

## 4. Dimension Table (what it contains)
Dimensions store attributes: customer name, segment, product category, region.

## 5. Why Both Exist
Facts are big and grow fast. Dimensions are smaller and help you slice the facts.

## 6. How Reporting Works
Join facts to dimensions to answer questions like "revenue by product category" or "sales by customer segment."

## 7. Final Mental Model
Facts are the receipts. Dimensions are the labels that explain the receipts.

## 8. Run Order
1. c001_fact_vs_dimension_demo.py
