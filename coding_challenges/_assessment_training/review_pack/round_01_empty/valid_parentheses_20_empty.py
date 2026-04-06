# LeetCode 20: Valid Parentheses (Round 01 Empty)
from typing import Callable, List, Tuple

tests: List[Tuple[str, bool]] = [
    ("()", True),
    ("()[]{}", True),
    ("(]", False),
    ("([)]", False),
    ("{[]}", True),
    ("", True),
    (")(", False),      # starts with closing bracket (even length) -> exposes stack[-1] bug
    ("])", False),      # starts with closing bracket (even length) -> exposes stack[-1] bug
    ("}{", False),      # starts with closing bracket (even length) -> exposes stack[-1] bug
]

def harness(func: Callable[[str], bool]) -> None:
    print(f"--- Running Tests for: {func.__name__} ---")
    passed = 0
    for i, (s, expected) in enumerate(tests, 1):
        try:
            result = func(s)
            if result == expected:
                print(f"Test {i}: PASSED")
                passed += 1
            else:
                print(f"Test {i}: FAILED | expected={expected}, got={result}")
        except Exception as e:
            print(f"Test {i}: ERROR | {type(e).__name__}: {e}")
    print(f"\nSummary: {passed}/{len(tests)} tests passed.")

def isValid(s: str) -> bool:
    if s == "" : return True
    if len(s) % 2 != 0 : return False
    phmap = {']':'[', '}':'{', ')':'('}
    stack=[]
    for ch in s:
        if ch not in phmap:
            stack.append(ch)
        else:
            if stack and phmap[ch] == stack[-1]:
                stack.pop()
            else:
                return False
    return not stack
        


harness(isValid)
