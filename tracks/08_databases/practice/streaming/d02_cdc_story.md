# CDC (Change Data Capture) - Story Map

## 1. Story (receipt printer)
A store keeps a ledger of items. Every time the ledger changes, a receipt printer spits out a slip. Other teams read the slips instead of re-reading the entire ledger.

## 2. Core Concepts (street version)
- Source table = the ledger of truth.
- CDC event = a change slip (insert, update, delete).
- Downstream consumer = a team that reacts to slips.

## 3. What CDC Does
CDC watches row changes and emits events that describe what changed, not the whole table.

## 4. Why It Matters
Downstream systems can update quickly without full rescans. They only process the change slips.

## 5. Insert / Update / Delete
- Insert: new row appears.
- Update: existing row changes.
- Delete: row removed.

## 6. Failure Mode (missed changes)
If CDC events are lost, downstream systems drift. This is why offsets and ordering matter.

## 7. Final Mental Model
CDC is a receipt printer for your database. Every row change becomes an event.

## 8. Run Order
1. c003_cdc_demo.py
