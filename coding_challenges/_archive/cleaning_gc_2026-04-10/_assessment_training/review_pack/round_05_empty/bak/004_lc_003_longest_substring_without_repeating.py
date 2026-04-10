# ============================================================================
# File: lc_003_longest_substring_without_repeating.py
#
# LeetCode 3: Longest Substring Without Repeating Characters (Medium)
#
# PROBLEM STATEMENT:
# Given a string s, find the length of the longest substring without 
# repeating characters.
#
# EXAMPLES:
# - s = "abcabcbb"  -> Expected: 3 (The answer is "abc")
# - s = "bbbbb"     -> Expected: 1 (The answer is "b")
# - s = "pwwkew"    -> Expected: 3 (The answer is "wke")
# ============================================================================

from typing import List, Callable

# --- TEST CASES ---
# Format: {"kwargs": {...}, "expected": ...}
longest_substring_tests: List[dict] = [
    {
        "kwargs": {"s": "abcabcbb"},
        "expected": 3
    },
    {
        "kwargs": {"s": "bbbbb"},
        "expected": 1
    },
    {
        "kwargs": {"s": "pwwkew"},
        "expected": 3
    },
    {
        # Edge case: Empty string
        "kwargs": {"s": ""},
        "expected": 0
    },
    {
        # Edge case: Single space
        "kwargs": {"s": " "},
        "expected": 1
    },
    {
        # Edge case: No repeating characters
        "kwargs": {"s": "au"},
        "expected": 2
    }
]

# --- TEST HARNESS ---
def test_harness(func: Callable, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #3: Longest Substring Without Repeating Characters.
    Validates integer output against expected integer lengths.
    """
    print(f"--- Running Tests for: {func.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases):
        kwargs = tc["kwargs"]
        expected: int = tc["expected"]
        
        try:
            # Execute the target function directly
            result = func(**kwargs)
            
            if result is None:
                print(f"Test {i+1}: FAILED | Got None, Expected {expected}")
            elif result == expected:
                # Formatting the output to stay readable if strings are very long
                s_display = kwargs['s']
                if len(s_display) > 30:
                    s_display = s_display[:27] + "..."
                print(f"Test {i+1}: PASSED (s='{s_display}')")
                passed += 1
            else:
                s_display = kwargs['s']
                if len(s_display) > 20:
                    s_display = s_display[:17] + "..."
                print(f"Test {i+1}: FAILED | Got {result}, Expected {expected} (s='{s_display}')")
                        
        except Exception as e:
            print(f"Test {i+1}: ERROR  | {type(e).__name__}: {e}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- USER TO IMPLEMENT SOLUTION BELOW ---
def lengthOfLongestSubstring(s: str) -> int:
    if len(s) <= 1:
        return len(s)

    seen = set()
    l, ret = 0, 0
    for ch in s:
        while ch in seen:
            seen.remove(s[l])
            l += 1
        seen.add(ch)
        ret = max(ret, len(seen))
    return ret
    
    


# Execute harness without __main__ block
test_harness(lengthOfLongestSubstring, longest_substring_tests)
