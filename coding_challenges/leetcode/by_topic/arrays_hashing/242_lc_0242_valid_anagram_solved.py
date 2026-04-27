"""
Problem: Valid Anagram
Category: Arrays & Hashing
Difficulty: Easy

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, 
typically using all the original letters exactly once.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    s1, t1 = "anagram", "nagaram"
    print(f"Test Case 1: '{s1}', '{t1}' -> {solution.isAnagram(s1, t1)} (Expected: True)")
    
    # Test Case 2
    s2, t2 = "rat", "car"
    print(f"Test Case 2: '{s2}', '{t2}' -> {solution.isAnagram(s2, t2)} (Expected: False)")
