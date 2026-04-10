# ============================================================================
# File: 019_contains_duplicate_217_empty.py
#
# LeetCode 217: Contains Duplicate (Easy)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return true if any value appears at least twice 
# in the array, and return false if every element is distinct.
#
# EXAMPLES:
# 1) nums = [1,2,3,1] -> Expected: True
# 2) nums = [1,2,3,4] -> Expected: False
# 3) nums = [1,1,1,3,3,4,3,2,4,2] -> Expected: True
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_boolean)
tests: List[Tuple[List[int], bool]] = [
    ([1, 2, 3, 1], True),                                 # Standard Example 1
    ([1, 2, 3, 4], False),                                # Standard Example 2
    ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),               # Standard Example 3
    ([], False),                                          # Edge Case: Empty list
    ([1], False),                                         # Edge Case: Single element
    ([2, 2], True),                                       # Boundary: Minimum duplicate
    ([2, 3], False),                                      # Boundary: Minimum distinct
    ([5, 5, 5, 5, 5], True),                              # Boundary: All identical elements
    ([1000000, -1000000, 1000000], True),                 # Boundary: Large numbers
    ([-1, -2, -3, -4], False),                            # Boundary: All distinct negatives
    (list(range(10000)) + [9999], True),                  # Stress test: Large list with duplicate at the end
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], bool]) -> None:
    """
    Test harness for LeetCode #217: Contains Duplicate.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def containsDuplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))


# Execute harness without __main__ block
harness(containsDuplicate)