# Cache Stampede — Story Map

## 1. Story (restaurant / one menu item runs out / everyone asks kitchen)
A menu item runs out. Ten waiters ask the kitchen at the same time. The kitchen gets flooded with the same request.

## 2. Core Concepts (street version)
- Many readers can miss together.
- Every miss hits the DB.
- TTL expiry can sync the misses.

## 3. What Cache Stampede Is
A burst of concurrent misses all rebuild the same cache entry.

## 4. Why It Happens
- Cache entry expires.
- Many requests arrive at once.
- Each request thinks it must fetch.

## 5. Why It Is Dangerous
It defeats the cache and overloads the DB exactly when traffic spikes.

## 6. Basic Ways To Prevent It
- Single-flight / request coalescing.
- Locks or mutex around rebuild.
- Serve stale for a short window (stale-while-revalidate).

## 7. Final Mental Model
Too many waiters, one kitchen, no line control.

## 8. Run Order
1. c072_stampede_demo.py
