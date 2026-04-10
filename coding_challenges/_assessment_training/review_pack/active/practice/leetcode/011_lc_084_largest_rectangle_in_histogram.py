# ============================================================================
# File: largest_rectangle_in_histogram_084_empty.py
#
# LeetCode 84: Largest Rectangle in Histogram (Hard)
#
# PROBLEM STATEMENT:
# Given an array of integers heights representing the histogram's bar height 
# where the width of each bar is 1, return the area of the largest rectangle 
# in the histogram.
#
# EXAMPLES:
# 1) heights = [2,1,5,6,2,3] -> Expected: 10
#    Explanation: The largest rectangle is shown in the histogram, which has 
#    a height of 5 and a width of 2 (bars 5 and 6). Area = 5 * 2 = 10.
# 2) heights = [2,4] -> Expected: 4
#    Explanation: The largest rectangle is just the bar of height 4.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (heights, expected_area)
tests: List[Tuple[List[int], int]] = [
    ([2, 1, 5, 6, 2, 3], 10),              # Standard Example 1
    ([2, 4], 4),                           # Standard Example 2
    ([0], 0),                              # Edge Case: Single zero
    ([5], 5),                              # Edge Case: Single element
    ([2, 2, 2, 2, 2], 10),                 # Boundary: All identical heights
    ([1, 2, 3, 4, 5], 9),                  # Boundary: Strictly increasing (3,4,5 -> 3*3=9)
    ([5, 4, 3, 2, 1], 9),                  # Boundary: Strictly decreasing
    ([2, 1, 2], 3),                        # Boundary: V-shape (entire width used)
    ([2, 0, 2], 2),                        # Boundary: Zero splits the histogram
    ([1, 5, 1, 5, 1, 5], 6),               # Boundary: Alternating high/low (base width 6 * 1)
    ([6, 2, 5, 4, 5, 1, 6], 12),           # Complex: Middle block (5,4,5 -> 4*3=12)
    ([2, 1, 5, 6, 2, 3, 2, 2], 12),        # Complex: Trailing numbers extending a base rectangle
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #84: Largest Rectangle in Histogram.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    
    for i, (heights, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(heights.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                heights_disp = str(heights) if len(heights) <= 12 else f"[{str(heights[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | heights={heights_disp}")
        except Exception as e:
            heights_disp = str(heights) if len(heights) <= 12 else f"[{str(heights[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | heights={heights_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def largestRectangleArea(heights: List[int]) -> int:
    stack = []                  # mono increasing ..Keeps (h, idx) .. idx is inherited from last popped.. Pop only for smaller cur height
    max_rect = 0
    if not heights: return 0
    
    
    
    for i, h in enumerate(heights):
        new_ind = i
        while stack and h < stack[-1][0]:
            p_h, p_ind = stack.pop()
            max_rect = max(max_rect, p_h * (i - p_ind))
            new_ind = p_ind
            
        stack.append((h, new_ind))
    while stack:
        p_h, p_ind = stack.pop()
        max_rect = max(max_rect, p_h * (len(heights) - p_ind))
        
    return max_rect
        
    


# Execute harness without __main__ block
harness(largestRectangleArea)