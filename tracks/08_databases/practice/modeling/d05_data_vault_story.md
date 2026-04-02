# Data Vault Basics - Story Map

## 1. Story (library cards)
The library keeps a card for each person, a card for each book, and a card for each checkout. Details about people and books are stored separately and updated over time without erasing old cards.

## 2. Core Concepts (street version)
- Hub = business keys only (stable identifiers).
- Link = relationships between hubs.
- Satellite = descriptive attributes + history.

## 3. Why It Exists
You keep audit-friendly history and can add new sources without redesigning the core model.

## 4. How It Works
Hubs store keys, links connect them, satellites store changing attributes with timestamps.

## 5. History Preservation
Satellites add new rows for changes instead of overwriting.

## 6. Final Mental Model
Data vault separates "who/what" (hubs), "how related" (links), and "what changed" (satellites).

## 7. Run Order
1. c006_data_vault_demo.py
