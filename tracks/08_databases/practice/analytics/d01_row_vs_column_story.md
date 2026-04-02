# Row vs Column Storage — Story Map

## 1. Story
You run analytics on receipts. The warehouse is full. Pulling every box is slow.

## 2. Core Concepts (street version)
- Row store = keeps full records together (OLTP mindset).
- Column store = keeps the same columns together (analytics mindset).

## 3. What Happens Under The Hood
Row storage pulls full rows, even if you need two fields.
Column storage pulls just the columns you touched and skips the rest.

## 4. Why Column Wins For Analytics
Analytics scans many rows but only a few columns.
Less data read = fewer pages = faster queries.

## 5. When Row Store Is Better
Point lookups and writes.
You need the whole row quickly, often.

## 6. Final Mental Model
Row store = pull the whole box.
Column store = pull only the labels you need.

## 7. Run Order
1. c060_row_vs_column_demo.py
