# Heap + Min Heap Micro Nuggets

Run these in order, one tiny idea at a time:

1. `python nugget_01_heap_meaning.py`
2. `python nugget_02_min_heap_ops.py`
3. `python nugget_03_max_heap_by_negation.py`
4. `python nugget_04_top_k_patterns.py`
5. `python nugget_05_common_tricks.py`

Goal: build intuition fast, then reuse the same patterns in interview questions.

## Min-Heap Operation Graph

```text
Start (heap with n elements)
   |
   +-- peek: heap[0] ----------------------> O(1)
   |
   +-- heappush(x)
   |      Step 1: put x at end
   |      Step 2: sift up
   |---------------------------------------> O(log n)
   |
   +-- heappop()
   |      Step 1: remove root (smallest)
   |      Step 2: move last element to root
   |      Step 3: sift down
   |---------------------------------------> O(log n)
   |
   +-- heapreplace(x)
   |      Step 1: pop root
   |      Step 2: place x at root
   |      Step 3: sift down
   |---------------------------------------> O(log n)
   |
   +-- heapify(list of n items)
          Build heap bottom-up
   ----------------------------------------> O(n)
```

## Quick Cost Table

| Operation | What it does | Time |
|---|---|---|
| `heap[0]` | Read current smallest | `O(1)` |
| `heappush` | Insert new item + restore heap | `O(log n)` |
| `heappop` | Remove smallest + restore heap | `O(log n)` |
| `heapreplace` | Pop smallest then push in one op | `O(log n)` |
| `heapify` | Convert unsorted list to heap | `O(n)` |

Note: heap internals are not fully sorted. Full ascending order appears only after repeated `heappop()`.
