# ============================================================================
# File: longest_consecutive_128_empty.py
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
# 1) nums = [100, 4, 200, 1, 3, 2] -> Expected: 4
#    Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. 
#    Therefore its length is 4.
# 2) nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1] -> Expected: 9
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_length)
tests: List[Tuple[List[int], int]] = [
    ([100, 4, 200, 1, 3, 2], 4),                           # Standard Example 1
    ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),                   # Standard Example 2
    ([], 0),                                               # Edge Case: Empty list
    ([5], 1),                                              # Edge Case: Single element
    ([1, 2, 0, 1], 3),                                     # Duplicate elements within sequence
    ([2, 2, 2, 2, 2], 1),                                  # Boundary: All duplicates
    ([-5, -4, -3, -1, 0, 1, 2], 4),                        # Negative numbers crossing zero (-1, 0, 1, 2)
    ([10, 20, 30, 40, 50], 1),                             # Boundary: No consecutive numbers
    ([1, 2, 3, 4, 5], 5),                                  # Boundary: Already sorted sequence
    ([5, 4, 3, 2, 1], 5),                                  # Boundary: Reverse sorted sequence
    ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6], 7),              # Complex mixed sequence
    (list(range(10000, 0, -1)) + [20000, 20001], 10000),   # Stress test: Large reverse sequence and separate small block
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], int]) -> None:
    """
    Test harness for LeetCode #128: Longest Consecutive Sequence.
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
                nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 12 else f"[{str(nums[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def longestConsecutive(nums: List[int]) -> int:
    snums = set(nums)
    if len(snums) <= 1 : return len(snums)
    max_cons = 0
    def seq_length(n):
        ret = 0
        while n in snums:
            ret += 1
            n += 1
        return ret

    for n in snums:
        if n-1 not in snums:        # starting of a seq
            max_cons = max(max_cons, seq_length(n))
    
    return max_cons

# Execute harness without __main__ block
harness(longestConsecutive)