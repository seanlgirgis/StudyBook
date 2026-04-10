# ============================================================================
# File: lc_056_merge_intervals.py
#
# LeetCode 56: Merge Intervals (Medium)
#
# PROBLEM STATEMENT:
# Given an array of intervals where intervals[i] = [start_i, end_i], merge all 
# overlapping intervals, and return an array of the non-overlapping intervals 
# that cover all the intervals in the input.
#
# EXAMPLES:
# - intervals = [[1,3],[2,6],[8,10],[15,18]] 
#   -> Expected: [[1,6],[8,10],[15,18]]
#   Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
#
# - intervals = [[1,4],[4,5]] 
#   -> Expected: [[1,5]]
#   Explanation: Intervals [1,4] and [4,5] are considered overlapping.
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
merge_intervals_tests: List[dict] = [
    {
        "kwargs": {"intervals": [[1, 3], [2, 6], [8, 10], [15, 18]]},
        "expected": [[1, 6], [8, 10], [15, 18]]
    },
    {
        "kwargs": {"intervals": [[1, 4], [4, 5]]},
        "expected": [[1, 5]]
    },
    {
        # Edge case: Unsorted input
        "kwargs": {"intervals": [[1, 4], [0, 4]]},
        "expected": [[0, 4]]
    },
    {
        # Edge case: Fully contained interval
        "kwargs": {"intervals": [[1, 4], [2, 3]]},
        "expected": [[1, 4]]
    },
    {
        # Edge case: Single interval
        "kwargs": {"intervals": [[1, 5]]},
        "expected": [[1, 5]]
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #56: Merge Intervals.
    Validates output intervals, accounting for overall sorting.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    def normalize_intervals(intervals: List[List[int]]) -> List[List[int]]:
        """Sorts intervals for safe and consistent comparison."""
        if intervals is None:
            return None
        return sorted(intervals, key=lambda x: (x[0], x[1]))

    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: List[List[int]] = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            # Normalize results for comparison
            norm_result = normalize_intervals(result)
            norm_expected = normalize_intervals(expected)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif norm_result == norm_expected:
                # Formatting the output to stay readable if arrays are very large
                intervals_display = str(kwargs['intervals'])
                if len(intervals_display) > 40:
                    intervals_display = intervals_display[:37] + "..."
                print(f"Test {i+1}: PASSED (intervals={intervals_display})")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected}")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def merge(intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort()
    out: List[List[int]] = [intervals[0]]
    
    def addInterval(int2):
        if out[-1][1] >= int2[0]:       # we are merging
            out[-1][1] = max(out[-1][1] , int2[1])
        else:
            out.append(int2)
        
    
    for i in range(1, len(intervals)):
        addInterval(intervals[i])
        
    return out
        
    
    
        


# Execute harness without __main__ block
test_harness(merge, merge_intervals_tests)
