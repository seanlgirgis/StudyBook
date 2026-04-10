# ============================================================================
# File: longest_consecutive_128_review_drill.py
#
# LeetCode 128: Longest Consecutive Sequence (Medium)
#
# PROBLEM STATEMENT:
# Given an unsorted array of integers nums, return the length of the longest 
# consecutive elements sequence.
# 
# You must write an algorithm that runs in O(n) time.
#
# EXAMPLES:
# - nums = [100, 4, 200, 1, 3, 2] -> Expected: 4
#   Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. 
#   Therefore its length is 4.
#
# - nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1] -> Expected: 9
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
longest_consecutive_tests: List[dict] = [
    {
        # Standard Example 1
        "kwargs": {"nums": [100, 4, 200, 1, 3, 2]},
        "expected": 4
    },
    {
        # Standard Example 2 (With duplicates)
        "kwargs": {"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]},
        "expected": 9
    },
    {
        # Edge case: Empty array
        "kwargs": {"nums": []},
        "expected": 0
    },
    {
        # Edge case: Single element
        "kwargs": {"nums": [99]},
        "expected": 1
    },
    {
        # Boundary: All identical elements
        "kwargs": {"nums": [5, 5, 5, 5, 5]},
        "expected": 1
    },
    {
        # Boundary: Negative numbers and crossing zero
        "kwargs": {"nums": [-5, -4, -3, -6, 1, 2, 0, -1, -2]},
        "expected": 9
    },
    {
        # Boundary: Multiple disconnected sequences of varying lengths
        "kwargs": {"nums": [10, 11, 12, 100, 101, 102, 103, 1000]},
        "expected": 4
    },
    {
        # Boundary: Already sorted
        "kwargs": {"nums": [1, 2, 3, 4, 5]},
        "expected": 5
    },
    {
        # Boundary: Reverse sorted
        "kwargs": {"nums": [5, 4, 3, 2, 1]},
        "expected": 5
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #128: Longest Consecutive Sequence.
    Validates integer output against the expected sequence length.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: int = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif result == expected:
                # Formatting the output to stay readable if arrays are very long
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 40:
                    nums_display = nums_display[:37] + "..."
                print(f"Test {i+1}: PASSED (nums={nums_display})")
                passed += 1
            else:
                nums_display = str(kwargs['nums'])
                if len(nums_display) > 20:
                    nums_display = nums_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (nums={nums_display})")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def longestConsecutive(nums: List[int]) -> int:
    # For O(n), convert nums to a set to remove duplicates and allow O(1) lookup.
    slist = set(nums)
    max_length = 0
    # Detect sequence starts by checking that n - 1 is not in the set.
    # From each start, walk forward to measure sequence length.
    
    def seq_length(n: int) -> int:
        ret = 0
        while n in slist:
            ret += 1
            n += 1
        return ret
        
    for n in slist:
        if n-1 not in slist:
            max_length = max(max_length , seq_length(n))
             
    return max_length


# Execute harness without __main__ block
test_harness(longestConsecutive, longest_consecutive_tests)
