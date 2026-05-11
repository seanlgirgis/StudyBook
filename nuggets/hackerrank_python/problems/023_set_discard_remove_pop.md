# 023. Set .discard(), .remove() & .pop()

## Source
HackerRank Python - Sets

## Problem Summary
Given a non-empty set of integers and a list of commands, execute each command (`pop`, `remove`, `discard`) on the set. After all commands, print the sum of remaining elements.

## Final Accepted Solution
```python
n = int(input())
s = set(map(int, input().split()))

nCommands = int(input())

for _ in range(nCommands):
    u_input = input().split()

    if u_input[0] == 'pop':
        s.pop()
    elif u_input[0] == 'remove':
        s.remove(int(u_input[1]))
    elif u_input[0] == 'discard':
        s.discard(int(u_input[1]))

print(sum(s))
```

## Plain-English Explanation
- Read initial set values.
- Read each command and apply it to the set.
- `pop()` removes an arbitrary element.
- `remove(x)` removes `x` and raises an error if `x` is not present.
- `discard(x)` removes `x` if present and does nothing otherwise.
- Print `sum(s)` after all operations.

## Sample Inputs and Outputs
- Input:
  - `9`
  - `1 2 3 4 5 6 7 8 9`
  - `10`
  - `pop`
  - `remove 9`
  - `discard 9`
  - `discard 8`
  - `remove 7`
  - `pop`
  - `discard 6`
  - `remove 5`
  - `pop`
  - `discard 5`
- Output: `4`

## Mistakes or Reminders
- `remove` can crash if element doesn’t exist.
- `discard` is safer when element may be missing.
- `pop` on empty set would error, but prompt guarantees valid flow here.

## Review Checklist
- [ ] I can explain `remove` vs `discard` behavior.
- [ ] I can parse and execute command-driven set operations.
- [ ] I can compute final aggregate result with `sum`.
