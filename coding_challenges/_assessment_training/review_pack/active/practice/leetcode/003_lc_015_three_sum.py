# ============================================================================
# File: three_sum_015_empty.py
#
# LeetCode 15: 3Sum (Medium)
#
# PROBLEM STATEMENT:
# Given an integer array nums, return all the triplets 
# [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, 
# and nums[i] + nums[j] + nums[k] == 0.
#
# Notice that the solution set must not contain duplicate triplets.
#
# EXAMPLES:
# 1) nums = [-1,0,1,2,-1,-4] -> Expected: [[-1,-1,2],[-1,0,1]]
#    Explanation: 
#    nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
#    nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
#    nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
#    The distinct triplets are [-1,0,1] and [-1,-1,2].
# 2) nums = [0,1,1] -> Expected: []
# 3) nums = [0,0,0] -> Expected: [[0,0,0]]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (nums, expected_triplets)
tests: List[Tuple[List[int], List[List[int]]]] = [
    ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]), # Standard Example 1
    ([0, 1, 1], []),                                    # Standard Example 2
    ([0, 0, 0], [[0, 0, 0]]),                           # Standard Example 3
    ([0, 0, 0, 0], [[0, 0, 0]]),                        # Boundary: Extra zeros
    ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),       # Multiple overlapping triplets
    ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),                   # Duplicate numbers yielding single distinct triplet
    ([], []),                                           # Edge case: Empty array
    ([1, 2], []),                                       # Edge case: Less than 3 elements
    ([-1, -1, -1, 2, 2, 2], [[-1, -1, 2]]),             # Boundary: Many duplicates of just two numbers
    ([1, 2, -2, -1], []),                               # Boundary: No zeros, no sum to zero
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int]], List[List[int]]]) -> None:
    """
    Test harness for LeetCode #15: 3Sum.
    Normalizes the output arrays to gracefully handle unsorted inner triplets 
    and unsorted outer lists since order does not matter for the final result.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    
    def normalize(triplets: List[List[int]]) -> List[Tuple[int, ...]]:
        """Normalizes the list of lists into a sorted list of sorted tuples for safe comparison."""
        if not triplets:
            return []
        return sorted([tuple(sorted(t)) for t in triplets])

    for i, (nums, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(nums.copy())

            # Structural and semantic checks before equality comparison.
            if not isinstance(got, list):
                raise AssertionError(f"Output must be List[List[int]]. got={type(got).__name__}")

            seen = set()
            for t in got:
                if not isinstance(t, list) or len(t) != 3:
                    raise AssertionError(f"Each triplet must be a 3-item list. bad_triplet={t}")
                if not all(isinstance(v, int) for v in t):
                    raise AssertionError(f"Triplet values must be integers. bad_triplet={t}")
                if sum(t) != 0:
                    raise AssertionError(f"Triplet does not sum to zero. bad_triplet={t}")
                key = tuple(sorted(t))
                if key in seen:
                    raise AssertionError(f"Duplicate triplet detected in output. duplicate={list(key)}")
                seen.add(key)
            
            # Normalize both actual and expected outputs for order-agnostic comparison
            norm_expected = normalize(expected)
            norm_got = normalize(got)
            
            if norm_got == norm_expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={norm_expected}, got={norm_got} | nums={nums_disp}")
        except Exception as e:
            nums_disp = str(nums) if len(nums) <= 10 else f"[{str(nums[:9])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | nums={nums_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---
def threeSum(nums: List[int]) -> List[List[int]]:
    out: List[List[int]] = []

    if len(nums) < 3:
        return []

    nums.sort()

    for i, num in enumerate(nums):
        # Once the anchor is > 0, remaining numbers are also >= 0 (sorted),
        # so a zero-sum triplet is no longer possible.
        if num > 0:
            break

        if i > 0 and num == nums[i-1]:
            continue
                
        l, r, target = i+1, len(nums) - 1, -num
        
        while l < r:
            if target == nums[l] + nums[r]:
                out.append([num, nums[l], nums[r]])
                l += 1
                r -= 1
                
                while l < r and nums[l] == nums[l-1]:
                    l += 1
                    
                while l < r and nums[r] == nums[r+1]:
                    r -= 1
                

                    
            elif target < nums[l] + nums[r]:
                r -= 1
            else:
                l += 1
    return out


# Execute harness without __main__ block
harness(threeSum)
