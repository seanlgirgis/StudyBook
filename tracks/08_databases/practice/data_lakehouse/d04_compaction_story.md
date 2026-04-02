# Compaction and Optimization - Story Map

## 1. Story (mail sorting)
Many small envelopes slow down sorting. Bundling them into fewer larger bags speeds the process.

## 2. Core Concepts (street version)
- Small files = high overhead per file.
- Compaction = rewrite many small files into fewer large files.
- Optimization = better layout for faster scans.

## 3. Why It Matters
Engines pay a cost to open each file. Too many files slows queries.

## 4. Final Mental Model
Compaction trades rewrite cost for faster reads.

## 5. Run Order
1. c005_compaction_demo.py
