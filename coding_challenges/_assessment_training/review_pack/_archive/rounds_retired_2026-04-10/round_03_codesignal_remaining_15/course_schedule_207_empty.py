# LeetCode 207: Course Schedule (Empty)
#
# PROBLEM STATEMENT
# There are `numCourses` courses and prerequisite pairs [a, b] meaning you must take b before a.
# Return True if all courses can be finished (no cycle), otherwise False.
#
# EXAMPLES
# 1) numCourses=2, [[1,0]] -> True
# 2) numCourses=2, [[1,0],[0,1]] -> False
#
# WHAT TO IMPLEMENT
# Implement `canFinish(numCourses, prerequisites)` (topological sort or cycle DFS).
from typing import Callable, List, Tuple

tests: List[Tuple[int, List[List[int]], bool]] = [
    (2, [[1,0]], True),
    (2, [[1,0],[0,1]], False),
    (5, [[1,4],[2,4],[3,1],[3,2]], True),
    (1, [], True),
    (3, [[0,1],[0,2],[1,2]], True),
    (3, [[0,1],[1,2],[2,0]], False),
]

def harness(func: Callable[[int, List[List[int]]], bool]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (n, pre, expected) in enumerate(tests, 1):
        try:
            got = func(n, [x[:] for x in pre])
            if got == expected: print(f"Test {i}: PASSED"); passed += 1
            else: print(f"Test {i}: FAILED | expected={expected}, got={got}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    
    if not prerequisites: return True
    
    graphMap = {i:[] for i in range(numCourses)}
    
    for course, preReq in prerequisites:
        graphMap[course].append(preReq)
    
    # 0 = unvisited
    # 1 = done
    # 2 =  on current path .. If you hit 2 again you are on a cycle
    
    visitSet = [0 for _ in  range(numCourses)]
    
    def isCycle(course: int) -> bool:
        #visiting
        visitSet[course] = 2
        
        for pre in graphMap[course]:
            if visitSet[pre] == 2:
                return True
            if visitSet[pre] == 0 and isCycle(pre):
                return True
        visitSet[course] = 1
        return False
        
        
        
        
    for course in range(numCourses):
        if visitSet[course] == 0 and isCycle(course):
            return False
        
    
    return True

harness(canFinish)

