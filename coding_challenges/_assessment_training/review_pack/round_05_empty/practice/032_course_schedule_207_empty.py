# ============================================================================
# File: course_schedule_207_empty.py
#
# LeetCode 207: Course Schedule (Medium)
#
# PROBLEM STATEMENT:
# There are a total of numCourses courses you have to take, labeled from 0 to 
# numCourses - 1. You are given an array prerequisites where 
# prerequisites[i] = [ai, bi] indicates that you must take course bi first if 
# you want to take course ai.
#
# For example, the pair [0, 1], indicates that to take course 0 you have to 
# first take course 1.
#
# Return true if you can finish all courses. Otherwise, return false.
#
# EXAMPLES:
# 1) numCourses = 2, prerequisites = [[1,0]] -> Expected: True
#    Explanation: There are a total of 2 courses to take. To take course 1 
#    you should have finished course 0. So it is possible.
# 2) numCourses = 2, prerequisites = [[1,0],[0,1]] -> Expected: False
#    Explanation: There are a total of 2 courses to take. To take course 1 you 
#    should have finished course 0, and to take course 0 you should also have 
#    finished course 1. So it is impossible.
# ============================================================================

from typing import Callable, List, Tuple

# --- TEST CASES ---
# Format: (numCourses, prerequisites, expected_boolean)
tests: List[Tuple[int, List[List[int]], bool]] = [
    (2, [[1, 0]], True),                                      # Standard Example 1
    (2, [[1, 0], [0, 1]], False),                             # Standard Example 2 (Direct Cycle)
    (5, [], True),                                            # Edge case: No prerequisites
    (1, [], True),                                            # Edge case: Single course, no prereqs
    (4, [[1, 0], [2, 1], [3, 2]], True),                      # Boundary: Linear dependency chain
    (4, [[1, 0], [0, 1], [3, 2]], False),                     # Boundary: Disconnected graph with cycle in one part
    (4, [[1, 0], [3, 2]], True),                              # Boundary: Disconnected components, no cycles
    (6, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3], [5, 3]], True), # Complex Valid DAG (Multiple paths to same course)
    (6, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3], [5, 4], [3, 5]], False), # Complex Invalid (Cycle deep in graph)
    (3, [[1, 0], [2, 1], [0, 2]], False)                      # Boundary: 3-node cycle
]

# --- TEST HARNESS ---
def harness(func: Callable[[int, List[List[int]]], bool]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (numCourses, prerequisites, expected) in enumerate(tests, 1):
        try:
            # Deep copy prerequisites to prevent accidental mutation by the function
            prereq_copy = [edge[:] for edge in prerequisites]
            got = func(numCourses, prereq_copy)
            
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                prereq_disp = str(prerequisites) if len(prerequisites) <= 5 else f"[{str(prerequisites[:4])[1:-1]}, ...]"
                print(f"Test {i}: FAILED | expected={expected}, got={got} | numCourses={numCourses}, prereqs={prereq_disp}")
        except Exception as e:
            prereq_disp = str(prerequisites) if len(prerequisites) <= 5 else f"[{str(prerequisites[:4])[1:-1]}, ...]"
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | numCourses={numCourses}, prereqs={prereq_disp}")
            
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    pass


# Execute harness without __main__ block
harness(canFinish)
