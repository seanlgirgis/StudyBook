# ============================================================================
# File: 933_circular_workers_with_rest.py
#
# Practice: Circular Workers with Rest Time
#
# PROBLEM:
# Workers are arranged in a ring. Worker i can handle capacity[i] tasks in one run.
# After a run, that worker must rest for rest[i] minutes.
#
# Time model:
# - Handling x tasks takes x minutes.
# - Total required tasks = t.
#
# Rules:
# - At each selection, scan workers in circular order.
# - Pick first ready worker.
# - If no ready worker right now, return -1 (no idle waiting).
#
# Counting:
# - Count only full runs.
# - Partial final run to complete t is not counted.
#
# Return full runs count.
# ============================================================================


from typing import Callable, List, Tuple

tests: List[Tuple[int, List[int], List[int], int]] = [
    (5, [2, 2, 100], [100, 1, 100], 2),
    (12, [2, 10], [100, 1], 2),
    (13, [2, 10], [100, 1], -1),
    (20, [3, 3], [1, 1], 6),
]


def harness(func: Callable[[int, List[int], List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (t, capacity, rest, expected) in enumerate(tests, 1):
        try:
            got = func(t, capacity.copy(), rest.copy())
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(
                    f"Test {i}: FAILED | expected={expected}, got={got} | "
                    f"t={t}, capacity={capacity}, rest={rest}"
                )
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


from collections import deque
def fullcapacityerRuns(t: int, capacity: List[int], rest: List[int]) -> int:

    n = len(capacity)
    ready_at = [0] * n      # all are ready at start of time
    
    cyc_itr = deque(range(n))
    clock = 0 
    
    used_nodes = 0
    
    while clock < t:
        found = False                                 #each iteration searching for a node. start from not found
        for _ in range(n):                            #problem states seaching more than one full circle is not useful
            i = cyc_itr[0]
            cyc_itr.rotate(-1)
            if ready_at[i] <= clock:                  #node is ready and can be used now  == Count only if it is going to be fully used 
                
                found = True
                rem = t - clock 
                
                if capacity[i] <= rem:                     # We can use use this node
                    clock += capacity[i]                   # advance the clock
                    used_nodes += 1                    # add the used node
                    
                    ready_at[i] = clock + rest[i]  #determine next ready at
                    
                else:                                  # partial final use: success, but not counted
                    # No rotate needed here because we return immediately.
                    return used_nodes
                break

            
        if not found:
            return -1
            
            
    return used_nodes
            
            
    

harness(fullcapacityerRuns)

