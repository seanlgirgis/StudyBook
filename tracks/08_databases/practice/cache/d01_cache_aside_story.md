# Cache Aside — Story Map

## 1. Story (restaurant / waiter / kitchen)
A waiter gets the same order all night. First time, they run to the kitchen. Next time, they remember it and serve fast.

## 2. Core Concepts (street version)
- Cache = fast memory layer.
- DB = source of truth but slower.
- App controls the cache, not the DB.

## 3. What Cache Aside Is
Check cache first. If miss, go to DB, then store the result in cache.

## 4. Cache Hit vs Miss
- Miss: slow trip to the kitchen.
- Hit: fast serve from memory.

## 5. Why It Improves Performance
Most reads repeat. Once warm, the app avoids slow DB trips.

## 6. When It Breaks (stale data)
If the DB changes and cache is not updated, you serve the old order.

## 7. Final Mental Model
Waiter checks memory, then kitchen, then memorizes the answer.

## 8. Run Order
1. c070_cache_aside_demo.py
