# LeetCode 84: Largest Rectangle in Histogram (Monotonic Increasing Stack)
#
# PROBLEM STATEMENT
# Given heights of bars in a histogram, return the area of the largest rectangle.
#
# MONOTONIC PATTERN
# Use a monotonic increasing stack of indices to compute maximal width when a bar drops.

from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int]] = [
    ([2, 1, 5, 6, 2, 3], 10),
    ([2, 4], 4),
    ([2, 1, 2], 3),
    ([0], 0),
    ([1, 1, 1, 1], 4),
]


def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (heights, expected) in enumerate(tests, 1):
        try:
            got = func(heights[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def largestRectangleArea(heights: List[int]) -> int:
    max_area = 0
    stack = []
    for i, h in enumerate(heights):
        cached_idx = i
        while stack and stack[-1][0] > h:
            (ph, pi) = stack.pop()
            max_area = max(max_area, ph *(i - pi))
            cached_idx = pi
        stack.append((h, cached_idx))
    while stack:
        (ph, pi) = stack.pop()
        max_area = max(max_area, ph * (len(heights) - pi))
    return max_area


harness(largestRectangleArea)
