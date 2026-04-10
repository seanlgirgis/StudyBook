# ============================================================================
# File: 040_doubly_linked_list_foundation_exercise.py
#
# Foundation Exercise: Doubly Linked List (Node holds key + val)
#
# GOAL:
# Build and reason about a reusable doubly linked list that is ideal for LRU-like
# problems. This file includes:
# - Node(key, val)
# - DoublyLinkedList with sentinel head/tail
# - A rich harness to validate behavior and pointer integrity
#
# Sean style mental model:
# - head <-> ... real nodes ... <-> tail
# - head.next = front (most-recent side in LRU-style designs)
# - tail.prev = back  (least-recent side in LRU-style designs)
# ============================================================================

from typing import Any, List, Optional, Tuple


class Node:
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None

    def as_pair(self) -> Tuple[int, int]:
        return (self.key, self.val)


class DoublyLinkedList:
    def __init__(self):
        # Dummy sentinels remove edge-case headaches.
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        return self.size == 0

    def add_to_front(self, node: Node) -> None:
        # head <-> first  => head <-> node <-> first
        first = self.head.next
        node.prev = self.head
        node.next = first
        self.head.next = node
        first.prev = node
        self.size += 1

    def add_to_back(self, node: Node) -> None:
        # last <-> tail  => last <-> node <-> tail
        last = self.tail.prev
        node.next = self.tail
        node.prev = last
        last.next = node
        self.tail.prev = node
        self.size += 1

    def remove(self, node: Node) -> None:
        # Remove only real nodes.
        if node is self.head or node is self.tail:
            return
        p, n = node.prev, node.next
        p.next = n
        n.prev = p
        node.prev = None
        node.next = None
        self.size -= 1

    def pop_back(self) -> Optional[Node]:
        # Return least-recent-side node (node before tail).
        if self.is_empty():
            return None
        node = self.tail.prev
        self.remove(node)
        return node

    def move_to_front(self, node: Node) -> None:
        self.remove(node)
        self.add_to_front(node)

    def find_by_key(self, key: int) -> Optional[Node]:
        cur = self.head.next
        while cur is not self.tail:
            if cur.key == key:
                return cur
            cur = cur.next
        return None

    def remove_by_key(self, key: int) -> bool:
        node = self.find_by_key(key)
        if not node:
            return False
        self.remove(node)
        return True

    def move_to_front_by_key(self, key: int) -> bool:
        node = self.find_by_key(key)
        if not node:
            return False
        self.move_to_front(node)
        return True

    def pairs_forward(self) -> List[Tuple[int, int]]:
        out: List[Tuple[int, int]] = []
        cur = self.head.next
        while cur is not self.tail:
            out.append(cur.as_pair())
            cur = cur.next
        return out

    def pairs_backward(self) -> List[Tuple[int, int]]:
        out: List[Tuple[int, int]] = []
        cur = self.tail.prev
        while cur is not self.head:
            out.append(cur.as_pair())
            cur = cur.prev
        return out

    def validate_integrity(self) -> bool:
        # Verify forward links and count.
        fcount = 0
        cur = self.head
        while cur.next is not None and cur is not self.tail:
            nxt = cur.next
            if nxt.prev is not cur:
                return False
            cur = nxt
            if cur is not self.tail:
                fcount += 1

        if cur is not self.tail:
            return False

        # Verify backward links and count.
        bcount = 0
        cur = self.tail
        while cur.prev is not None and cur is not self.head:
            prv = cur.prev
            if prv.next is not cur:
                return False
            cur = prv
            if cur is not self.head:
                bcount += 1

        if cur is not self.head:
            return False

        return fcount == bcount == self.size


# --- TEST HARNESS ---
# Format:
# (commands, args, expected_returns, expected_final_forward, expected_final_backward, expected_size)
tests = [
    (
        ["DLL", "push_front", "push_front", "forward", "backward"],
        [[], [1, 10], [2, 20], [], []],
        [None, None, None, [(2, 20), (1, 10)], [(1, 10), (2, 20)]],
        [(2, 20), (1, 10)],
        [(1, 10), (2, 20)],
        2,
    ),
    (
        ["DLL", "push_back", "push_back", "move_front_key", "forward", "size"],
        [[], [1, 10], [2, 20], [2], [], []],
        [None, None, None, True, [(2, 20), (1, 10)], 2],
        [(2, 20), (1, 10)],
        [(1, 10), (2, 20)],
        2,
    ),
    (
        ["DLL", "push_back", "push_back", "remove_key", "forward", "size"],
        [[], [1, 10], [2, 20], [1], [], []],
        [None, None, None, True, [(2, 20)], 1],
        [(2, 20)],
        [(2, 20)],
        1,
    ),
    (
        ["DLL", "push_back", "push_back", "pop_back", "forward", "size"],
        [[], [1, 10], [2, 20], [], [], []],
        [None, None, None, (2, 20), [(1, 10)], 1],
        [(1, 10)],
        [(1, 10)],
        1,
    ),
    (
        ["DLL", "push_back", "find", "find", "remove_key", "remove_key", "size"],
        [[], [7, 70], [7], [99], [99], [7], []],
        [None, None, 70, None, False, True, 0],
        [],
        [],
        0,
    ),
]


def test_harness() -> None:
    print("--- Running Tests for: DoublyLinkedList ---")
    passed = 0

    for i, (commands, args, expected_returns, final_fwd, final_bwd, final_size) in enumerate(tests, 1):
        dll = None
        results: List[Any] = []
        ok = True
        err = ""

        try:
            for cmd, arg in zip(commands, args):
                if cmd == "DLL":
                    dll = DoublyLinkedList()
                    results.append(None)
                elif cmd == "push_front":
                    dll.add_to_front(Node(arg[0], arg[1]))
                    results.append(None)
                elif cmd == "push_back":
                    dll.add_to_back(Node(arg[0], arg[1]))
                    results.append(None)
                elif cmd == "remove_key":
                    results.append(dll.remove_by_key(arg[0]))
                elif cmd == "move_front_key":
                    results.append(dll.move_to_front_by_key(arg[0]))
                elif cmd == "pop_back":
                    node = dll.pop_back()
                    results.append(node.as_pair() if node else None)
                elif cmd == "find":
                    node = dll.find_by_key(arg[0])
                    results.append(node.val if node else None)
                elif cmd == "forward":
                    results.append(dll.pairs_forward())
                elif cmd == "backward":
                    results.append(dll.pairs_backward())
                elif cmd == "size":
                    results.append(len(dll))
                else:
                    raise ValueError(f"Unknown command: {cmd}")

            if results != expected_returns:
                ok = False
                err = f"Return mismatch | expected={expected_returns}, got={results}"

            if ok and dll.pairs_forward() != final_fwd:
                ok = False
                err = f"Final forward mismatch | expected={final_fwd}, got={dll.pairs_forward()}"

            if ok and dll.pairs_backward() != final_bwd:
                ok = False
                err = f"Final backward mismatch | expected={final_bwd}, got={dll.pairs_backward()}"

            if ok and len(dll) != final_size:
                ok = False
                err = f"Final size mismatch | expected={final_size}, got={len(dll)}"

            if ok and not dll.validate_integrity():
                ok = False
                err = "Pointer integrity validation failed"

        except Exception as e:
            ok = False
            err = f"{type(e).__name__}: {e}"

        if ok:
            print(f"Test {i}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {err}")

    print(f"\nSummary: {passed}/{len(tests)} tests passed.\n")


test_harness()

