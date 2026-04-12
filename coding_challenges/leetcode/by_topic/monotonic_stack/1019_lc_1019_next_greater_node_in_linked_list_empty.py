"""
id: lc_1019
title: Next Greater Node In Linked List
source: leetcode
difficulty: medium
primary: stack
tags: [linked-list, stack, monotonic-stack, arrays]
leetcode_url: https://leetcode.com/problems/next-greater-node-in-linked-list/
status: draft
last_updated: 2026-04-12
notes: 
- key idea: Convert linked list to array first, then use a monotonic decreasing stack to find the next greater element in O(n).
- time: O(n)
- space: O(n)
"""

# ============================================================================
# File: 1019_lc_1019_next_greater_node_in_linked_list_empty.py
# Problem 1019: Next Greater Node In Linked List (Medium)
# 
# PROBLEM STATEMENT:
# You are given the head of a linked list with n nodes.
# For each node in the list, find the value of the next greater node. That is, 
# for a given node, its next greater node is the node currently on its right, 
# which has a value strictly larger than its value.
#
# Return an integer array answer where answer[i] is the value of the next 
# greater node of the ith node (1-indexed). If the ith node does not have a 
# next greater node, set answer[i] = 0.
#
# EXAMPLES:
# Input: head = [2,1,5]
# Output: [5,5,0]
#
# Input: head = [2,7,4,3,5]
# Output: [7,0,5,5,0]
# ============================================================================

from typing import List, Optional, Tuple, Callable

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_linked_list(arr: List[int]) -> Optional[ListNode]:
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

# Test Cases: List[Tuple[input_list, expected_output]]
tests: List[Tuple[List[int], List[int]]] = [
    ([2, 1, 5], [5, 5, 0]),               # Standard Example 1
    ([2, 7, 4, 3, 5], [7, 0, 5, 5, 0]),   # Standard Example 2
    ([1, 7, 5, 1, 9, 2, 5, 1], [7, 9, 9, 9, 0, 5, 0, 0]), # Complex Sequence
    ([5], [0]),                           # Edge Case: Single element
    ([1, 2, 3, 4, 5], [2, 3, 4, 5, 0]),   # Boundary: Strictly increasing
    ([5, 4, 3, 2, 1], [0, 0, 0, 0, 0]),   # Boundary: Strictly decreasing
    ([2, 2, 2], [0, 0, 0]),               # Edge Case: Identical elements (strictly larger)
    ([3, 1, 2], [0, 2, 0]),               # Dip and recover
    ([1, 5, 2, 5], [5, 0, 5, 0]),         # Multiple occurrences of same max
    ([10, 1, 1, 1, 11], [11, 11, 11, 11, 0]), # Long wait for greater element
    ([7, 6, 5, 10], [10, 10, 10, 0]),     # Catch-up at the end
    ([1, 2, 1, 3], [2, 3, 3, 0]),         # Simple mixed
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0
    
    print(f"\n--- Testing: {func.__name__} ---")
    
    for i, (arr, expected) in enumerate(tests):
        # Build the linked list for the function
        head = build_linked_list(arr)
        
        try:
            result = func(head)
            
            display_input = str(arr) if len(str(arr)) < 50 else f"{str(arr)[:47]}..."
            
            if result == expected:
                print(f"Test {i+1}: PASSED | Input: {display_input}")
                passed += 1
            else:
                print(f"Test {i+1}: FAILED | Input: {display_input}")
                print(f"   Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"Test {i+1}: ERROR  | Input: {display_input}")
            print(f"   Exception: {e}")
            failed += 1
            
    print(f"\nResults: {passed} Passed, {failed} Failed\n")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def nextGreaterNodes(head: Optional[ListNode]) -> List[int]:
    # Step 1: flatten linked list into array — we need indexing for NGE
    nums = []
    node = head
    while node:
        nums.append(node.val)
        node = node.next

    # Step 2: standard NGE with monotonic decreasing stack
    # stack holds indices of unresolved nodes (no NGE found yet)
    # result pre-filled with 0 — unresolved at end stays 0
    result = [0] * len(nums)
    stack = []

    for i, val in enumerate(nums):
        # current val is greater than top → top found its NGE
        while stack and nums[stack[-1]] < val:
            idx = stack.pop()
            result[idx] = val       # record on pop
        stack.append(i)

    return result

harness(nextGreaterNodes)