# 008. Finding the percentage

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given student names and marks, store marks in a dictionary. Then read a query student name and print that student's average mark formatted to exactly 2 decimal places.

## Final Accepted Solution
```python
if __name__ == '__main__':
    n = int(input())
    student_marks = {}

    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores

    query_name = input()
    marks = student_marks[query_name]

    print(f"{sum(marks) / len(marks):.2f}")
```

## Plain-English Explanation
- Use a dictionary where key is student name and value is list of scores.
- `name, *line = input().split()` separates name from score text.
- `map(float, line)` converts score strings into numbers.
- Get queried student's marks, compute average, then format to 2 decimal places with `:.2f`.

## Sample Inputs and Outputs
- Input:
  - `3`
  - `Krishna 67 68 69`
  - `Arjun 70 98 63`
  - `Malika 52 56 60`
  - `Malika`
- Output: `56.00`

## Mistakes or Reminders
- Convert marks to `float`, not `int`.
- Use exact formatting to two decimal places.
- Query name must match dictionary key exactly.

## Review Checklist
- [ ] I can parse variable-length input using `*line`.
- [ ] I can store list values inside a dictionary.
- [ ] I can compute and format averages with f-strings.
