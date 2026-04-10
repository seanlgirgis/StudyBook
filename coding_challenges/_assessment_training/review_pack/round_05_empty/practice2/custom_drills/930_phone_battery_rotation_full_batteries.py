# ============================================================================
# File: 029_phone_battery_rotation_full_batteries.py
#
# Custom Assessment Practice:
# Minimum Full Batteries Used to Keep Phone On for t Minutes
#
# PROBLEM STATEMENT:
# You have N batteries. Battery i has:
# - capacity[i]: how many minutes it can power the phone when full
# - recharge[i]: how many minutes it needs to recharge after being used
#
# At time 0, all batteries are fully charged.
# You can switch batteries instantly (no switching cost).
# You always pick from the next battery index in circular order.
#
# Goal:
# Keep the phone on for exactly t minutes (or longer), while minimizing/returning
# how many FULL batteries were used.
#
# Important counting rule:
# - If a battery is used for its entire capacity, count it as 1 full battery used.
# - If the final battery is only partially used to reach t, do NOT count that battery.
#
# Return:
# - minimum number of full batteries used
# - or -1 if at some moment no battery is available and phone would turn off
#
# EXAMPLES:
# 1) t = 8, capacity = [2, 5], recharge = [10, 4]
#    Use battery 0 for 2 min (full), then battery 1 for 5 min (full), now t=7.
#    Need only 1 more minute, but battery 0 is still recharging until t=12.
#    No available battery => return -1
#
# 2) t = 10, capacity = [7, 5], recharge = [12, 4]
#    Use battery 0 for 7 min (count 1).
#    Use battery 1 for only 3 min to reach total 10 (partial, not counted).
#    Return 1.
# ============================================================================

from collections import deque
from typing import Callable, Deque, List, Tuple


# --- TEST CASES ---
# Format: (label, t, capacity, recharge, expected)
tests: List[Tuple[str, int, List[int], List[int], int]] = [
    # --- Core examples / baseline ---
    ("baseline: impossible gap after two full uses", 8, [2, 5], [10, 4], -1),
    ("baseline: reach t with final partial battery", 10, [7, 5], [12, 4], 1),
    ("baseline: both batteries still charging", 8, [2, 4], [7, 3], -1),
    ("baseline: exact finish with two full batteries", 6, [3, 3], [1, 1], 2),
    ("baseline: two full then partial to finish", 11, [4, 6], [2, 10], 2),

    # --- Output can be 0 ---
    ("output-0: target met via partial first battery", 1, [5], [3], 0),

    # --- Single-battery behavior ---
    ("single battery exact full use", 5, [5], [3], 1),
    ("single battery cannot wait for recharge", 6, [5], [3], -1),
    ("single battery immediate gap still fails (no idle allowed)", 4, [2], [1], -1),

    # --- Multi-battery exact/partial patterns ---
    ("three batteries exact all-full", 9, [3, 3, 3], [100, 100, 100], 3),
    ("three batteries partial at the end", 10, [4, 4, 4], [1, 1, 1], 2),
    ("three batteries exact with all full", 12, [4, 4, 4], [1, 1, 1], 3),
    ("three batteries after exact then one-minute extra", 13, [4, 4, 4], [1, 1, 1], 3),

    # --- Fast recharge, multiple cycles ---
    ("two batteries many cycles then partial finish", 20, [3, 3], [1, 1], 6),

    # --- Circular-order stress ---
    ("start pointer rotates to large third battery partial", 5, [2, 2, 100], [100, 1, 100], 2),
    ("index-0 unavailable, index-1 exact carry", 12, [2, 10], [100, 1], 2),
    ("index-0 unavailable and index-1 not ready yet", 13, [2, 10], [100, 1], -1),
]


def harness(func: Callable[[int, List[int], List[int]], int]) -> None:
    """Simple harness for battery rotation exercise."""
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (label, t, capacity, recharge, expected) in enumerate(tests, 1):
        try:
            got = func(t, capacity.copy(), recharge.copy())
            if got == expected:
                print(f"Test {i}: PASSED | {label}")
                passed += 1
            else:
                print(
                    f"Test {i}: FAILED | expected={expected}, got={got} | "
                    f"{label} | t={t}, capacity={capacity}, recharge={recharge}"
                )
        except Exception as e:
            print(
                f"Test {i}: ERROR  | {type(e).__name__}: {e} | "
                f"{label} | t={t}, capacity={capacity}, recharge={recharge}"
            )
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def solution(t: int, capacity: List[int], recharge: List[int]) -> int:
    n = len(capacity)
    ready_at = [0] * n                                              # Time where battery is ready to use

    cur_time = 0
    full_used = 0
    start_ptr = 0

    while cur_time < t:
        found = False

        for k in range(n):  # one full circular pass only
            i = (start_ptr + k) % n
            if ready_at[i] <= cur_time:
                found = True
                remaining = t - cur_time

                if capacity[i] <= remaining:
                    # full drain -> count it
                    cur_time += capacity[i]
                    full_used += 1
                    ready_at[i] = cur_time + recharge[i]
                    start_ptr = (i + 1) % n
                else:
                    # partial final use -> not counted
                    return full_used
                break

        if not found:
            return -1

    return full_used

        
            
    



# Execute harness without __main__ block
harness(solution)
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def solution2(t: int, capacity: List[int], recharge: List[int]) -> int:
    n = len(capacity)
    ready_at = [0] * n  # time when battery i becomes usable again
    order: Deque[int] = deque(range(n))  # circular battery order
 
    cur_time = 0
    used_batteries = 0

    while cur_time < t:
        found = False
        # one full circle at current time
        for _ in range(n):
            
            i = order[0]
            order.rotate(-1)
            if ready_at[i] <= cur_time:
                found = True
                remaining = t - cur_time

                if capacity[i] <= remaining:
                    cur_time += capacity[i]
                    used_batteries += 1
                    ready_at[i] = cur_time + recharge[i]
                    # next search starts from the battery after i
                    
                else:
                    return used_batteries
                break


        if not found:
            return -1

    return used_batteries
    
harness(solution2)
