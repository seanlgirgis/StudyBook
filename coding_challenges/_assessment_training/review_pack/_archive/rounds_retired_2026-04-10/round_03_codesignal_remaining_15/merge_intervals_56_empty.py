# LeetCode 56: Merge Intervals (Empty)
#
# PROBLEM STATEMENT
# Given a list of intervals where intervals[i] = [start, end], merge all overlapping intervals.
# Return a list of non-overlapping intervals that covers the same ranges.
#
# EXAMPLES
# 1) [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]]
# 2) [[1,4],[4,5]] -> [[1,5]]
#
# WHAT TO IMPLEMENT
# Implement `merge(intervals)` (typically sort by start then scan/merge).
from typing import Callable, List, Tuple

tests: List[Tuple[List[List[int]], List[List[int]]]] = [
    ([[1,3],[2,6],[8,10],[15,18]], [[1,6],[8,10],[15,18]]),
    ([[1,4],[4,5]], [[1,5]]),
    ([], []),
    ([[1,4]], [[1,4]]),
    ([[1,4],[2,3]], [[1,4]]),
    ([[1,5],[2,3],[4,8]], [[1,8]]),
    ([[6,8],[1,9],[2,4],[4,7]], [[1,9]]),
]

def harness(func: Callable[[List[List[int]]], List[List[int]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (intervals, expected) in enumerate(tests, 1):
        try:
            got = func([x[:] for x in intervals])
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def merge(intervals: List[List[int]]) -> List[List[int]]:
    if len(intervals) < 2: return intervals[:]
    intervals.sort()
    out = [intervals[0]]
    def merge_one(lst2):
        lst1 = out[-1]
        if lst2[0] <= lst1[1]:
            # merging
            out[-1][1] = max(lst2[1], out[-1][1])
        else:
            out.append(lst2)
    for i in range(1, len(intervals)):
        merge_one(intervals[i])
    return out


harness(merge)

