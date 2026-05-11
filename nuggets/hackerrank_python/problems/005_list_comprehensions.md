# 005. List Comprehensions

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given four integers `x`, `y`, `z`, and `n`, generate all possible 3D coordinates `[i, j, k]` where `0 <= i <= x`, `0 <= j <= y`, and `0 <= k <= z`, but exclude coordinates where `i + j + k == n`. Print the final list in lexicographic order.

## Final Accepted Solution
```python
if __name__ == '__main__':
    x = int(input())
    y = int(input())
    z = int(input())
    n = int(input())

    result = [
        [i, j, k]
        for i in range(x + 1)
        for j in range(y + 1)
        for k in range(z + 1)
        if i + j + k != n
    ]

    print(result)
```

## Plain-English Explanation
- `range(x + 1)` includes `0` through `x`.
- The three `for` clauses build every coordinate combination.
- The `if i + j + k != n` filter removes forbidden coordinates.
- List comprehensions make this compact and readable once you get used to the order.

## Sample Inputs and Outputs
- Input:
  - `1`
  - `1`
  - `1`
  - `2`
- Output: `[[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]]`

## Mistakes or Reminders
- Use `x + 1`, `y + 1`, and `z + 1` so endpoints are included.
- Keep the `if` at the end of the comprehension.
- Output must be one list, not separate prints.

## Review Checklist
- [ ] I can read a nested list comprehension left to right.
- [ ] I can explain where filtering happens in a comprehension.
- [ ] I can convert this to nested loops if needed.
