# Watermarks vs High-Water Marks - Story Map

## 1. Story (train schedule)
A station tracks the last train that arrived (high-water mark). It also posts a cutoff time after which late trains are ignored (watermark).

## 2. Core Concepts (street version)
- High-water mark = the latest event_time successfully processed.
- Watermark = a moving cutoff time for late data (max event_time - tolerance).
- Late data = events older than the watermark.

## 3. High-Water Mark (what it does)
The high-water mark tracks progress. It is the checkpoint for “how far we got.”

## 4. Watermark (what it does)
The watermark decides whether an event is too late to be processed.

## 5. Failure Mode (late arrivals)
If late events arrive after the watermark, they are dropped or routed to a late-data queue.

## 6. Final Mental Model
High-water mark = progress. Watermark = lateness cutoff. They move together but serve different roles.

## 7. Run Order
1. c003_watermarks_demo.py
