"""
id: lc_custom_harmonious_buildings
title: Harmonious Building Patterns
source: codesignal
difficulty: medium
primary: greedy
tags: [greedy, math, array, sequence]
leetcode_url: https://app.codesignal.com/custom/harmonious-buildings
status: draft
last_updated: 2026-04-10
notes: 
- key idea: The sequence is a rigid staircase where H[i+1] = H[i] ± 1.
- Because we can ONLY ADD height, the tallest building relative to its position 
  sets the "floor" for the entire staircase.
- time: O(N)
- space: O(1)
"""

# ============================================================================
# File: custom_codesignal_harmonious_building_patterns.py
# Problem: Harmonious Building Patterns (Custom / CodeSignal)
# Difficulty: Medium
#
# PROBLEM STATEMENT:
# Given integer heights `structures`, transform them into a sequence where each
# adjacent pair differs by exactly 1:
#   - strictly ascending by 1, or
#   - strictly descending by 1.
#
# Allowed operation:
#   - In one operation, increase one building by 1.
#   - Decreasing is NOT allowed.
#
# Goal:
#   Return the minimum total operations needed to make either valid pattern.
#
# Example:
#   structures = [1, 4, 3, 2]
#   Desc target: [5, 4, 3, 2] -> cost = 4
#   Asc target : [4, 5, 6, 7] -> cost = 12
#   Answer = 4
# ============================================================================

from typing import List, Tuple, Callable

# (Input Array, Expected Output)
tests: List[Tuple[List[int], int]] = [
    ([1, 4, 3, 2], 4),                       # Desc [5,4,3,2] => 4
    ([5, 7, 9, 4, 11], 9),                   # Asc [7,8,9,10,11] => 2+1+0+6+0
    ([1, 2, 3], 0),                          # Already valid ascending
    ([3, 2, 1], 0),                          # Already valid descending
    ([1, 2, 3, 4, 10], 20),                  # Best is asc [6,7,8,9,10]
    ([10, 4, 3, 2, 1], 20),                  # Best is desc [10,9,8,7,6]
    ([1, 5, 1], 8),                          # Both asc/desc need 8
    ([10, 10, 10], 3),                       # [10,11,12] or [12,11,10]
    ([5, 4, 5, 4], 4),                       # Best is desc [7,6,5,4]
    ([1, 1, 1, 1], 6),                       # [1,2,3,4] or [4,3,2,1]
    ([10, 1, 10, 1], 20),                    # Desc [12,11,10,9] => 2+10+0+8
]

def harness(func: Callable) -> None:
    print(f"Testing function: {func.__name__}")
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

UP, DOWN = 1, -1

def solution(structures: List[int]) -> int:
    """
    Key insight — index-offset normalization:
      A valid staircase satisfies: H[i] = staircase_base + i * direction
      Rearranging:                  staircase_base >= structures[i] - i * direction

      Since we can ONLY ADD height, staircase_base must be at least as tall as
      the most demanding building. So:
          staircase_base = max(structures[i] - i * direction)  for all i

      Total ops = sum of gaps between each target height and its current height.
    """
    if len(structures) < 2:
        return 0

    def min_ops_for_direction(direction: int) -> int:
        # Normalize each building to what H[0] would need to be for this slot.
        # staircase_base = the highest such requirement — satisfies all buildings.
        adjusted = [h - i * direction for i, h in enumerate(structures)]
        staircase_base = max(adjusted)
        return sum(staircase_base - a for a in adjusted)  # always >= 0 by construction

    return min(min_ops_for_direction(UP), min_ops_for_direction(DOWN))

harness(solution)


# ============================================================================
# VERBOSE VERSION — same logic, no direction trick, two explicit methods
# ============================================================================

def cost_of_ascending(structures: List[int]) -> int:
    """
    Target: [B, B+1, B+2, B+3, ...]   where B is the starting base height.

    Each building i needs to reach exactly: base + i
    So the base must be at least:          structures[i] - i   (for every i)
    The most demanding building sets the base — we take the max.

    Example: [1, 4, 3, 2]
      needs_base = [1-0, 4-1, 3-2, 2-3] = [1, 3, 1, -1]
      base = 3  →  targets = [3, 4, 5, 6]
      ops  = (3-1)+(4-4)+(5-3)+(6-2) = 2+0+2+4 = 8
    """
    needs_base = [h - i for i, h in enumerate(structures)]
    base       = max(needs_base)
    targets    = [base + i for i in range(len(structures))]
    return sum(t - h for t, h in zip(targets, structures))


def cost_of_descending(structures: List[int]) -> int:
    """
    Target: [B, B-1, B-2, B-3, ...]   where B is the starting base height.

    Each building i needs to reach exactly: base - i
    So the base must be at least:          structures[i] + i   (for every i)
    The most demanding building sets the base — we take the max.

    Example: [1, 4, 3, 2]
      needs_base = [1+0, 4+1, 3+2, 2+3] = [1, 5, 5, 5]
      base = 5  →  targets = [5, 4, 3, 2]
      ops  = (5-1)+(4-4)+(3-3)+(2-2) = 4+0+0+0 = 4
    """
    needs_base = [h + i for i, h in enumerate(structures)]
    base       = max(needs_base)
    targets    = [base - i for i in range(len(structures))]
    return sum(t - h for t, h in zip(targets, structures))


def solution_verbose(structures: List[int]) -> int:
    if len(structures) < 2:
        return 0
    return min(cost_of_ascending(structures),
               cost_of_descending(structures))


harness(solution_verbose)


####################################
#  The way it clicked
#  Given my buildings and a desired shape — what is the minimum number of floors I need to add to make my buildings match that shape?"
#
#####################################

def sean_solution(L: List[int]) -> int:

    def cost_to_fit(heights, basis):
        # Shift the basis up until every building fits inside the staircase
        base        = max(h - b for h, b in zip(heights, basis))
        target      = [base + b for b in basis]
        floors_added = [t - h   for t, h in zip(target, heights)]
        return sum(floors_added)

    n             = len(L)
    ascending_basis  = list(range(n))             # [0, 1, 2, ..., n-1]
    descending_basis = list(range(n - 1, -1, -1)) # [n-1, ..., 1, 0]

    return min(cost_to_fit(L, ascending_basis),
               cost_to_fit(L, descending_basis))

harness(sean_solution)






