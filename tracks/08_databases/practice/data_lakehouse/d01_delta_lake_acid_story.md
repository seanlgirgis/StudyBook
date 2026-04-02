# ACID on Object Storage (Delta Lake Concepts) - Story Map

## 1. Story (shared notebook)
A shared notebook tracks every change. Readers can open a specific version and see a consistent view.

## 2. Core Concepts (street version)
- Transaction log = ordered record of commits.
- Atomic commit = all-or-nothing file add.
- Snapshot = consistent view at a version.

## 3. How ACID Works
Each write appends a new log entry with the files added. Readers choose a version to read.

## 4. Safe Concurrent Updates
Multiple writers add new versions without corrupting old snapshots.

## 5. Final Mental Model
The log is the truth. Files are immutable. Snapshots provide consistency.

## 6. Run Order
1. c002_delta_lake_acid_demo.py
