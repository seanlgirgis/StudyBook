"""
Problem: Valid Palindrome
Category: Two Pointers
Difficulty: Easy

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. 
Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
"""

class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            if not s[left].isalnum():
                left += 1
            elif not s[right].isalnum():
                right -= 1
            else:
                if s[left].lower() != s[right].lower():
                    return False
                left += 1
                right -= 1
            
        return True

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    s1 = "A man, a plan, a canal: Panama"
    print(f"Test Case 1: '{s1}' -> {solution.isPalindrome(s1)} (Expected: True)")
    
    # Test Case 2
    s2 = "race a car"
    print(f"Test Case 2: '{s2}' -> {solution.isPalindrome(s2)} (Expected: False)")
    
    # Test Case 3
    s3 = " "
    print(f"Test Case 3: '{s3}' -> {solution.isPalindrome(s3)} (Expected: True)")
