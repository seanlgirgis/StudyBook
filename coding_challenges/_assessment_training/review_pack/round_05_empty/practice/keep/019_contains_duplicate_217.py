# ============================================================================
# File: contains_duplicate_217.py
#
# LeetCode 217: Contains Duplicate (Easy)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return true if any value appears at least twice 
# in the array, and return false if every element is distinct.
#
# EXAMPLES:
# 1) nums = [1, 2, 3, 1] -> Expected: True
# 2) nums = [1, 2, 3, 4] -> Expected: False
# 3) nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2] -> Expected: True
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_boolean)
tests: List[Tuple[List[int], bool]] = [
    ([1, 2, 3, 1], True),
    ([1, 2, 3, 4], False),
    ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ([], False),                                # Edge case: Empty array
    ([0], False),                               # Edge case: Single element
    ([1000000000, 1000000000], True),           # Boundary: Large identical numbers
    ([-1, -2, -3, -4, -1], True),               # Boundary: Negative numbers with duplicate
    ([5, 10, 15, 20, 25, 30], False),           # Boundary: Longer strictly distinct array
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], bool]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy of nums to prevent accidental mutation by the function
            result = func(nums.copy())
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={result} | nums={nums_display}")
        except Exception as e:
            nums_display = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_display}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def containsDuplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))



# Execute harness without __main__ block
harness(containsDuplicate)


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def containsDuplicateWithSeen(nums: List[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
        
    return False




# Execute harness without __main__ block
harness(containsDuplicateWithSeen)


