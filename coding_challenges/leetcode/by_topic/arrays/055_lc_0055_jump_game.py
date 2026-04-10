"""
id: lc_0055
title: Jump Game
source: leetcode
difficulty: medium
primary: arrays
tags: [arrays, greedy, dynamic-programming]
leetcode_url: https://leetcode.com/problems/jump-game/
status: complete
last_updated: 2026-04-10
notes:
- key idea: Greedy — either track max_reach forward (strand check) or walk
            the goal post backwards. Both reduce to O(n) / O(1). DP and
            memoised recursion give O(n²) / O(n) by caching per-index results.
- time: O(n) greedy | O(n²) DP / memoised recursive | O(2^n) naive recursive
- space: O(1) greedy | O(n) DP / recursive (cache + call stack)
"""

# ============================================================================
# File: 055_lc_055_jump_game_empty.py
# Problem: LC055 - Jump Game
# Difficulty: Medium
# 
# PROBLEM STATEMENT:
# You are given an integer array nums. You are initially positioned at the 
# array's first index, and each element in the array represents your maximum 
# jump length at that position.
# 
# Return true if you can reach the last index, or false otherwise.
# 
# EXAMPLES:
# Example 1:
# Input: nums = [2,3,1,1,4]
# Output: true
# Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
# 
# Example 2:
# Input: nums = [3,2,1,0,4]
# Output: false
# Explanation: You will always arrive at index 3 no matter what. Its maximum
# jump length is 0, which makes it impossible to reach the last index.
# ============================================================================

from typing import List, Callable, Tuple


# Test cases: (nums, expected_output)
tests: List[Tuple[List[int], bool]] = [
    ([2, 3, 1, 1, 4], True),           # Example 1
    ([3, 2, 1, 0, 4], False),          # Example 2
    ([0], True),                       # Edge: Single element (already at end)
    ([2, 0], True),                    # Edge: Small jump to end
    ([1, 0, 1], False),                # Stuck at middle zero
    ([0, 1], False),                   # Stuck at start zero
    ([2, 0, 0], True),                 # Jump exactly to the end
    ([1, 1, 1, 1], True),              # Consistent small steps
    ([5, 4, 3, 2, 1, 0, 0], False),    # Large jumps failing at a late zero
    ([10, 0, 0, 0, 0, 0], True),       # Large jump over multiple zeros
    ([1, 2, 3], True),                 # Strictly increasing
    ([3, 2, 1], True),                 # Strictly decreasing
]

def harness(func: Callable) -> None:
    passed = 0
    for i, (nums, expected) in enumerate(tests):
        # Create a deep copy to prevent mutation issues
        nums_copy = list(nums)
        try:
            result = func(nums_copy)
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: {str(nums)[:50]}... -> Result: {result}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {str(nums)[:50]}... -> Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {str(nums)[:50]}... -> {type(e).__name__}: {e}")
    
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

# ============================================================================
# SOLUTION COMPLEXITY COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
# Approach                   │ Time      │ Space     │ Notes
# ─────────────────────────────────────────────────────────────────────────────
# 1. Naive Recursive         │ O(2^n)    │ O(n)      │ Re-explores same indices
# 2. Recursive + LRU Cache   │ O(n²)     │ O(n)      │ Each index cached once;
#                            │           │           │   inner loop still O(n)
# 3. Bottom-Up DP            │ O(n²)     │ O(n)      │ Same work as #2 but iter.
# 4. Greedy Forward          │ O(n)      │ O(1)      │ Track max reach, one pass
# 5. Greedy Backward (✓best) │ O(n)      │ O(1)      │ Walk goal post left
# ─────────────────────────────────────────────────────────────────────────────
# ============================================================================


# ----------------------------------------------------------------------------
# 1. NAIVE RECURSIVE (DFS)
#
# Time:  O(2^n) — at each index we branch into up to nums[i] recursive calls,
#                 and the same sub-indices are re-explored repeatedly.
#                 Worst case: every element = n, giving a full branching tree.
# Space: O(n)   — maximum call-stack depth equals the array length (n levels
#                 before hitting the base case or bottoming out).
# ----------------------------------------------------------------------------

def canJump_Recursive(nums: List[int]) -> bool:
    """
    Naive DFS — try every possible jump from each position.

    From index i, attempt every jump length j in [1 .. nums[i]].
    Return True as soon as any path reaches or passes the last index.
    No caching: the same index may be visited exponentially many times.

    Useful as a baseline to understand the problem structure before optimising.
    """
    last = len(nums) - 1

    def dfs(i: int) -> bool:
        # Base case: we're at or past the end — success.
        if i >= last:
            return True
        # Try every jump size from 1 up to the max allowed at position i.
        # We iterate largest-first as a minor heuristic (reach far fast),
        # but worst-case complexity is unchanged.
        for jump in range(nums[i], 0, -1):
            if dfs(i + jump):
                return True
        # No jump from i leads to the end.
        return False

    return dfs(0)


# ----------------------------------------------------------------------------
# 2. RECURSIVE + LRU CACHE (TOP-DOWN DP / MEMOISATION)
#
# Time:  O(n²) — each of the n indices is computed exactly once (lru_cache
#                ensures that). Computing index i may scan up to nums[i]
#                neighbours, and nums[i] ≤ n, so total work is O(n × n).
# Space: O(n)  — the cache stores one boolean per index (n entries), plus
#                O(n) call-stack depth in the worst case.
# ----------------------------------------------------------------------------
from functools import lru_cache
def canJump_Recursive_LRU(nums: List[int]) -> bool:
    """
    Top-down DP (memoised DFS) — same recursion as the naive version,
    but lru_cache stores the result for each index so it is never
    re-computed.

    The inner function dfs(i) closes over `nums`; lru_cache keys only
    on `i`, which is safe because nums is immutable during one call.

    This is the natural evolution from the naive recursive approach:
    identify overlapping sub-problems → cache them.
    """
    last = len(nums) - 1

    @lru_cache(maxsize=None)
    def dfs(i: int) -> bool:
        # Base case: reached or passed the last index.
        if i >= last:
            return True
        # Explore all reachable next indices; cache prevents re-work.
        for jump in range(nums[i], 0, -1):
            if dfs(i + jump):
                return True
        return False

    result = dfs(0)
    dfs.cache_clear()   # avoid stale cache if harness reuses the closure
    return result


# ----------------------------------------------------------------------------
# 3. BOTTOM-UP DYNAMIC PROGRAMMING
#
# Time:  O(n²) — outer loop runs n times; inner loop scans up to nums[i]
#                neighbours per index, which is at most n. Total: O(n × n).
# Space: O(n)  — a boolean dp array of length n.
# ----------------------------------------------------------------------------
def canJump_DP(nums: List[int]) -> bool:
    """
    Iterative bottom-up DP — the memoised recursion turned inside-out.

    dp[i] = True  if the last index is reachable from index i.
    dp[i] = False otherwise.

    Fill from right to left:
      - dp[last] = True  (base case: already at the goal).
      - dp[i]    = True  if any dp[j] is True for j in [i+1 .. i+nums[i]].

    Mechanically equivalent to the LRU version but avoids recursion overhead
    and is easier to reason about iteratively.
    """
    n = len(nums)
    # Start pessimistic: assume no index can reach the end.
    dp = [False] * n
    # Base case: the last index is trivially reachable from itself.
    dp[n - 1] = True

    # Fill backwards; we only need results to the right.
    for i in range(n - 2, -1, -1):
        # Farthest index reachable from i, capped at the last index.
        farthest = min(i + nums[i], n - 1)
        # If any reachable neighbour is marked True, so is i.
        for j in range(i + 1, farthest + 1):
            if dp[j]:
                dp[i] = True
                break   # no need to check further — one True is enough

    # Answer lives at the start: can we reach the end from index 0?
    return dp[0]


# ----------------------------------------------------------------------------
# 4. GREEDY — FORWARD (MAX REACH)
#
# Time:  O(n) — single left-to-right pass, one operation per element.
# Space: O(1) — only one integer (max_reach) is maintained.
# ----------------------------------------------------------------------------
def canJump_Greedy_Forward(nums: List[int]) -> bool:
    """
    Forward greedy — track the farthest index reachable so far.

    Key insight:
        If you can reach index k, you can also reach every index between
        your current position and k (by taking smaller jumps). So the only
        thing that matters is the single number max_reach — the rightmost
        index the jumps seen so far can collectively cover.

    Algorithm:
        Scan left to right. At each index i:
          1. If i > max_reach, we are stranded — no prior jump reaches here.
          2. Otherwise update max_reach = max(max_reach, i + nums[i]).
        If we complete the scan without getting stranded, return True.

    Example: nums = [2, 3, 1, 1, 4]
        i=0: max_reach = max(0, 0+2) = 2
        i=1: max_reach = max(2, 1+3) = 4
        i=2: max_reach = max(4, 2+1) = 4
        i=3: max_reach = max(4, 3+1) = 4  ← already covers the end
        i=4: max_reach = max(4, 4+4) = 8  (past the end) → True

    Example: nums = [3, 2, 1, 0, 4]
        i=0: max_reach = 3
        i=1: max_reach = 3
        i=2: max_reach = 3
        i=3: max_reach = 3
        i=4: 4 > 3  → stranded → False
    """
    max_reach = 0  # farthest index reachable from positions seen so far

    for i, jump in enumerate(nums):
        # If current index is beyond what we can reach, we're stuck.
        if i > max_reach:
            return False
        # Expand the frontier if this position lets us jump farther.
        max_reach = max(max_reach, i + jump)

    # Survived the full scan without getting stranded.
    return True


# ----------------------------------------------------------------------------
# 5. GREEDY — BACKWARD (GOAL POST WALK)  ← optimal / recommended
#
# Time:  O(n) — single right-to-left pass, one comparison per element.
# Space: O(1) — only one integer (goal_post) is maintained.
# ----------------------------------------------------------------------------
def canJump(nums: List[int]) -> bool:
    """
    Greedy — Walk the goal post backwards.

    Strategy:
        Instead of asking "can I reach the end from here?", ask the reverse:
        "can I reach the current goal from an earlier index?"

        Start with goal_post at the last index (the actual target).
        Scan right-to-left: whenever index i can reach or pass goal_post
        (i.e. i + nums[i] >= goal_post), shift goal_post back to i —
        because if we can get to i, we can now get to the end.

        If goal_post walks all the way back to index 0, we've proven
        a valid path exists from start to finish.

    Example: nums = [2, 3, 1, 1, 4]
        goal_post starts at 4
        i=4: 4+4=8 >= 4 → goal_post = 4  (same, already the target)
        i=3: 3+1=4 >= 4 → goal_post = 3
        i=2: 2+1=3 >= 3 → goal_post = 2
        i=1: 1+3=4 >= 2 → goal_post = 1
        i=0: 0+2=2 >= 1 → goal_post = 0  ← reached the start → True

    Example: nums = [3, 2, 1, 0, 4]
        goal_post starts at 4
        i=3: 3+0=3 < 4 → no shift
        i=2: 2+1=3 < 4 → no shift
        i=1: 1+2=3 < 4 → no shift
        i=0: 0+3=3 < 4 → no shift
        goal_post is still 4, not 0 → False

    Time:  O(n) — single right-to-left scan
    Space: O(1) — only goal_post is tracked
    """
    # Start: the target we need to prove is reachable from index 0.
    # Initially that target is the last index itself.
    target = len(nums) - 1

    # Walk backwards from the second-to-last index toward the start.
    # (No need to check the last index as a launch pad — we only care
    #  whether we can land on it, not jump from it.)
    for i in range(len(nums) - 1, -1, -1):
        # If standing at i, can we jump far enough to reach target?
        # i + nums[i] is the farthest index reachable from i.
        max_jump = nums[i]
        if i + max_jump >= target:
            # Yes — so i is now our new interim goal.
            # Proving we can reach i is equivalent to proving we can reach the end.
            target = i

    # If goal_post walked all the way back to index 0, a valid path exists.
    return target == 0


# ============================================================================
# RUN ALL SOLUTIONS THROUGH THE HARNESS
# ============================================================================
solutions: List[Callable] = [
    canJump_Recursive,        # 1. Naive DFS         — O(2^n) time | O(n) space
    canJump_Recursive_LRU,    # 2. Memoised DFS      — O(n²)  time | O(n) space
    canJump_DP,               # 3. Bottom-up DP      — O(n²)  time | O(n) space
    canJump_Greedy_Forward,   # 4. Greedy (forward)  — O(n)   time | O(1) space
    canJump,                  # 5. Greedy (backward) — O(n)   time | O(1) space
]

for sol in solutions:
    print(f"\n{'='*60}")
    harness(sol)