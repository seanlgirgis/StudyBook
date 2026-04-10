# ============================================================================
# File: 020_product_except_self_238_empty.py
#
# LeetCode 238: Product of Array Except Self (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return an array answer such that answer[i] is 
# equal to the product of all the elements of nums except nums[i].
#
# The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
#
# You must write an algorithm that runs in O(n) time and without using the division operation.
#
# EXAMPLES:
# 1) nums = [1,2,3,4] -> Expected: [24,12,8,6]
# 2) nums = [-1,1,0,-3,3] -> Expected: [0,0,9,0,0]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_array)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3, 4], [24, 12, 8, 6]),                # Standard Example 1
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),          # Standard Example 2 (Single zero)
    ([0, 4, 0], [0, 0, 0]),                        # Boundary: Multiple zeros (all products should be 0)
    ([0, 0, 0, 0], [0, 0, 0, 0]),                  # Boundary: All zeros
    ([1, 2], [2, 1]),                              # Edge Case: Minimum length (2 elements)
    ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),            # Boundary: All ones
    ([-1, -2, -3, -4], [-24, -12, -8, -6]),        # Boundary: All negatives
    ([2, 3, 4, 5, 6], [360, 240, 180, 144, 120]),  # Standard positive integers
    ([1, -1, 1, -1, 1], [1, -1, 1, -1, 1]),        # Alternating ones
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[int]]) -> None:
    """
    Test harness for LeetCode #238: Product of Array Except Self.
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
def productExceptSelf(nums: List[int]) -> List[int]:
    prefix , postfix= 1, 1
    out = [1] * len(nums)
    
    for i in range(len(nums)):
        out[i] = prefix
        prefix *= nums[i]
        
    for j in range(len(nums)-1, -1 , -1):
        out[j] *= postfix
        postfix *= nums[j]
    
    return out


# Execute harness without __main__ block
harness(productExceptSelf)