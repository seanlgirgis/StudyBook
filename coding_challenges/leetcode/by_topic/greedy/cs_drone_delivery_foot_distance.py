"""
id: cs_drone_delivery_foot_distance
title: Drone Delivery Foot Distance
source: codesignal
difficulty: medium
primary: greedy
tags: [greedy, simulation, sorting]
codesignal_url: https://app.codesignal.com/test/gGya72ovLpQNGSvwq/question/7ZxmZNZ3Sm4Cqkyiu
status: draft
last_updated: 2026-04-11
notes:
- key idea:
- time:
- space:
"""

# ============================================================================
# File: cs_drone_delivery_foot_distance.py
# Problem: Drone Delivery Foot Distance (Medium)
#
# Problem Statement:
# You are designing a delivery system using drones in a linear warehouse
# represented as a number line from position 0 to position target (target > 0).
# Charging stations are placed at positions given by the array stations,
# where stations[i] is the position of the ith charging station.
#
# A drone has a limited battery allowing it to travel a maximum of 10 units
# after being fully charged.
#
# Delivery protocol (repeat until target is reached):
#   1. From your current position, carry the cargo ON FOOT to the nearest
#      charging station ahead. If no stations remain, carry on foot to target.
#   2. Deploy a fully charged drone from that station; it flies as far as
#      possible toward the target (up to 10 units).
#   3. Walk to where the drone landed, retrieve the cargo, repeat from step 1.
#
# Return the total distance over which the cargo is carried ON FOOT.
#
# Constraints:
# - 1 <= target <= 10^9
# - 0 <= stations.length <= 10^5
# - 0 <= stations[i] <= target
# - Time complexity not worse than O(stations.length x target)
#
# Examples:
# Example 1:
# Input: target = 21, stations = [7, 4, 14]
# Output: 4
# Explanation: Walk to station at 4 (foot +4), drone flies to 14,
#              drone flies to 24 >= 21. Total foot = 4.
#
# Example 2:
# Input: target = 27, stations = [15, 7, 3, 10]
# Output: 7
# Explanation: Walk to 3 (foot +3), drone to 13, walk to 15 (foot +2),
#              drone to 25, walk to 27 (foot +2). Total foot = 7.
#
# Example 3:
# Input: target = 10, stations = []
# Output: 10
# Explanation: No stations — carry entire distance on foot.
# ============================================================================

from typing import List, Tuple, Callable

# Test Suite: (Input -> (target, stations), Expected Output)
tests: List[Tuple[Tuple[int, List[int]], int]] = [
    ((21, [7, 4, 14]),       4),   # Example 1: Basic two-hop drone path
    ((27, [15, 7, 3, 10]),   7),   # Example 2: Three foot segments
    ((10, []),              10),   # Example 3: No stations, full foot carry
    ((10, [0]),              0),   # Station at start, drone covers everything
    ((20, [10]),            10),   # One station, drone lands exactly at target
    ((25, [10, 20]),        10),   # Two stations, drone hops land on stations
    ((15, [3, 8]),           5),   # Second station behind drone landing — foot gap
    ((30, [5, 15, 25]),      5),   # Evenly spaced stations, minimal foot
    ((1,  []),               1),   # Minimal target, no stations
    ((11, [1]),              1),   # One station near start, drone covers rest
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"--- Running Tests for: {func.__name__} ---")

    for i, ((target, stations), expected) in enumerate(tests):
        stations_copy = list(stations)

        try:
            actual = func(target, stations_copy)
            if actual == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {actual})"
                failed += 1
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
            failed += 1

        display_input = f"target={target}, stations={stations}"
        if len(display_input) > 50:
            display_input = f"{display_input[:47]}..."
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def solution(target: int, stations: List[int]) -> int:
    pass


harness(solution)
