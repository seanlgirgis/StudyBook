# 009. Lists

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given `N` commands, maintain a list and perform operations such as `insert`, `append`, `remove`, `sort`, `pop`, `reverse`, and `print`. The first input `N` is the number of command lines.

## Final Accepted Solution
```python
if __name__ == '__main__':
    N = int(input())
    result = []

    for _ in range(N):
        command, *nums = input().split()
        nums = list(map(int, nums))

        if command == "append":
            result.append(nums[0])
        elif command == "sort":
            result.sort()
        elif command == "reverse":
            result.reverse()
        elif command == "pop":
            result.pop()
        elif command == "remove":
            result.remove(nums[0])
        elif command == "print":
            print(result)
        elif command == "insert":
            result.insert(nums[0], nums[1])
```

## Plain-English Explanation
- Keep one working list called `result`.
- Read each command line, split command name and numbers.
- Convert numeric parts with `map(int, nums)`.
- Use `if/elif` to dispatch to the matching list method.
- Print only when command is `print`.

## Sample Inputs and Outputs
- Input:
  - `4`
  - `append 1`
  - `append 2`
  - `insert 1 3`
  - `print`
- Output: `[1, 3, 2]`

## Mistakes or Reminders
- `insert` needs two numbers: index and value.
- `remove x` removes by value, not index.
- `pop` removes last item when no index is provided.

## Review Checklist
- [ ] I can parse command plus variable argument counts.
- [ ] I can explain `remove` vs `pop`.
- [ ] I can apply list methods in command-driven problems.
