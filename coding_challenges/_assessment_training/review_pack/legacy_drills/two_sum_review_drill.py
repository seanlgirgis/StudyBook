# LeetCode 1: Two Sum (Review Drill)

from typing import Callable, List, Tuple


# --- TEST CASES ---
# Format: (nums_array, target, expected_indices)
two_sum_tests: List[Tuple[List[int], int, List[int]]] = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([3, 3], 6, [0, 1]),
    ([0, 4, 3, 0], 0, [0, 3]),
    ([-1, -2, -3, -4, -5], -8, [2, 4]),
    ([10, 20, 30, 40, 50], 90, [3, 4]),
    ([5, 75, 25], 100, [1, 2]),
    ([-10, 7, 19, 15], 9, [0, 2]),
    ([1, 5, 1, 5], 10, [1, 3]),
    ([2, 1, 9, 4, 4, 56, 90, 3], 8, [3, 4]),
]


# --- TEST HARNESS ---
def test_harness(
    func: Callable[[List[int], int], List[int]],
    test_cases: List[Tuple[List[int], int, List[int]]],
) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    for i, (nums, target, expected) in enumerate(test_cases):
        try:
            result: List[int] = func(nums.copy(), target)
            if sorted(result) == sorted(expected):
                print(f"Test {i + 1}: PASSED")
                passed += 1
            else:
                print(f"Test {i + 1}: FAILED")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
        except Exception as e:
            print(f"Test {i + 1}: ERROR | {type(e).__name__}: {e}")

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")


# --- YOUR IMPLEMENTATION ---
def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Given an array of integers nums and an integer target, return indices of the
    two numbers such that they add up to target.

    You may assume each input has exactly one solution, and you may not use the
    same element twice.
    """
    seen = {}
    for i, num in enumerate(nums):
        if (target - num) in seen:
            return [seen[target - num ], i]
        seen[num] = i
    return []
        



test_harness(twoSum, two_sum_tests)
