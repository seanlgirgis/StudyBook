# Parquet — Story Map

## 1. Story
You export a year of receipts to CSV. It works, but every report feels heavy and slow.

## 2. Core Concepts (street version)
- CSV = simple text rows.
- Parquet = columnar binary format.

## 3. Why Parquet Exists
Analytics reads lots of rows but only a few columns.
CSV makes you drag every column, every time.

## 4. Why Parquet Is Better Than CSV For Analytics
Parquet stores columns together and compresses them well.
Engines read less, store less, and scan faster.

## 5. What Parquet Stores That Helps Engines Work Smarter
Column chunks and metadata about columns.
That lets engines skip work and only load what’s needed.

## 6. When CSV Is Still Fine
Small data, quick sharing, or one-off debugging.
You want human-readable files.

## 7. Final Mental Model
CSV = read the whole receipt box.
Parquet = pull just the totals column.

## 8. Run Order
1. c061_parquet_demo.py
