"""
id: lc_0134
title: Gas Station
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, greedy]
leetcode_url: https://leetcode.com/problems/gas-station/
status: draft
last_updated: 2026-04-12
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0134_lc_134_gas_station.py
# Problem 134: Gas Station (Medium)
# 
# There are n gas stations along a circular route, where the amount of gas at 
# the ith station is gas[i].
#
# You have a car with an unlimited gas tank and it costs cost[i] of gas to 
# travel from the ith station to its next (i + 1)th station. You begin the 
# journey with an empty tank at one of the gas stations.
#
# Given two integer arrays gas and cost, return the starting gas station's 
# index if you can travel around the circuit once in the clockwise direction, 
# otherwise return -1. If there exists a solution, it is guaranteed to be unique.
#
# EXAMPLES:
# Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
# Output: 3
# Explanation: Start at station 3 (index 3) and fill up with 4 unit of gas. 
# Your tank = 0 + 4 = 4. Cost to next station = 1. Remaining gas = 4 - 1 = 3.
# ... (Total circuit possible)
#
# Input: gas = [2,3,4], cost = [3,4,3]
# Output: -1
# ============================================================================

from typing import List, Callable, Tuple

# Test cases: (gas, cost, expected_output)
tests: List[Tuple[List[int], List[int], int]] = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),        # Standard Case: Example 1
    ([2, 3, 4], [3, 4, 3], -1),                  # Standard Case: Example 2 (Impossible)
    ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1], 4),        # Shifted: Success at last index
    ([3, 1, 1], [1, 2, 2], 0),                   # Edge Case: Success at first index
    ([2], [2], 0),                               # Edge Case: Single element (exact match)
    ([1], [2], -1),                              # Edge Case: Single element (impossible)
    ([5, 8, 2, 8], [6, 5, 6, 6], 3),             # Complex: Multiple local dips
    ([0, 0, 0, 2], [0, 0, 1, 0], 3),             # Boundary: Lots of zeros
    ([1, 2], [2, 1], 1),                         # Small: Two elements flip
    ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 0),       # Boundary: Net change zero at every step
    ([4, 5, 2, 6, 5, 3], [3, 2, 7, 3, 2, 9], -1), # Large: Total gas < Total cost
    ([1, 1, 1, 1, 10], [2, 2, 2, 2, 1], 4)       # Greedy: One massive surplus at the end
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (gas, cost, expected) in enumerate(tests):
        # Pass deep copies to protect test data integrity
        g_copy = gas[:]
        c_copy = cost[:]
        
        try:
            result = func(g_copy, c_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: gas={gas[:5]}... cost={cost[:5]}... | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")

    print(f"\nResult: {passed}/{len(tests)} cases passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    """
    Finds the starting gas station index to complete a circular circuit.
    """
    net_gain = [x-y for x,y in zip(gas,cost)]
    if sum(net_gain) < 0 :   # a whoel circle can never happen
        return -1
        
    current_balance= 0
    start_index= 0
    
    for i, amount in enumerate(net_gain):
        current_balance += amount
        #if current_balance < 0 reset
        if current_balance < 0:
            current_balance = 0
            start_index = i + 1
            
    return start_index

harness(canCompleteCircuit)