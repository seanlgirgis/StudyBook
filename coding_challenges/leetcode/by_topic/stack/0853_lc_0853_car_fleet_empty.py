"""
id: lc_0853
title: Car Fleet
source: leetcode
difficulty: medium
primary: stack
tags: [stack, greedy, sorting, arrays]
leetcode_url: https://leetcode.com/problems/car-fleet/
status: draft
last_updated: 2026-04-11
notes: 
- key idea: 
- time: 
- space: 
"""

# ============================================================================
# File: 0853_lc_0853_car_fleet_empty.py
#
# LeetCode 853: Car Fleet
# Difficulty: Medium
#
# PROBLEM STATEMENT:
# There are n cars at given miles away from the destination, moving at given 
# speeds. A car can never pass another car ahead of it, but it can catch up 
# to it and drive at the same speed as the slower car, forming a "car fleet".
#
# If a car catches up to another car right at the destination point, it is 
# still considered as one car fleet.
#
# Return the number of car fleets that will arrive at the destination.
#
# EXAMPLES:
# 1) target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
#    Output: 3
#    Explanation: 
#    - Cars at 10 and 8 form a fleet at 12.
#    - Car at 0 arrives at 12.
#    - Cars at 5 and 3 form a fleet at 10.
#
# 2) target = 10, position = [3], speed = [3]
#    Output: 1
#
# 3) target = 100, position = [0,2,4], speed = [4,2,1]
#    Output: 1
# ============================================================================

from typing import Callable, List, Tuple
import copy

# --- TEST CASES ---
# Format: (target, position, speed, expected_output)
tests: List[Tuple[int, List[int], List[int], int]] = [
    (12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], 3),     # Example 1
    (10, [3], [3], 1),                              # Example 2
    (100, [0, 2, 4], [4, 2, 1], 1),                  # Example 3
    (10, [6, 8], [3, 2], 2),                         # Boundary: Catch up exactly at target
    (10, [0, 4, 2], [2, 1, 3], 1),                   # Boundary: All merge into one
    (10, [], [], 0),                                 # Edge Case: No cars
    (10, [5], [2], 1),                               # Edge Case: Single car
    (10, [2, 4], [2, 2], 2),                         # Boundary: Same speed, never catch up
    (100, [10, 20, 30], [10, 10, 10], 3),            # Equal speeds, different start points
    (10, [8, 6], [2, 100], 1),                       # Fast car behind slow car near target
    (16, [11, 4, 13, 6], [3, 2, 2, 5], 4),           # Mixed scenario
    (10, [9, 1], [1, 1], 2),                         # Two cars, constant distance
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (target, position, speed, expected) in enumerate(tests):
        # Deep copy lists to protect test suite
        pos_copy = copy.deepcopy(position)
        spd_copy = copy.deepcopy(speed)
        try:
            result = func(target, pos_copy, spd_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Target: {target} | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Target: {target} | Exception: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def carFleet(target: int, position: List[int], speed: List[int]) -> int:
    n = len(position)
    if n < 2: return n
    cars = [target - x for x in position]
    cars = [(x, s) for x, s in zip(cars, speed)]
    cars.sort()
    cars = [x/s for (x,s) in cars]
    fleets = 1
    fleet_leader = cars[0]
    for i in range(1, n):
        if cars[i] > fleet_leader:
            fleets +=1
            fleet_leader = cars[i]
    return fleets

def carFleetStack(target: int, position: List[int], speed: List[int]) -> int:
    # Monotonic INCREASING stack — each entry is a fleet leader's arrival time.
    # We never pop: a slower car (higher time) always pushes a new entry.
    # A faster car (lower time) is silently skipped — it catches the fleet ahead
    # and never becomes a leader, so it never earns a place on the stack.
    # Stack grows only when a new SLOWER car arrives → len(stack) = fleet count.
    n = len(position)
    if n < 2: return n
    cars = sorted(zip([target - x for x in position], speed))
    times = [x / s for x, s in cars]
    stack = []
    for time in times:
        if not stack or stack[-1] < time:   # slower than current leader → new fleet
            stack.append(time)
        # else: time <= stack[-1] → faster, catches fleet ahead, skip
    return len(stack)


solutions = [carFleet, carFleetStack]

for sol in solutions:
    print()
    harness(sol)