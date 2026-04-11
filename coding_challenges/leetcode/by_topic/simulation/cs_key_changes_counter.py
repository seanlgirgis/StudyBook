"""
id: cs_key_changes_counter
title: Key Changes Counter
source: codesignal
difficulty: easy
primary: simulation
tags: [simulation, arrays, strings]
codesignal_url: https://app.codesignal.com/test/gGya72ovLpQNGSvwq/question/DvbLsFNdgxpnYSLHP
status: draft
last_updated: 2026-04-11
notes:
- key idea:
- time:
- space:
"""

# ============================================================================
# File: cs_key_changes_counter.py
# Problem: Key Changes Counter (Easy)
#
# Problem Statement:
# You are given an array of uppercase and lowercase English letters,
# recording, representing a sequence of letters typed by the user.
#
# Count the number of times the user changed keys while typing, considering
# that uppercase and lowercase letters require the same key press (modifiers
# like Shift or Caps Lock are ignored). For example, typing 'W' and 'w'
# require the same key, whereas typing 'w' and 'e' require different keys.
#
# Constraints:
# - 1 <= recording.length <= 1000
# - recording contains only uppercase and/or lowercase English letters
#
# Examples:
# Example 1:
# Input: recording = ['W', 'w', 'a', 'A', 'a', 'b', 'B']
# Output: 2
# Explanation: W->w (same key), w->a (CHANGE), a->A (same key),
#              A->a (same key), a->b (CHANGE), b->B (same key). Changes = 2.
#
# Example 2:
# Input: recording = ['w', 'W', 'a', 'w', 'a']
# Output: 3
# Explanation: w->W (same), W->a (CHANGE), a->w (CHANGE), w->a (CHANGE).
#              Changes = 3.
# ============================================================================

from typing import List, Tuple, Callable

# Test Suite: (Input, Expected Output)
tests: List[Tuple[List[str], int]] = [
    (['W', 'w', 'a', 'A', 'a', 'b', 'B'], 2),   # Example 1: Basic key changes
    (['w', 'W', 'a', 'w', 'a'],           3),   # Example 2: Multiple changes
    (['a'],                                0),   # Edge Case: Single character
    (['a', 'A', 'a', 'A'],                 0),   # Edge Case: Same key, case alternating
    (['a', 'b', 'c', 'd'],                 3),   # All different keys
    (['A', 'B', 'A', 'B'],                 3),   # Alternating two keys
    (['a', 'a', 'a'],                      0),   # Repeated same letter
    (['A', 'a', 'B', 'b', 'C', 'c'],       2),   # Case pairs with 2 key changes
    (['z', 'Z', 'y', 'Y', 'x'],            2),   # Mixed case groups
    (['a', 'b', 'a', 'b', 'a'],            4),   # Rapid alternation
]

def harness(func: Callable) -> None:
    passed = 0
    failed = 0

    print(f"--- Running Tests for: {func.__name__} ---")

    for i, (recording_in, expected) in enumerate(tests):
        # Create a copy to prevent mutation issues
        recording_copy = list(recording_in)

        try:
            actual = func(recording_copy)
            if actual == expected:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (Expected {expected}, got {actual})"
                failed += 1
        except Exception as e:
            status = f"ERROR ({type(e).__name__}: {e})"
            failed += 1

        # Truncate long inputs for cleaner output
        display_input = str(recording_in) if len(str(recording_in)) < 50 else f"{str(recording_in)[:47]}..."
        print(f"Test {i+1:02d}: {status} | Input: {display_input}")

    print(f"\n--- Result: {passed} Passed, {failed} Failed ---")

# --- USER TO IMPLEMENT SOLUTION BELOW ---

def solution(recording: List[str]) -> int:
    changes = 0
    for i in range(1, len(recording)):
        cur_key  = recording[i].lower()
        prev_key = recording[i - 1].lower()
        if cur_key != prev_key:
            changes += 1
    return changes


def solution_zip(recording: List[str]) -> int:
    return sum(
        a.lower() != b.lower()
        for a, b in zip(recording, recording[1:])
    )


solutions: List[Callable] = [
    solution,
    solution_zip,
]

for sol in solutions:
    print()
    harness(sol)
