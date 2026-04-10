# ============================================================================
# File: product_except_self_238_empty.py
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
# Format: (nums, expected_product_array)
tests: List[Tuple[List[int], List[int]]] = [
    ([1, 2, 3, 4], [24, 12, 8, 6]),                      # Standard Example 1
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),                # Standard Example 2 (One Zero)
    ([0, 0], [0, 0]),                                    # Boundary: Multiple Zeros
    ([0, 4, 0], [0, 0, 0]),                              # Boundary: Multiple Zeros with non-zero
    ([2, 3], [3, 2]),                                    # Boundary: Minimum size array (n=2)
    ([-1, -2, -3, -4], [-24, -12, -8, -6]),              # Edge case: All negatives
    ([5, 5, 5, 5], [125, 125, 125, 125]),                # Edge case: All identical elements
    ([1, -1, 1, -1, 1], [1, -1, 1, -1, 1]),             # Edge case: Alternating signs
]

def harness(func: Callable[[List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums, expected) in enumerate(tests, 1):
        try:
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
def productExceptSelf(nums: List[int]) -> List[int]:

    prefix, postfix = 1, 1
    out = [1] * len(nums)

    for i in range(len(nums)):
        out[i] = prefix
        prefix *= nums[i]
    

    for j in range(len(nums) -1, -1, -1):
        out[j] *= postfix
        postfix *= nums[j]
 
    return out    


# Execute harness without __main__ block
harness(productExceptSelf)
