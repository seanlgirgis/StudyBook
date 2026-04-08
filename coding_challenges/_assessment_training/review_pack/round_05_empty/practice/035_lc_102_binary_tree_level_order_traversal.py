# ============================================================================
# File: 035_lc_102_binary_tree_level_order_traversal.py
#
# LeetCode 102: Binary Tree Level Order Traversal
# ============================================================================

from collections import deque
from typing import Callable, List, Optional, Tuple


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(level: List[Optional[int]]) -> Optional[TreeNode]:
    if not level:
        return None
    if level[0] is None:
        return None
    root = TreeNode(level[0])
    q = deque([root])
    i = 1
    while q and i < len(level):
        node = q.popleft()
        if i < len(level) and level[i] is not None:
            node.left = TreeNode(level[i])
            q.append(node.left)
        i += 1
        if i < len(level) and level[i] is not None:
            node.right = TreeNode(level[i])
            q.append(node.right)
        i += 1
    return root


tests: List[Tuple[List[Optional[int]], List[List[int]]]] = [
    ([3, 9, 20, None, None, 15, 7], [[3], [9, 20], [15, 7]]),
    ([1], [[1]]),
    ([], []),
    ([1, 2, 3, 4, 5], [[1], [2, 3], [4, 5]]),
    ([1, None, 2, None, 3], [[1], [2], [3]]),
]


def harness(func: Callable[[Optional[TreeNode]], List[List[int]]]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (arr, expected) in enumerate(tests, 1):
        try:
            root = build_tree(arr)
            got = func(root)
            if got == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={got} | tree={arr}")
        except Exception as e:
            print(f"Test {i}: ERROR  | {type(e).__name__}: {e} | tree={arr}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    if not root: return []
    q = deque()
    q.append (root)
    out: List[List[int]] = []
    
    while q:
        lvl = len(q)
        row = []
        for _ in range(lvl):
            node = q.popleft()
            row.append(node.val)
            if node.left : q.append(node.left)
            if node.right : q.append(node.right)
        out.append(row)
    return out         
            


harness(levelOrder)
