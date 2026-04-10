# ============================================================================
# File: 932_printer_slots_round_robin.py
#
# Practice: Printer Slots Round-Robin (deque circular scan)
#
# PROBLEM:
# You have multiple printers in circular order.
# printer_pages[i] pages can be printed when printer i is selected.
# After use, printer i needs recharge[i] minutes before next use.
#
# Goal:
# Print exactly/at least target pages over time.
#
# Rules:
# - At each decision time, scan in circular order from current deque front.
# - Choose first available printer (ready_at[i] <= cur_time).
# - Printing pages also advances time by same amount (1 page per minute).
# - If no printer available at current time => return -1.
#
# Counting:
# - Count full printer uses only.
# - If final selection is partial to hit target, do not count it.
#
# Return number of full printer uses.
# ============================================================================

from collections import deque
from typing import Callable, List, Tuple

tests: List[Tuple[int, List[int], List[int], int]] = [
    (10, [7, 5], [12, 4], 1),
    (8, [2, 5], [10, 4], -1),
    (9, [3, 3, 3], [100, 100, 100], 3),
    (10, [4, 4, 4], [1, 1, 1], 2),
]


def harness(func: Callable[[int, List[int], List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (target, pages, recharge, expected) in enumerate(tests, 1):
        try:
            got = func(target, pages.copy(), recharge.copy())
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(
                    f"Test {i}: FAILED | expected={expected}, got={got} | "
                    f"target={target}, pages={pages}, recharge={recharge}"
                )
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

from collections import deque

def minFullPrinterUses(target: int, printer_pages: List[int], recharge: List[int]) -> int:

    n = len(printer_pages)
    ready_at = [0] * n      # all are ready at start of time
    
    cyc_itr = deque(range(n))
    clock = 0 
    
    used_printers = 0
    
    while clock < target:
        found = False                                 #each iteration searching for a node. start from not found
        for _ in range(n):                            #problem states seaching more than one full circle is not useful
            i = cyc_itr[0]
            cyc_itr.rotate(-1)
            if ready_at[i] <= clock:                  #node is ready and can be used now  == Count only if it is going to be fully used 
                
                found = True
                rem = target - clock 
                
                if printer_pages[i] <= rem:                     # We can use use this node
                    clock += printer_pages[i]                   # advance the clock
                    used_printers += 1                    # add the used node
                    
                    ready_at[i] = clock + recharge[i]  #determine next ready at
                    
                else:                                  # partial final use: success, but not counted
                    # No rotate needed here because we return immediately.
                    return used_printers
                break

            
        if not found:
            return -1

    return used_printers

harness(minFullPrinterUses)
