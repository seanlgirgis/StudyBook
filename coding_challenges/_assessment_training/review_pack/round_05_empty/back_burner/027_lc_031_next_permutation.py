# ============================================================================
# File: 027_lc_031_next_permutation.py
#
# LeetCode 31: Next Permutation (Medium)
#
# PROBLEM STATEMENT:
# Implement next permutation, which rearranges numbers into the lexicographically
# next greater permutation of numbers.
#
# If such arrangement is not possible, it must rearrange it as the lowest
# possible order (i.e., sorted in ascending order).
#
# The replacement must be in place and use only constant extra memory.
#
# EXAMPLES:
# 1) nums = [1,2,3] -> [1,3,2]
# 2) nums = [3,2,1] -> [1,2,3]
# 3) nums = [1,1,5] -> [1,5,1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (input_nums, expected_nums_after_in_place_call)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3], [1, 3, 2]),             # Standard increasing
    ([3, 2, 1], [1, 2, 3]),             # Fully decreasing -> reset to lowest
    ([1, 1, 5], [1, 5, 1]),             # Duplicates
    ([1], [1]),                         # Single element
    ([1, 3, 2], [2, 1, 3]),             # Pivot in middle
    ([2, 3, 1], [3, 1, 2]),             # Pivot at start
    ([1, 5, 1], [5, 1, 1]),             # Duplicate with larger leading swap
    ([2, 2, 0, 4, 3, 1], [2, 2, 1, 0, 3, 4]),  # Longer case
    ([1, 4, 3, 2], [2, 1, 3, 4]),       # Reverse suffix case
    ([1, 2, 2, 3], [1, 2, 3, 2]),       # Repeated near end
]


# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], None]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0

    for i, (arr, expected) in enumerate(tests, 1):
        try:
            nums = arr.copy()
            func(nums)  # in-place mutation expected

            if nums == expected:
                display_nums = str(arr) if len(arr) <= 10 else f"[{str(arr[:9])[1:-1]}, ...]"
                print(f"Test {i}: PASSED (nums={display_nums})")
                passed += 1
            else:
                display_nums = str(arr) if len(arr) <= 10 else f"[{str(arr[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={nums} | nums={display_nums}")
        except Exception as e:
            display_nums = str(arr) if len(arr) <= 10 else f"[{str(arr[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={display_nums}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def nextPermutation(nums: List[int]) -> None:
    pass


# Execute harness without __main__ block
harness(nextPermutation)
