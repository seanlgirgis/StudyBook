# ============================================================================
# File: 031_lc_1882_process_tasks_using_servers_empty.py
#
# LeetCode 1882: Process Tasks Using Servers (Medium)
#
# PROBLEM STATEMENT:
# You are given two 0-indexed integer arrays servers and tasks of lengths n 
# and m respectively. servers[i] is the weight of the ith server, and tasks[j] 
# is the time needed to process the jth task in seconds.
#
# Tasks are assigned to the servers using a task queue. Initially, all servers 
# are free, and the queue is empty.
#
# At second j, the jth task is inserted into the queue (starting with the 0th 
# task being inserted at second 0). As long as there are free servers and the 
# queue is not empty, the task in the front of the queue will be assigned to a 
# free server with the smallest weight, and in case of a tie, it is assigned 
# to a free server with the smallest index.
#
# If there are no free servers and the queue is not empty, we wait until a 
# server becomes free and immediately assign the next task. If multiple servers 
# become free at the same time, then multiple tasks from the queue will be 
# assigned in order of priority.
#
# Return an array ans of length m where ans[j] is the index of the server the 
# jth task will be assigned to.
#
# DESIGN HINT:
# You will likely need TWO Min-Heaps:
# 1. `available_servers`: Stores (weight, index) to prioritize who gets work.
# 2. `busy_servers`: Stores (time_it_becomes_free, weight, index) to track 
#    when a server will join the available heap again.
#
# EXAMPLES:
# 1) servers = [3,2,2], tasks = [1,2,3,2,1,2] -> Expected: [2,2,0,2,1,2]
# 2) servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1] -> Expected: [1,4,1,4,1,3,2]
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (servers, tasks, expected_assignment_list)
tests: List[Tuple[List[int], List[int], List[int]]] = [
    ([3, 3, 2], [1, 2, 3, 2, 1, 2], [2, 2, 0, 2, 1, 2]),           # Standard Example 1
    ([5, 1, 4, 3, 2], [2, 1, 2, 4, 5, 2, 1], [1, 4, 1, 4, 1, 3, 2]), # Standard Example 2
    ([10], [1, 1, 1], [0, 0, 0]),                                  # Edge Case: Single server
    ([10, 20, 30], [1, 1, 1], [0, 0, 0]),                          # Edge Case: Same best server always free at next arrival
    ([3, 3, 3], [1, 1, 1, 1], [0, 0, 0, 0]),                       # Boundary: Tie by weight always resolves to smallest index
    ([1, 2], [10, 10, 10, 10], [0, 1, 0, 1]),                      # Complex: Forces time-jumping (all servers busy)
    ([1], [100000, 1], [0, 0]),                                    # Boundary: Huge task duration, jump forward
    ([10, 10, 10], [5, 5, 5, 5, 5, 5], [0, 1, 2, 0, 1, 2]),        # Symmetrical cycling
    ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [4, 4, 3, 4, 2]),           # Decreasing weights with busy-time effects
    ([2, 2, 2, 2], [4, 3, 2, 1], [0, 1, 2, 3]),                    # Identical servers
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[int], List[int]], List[int]]) -> None:
    """
    Test harness for LeetCode #1882: Process Tasks Using Servers.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (servers, tasks, expected) in enumerate(tests, 1):
        try:
            # Pass copies to prevent accidental mutation by the user's function
            got = func(servers.copy(), tasks.copy())
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                servers_disp = str(servers) if len(servers) <= 6 else f"[{str(servers[:5])[1:-1]}, ...]"
                tasks_disp = str(tasks) if len(tasks) <= 8 else f"[{str(tasks[:7])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | servers={servers_disp}, tasks={tasks_disp}")
        except Exception as e:
            servers_disp = str(servers) if len(servers) <= 6 else f"[{str(servers[:5])[1:-1]}, ...]"
            tasks_disp = str(tasks) if len(tasks) <= 8 else f"[{str(tasks[:7])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | servers={servers_disp}, tasks={tasks_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

import heapq
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def assignTasks(servers: List[int], tasks: List[int]) -> List[int]:
    res = []
    clock = 0
    available = [(w, i) for i, w in enumerate(servers)]                     #min heap of weight and index
    heapq.heapify(available)
    
    busy = []                                 # heapified queue of (time_it_becomes_free, weight, index)

    for i, duration in enumerate(tasks):
        # a task arrives at i (index) time and takes duration time to finish
        # The clock must be at least the current task's arrival time (i)
        #ensures we don't process a task before it arrives,
        clock = max(clock, i )
        #if no available server move the clock to when the first server becomes available)
        if not available:
            clock =   busy[0][0]
            
        # at said time (clock) mocve all busy to available queue as they become available
        while busy and busy[0][0] <= clock:
            _, weight, index = heapq.heappop(busy)
            heapq.heappush(available, (weight, index))
            
        weight, index = heapq.heappop(available)
        res.append(index)                     #index of server which will handle the job
        heapq.heappush(busy, (clock + duration ,weight, index ))
        
    return res
        
            
        
            
    


# Execute harness without __main__ block
harness(assignTasks)
