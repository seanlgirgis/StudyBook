# 006. Find the Runner-Up Score!

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given `n` participant scores, find the runner-up score. The runner-up is the second highest unique score, so duplicate highest scores do not count.

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))

    runner = -float('inf')
    runner_up = -float('inf')

    for score in arr:
        if score > runner:
            runner_up = runner
            runner = score
        elif score != runner and score > runner_up:
            runner_up = score

    print(runner_up)
```

## Plain-English Explanation
- `runner` tracks the highest score seen so far.
- `runner_up` tracks the second highest unique score.
- If a new score is greater than `runner`, move old `runner` down into `runner_up`.
- Otherwise, update `runner_up` only if the score is different from `runner` and larger than current `runner_up`.

## Sample Inputs and Outputs
- Input:
  - `5`
  - `2 3 6 6 5`
- Output: `5`

- Input:
  - `4`
  - `1 1 1 2`
- Output: `1`

## Mistakes or Reminders
- Runner-up must be unique, not just the second element after sorting.
- Do not let duplicate max values overwrite runner-up logic.
- `-float('inf')` is a safe start value when scores can be negative.

## Review Checklist
- [ ] I can explain why duplicate max scores are skipped.
- [ ] I can track max and second-max in one loop.
- [ ] I can solve this without sorting if needed.
