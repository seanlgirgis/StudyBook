# Pattern Drill: Next Smaller Element (Monotonic Increasing Stack)
#
# PROBLEM STATEMENT
# For each index i in `nums`, return the first smaller value to the right of nums[i].
# If no smaller value exists, return -1.
#
# MONOTONIC PATTERN
# Use a monotonic increasing stack of candidate values (or indices).

from typing import Callable, List, Tuple

tests: List[Tuple[List[int], List[int]]] = [
    ([4, 8, 5, 2, 25], [2, 5, 2, -1, -1]),
    ([13, 7, 6, 12], [7, 6, -1, -1]),
    ([1, 2, 3], [-1, -1, -1]),
    ([3, 2, 1], [2, 1, -1]),
    ([2, 2, 1], [1, 1, -1]),
]


def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            got = func(nums[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")


def nextSmallerElement(nums: List[int]) -> List[int]:
    pass


harness(nextSmallerElement)

