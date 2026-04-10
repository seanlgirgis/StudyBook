# Deque (Double-Ended Queue) — Basics Sheet

---

## What is a Deque?

A **deque** (pronounced *"deck"*) is a linear data structure where you can **add and remove elements from both ends** — left and right — in O(1) time.

```
         LEFT end                      RIGHT end
            │                               │
            ▼                               ▼
    ┌───────────────────────────────────────┐
    │  [A]  │  [B]  │  [C]  │  [D]  │  [E] │
    └───────────────────────────────────────┘
            ▲                               ▲
            │                               │
      appendleft()                      append()
      popleft()                          pop()
```

In Python:
```python
from collections import deque

dq = deque()
dq = deque([1, 2, 3])        # initialize with iterable
dq = deque([1, 2, 3], maxlen=5)  # bounded deque (auto-evicts oldest)
```

---

## Core Operations

### `append(x)` — Add to RIGHT

```
Before:  [A] [B] [C]
After:   [A] [B] [C] [X]
                      ▲
                   appended
```
```python
dq = deque([1, 2, 3])
dq.append(4)
# deque([1, 2, 3, 4])
```

---

### `appendleft(x)` — Add to LEFT

```
Before:      [A] [B] [C]
After:   [X] [A] [B] [C]
          ▲
       appendleft
```
```python
dq = deque([1, 2, 3])
dq.appendleft(0)
# deque([0, 1, 2, 3])
```

---

### `pop()` — Remove from RIGHT

```
Before:  [A] [B] [C] [D]
After:   [A] [B] [C]
                      ▲
                   removed → returns D
```
```python
dq = deque([1, 2, 3, 4])
val = dq.pop()
# val = 4,  dq = deque([1, 2, 3])
```

---

### `popleft()` — Remove from LEFT

```
Before:  [A] [B] [C] [D]
After:        [B] [C] [D]
          ▲
       removed → returns A
```
```python
dq = deque([1, 2, 3, 4])
val = dq.popleft()
# val = 1,  dq = deque([2, 3, 4])
```

---

### `extend(iterable)` — Bulk append to RIGHT

```python
dq = deque([1, 2])
dq.extend([3, 4, 5])
# deque([1, 2, 3, 4, 5])
```

---

### `extendleft(iterable)` — Bulk append to LEFT

> ⚠️ Elements are added one by one to the LEFT — so the iterable gets **reversed**

```python
dq = deque([4, 5])
dq.extendleft([3, 2, 1])
# deque([1, 2, 3, 4, 5])   ← 1 added last to left, ends up first
```

---

### `rotate(n)` — Rotate the deque

Positive `n` → rotate **right** (elements move right, wrap around left)
Negative `n` → rotate **left**

```
dq = deque([1, 2, 3, 4, 5])

rotate(+2):
Before:  [1] [2] [3] [4] [5]
After:   [4] [5] [1] [2] [3]
          ▲───────────────┘
         last 2 wrap to front

rotate(-2):
Before:  [1] [2] [3] [4] [5]
After:   [3] [4] [5] [1] [2]
                      └──────▲
                   first 2 wrap to back
```
```python
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)   # deque([4, 5, 1, 2, 3])
dq.rotate(-2)  # deque([1, 2, 3, 4, 5])  back to original
```

---

### Other Useful Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `len(dq)` | Number of elements | `len(deque([1,2,3])) → 3` |
| `dq[0]` | Peek left (no removal) | `deque([1,2,3])[0] → 1` |
| `dq[-1]` | Peek right (no removal) | `deque([1,2,3])[-1] → 3` |
| `dq.count(x)` | Count occurrences of x | `deque([1,2,2]).count(2) → 2` |
| `dq.clear()` | Remove all elements | `dq = deque()` |
| `dq.reverse()` | Reverse in place | `deque([1,2,3]) → deque([3,2,1])` |
| `x in dq` | Membership check | `2 in deque([1,2,3]) → True` |
| `dq.remove(x)` | Remove first occurrence of x | removes leftmost match |
| `dq.index(x)` | Find index of x | position from left |

---

## Big O Complexity

```
┌─────────────────────────────┬──────────┬──────────────────────────────┐
│ Operation                   │  Big O   │ Notes                        │
├─────────────────────────────┼──────────┼──────────────────────────────┤
│ append(x)                   │  O(1)    │ Right end                    │
│ appendleft(x)               │  O(1)    │ Left end                     │
│ pop()                       │  O(1)    │ Right end                    │
│ popleft()                   │  O(1)    │ Left end ← KEY advantage     │
│ extend(iterable)            │  O(k)    │ k = length of iterable       │
│ extendleft(iterable)        │  O(k)    │ k = length of iterable       │
│ rotate(n)                   │  O(n)    │ n = rotation amount          │
│ len(dq)                     │  O(1)    │                              │
│ dq[0] or dq[-1]            │  O(1)    │ Peek either end              │
│ dq[i] (middle access)       │  O(n)    │ Not optimized for this       │
│ x in dq                     │  O(n)    │ Linear scan                  │
│ remove(x)                   │  O(n)    │ Linear scan                  │
│ reverse()                   │  O(n)    │                              │
│ clear()                     │  O(n)    │                              │
└─────────────────────────────┴──────────┴──────────────────────────────┘
```

### Deque vs List — Why it matters

```
                 list        deque
append right     O(1)    vs  O(1)   → same
pop right        O(1)    vs  O(1)   → same
appendleft      O(n) ❌  vs  O(1) ✅ → deque wins
popleft         O(n) ❌  vs  O(1) ✅ → deque wins
random access    O(1)    vs  O(n)   → list wins
```

> **Rule of thumb**: Use `deque` when you need fast operations on **both ends**.
> Use `list` when you need fast **random index access**.

---

## Tricks & Usage Patterns

---

### 1. BFS (Breadth-First Search)

`popleft()` in O(1) makes deque the perfect BFS queue.

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()   # O(1) — critical!
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

> Using a `list` with `pop(0)` would make BFS O(n²) overall. Deque keeps it O(V+E).

---

### 2. Sliding Window Maximum

Use a **monotonic deque** to track the max in a sliding window in O(n).

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()   # stores indices, front = current max
    result = []

    for i, num in enumerate(nums):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back (they'll never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])  # front is always the max

    return result
```

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [3, 3, 5, 5, 6, 7]
```

---

### 3. Bounded / Fixed-Size Window (maxlen)

```python
dq = deque(maxlen=3)
dq.append(1)   # [1]
dq.append(2)   # [1, 2]
dq.append(3)   # [1, 2, 3]
dq.append(4)   # [2, 3, 4]  ← 1 auto-evicted from left
```

Great for **last N elements**, **moving averages**, or **recent history**.

---

### 4. Palindrome Check

```python
def is_palindrome(s):
    dq = deque(s)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True
```

Pop from both ends simultaneously — elegant and O(n).

---

### 5. Stack + Queue in One

```python
dq = deque()

# Use as Stack (LIFO)
dq.append(x)     # push
dq.pop()         # pop

# Use as Queue (FIFO)
dq.append(x)     # enqueue
dq.popleft()     # dequeue
```

---

### 6. Rotate to Simulate Circular Structures

```python
# Round-robin task scheduler
tasks = deque(['A', 'B', 'C', 'D'])

for _ in range(6):
    task = tasks[0]
    print(f"Processing {task}")
    tasks.rotate(-1)   # move current task to back

# Output: A B C D A B
```

---

### 7. Monotonic Deque (General Pattern)

Used in problems involving **range min/max** queries.

```
Maintain deque so front is always the min (or max):

- New element comes in
- Pop from back while back is >= new element (for min deque)
- Push new element to back
- Front = current minimum of window
```

```python
# Min deque template
dq = deque()
for i, val in enumerate(nums):
    while dq and nums[dq[-1]] >= val:
        dq.pop()
    dq.append(i)
    # dq[0] is always index of minimum in current window
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│              DEQUE CHEAT SHEET              │
├────────────────────┬────────────────────────┤
│  LEFT (front)      │  RIGHT (back)          │
├────────────────────┼────────────────────────┤
│  appendleft(x)     │  append(x)             │
│  popleft()         │  pop()                 │
│  dq[0]  (peek)     │  dq[-1]  (peek)        │
├────────────────────┴────────────────────────┤
│  All 4 end operations → O(1)               │
│  Middle access / search → O(n)             │
│  Use over list when popleft() needed       │
└─────────────────────────────────────────────┘
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Using `list.pop(0)` for queue | Use `deque.popleft()` instead |
| Accessing middle elements often | Reconsider if deque is the right structure |
| Forgetting `extendleft` reverses | Always test with a small example |
| Not checking empty before pop | `if dq:` or `while dq:` before popping |
| Using deque when only one end needed | A list or heapq may be simpler |
