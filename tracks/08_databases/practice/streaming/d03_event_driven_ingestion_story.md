# Event-Driven Ingestion - Story Map

## 1. Story (kitchen bell vs hallway checks)
A restaurant can check the kitchen every minute to see if food is ready, or the kitchen can ring a bell the moment a dish is done. The bell is faster and wastes less effort.

## 2. Core Concepts (street version)
- Polling = repeatedly asking "anything new?"
- Event-driven = producer announces changes immediately.
- Fan-out = multiple listeners react to the same event.

## 3. How It Works
CDC-style producers emit events when rows change. The stream becomes the bell. Consumers react as events arrive.

## 4. Why It Matters
No wasted polling, faster reactions, and many downstream services can stay in sync.

## 5. Failure Mode (backpressure)
If consumers are slow, events pile up. The stream must buffer until they catch up.

## 6. Final Mental Model
Event-driven ingestion is "ring the bell on change" instead of "check the kitchen repeatedly."

## 7. Run Order
1. c004_event_driven_ingestion_demo.py
