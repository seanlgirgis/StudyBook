# LC055 — Jump Game

## Why It Is Priority
- repeat count: 4
- bucket: Greedy
- selected from lc_review_priority backlog

## Problem Snapshot
- goal: determine if you can reach the last index starting from index 0
- input shape: integer array `nums` where `nums[i]` is max jump length
- output: boolean
- constraints: array length up to 10^4

## Core Pattern
- greedy tracking of maximum reachable index
- maintain the furthest index reachable so far
- if the current index overtakes the furthest reachable index, you are stuck

## Recognition Triggers
- "can you reach the end"
- local maximums leading to global limits
- simulating options where O(N^2) DFS/BFS is too expensive

## Correct Approach Outline
1. Initialize `max_reach = 0`
2. Iterate `i` from 0 to `len(nums) - 1`
3. If `i > max_reach`, return False (stuck before reaching `i`)
4. Update `max_reach = max(max_reach, i + nums[i])`
5. If `max_reach >= len(nums) - 1`, return True (early exit optimization)
6. Return `max_reach >= len(nums) - 1` after loop

## Complexity
- time: O(N)
- space: O(1)
- why: single linear pass storing one scalar variable

## Common Failure Modes
- Over-engineering with Dynamic Programming (O(N^2) leads to TLE)
- Implementing recursive BFS/DFS without memoization
- Incorrect loop limits or misunderstanding what `nums[i]` means (it's the *max* step, not the *exact* step)

## Implementation Checklist
- [ ] `max_reach` tracks the absolute furthest index reachable
- [ ] Loop strictly checks `if i > max_reach: return False` FIRST
- [ ] Update `max_reach = max(max_reach, i + nums[i])`
- [ ] Terminate early if `max_reach >= len - 1`

## What To Practice Next
- LC045 Jump Game II
- LC134 Gas Station

## Promotion Status
- status: enriched
- source: PracticeHistory
- notes: classic single-pass greedy reachability check

## Pattern Links
- Primary: Greedy
