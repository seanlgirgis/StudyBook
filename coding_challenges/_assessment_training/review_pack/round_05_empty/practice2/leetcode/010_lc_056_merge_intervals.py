# ============================================================================
# File: merge_intervals_056_empty.py
#
# LeetCode 56: Merge Intervals (Medium)
#
# PROBLEM STATEMENT:
# Given an array of intervals where intervals[i] = [starti, endi], merge all 
# overlapping intervals, and return an array of the non-overlapping intervals 
# that cover all the intervals in the input.
#
# EXAMPLES:
# 1) intervals = [[1,3],[2,6],[8,10],[15,18]] -> Expected: [[1,6],[8,10],[15,18]]
#    Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
# 2) intervals = [[1,4],[4,5]] -> Expected: [[1,5]]
#    Explanation: Intervals [1,4] and [4,5] are considered overlapping.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (intervals, expected_merged_intervals)
tests: List[Tuple[List[List[int]], List[List[int]]]] = [
    ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]), # Standard Example 1
    ([[1, 4], [4, 5]], [[1, 5]]),                                       # Standard Example 2 (Exact boundary overlap)
    ([[1, 4], [2, 3]], [[1, 4]]),                                       # Boundary: One interval fully contains another
    ([[1, 4], [0, 4]], [[0, 4]]),                                       # Boundary: Same end, different start
    ([[1, 4], [1, 5]], [[1, 5]]),                                       # Boundary: Same start, different end
    ([[1, 10], [2, 6], [8, 10], [15, 18]], [[1, 10], [15, 18]]),        # Complex: Large interval swallowing multiple
    ([[1, 4], [0, 0]], [[0, 0], [1, 4]]),                               # Boundary: Unsorted input with isolated zero-length
    ([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]], [[1, 10]]),             # Boundary: Unsorted input, last interval merges all
    ([[1, 4], [5, 6], [7, 9]], [[1, 4], [5, 6], [7, 9]]),               # No overlaps
    ([[1, 1]], [[1, 1]]),                                               # Edge Case: Single element, zero duration
    ([], []),                                                           # Edge Case: Empty list
    ([[-5, -1], [-4, 2], [3, 5]], [[-5, 2], [3, 5]]),                   # Negative numbers
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[List[int]]], List[List[int]]]) -> None:
    """
    Test harness for LeetCode #56: Merge Intervals.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    
    for i, (intervals, expected) in enumerate(tests, 1):
        try:
            # Pass a deep copy to prevent accidental mutation by the user's function
            intervals_copy = [interval[:] for interval in intervals]
            got = func(intervals_copy)
            
            # Sort both the expected and the result to ensure order doesn't fail a valid merge
            if got is not None:
                got.sort()
            expected_sorted = sorted(expected)
            
            if got == expected_sorted:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                intervals_disp = str(intervals) if len(intervals) <= 5 else f"[{str(intervals[:4])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected_sorted}, got={got} | intervals={intervals_disp}")
        except Exception as e:
            intervals_disp = str(intervals) if len(intervals) <= 5 else f"[{str(intervals[:4])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | intervals={intervals_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort()
    out: List[List[int]] = []
    if len(intervals) == 0 : return []
    
    out.append(intervals[0])
    
    def mergeMe(int2):
        if out[-1][1] >= int2[0]:
            out[-1][1] = max(out[-1][1] , int2[1])
        else:
            out.append(int2)
    
    for i in range(1, len(intervals)):
        mergeMe(intervals[i])
     
     
    return out
            
        
     
        
    
    


# Execute harness without __main__ block
harness(merge)