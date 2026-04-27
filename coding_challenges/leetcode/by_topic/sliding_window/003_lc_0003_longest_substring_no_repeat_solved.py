"""
Problem: Longest Substring Without Repeating Characters
Category: Sliding Window
Difficulty: Medium

Given a string s, find the length of the longest substring without repeating characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        print(f"processing string {s} with length {len(s)}")
        seen = {}
        left = max_length = 0
        for right, char in enumerate(s):
            #print(f"{char}")
            # If char was seen and is inside current window → jump left
            if char in seen and seen[char] >= left:
                left = seen[char] + 1
            seen[char] = right
            max_length = max (max_length, right - left +1)
        return max_length
            
        # TODO: Implement this method
        # Hint: Use a sliding window (left, right pointers) and a Set to track characters in the current window.
        # If s[right] is in the set, remove s[left] and shrink window until s[right] is valid again.
        pass

# Test cases to run locally
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    s1 = "abcabcbb"
    print(f"Test Case 1: '{s1}' -> {solution.lengthOfLongestSubstring(s1)} (Expected: 3)")
    
    # Test Case 2
    s2 = "bbbbb"
    print(f"Test Case 2: '{s2}' -> {solution.lengthOfLongestSubstring(s2)} (Expected: 1)")
    
    # Test Case 3
    s3 = "pwwkew"
    print(f"Test Case 3: '{s3}' -> {solution.lengthOfLongestSubstring(s3)} (Expected: 3)")

    #Test Case 4
    s4 = "seanlukagirgis"
    print(f"Test Case 4: '{s4}' -> {solution.lengthOfLongestSubstring(s4)} (Expected: 8)")

