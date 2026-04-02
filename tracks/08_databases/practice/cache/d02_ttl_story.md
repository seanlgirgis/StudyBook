# TTL — Story Map

## 1. Story (fridge leftovers / timestamp sticker)
You stick a time label on leftovers. If the label says it expired, you throw it out and cook again.

## 2. Core Concepts (street version)
- TTL = time-to-live.
- Cache value is valid only for a window.
- Short TTL = fresher but more misses.

## 3. What TTL Is
A cached value carries an expiration time. After that, it is treated as missing.

## 4. Hit Before Expiry
If you read before the timer ends, you get a fast cache hit.

## 5. Miss After Expiry
Once the timer is past, the cache entry is stale and you must fetch again.

## 6. Why TTL Helps
It limits how long stale data can live while still speeding up repeats.

## 7. What TTL Does Not Solve Perfectly
TTL does not guarantee freshness. You can still serve stale data inside the window.

## 8. Final Mental Model
Time sticker on leftovers: good until the clock runs out.

## 9. Run Order
1. c071_ttl_demo.py
