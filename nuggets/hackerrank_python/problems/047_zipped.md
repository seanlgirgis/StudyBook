# 047. Zipped!

## Source
HackerRank Python - Built-Ins

## Problem summary
Given `N` students and `X` subjects, input is provided as `X` rows (one per subject) with `N` scores each. Regroup scores by student using `zip`, then print each student's average.

## Accepted solution
```python
# N = number of students
# X = number of subjects

N, X = map(int, input().strip().split())

lsts = []

for _ in range(X):
    lsts.append(list(map(float, input().strip().split())))

m = zip(*lsts)

for row in m:
    print(sum(row) / X)
```

## Provided solution reviewed
The provided solution is correct and should pass.

What is good:
- `N` and `X` are read correctly from first line.
- Loop runs `X` times for subject rows.
- Each row is parsed as `float` values.
- `zip(*lsts)` correctly transposes subject rows into student groups.
- `sum(row) / X` computes each student's average.
- Prints one average per student line.

## Plain-English explanation
Input is organized by subject, but output needs student averages.

Example:
- `5 3`
- Subject 1: `89 90 78 93 80`
- Subject 2: `90 91 85 88 86`
- Subject 3: `91 92 83 89 90.5`

`zip(*lsts)` flips rows into student columns:
- Student 1: `89, 90, 91`
- Student 2: `90, 91, 92`
- Student 3: `78, 85, 83`
- Student 4: `93, 88, 89`
- Student 5: `80, 86, 90.5`

Then average each student row.

## Important learning notes
- `zip` groups items by index position.
- `*` unpacks list rows into zip arguments.
- `zip(*lsts)` is a transpose pattern.
- Scores should be `float` because decimal marks can appear.
- `N` may be unused directly but must be read.
- Divide by `X` (subjects), not `N`.

## Sample input/output
- Input:
  - `5 3`
  - `89 90 78 93 80`
  - `90 91 85 88 86`
  - `91 92 83 89 90.5`
- Output:
  - `90.0`
  - `91.0`
  - `82.0`
  - `90.0`
  - `85.5`

## Mistakes/reminders
- Do not average subject rows.
- Use `float` parsing.
- Do not forget `*` in `zip(*lsts)`.
- Divide by `X`, not `N`.
- Print one average per student.
- Do not print zipped tuples directly.
