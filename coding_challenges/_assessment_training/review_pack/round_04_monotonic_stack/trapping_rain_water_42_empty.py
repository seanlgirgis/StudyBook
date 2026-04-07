# LeetCode 42: Trapping Rain Water (Monotonic Decreasing Stack Variant)
#
# PROBLEM STATEMENT
# Given non-negative heights where width of each bar is 1, compute how much water
# can be trapped after raining.
#
# MONOTONIC PATTERN
# A monotonic decreasing stack of indices can identify bounded valleys and fill area.

from typing import Callable, List, Tuple

tests: List[Tuple[List[int], int]] = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([1, 0, 1], 1),
    ([3, 3, 3], 0),
    ([], 0),
]


def harness(func: Callable[[List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (height, expected) in enumerate(tests, 1):
        try:
            got = func(height[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def trap(height: List[int]) -> int:
    pass


harness(trap)

