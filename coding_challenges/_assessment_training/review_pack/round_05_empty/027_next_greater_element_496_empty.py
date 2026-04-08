# ============================================================================
# File: next_greater_element_496_empty.py
#
# LeetCode 496: Next Greater Element I (Easy)
#
# PROBLEM STATEMENT:
# Given two arrays `nums1` and `nums2`, where all values in `nums1` exist in `nums2`,
# return an array such that for each value in `nums1`, you find the first greater
# value to its right in `nums2`; otherwise return -1.
#
# MONOTONIC PATTERN:
# Use a monotonic decreasing stack of values while scanning nums2 left -> right.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums1, nums2, expected)
tests: List[Tuple[List[int], List[int], List[int]]] = [
    ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
    ([2, 4], [1, 2, 3, 4], [3, -1]),
    ([1, 3, 5, 2, 4], [6, 5, 4, 3, 2, 1, 7], [7, 7, 7, 7, 7]),
    ([1], [1], [-1]),
    ([1, 2, 3], [3, 2, 1], [-1, -1, -1]),               # Boundary: Strictly decreasing (no greater elements)
    ([1, 2, 3], [1, 2, 3, 4], [2, 3, 4]),               # Boundary: Strictly increasing
    ([4, 2, 6], [1, 2, 3, 4, 5, 6, 7], [5, 3, 7]),      # Boundary: Spread out targets
    ([10, 9, 8], [8, 9, 10, 11, 12], [11, 10, 9]),      # Mixed target ordering vs source ordering
    ([5], [6, 5, 4, 3, 2, 1], [-1]),                    # Edge Case: Element exists but has no right-side greater
    ([13, 7, 5, 9], [5, 7, 13, 9, 12], [-1, 13, 7, 12]) # Random unsorted array layout
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], List[int]], List[int]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums1, nums2, expected) in enumerate(tests, 1):
        try:
            # Pass copies to prevent accidental mutation by the function
            got = func(nums1[:], nums2[:])
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums1_disp = str(nums1) if len(nums1) <= 10 else f"[{str(nums1[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums1={nums1_disp}")
        except Exception as e:
            nums1_disp = str(nums1) if len(nums1) <= 10 else f"[{str(nums1[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums1={nums1_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def nextGreaterElement(nums1: List[int], nums2: List[int]) -> List[int]:
    # Next greater element is determined by traversal in nums2.
    res = [-1] * len(nums1)
    lookup = {n: i for i, n in enumerate(nums1)}
    stack: List[int] = []  # Monotonic decreasing stack of indices into nums2.

    for i, num in enumerate(nums2):
        while stack and nums2[stack[-1]] < num:
            idx = stack.pop()
            if nums2[idx] in lookup:
                nums1_idx = lookup[nums2[idx]]
                res[nums1_idx] = num
        stack.append(i)

    return res
    

    
    


# Execute harness without __main__ block
harness(nextGreaterElement)
