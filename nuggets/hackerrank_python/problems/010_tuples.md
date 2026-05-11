# 010. Tuples

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given an integer `n` and a line of `n` space-separated integers, create a tuple from those integers, then compute and print `hash(tuple_values)`.

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input())
    integer_list = map(int, input().split())
    t = tuple(integer_list)
    print(hash(t))
```

## Plain-English Explanation
- Read `n` (count of values).
- Read the integers and convert them with `map(int, ...)`.
- Convert mapped values into a tuple.
- Call `hash()` on the tuple and print it.

## Sample Inputs and Outputs
- Input:
  - `2`
  - `1 2`
- Output: hash value of `(1, 2)` (platform/runtime dependent integer)

## Mistakes or Reminders
- `hash()` here should be applied to a tuple, not a list.
- `map` returns an iterator, so converting to tuple is important.
- The exact hash number can vary by runtime settings.

## Review Checklist
- [ ] I can convert split input into integers with `map`.
- [ ] I can explain why tuple is used instead of list for hashing.
- [ ] I can create tuple directly from an iterator.
