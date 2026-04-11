"""
id: lc_custom_harmonious_buildings_flexible
title: Harmonious Building Patterns (Flexible)
source: codesignal
difficulty: medium
primary: greedy
tags: [greedy, math, median, geometry]
leetcode_url: https://app.codesignal.com/custom/harmonious-buildings
status: draft
last_updated: 2026-04-11
notes: 
- key idea: With both add/remove allowed, we minimize sum|H[i] - Target[i]|.
- For a fixed slope, the optimal 'base' is the median of (structures[i] - i*slope).
- time: O(N log N) due to sorting for median, or O(N) with quickselect.
- space: O(N) to store normalized values.
"""

# ============================================================================
# File: custom_harmonious_building_patterns_flexible.py
# Problem: Harmonious Building Patterns (Flexible)
# Difficulty: Medium
#
# PROBLEM STATEMENT:
# Given integer heights `structures`, transform them into a sequence where each
# adjacent pair differs by exactly 1 (strictly ascending or strictly descending).
#
# Allowed operation:
#   - Add 1 floor to a building (Cost: 1)
#   - Remove 1 floor from a building (Cost: 1)
#
# Goal:
#   Return the minimum total operations needed to make either valid pattern.
#
# Logic:
#   To minimize Sum|Actual[i] - (Base + i*Slope)|, we find Base that minimizes
#   Sum| (Actual[i] - i*Slope) - Base |. This is minimized when Base is the 
#   MEDIAN of the set {Actual[i] - i*Slope}.
# ============================================================================

from typing import List, Tuple, Callable
import statistics

# (Input Array, Expected Output)
tests: List[Tuple[List[int], int]] = [
    ([1, 4, 3, 2],      4),   # asc h-i=[1,3,1,-1] median=1 cost=4 | desc h+i=[1,5,5,5] median=5 cost=4
    ([1, 1, 1, 1],      4),   # asc h-i=[1,0,-1,-2] median=0 cost=4 | desc same
    ([10, 10, 10, 10],  4),   # asc h-i=[10,9,8,7] median=9 cost=4
    ([5, 7, 9, 4, 11],  8),   # asc h-i=[5,6,7,1,7] median=6 cost=8 (beats add-only 9)
    ([1, 2, 3],         0),   # already valid ascending
    ([3, 2, 1],         0),   # already valid descending
    ([1, 100],         98),   # asc h-i=[1,99] median=99 cost=98
    ([1, 5, 1],         5),   # asc h-i=[1,4,-1] median=1 cost=5
    ([10, 20, 30, 40], 36),   # asc h-i=[10,19,28,37] median=28 cost=36
    ([0, 0, 0, 0, 0],   6),   # asc h-i=[0,-1,-2,-3,-4] median=-2 cost=6
]

def harness(func: Callable) -> None:
    print(f"Testing function: {func.__name__} (ADD/REMOVE ALLOWED)")
    passed = 0
    for i, (structures, expected) in enumerate(tests):
        arg_copy = list(structures)
        try:
            result = func(arg_copy)
            if result == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {result})"
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
        
        print(f"Test {i+1:02d}: {status} | Input: {structures}")
    
    print(f"\nFinal Result: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def minOpsHarmonious(structures: List[int]) -> int:
    """
    To minimize Sum|H[i] - Target[i]| where Target[i] = Base + i*Direction:
    1. Fix Direction (+1 or -1).
    2. Normalize: A[i] = H[i] - i*Direction.
    3. The optimal Base is the Median of A.
    4. Cost = Sum|A[i] - Median|.
    """
    if not structures:
        return 0
    
    def get_min_cost(direction: int) -> int:
        n = len(structures)
        # Normalize heights
        normalized = [structures[i] - (i * direction) for i in range(n)]
        normalized.sort()
        
        # Median minimizes absolute deviation
        median = normalized[n // 2]
        
        return sum(abs(val - median) for val in normalized)

    # Return the better of strictly ascending or strictly descending
    return min(get_min_cost(1), get_min_cost(-1))

harness(minOpsHarmonious)




####################################
#  The way it clicked
#  Given my buildings and a desired shape — what is the minimum number of floors I need to add to make my buildings match that shape?"
#
#####################################

def sean_solution(L: List[int]) -> int:

    def cost_to_fit(heights, basis):
        h_b    = sorted(h - b for h, b in zip(heights, basis))
        median = h_b[len(h_b) // 2]
        return sum(abs(v - median) for v in h_b)  # sum over adjusted, not original


    n             = len(L)
    ascending_basis  = list(range(n))             # [0, 1, 2, ..., n-1]
    descending_basis = list(range(n - 1, -1, -1)) # [n-1, ..., 1, 0]

    return min(cost_to_fit(L, ascending_basis),
               cost_to_fit(L, descending_basis))

harness(sean_solution)


def sean_solution2(L: List[int]) -> int:

    def cost_to_fit(heights, basis):
        #h = sorted(heights)
        h_b    = sorted([h - b for h, b in zip(heights, basis)])
        base = h_b[len(h_b) // 2]
        target      = [base + b for b in basis]
        floors_changed = [abs(t - h)   for t, h in zip(target, heights)]
        return sum(floors_changed)


    n             = len(L)
    ascending_basis  = list(range(n))             # [0, 1, 2, ..., n-1]
    descending_basis = list(range(n - 1, -1, -1)) # [n-1, ..., 1, 0]

    return min(cost_to_fit(L, ascending_basis),
               cost_to_fit(L, descending_basis))

harness(sean_solution2)