# ============================================================================
# File: 029_lc_621_task_scheduler_empty.py
#
# LeetCode 621: Task Scheduler (Medium)
#
# PROBLEM STATEMENT:
# Given a characters array tasks, representing the tasks a CPU needs to do, 
# where each letter represents a different task. Tasks could be done in any order. 
# Each task is done in one unit of time. For each unit of time, the CPU could 
# complete either one task or just be idle.
# 
# However, there is a non-negative integer n that represents the cooldown period 
# between two same tasks (the same letter in the array), that is that there must 
# be at least n units of time between any two same tasks.
# 
# Return the least number of units of times that the CPU will take to finish all 
# the given tasks.
#
# EXAMPLES:
# 1) tasks = ["A","A","A","B","B","B"], n = 2 -> Expected: 8
#    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
# 2) tasks = ["A","C","A","B","D","B"], n = 1 -> Expected: 6
#    Explanation: A -> B -> C -> D -> A -> B
# 3) tasks = ["A","A","A","B","B","B"], n = 3 -> Expected: 10
#    Explanation: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (tasks, n, expected_intervals)
tests: List[Tuple[List[str], int, int]] = [
    (["A", "A", "A", "B", "B", "B"], 2, 8),                      # Standard Example 1
    (["A", "C", "A", "B", "D", "B"], 1, 6),                      # Standard Example 2
    (["A", "A", "A", "B", "B", "B"], 3, 10),                     # Standard Example 3
    (["A", "B", "C"], 0, 3),                                     # Edge Case: Zero cooldown
    (["A"], 9, 1),                                               # Edge Case: Single task, high cooldown
    (["A", "A", "A"], 1, 5),                                     # Single task repeated
    (["A", "A", "A", "B", "B", "B", "C", "C", "C"], 2, 9),       # Perfect fit, no idle time needed
    (["A", "B", "C", "D", "E", "A", "B", "C", "D", "E"], 4, 10), # Long sequence, naturally spaces out
    (
        ["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 
        2, 16
    ),                                                           # High frequency task dictates length
    (
        ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E", "F", "F", "G", "G", "H", "H", "I", "I", "J", "J", "K", "K", "L", "L", "M", "M", "N", "N", "O", "O", "P", "P", "Q", "Q", "R", "R", "S", "S", "T", "T", "U", "U", "V", "V", "W", "W", "X", "X", "Y", "Y", "Z", "Z"],
        2, 52
    )                                                            # Stress Test: Full alphabet pairs
]

# --- TEST HARNESS ---
def harness(func: Callable[[List[str], int], int]) -> None:
    """
    Test harness for LeetCode #621: Task Scheduler.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (tasks, n, expected) in enumerate(tests, 1):
        try:
            # Pass a copy to prevent accidental mutation by the user's function
            got = func(tasks.copy(), n)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                tasks_disp = str(tasks) if len(tasks) <= 12 else f"[{str(tasks[:11])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | n={n}, tasks={tasks_disp}")
        except Exception as e:
            tasks_disp = str(tasks) if len(tasks) <= 12 else f"[{str(tasks[:11])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | n={n}, tasks={tasks_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")

from collections import Counter
from collections import deque
import heapq
class MaxHeap:
    def __init__(self):
        self._data = []
    
    def push(self, freq ):
        heapq.heappush(self._data, -freq)
 
    def pop(self):
        return -heapq.heappop(self._data)
       
    def __bool__(self):
        return bool(self._data )
    
# --- USER TO IMPLEMENT SOLUTION BELOW ---
def leastInterval(tasks: List[str], n: int) -> int:
    counts = Counter(tasks)

    mh = MaxHeap()
    for freq in counts.values():
        mh.push(freq)
    
    cooler = deque()                 # stores cooling tasks and their next available time ( ready_time, left_cng
    
    clock = 0   

    while mh or cooler:
        clock += 1                               # burning a task takes a minute
        if mh:
            cnt = mh.pop()
            cnt -= 1
            if cnt:
                cooler.append((clock + n , cnt))
        if cooler and cooler[0][0] == clock:
            mh.push(cooler.popleft()[1])
    return clock
            
            
        


# Execute harness without __main__ block
harness(leastInterval)