# ============================================================================
# File: 931_token_ring_cooldown.py
#
# Practice: Token Ring with Node Cooldown (deque circular simulation)
#
# PROBLEM:
# You have n nodes in a ring. At time 0, all nodes are available.
# A token must be passed for exactly t total time units.
#
# For each use of node i:
# - It contributes work[i] time units.
# - Then it becomes unavailable for cooldown[i] time units.
#
# Rules:
# - Scan nodes in circular order using deque front.
# - If front node is not available at current time, rotate left and keep scanning.
# - At one decision moment, scanning more than n nodes is useless.
# - If no node is available at current time, return -1.
#
# Counting:
# - Count a node only when it is used for full work[i].
# - If final step needs only partial work to reach t, do NOT count that node.
#
# Return number of full node uses.
# ============================================================================

from typing import Callable, Deque, List, Tuple

tests: List[Tuple[int, List[int], List[int], int]] = [
    (8, [2, 5], [10, 4], -1),
    (10, [7, 5], [12, 4], 1),
    (6, [3, 3], [1, 1], 2),
    (1, [5], [3], 0),
# EDGE CASE 1: Exact match (Should count the last node)
    (10, [5, 5], [0, 0], 2), 
    
    # EDGE CASE 2: t is 0 (Should return 0 immediately)
    (0, [5, 5], [0, 0], 0),
    
    # EDGE CASE 3: Large cooldown vs small t
    (5, [2, 2], [100, 100], -1), # Node 0 used (clock=2), Node 1 used (clock=4), Node 0 checked (busy), Node 1 checked (busy) -> -1
    
    # EDGE CASE 4: The "Skip" logic
    # Node 0: work 1, cool 10. Node 1: work 10, cool 1. 
    # Target 5. 
    # Step 1: Use Node 0. Clock=1. Node 0 ready at 11.
    # Step 2: Check Node 1. Work (10) > Rem (4). Return used_nodes (1).
    (5, [1, 10], [10, 1], 1),

    # EDGE CASE 5: Demonstrates why rotate-after-full must stay.
    # If rotate-after-full is removed, node 0 can be reused immediately (cooldown 0),
    # which violates next-node ring order and gives a wrong count.
    (6, [2, 100, 2], [0, 0, 0], 1),

    # EDGE CASE 6: Partial on first chosen node returns immediately with 0.
    # No rotate is needed in the partial branch because function exits.
    (3, [10, 1, 1], [0, 0, 0], 0),
]


def harness(func: Callable[[int, List[int], List[int]], int]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (t, work, cooldown, expected) in enumerate(tests, 1):
        try:
            got = func(t, work.copy(), cooldown.copy())
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(
                    f"Test {i}: FAILED | expected={expected}, got={got} | "
                    f"t={t}, work={work}, cooldown={cooldown}"
                )
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

from collections import deque
def tokenRing(t: int, work: List[int], cooldown: List[int]) -> int:
    """
    TODO:
    Implement using deque rotation.
    Hint state:
    - ready_at[i]
    - order deque of indices
    - cur_time, full_used
    """
    n = len(work)
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
                
                if work[i] <= rem:                     # We can use use this node
                    clock += work[i]                   # advance the clock
                    used_nodes += 1                    # add the used node
                    
                    ready_at[i] = clock + cooldown[i]  #determine next ready at
                    
                else:                                  # partial final use: success, but not counted
                    # No rotate needed here because we return immediately.
                    return used_nodes
                break

            
        if not found:
            return -1
            
            
    return used_nodes
            
            
    

harness(tokenRing)
