"""
id: cs_phone_battery_simulation
title: Phone Battery Simulation
source: codesignal
difficulty: medium
primary: simulation
tags: [simulation, arrays]
codesignal_url: https://app.codesignal.com/test/gGya72ovLpQNGSvwq/question/kxzWSgA4dsng2Z66o
status: draft
last_updated: 2026-04-11
notes:
- key idea:
- time:
- space:
"""

# ============================================================================
# File: cs_phone_battery_simulation.py
# Problem: Phone Battery Simulation (Medium)
#
# Problem Statement:
# Your phone is currently out of battery. You need to use it for t minutes.
# You have n batteries. Each battery i has:
#   - capacity[i]  : number of minutes it lets you use the phone when fully charged
#   - recharge[i]  : minutes required to fully recharge it after it depletes
#
# Rules:
#   - You start connected to battery 0
#   - When a battery depletes, it immediately starts recharging
#   - You then try to switch to the next battery cyclically (0->1->2->0->...)
#   - You pick the first available battery in that cyclic scan
#   - A battery is available if its recharge has completed (ready_at <= current_time)
#   - If ALL batteries are still recharging when you need to switch -> return -1
#   - If you successfully power the phone for t minutes -> return the number of
#     batteries that were FULLY drained (used to their full capacity)
#   - A battery used only partially (phone reached t before it depleted) does NOT count
#
# Constraints:
#   - 1 <= t <= 5000
#   - 1 <= capacity.length <= 100
#   - 1 <= capacity[i] < 100
#   - recharge.length == capacity.length
#   - 1 <= recharge[i] < 100
#
# Examples:
# Example 1:
# Input:  t=16, capacity=[2,5,6], recharge=[12,8,4]
# Output: -1
#
# Example 2 (constructed):
# Input:  t=10, capacity=[3,4,5], recharge=[2,3,1]
# Output: 2
# ============================================================================

# ============================================================================
# STEP-BY-STEP WALKTHROUGH — Example 1
# t=16, capacity=[2,5,6], recharge=[12,8,4]
#
# Plain English Setup:
#   Battery 0: runs for 2 mins, then needs 12 mins to recharge
#   Battery 1: runs for 5 mins, then needs  8 mins to recharge
#   Battery 2: runs for 6 mins, then needs  4 mins to recharge
#
# We track ready_at[i] = the time each battery becomes usable again
# Initially ready_at = [0, 0, 0]  (all available from the start)
# We need the phone running until t=16
#
# ── STEP 1 ───────────────────────────────────────────────────────────────────
# current_time = 0  |  use Battery 0  (capacity=2)
#   Phone runs:        t=0  ->  t=2
#   Battery 0 depletes at t=2, starts recharging
#   ready_at[0] = 2 + 12 = 14         (available again at t=14)
#   full_used   = 1
#   current_time = 2
#   Still need: 2 < 16 -> must continue
#   Scan cyclically for next battery:
#     Battery 1: ready_at[1]=0 <= 2  AVAILABLE -> switch
#
# ── STEP 2 ───────────────────────────────────────────────────────────────────
# current_time = 2  |  use Battery 1  (capacity=5)
#   Phone runs:        t=2  ->  t=7
#   Battery 1 depletes at t=7, starts recharging
#   ready_at[1] = 7 + 8 = 15          (available again at t=15)
#   full_used   = 2
#   current_time = 7
#   Still need: 7 < 16 -> must continue
#   Scan cyclically for next battery:
#     Battery 2: ready_at[2]=0 <= 7  AVAILABLE -> switch
#
# ── STEP 3 ───────────────────────────────────────────────────────────────────
# current_time = 7  |  use Battery 2  (capacity=6)
#   Phone runs:        t=7  ->  t=13
#   Battery 2 depletes at t=13, starts recharging
#   ready_at[2] = 13 + 4 = 17         (available again at t=17)
#   full_used   = 3
#   current_time = 13
#   Still need: 13 < 16 -> must continue
#   Scan cyclically for next battery:
#     Battery 0: ready_at[0]=14 > 13  RECHARGING
#     Battery 1: ready_at[1]=15 > 13  RECHARGING
#     Battery 2: ready_at[2]=17 > 13  RECHARGING
#     ALL BATTERIES UNAVAILABLE -> return -1
#
# ANSWER: -1
# ============================================================================

# ============================================================================
# STEP-BY-STEP WALKTHROUGH — Example 2 (constructed)
# t=10, capacity=[3,4,5], recharge=[2,3,1]
#
# Battery 0: runs 3 mins, recharges in 2 mins
# Battery 1: runs 4 mins, recharges in 3 mins
# Battery 2: runs 5 mins, recharges in 1 min
#
# ready_at = [0, 0, 0]
#
# ── STEP 1 ───────────────────────────────────────────────────────────────────
# current_time = 0  |  use Battery 0  (capacity=3)
#   Phone runs:        t=0  ->  t=3
#   ready_at[0] = 3 + 2 = 5
#   full_used   = 1
#   current_time = 3
#   3 < 10 -> continue
#   Battery 1: ready_at[1]=0 <= 3  AVAILABLE -> switch
#
# ── STEP 2 ───────────────────────────────────────────────────────────────────
# current_time = 3  |  use Battery 1  (capacity=4)
#   Phone runs:        t=3  ->  t=7
#   ready_at[1] = 7 + 3 = 10
#   full_used   = 2
#   current_time = 7
#   7 < 10 -> continue
#   Battery 2: ready_at[2]=0 <= 7  AVAILABLE -> switch
#
# ── STEP 3 ───────────────────────────────────────────────────────────────────
# current_time = 7  |  use Battery 2  (capacity=5)
#   Need only: 10 - 7 = 3 more minutes
#   Battery 2 capacity is 5, but we only need 3 -> NOT fully drained
#   Phone runs:        t=7  ->  t=10
#   current_time = 10 = t  -> DONE
#   full_used stays at 2   (battery 2 was not fully depleted)
#
# ANSWER: 2
# ============================================================================

from typing import List, Tuple, Callable

# Test Suite: (Input -> (t, capacity, recharge), Expected Output)
tests: List[Tuple[Tuple[int, List[int], List[int]], int]] = [
    ((16, [2, 5, 6], [12, 8, 4]),  -1),   # Example 1: all recharging at t=13
    ((10, [3, 4, 5], [2, 3, 1]),    2),   # Example 2: third battery not fully drained
    ((3,  [5],       [10]),          0),   # Single battery, t reached before depletion
    ((5,  [5],       [10]),          1),   # Single battery depletes exactly at t
    ((10, [5],       [10]),         -1),   # Single battery, recharge too slow
    ((10, [5, 5],    [3, 3]),        2),   # Two batteries, both fully drained
    ((7,  [5, 5],    [3, 3]),        1),   # Two batteries, second not fully drained
    ((2,  [1, 1],    [5, 5]),        2),   # Two tiny batteries, both drained
    ((3,  [1, 1],    [5, 5]),       -1),   # Both drained, neither recharged in time
    ((20, [3, 3, 3], [1, 1, 1]),     6),   # Three batteries cycling, fast recharge
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"--- Running Tests for: {func.__name__} ---")

    for i, ((t, capacity, recharge), expected) in enumerate(tests):
        capacity_copy = list(capacity)
        recharge_copy = list(recharge)

        try:
            actual = func(t, capacity_copy, recharge_copy)
            if actual == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {actual})"
                failed += 1
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
            failed += 1

        display_input = f"t={t}, cap={capacity}, rch={recharge}"
        if len(display_input) > 50:
            display_input = f"{display_input[:47]}..."
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def solution(t: int, capacity: List[int], recharge: List[int]) -> int:
    pass


harness(solution)
