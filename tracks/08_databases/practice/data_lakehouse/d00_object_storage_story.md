# Object Storage Concepts - Story Map

## 1. Story (warehouse shelves)
A warehouse stores boxes on shelves. You find items by aisle/prefix, not by row IDs.

## 2. Core Concepts (street version)
- Bucket = top-level container.
- Prefix = folder-like path inside the bucket.
- Object = immutable file stored at a key.

## 3. File-Based Layout
Data is stored as files (Parquet/CSV) organized by prefixes like `raw/` and `curated/`.

## 4. Immutability
Objects are not updated in place; changes create new objects.

## 5. Why It Differs from Databases
Databases update rows in place. Object storage writes new files and scans them later.

## 6. Final Mental Model
Buckets + prefixes + immutable objects = scalable file storage for data lakes.

## 7. Run Order
1. c001_object_storage_demo.py
