# Time Travel Queries - Story Map

## 1. Story (library archive)
A library keeps archived editions. You can open the 2020 edition even if the 2024 edition is current.

## 2. Core Concepts (street version)
- Snapshot = versioned table state.
- Time travel = query a past snapshot.
- Safety = no writes, just read historical state.

## 3. How It Works
Each commit creates a new snapshot. Queries specify which snapshot to read.

## 4. Final Mental Model
Time travel lets you see the past without mutating the present.

## 5. Run Order
1. c004_time_travel_demo.py
