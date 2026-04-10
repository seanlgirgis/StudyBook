# ============================================================================
# File: 027_lc_496_next_greater_element_i_empty.py
#
# LeetCode 496: Next Greater Element I (Easy)
#
# PROBLEM STATEMENT:
# The next greater element of some element x in an array is the first greater 
# element that is to the right of x in the same array.
#
# You are given two distinct 0-indexed integer arrays nums1 and nums2, where 
# nums1 is a subset of nums2.
#
# For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] 
# and determine the next greater element of nums2[j] in nums2. If there is no 
# next greater element, then the answer for this query is -1.
#
# Return an array ans of length nums1.length such that ans[i] is the next 
# greater element as described above.
#
# EXAMPLES:
# 1) nums1 = [4,1,2], nums2 = [1,3,4,2] -> Expected: [-1,3,-1]
#    Explanation: 
#    - 4 is underlined in [1,3,4,2]. There is no next greater element, so answer is -1.
#    - 1 is underlined in [1,3,4,2]. The next greater element is 3.
#    - 2 is underlined in [1,3,4,2]. There is no next greater element, so answer is -1.
# 2) nums1 = [2,4], nums2 = [1,2,3,4] -> Expected: [3,-1]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums1, nums2, expected_list)
tests: List[Tuple[List[int], List[int], List[int]]] = [
    ([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),                    # Standard Example 1
    ([2, 4], [1, 2, 3, 4], [3, -1]),                           # Standard Example 2
    ([1, 2, 3], [1, 2, 3], [2, 3, -1]),                        # Boundary: nums1 equals nums2, increasing
    ([3, 2, 1], [3, 2, 1], [-1, -1, -1]),                      # Boundary: nums1 equals nums2, decreasing
    ([1, 3], [3, 1, 2], [2, -1]),                              # Mixed ordering between subset and full set
    ([4], [4], [-1]),                                          # Edge Case: Single element
    ([1, 5, 8], [5, 4, 3, 2, 1, 8, 9, 7], [8, 8, 9]),          # Scattered subset with peaks later in the array
    ([13, 7, 6, 12], [13, 7, 6, 12], [-1, 12, 12, -1]),        # Valleys
    ([-1, -2], [-2, -1, 0], [0, -1]),                          # Negative numbers
    ([10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [-1]),             # Subset element at the very end of nums2
    ([1, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 10]),        # Small subset spanning entire nums2 range
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], List[int]], List[int]]) -> None:
    """
    Test harness for LeetCode #496: Next Greater Element I.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (nums1, nums2, expected) in enumerate(tests, 1):
        try:
            # Pass copies to prevent accidental mutation by the user's function
            got = func(nums1.copy(), nums2.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                n1_disp = str(nums1) if len(nums1) <= 6 else f"[{str(nums1[:5])[1:-1]}, ...]"
                n2_disp = str(nums2) if len(nums2) <= 8 else f"[{str(nums2[:7])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums1={n1_disp}, nums2={n2_disp}")
        except Exception as e:
            n1_disp = str(nums1) if len(nums1) <= 6 else f"[{str(nums1[:5])[1:-1]}, ...]"
            n2_disp = str(nums2) if len(nums2) <= 8 else f"[{str(nums2[:7])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums1={n1_disp}, nums2={n2_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def nextGreaterElement(nums1: List[int], nums2: List[int]) -> List[int]:
    lookup = { n: i for i, n in enumerate(nums1)}
    out = [-1] * len(nums1)
    stack = []

    for i, num in enumerate(nums2):
        while stack and num > nums2[stack[-1]] :
            idx = stack.pop()
            the_num = nums2[idx]
            if the_num in lookup:
                out[lookup[the_num]] = num    
        stack.append(i) 
    return out



# Execute harness without __main__ block
harness(nextGreaterElement)