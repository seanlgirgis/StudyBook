# Monotonic Stacks — Basics Sheet

---

## What is a Monotonic Stack?

A **monotonic stack** is a regular stack that is always kept in sorted order (increasing or decreasing) by **popping elements that violate the order** before pushing a new one.

The key insight: the **moment of popping** is where the answer is computed — not at push time.

---

## The Core Template

```python
# Monotonic Increasing Stack (bottom → top: small → large)
stack = []
for x in nums:
    while stack and stack[-1] > x:   # pop anything LARGER
        stack.pop()
    stack.append(x)

# Monotonic Decreasing Stack (bottom → top: large → small)
stack = []
for x in nums:
    while stack and stack[-1] < x:   # pop anything SMALLER
        stack.pop()
    stack.append(x)
```

---

## Increasing Stack — Visual

```
nums = [3, 1, 4, 2, 5]

x=3:  stack=[]       push 3  → [3]
x=1:  3 > 1, pop 3   push 1  → [1]
x=4:  1 < 4, ok      push 4  → [1, 4]
x=2:  4 > 2, pop 4   push 2  → [1, 2]
x=5:  2 < 5, ok      push 5  → [1, 2, 5]

Stack always bottom → top:  small → large  ✓
```

---

## Decreasing Stack — Visual

```
nums = [3, 1, 4, 2, 5]

x=3:  stack=[]       push 3  → [3]
x=1:  3 > 1, ok      push 1  → [3, 1]
x=4:  1 < 4, pop 1
      3 < 4, pop 3   push 4  → [4]
x=2:  4 > 2, ok      push 2  → [4, 2]
x=5:  2 < 5, pop 2
      4 < 5, pop 4   push 5  → [5]

Stack always bottom → top:  large → small  ✓
```

---

## When to Use Which

```
┌──────────────────────────────┬──────────────────────────────────────┐
│  Problem asks for...         │  Use...                              │
├──────────────────────────────┼──────────────────────────────────────┤
│  Next Greater Element        │  Decreasing stack                    │
│  Next Smaller Element        │  Increasing stack                    │
│  Previous Greater Element    │  Decreasing stack (right to left)    │
│  Previous Smaller Element    │  Increasing stack (right to left)    │
│  Largest Rectangle           │  Increasing stack                    │
│  Sliding Window Maximum      │  Decreasing stack (deque)            │
│  Trapping Rainwater          │  Decreasing stack                    │
└──────────────────────────────┴──────────────────────────────────────┘
```

---

## The KEY Mental Model

```
┌─────────────────────────────────────────────────────────────┐
│  DECREASING stack                                           │
│  → Elements sit waiting for something LARGER to arrive      │
│  → Pop trigger = "I found your next greater element"        │
│                                                             │
│  INCREASING stack                                           │
│  → Elements sit waiting for something SMALLER to arrive     │
│  → Pop trigger = "I found your next smaller element"        │
└─────────────────────────────────────────────────────────────┘
```

---

## Pattern 1 — Next Greater Element (Decreasing Stack)

> For each element, find the first element to the RIGHT that is greater.

```python
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []   # stores indices, decreasing by value

    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num      # num is the next greater for idx
        stack.append(i)

    return result
```

```
nums   = [2,  1,  5,  6,  2,  3]
result = [5,  5,  6, -1,  3, -1]

Step by step:
  i=0, num=2 → stack=[0]
  i=1, num=1 → stack=[0,1]
  i=2, num=5 → pop 1 (nums[1]=1 < 5) result[1]=5
              → pop 0 (nums[0]=2 < 5) result[0]=5
              → stack=[2]
  i=3, num=6 → pop 2 (nums[2]=5 < 6) result[2]=6
              → stack=[3]
  i=4, num=2 → stack=[3,4]
  i=5, num=3 → pop 4 (nums[4]=2 < 3) result[4]=3
              → stack=[3,5]
  End: indices 3,5 never popped → result stays -1
```

---

## Pattern 2 — Next Smaller Element (Increasing Stack)

> For each element, find the first element to the RIGHT that is smaller.

```python
def next_smaller(nums):
    n = len(nums)
    result = [-1] * n
    stack = []   # stores indices, increasing by value

    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] > num:
            idx = stack.pop()
            result[idx] = num      # num is the next smaller for idx
        stack.append(i)

    return result
```

```
nums   = [4,  3,  2,  5,  1]
result = [3,  2,  1,  1, -1]
```

---

## Pattern 3 — Previous Greater Element (Decreasing Stack, answer at push time)

> For each element, find the first element to the LEFT that is greater.

```python
def previous_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []   # decreasing stack

    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] <= num:
            stack.pop()
        if stack:
            result[i] = nums[stack[-1]]   # answer computed at PUSH time
        stack.append(i)

    return result
```

```
nums   = [1,  3,  2,  5,  4]
result = [-1, -1,  3, -1,  5]
```

---

## Pattern 4 — Largest Rectangle in Histogram (Increasing Stack)

```python
def largest_rectangle(heights):
    stack = []     # increasing stack of indices
    max_area = 0
    heights = heights + [0]   # sentinel to flush remaining stack

    for i, h in enumerate(heights):
        start = i
        while stack and heights[stack[-1]] > h:
            idx = stack.pop()
            width = i - stack[-1] - 1 if stack else i
            max_area = max(max_area, heights[idx] * width)
        stack.append(i)

    return max_area
```

```
heights = [2, 1, 5, 6, 2, 3]

     █
   █ █
   █ █
   █ █   █
 █ █ █ █ █ █
 █ █ █ █ █ █
 2  1  5  6  2  3

Largest rectangle = 10  (bars of height 5 and 6, width 2)

Why increasing stack?
  We pop a bar when a shorter bar arrives to the right
  At that point we know the full width it could span
```

---

## Pattern 5 — Trapping Rainwater (Decreasing Stack)

```python
def trap(height):
    stack = []   # decreasing stack of indices
    water = 0

    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if stack:
                left = stack[-1]
                width = i - left - 1
                bounded_height = min(height[left], h) - height[bottom]
                water += width * bounded_height
        stack.append(i)

    return water
```

```
height = [0,1,0,2,1,0,1,3,1,0,1,2]
water  = 6

  █               █
  █   █       █   █   █
  █ █ █ █ █ █ █ █ █ █ █ █
  ▓ ░ ▓ ▓ ░ ░ ▓ ▓ ░ ░ ▓ ▓
        trapped water = 6
```

---

## Strict vs Non-Strict Comparison

```python
# Strict — pop on equal → no duplicates allowed in stack
while stack and stack[-1] <= x:
    stack.pop()

# Non-strict — keep duplicates
while stack and stack[-1] < x:
    stack.pop()
```

| Use Case | Strict? |
|----------|---------|
| Next Greater (distinct values) | Either works |
| Rectangle width calculation | Use strict — duplicates cause wrong widths |
| Sliding window max | Use strict |

---

## Complexity

```
┌─────────────────────┬──────────────────────────────────────────────┐
│ Time                │ O(n) — each element pushed once, popped once │
│ Space               │ O(n) — worst case stack holds all elements   │
└─────────────────────┴──────────────────────────────────────────────┘
```

> Even with a `while` loop inside a `for` loop — the total number of pops
> across the entire run is at most n. So it is O(n) overall, not O(n²).

---

## Tricks & Tips

---

### Store Indices, Not Values

Almost always store **indices** in the stack — you can always get the value via `nums[idx]`, but you can't get the index back from a value alone (needed for width calculations).

```python
stack.append(i)          # ✓ store index
val = nums[stack[-1]]    # retrieve value when needed
```

---

### Sentinel Values to Flush the Stack

Append a dummy element to force remaining stack items to be processed:

```python
heights = heights + [0]   # sentinel 0 forces all remaining bars to pop
```

Saves writing a separate cleanup loop after the main loop.

---

### Answer at Pop vs Push

```
Next Greater / Next Smaller → answer computed at POP time
  (the element that causes the pop IS the answer)

Previous Greater / Previous Smaller → answer computed at PUSH time
  (whatever remains on top of stack when you push IS the answer)
```

---

### Circular Arrays

For circular problems (e.g. next greater in circular array), iterate twice:

```python
for i in range(2 * n):
    num = nums[i % n]
    while stack and nums[stack[-1]] < num:
        result[stack.pop()] = num
    if i < n:
        stack.append(i)
```

---

## Recognition Checklist

```
Ask yourself:
  ✓ Do I need next / previous greater or smaller element?
  ✓ Is the brute force O(n²) nested loop?
  ✓ Does the answer for element i depend on nearby elements?
  ✓ Is there a "domination" concept — bigger blocks or replaces smaller?
  ✓ Am I computing spans, widths, or areas involving heights?

If yes to any → think monotonic stack
```

---

## Quick Reference

```
┌──────────────────────────────────────────────────────────────┐
│               MONOTONIC STACK CHEAT SHEET                   │
├─────────────────────┬────────────────────────────────────────┤
│  INCREASING         │  DECREASING                           │
│  bottom→top: ↑      │  bottom→top: ↓                        │
├─────────────────────┼────────────────────────────────────────┤
│  Pop when: top > x  │  Pop when: top < x                    │
│  Finds: next/prev   │  Finds: next/prev                     │
│         SMALLER     │         GREATER                       │
├─────────────────────┴────────────────────────────────────────┤
│  Always store indices, not values                           │
│  Answer computed at POP (next) or PUSH (previous)           │
│  Each element pushed once + popped once = O(n) total        │
└──────────────────────────────────────────────────────────────┘
```
