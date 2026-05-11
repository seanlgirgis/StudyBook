# 007. Nested Lists

## Source
HackerRank Python - Basic Data Types

## Problem Summary
Given names and grades for students, print the name(s) of students with the second lowest grade. If there are multiple students, print names in alphabetical order, one per line.

## Final Accepted Solution
```python
if __name__ == '__main__':
    score_to_names = {}

    for _ in range(int(input())):
        name = input()
        score = float(input())

        if score in score_to_names:
            score_to_names[score].append(name)
        else:
            score_to_names[score] = [name]

    sorted_scores = sorted(score_to_names.keys())
    second_lowest_score = sorted_scores[1]

    for name in sorted(score_to_names[second_lowest_score]):
        print(name)
```

## Plain-English Explanation
- Use a dictionary where each score maps to a list of names.
- This groups students who share the same grade.
- Sort the unique scores and take index `1` for the second lowest.
- Sort names under that score so output is alphabetical.

## Sample Inputs and Outputs
- Input:
  - `5`
  - `Harry`
  - `37.21`
  - `Berry`
  - `37.21`
  - `Tina`
  - `37.2`
  - `Akriti`
  - `41`
  - `Harsh`
  - `39`
- Output:
  - `Berry`
  - `Harry`

## Mistakes or Reminders
- The second lowest must be from unique scores, not just second item read.
- Keep score as `float`.
- Sort names before printing to match expected output.

## Review Checklist
- [ ] I can group values with a dictionary of lists.
- [ ] I can get the second smallest unique value safely.
- [ ] I can produce sorted multiline output exactly.
