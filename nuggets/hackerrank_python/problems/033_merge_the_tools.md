# 033. Merge the Tools!

## Source
HackerRank Python - Strings

## Problem Summary
Given a string and an integer `k`, split the string into equal-sized chunks of length `k`. For each chunk, remove repeated characters while preserving first-occurrence order, then print the cleaned chunk on its own line.

## Accepted Solution
```python
def merge_the_tools(string, k):
    for i in range(0, len(string), k):
        seen = set()
        out = ""

        for ch in string[i:i + k]:
            if ch not in seen:
                out += ch
                seen.add(ch)

        print(out)


if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)
```

## Provided Solution Reviewed
The provided solution is correct and should pass.

Provided solution:
```python
def merge_the_tools(string, k):
    for i in range(0, len(string) - k + 1, k):
        seen = set()
        out = ""

        for ch in string[i:i + k]:
            if ch not in seen:
                out += ch
                seen.add(ch)

        print(out)
```

What is good:
- The loop advances by `k`, so each iteration handles one chunk.
- A new `seen` set is created for each chunk.
- The output string `out` is reset for each chunk.
- The code checks each character in original order.
- Repeated characters are skipped after their first occurrence.
- Each cleaned chunk is printed on a separate line.

Small simplification:
Because the problem guarantees the string length is a multiple of `k`,
`range(0, len(string) - k + 1, k)` can be simplified to `range(0, len(string), k)`.
Both versions are correct.

## Plain-English Explanation
The problem asks us to break the string into equal chunks of size `k`.

Example:
- `string = "AABCAAADA"`
- `k = 3`

Chunks:
- `AAB`
- `CAA`
- `ADA`

For each chunk, keep only first occurrences in order.

Chunk 1:
- `A` kept
- second `A` skipped
- `B` kept
- output: `AB`

Chunk 2:
- `C` kept
- `A` kept
- second `A` skipped
- output: `CA`

Chunk 3:
- `A` kept
- `D` kept
- second `A` skipped
- output: `AD`

Important learning notes:
- `range(0, len(string), k)` steps through chunk starts.
- `string[i:i + k]` gets the current chunk.
- A set is useful to test if a character has been seen.
- `seen` must reset per chunk.
- `out` must reset per chunk.
- Do not convert full chunk directly to `set`, because this task needs order preserved.

## Sample Inputs and Outputs
- Input:
  - `AABCAAADA`
  - `3`
- Output:
  - `AB`
  - `CA`
  - `AD`

## Mistakes or Reminders
- Do not use `set(chunk)` directly; order can be lost.
- Do not reuse one `seen` set across chunks.
- Print one result per chunk, not one combined line.
- Use step size `k` in the outer loop.
- Repeated characters are removed only within each chunk.

## Review Checklist
- [ ] I can explain chunking with step size `k`.
- [ ] I can remove duplicates while preserving order.
- [ ] I can explain why `seen` must reset for each chunk.
