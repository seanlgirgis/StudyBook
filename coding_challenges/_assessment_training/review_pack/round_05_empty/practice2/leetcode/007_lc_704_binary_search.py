# ============================================================================
# File: binary_search_704_empty.py
#
# LeetCode 704: Binary Search (Easy)
#
# PROBLEM STATEMENT:
# Given an array of integers nums which is sorted in ascending order, and an 
# integer target, write a function to search target in nums. If target exists, 
# then return its index. Otherwise, return -1.
#
# You must write an algorithm with O(log n) runtime complexity.
#
# EXAMPLES:
# 1) nums = [-1, 0, 3, 5, 9, 12], target = 9 -> Expected: 4
#    Explanation: 9 exists in nums and its index is 4
# 2) nums = [-1, 0, 3, 5, 9, 12], target = 2 -> Expected: -1
#    Explanation: 2 does not exist in nums so return -1
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, target, expected_index)
tests: List[Tuple[List[int], int, int]] = [
    ([-1, 0, 3, 5, 9, 12], 9, 4),              # Standard Example 1
    ([-1, 0, 3, 5, 9, 12], 2, -1),             # Standard Example 2
    ([5], 5, 0),                               # Edge Case: Single element (Target found)
    ([5], -5, -1),                             # Edge Case: Single element (Target missing)
    ([2, 5], 5, 1),                            # Boundary: Two elements, found at end
    ([2, 5], 2, 0),                            # Boundary: Two elements, found at start
    ([1, 3, 5, 6], 0, -1),                     # Boundary: Target smaller than all elements
    ([1, 3, 5, 6], 7, -1),                     # Boundary: Target larger than all elements
    ([1, 3, 5, 6], 4, -1),                     # Boundary: Target falls between elements
    ([-10, -5, 0, 5, 10, 15], 0, 2),           # Boundary: Negative and positive crossover
    ([], 5, -1),                               # Edge Case: Empty array
    ([1, 2, 3, 4, 5, 6, 7], 7, 6),             # Tricky: Right half narrowing
    ([1, 2, 3, 4, 5, 6, 7], 1, 0),             # Tricky: Left half narrowing
    (list(range(1, 10001)), 9999, 9998),       # Stress: Larger array, target at the far right
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], int], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, target, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy(), target)

            if not isinstance(got, int):
                raise AssertionError(f"Output must be int. got={type(got).__name__}")
            if got < -1 or got >= len(nums):
                raise AssertionError(f"Output index out of valid range [-1, {len(nums) - 1}]. got={got}")
            if got != -1 and nums[got] != target:
                raise AssertionError(f"Returned index does not point to target. nums[{got}]={nums[got]}, target={target}")
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | target={target}, nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | target={target}, nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def search(nums: List[int], target: int) -> int:
    if len(nums) == 0:
        return -1

    l, r = 0, len(nums) - 1
    
    while l <= r:
        mid = l + (r - l) // 2
        n_at_mid = nums[mid]
        if target == n_at_mid:
            return mid
        elif target > n_at_mid:
            l = mid + 1
        else:
            r = mid - 1
    return -1

# Execute harness without __main__ block
harness(search)
