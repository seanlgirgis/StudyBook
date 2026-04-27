"""
Problem: Valid Parentheses
Category: Stack
Difficulty: Easy

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false
"""

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        pairs = {')':'(', ']':'[', '}':'{'}
        for char in s:
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack or stack.pop() != pairs[char]:
                    return False
        return (len(stack) == 0)


# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    s1 = "()"
    print(f"Test Case 1: '{s1}' -> {solution.isValid(s1)} (Expected: True)")
    
    # Test Case 2
    s2 = "()[]{}"
    print(f"Test Case 2: '{s2}' -> {solution.isValid(s2)} (Expected: True)")
    
    # Test Case 3
    s3 = "(]"
    print(f"Test Case 3: '{s3}' -> {solution.isValid(s3)} (Expected: False)")
    
    # Test Case 4
    s4 = "([)]"
    print(f"Test Case 4: '{s4}' -> {solution.isValid(s4)} (Expected: False)")