# ============================================================================
# File: online_stock_span_901.py
#
# LeetCode 901: Online Stock Span (Medium)
#
# PROBLEM STATEMENT:
# Design a class StockSpanner which collects daily price quotes for some stock 
# and returns the span of that stock's price for the current day.
#
# The span of the stock's price in one day is the maximum number of consecutive 
# days (starting from that day and going backward) for which the stock price 
# was less than or equal to the price of that day.
#
# EXAMPLES:
# - If the prices of the stock in the last four days is [7,2,1,2] and the 
#   price of the stock today is 2, then the span of today is 4 because 
#   starting from today, the price of the stock was less than or equal 2 for 4 days.
#
# - Input: ["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
#   Args:  [[], [100], [80], [60], [70], [60], [75], [85]]
#   Output: [null, 1, 1, 1, 2, 1, 4, 6]
# ============================================================================

from typing import List, Optional, Any

# --- TEST CASES ---
# Format: {"commands": [...], "args": [...], "expected": [...]}
stock_spanner_tests: List[dict] = [
    {
        # Standard Example 1
        "commands": ["StockSpanner", "next", "next", "next", "next", "next", "next", "next"],
        "args": [[], [100], [80], [60], [70], [60], [75], [85]],
        "expected": [None, 1, 1, 1, 2, 1, 4, 6]
    },
    {
        # Boundary: Strictly decreasing prices (span is always 1)
        "commands": ["StockSpanner", "next", "next", "next", "next"],
        "args": [[], [10], [9], [8], [7]],
        "expected": [None, 1, 1, 1, 1]
    },
    {
        # Boundary: Strictly increasing prices (span grows with every day)
        "commands": ["StockSpanner", "next", "next", "next", "next"],
        "args": [[], [1], [2], [3], [4]],
        "expected": [None, 1, 2, 3, 4]
    },
    {
        # Edge case: Identical prices (span grows, as definition says "less than or EQUAL to")
        "commands": ["StockSpanner", "next", "next", "next", "next"],
        "args": [[], [5], [5], [5], [5]],
        "expected": [None, 1, 2, 3, 4]
    },
    {
        # Edge case: High fluctuation
        "commands": ["StockSpanner", "next", "next", "next", "next", "next", "next"],
        "args": [[], [30], [20], [25], [28], [20], [30]],
        "expected": [None, 1, 1, 2, 3, 1, 6]
    }
]

# --- TEST HARNESS ---
def test_harness(target_class: type, test_cases: List[dict]) -> None:
    """
    Test harness for LeetCode #901: Online Stock Span.
    Validates sequential state execution and correct span calculations.
    """
    print(f"--- Running Tests for: {target_class.__name__} ---")
    passed: int = 0
    
    for i, tc in enumerate(test_cases, 1):
        commands: List[str] = tc["commands"]
        args: List[List[Any]] = tc["args"]
        expected: List[Optional[int]] = tc["expected"]
        
        obj = None
        results: List[Optional[int]] = []
        test_passed: bool = True
        error_msg: str = ""
        
        try:
            # Execute commands
            for step, (cmd, arg) in enumerate(zip(commands, args)):
                if cmd == "StockSpanner":
                    obj = target_class()
                    results.append(None)
                elif cmd == "next":
                    results.append(obj.next(arg[0]))
                else:
                    raise ValueError(f"Unknown command: {cmd}")
            
            # Validate results
            for step, (res, exp) in enumerate(zip(results, expected)):
                if res != exp:
                    test_passed = False
                    error_msg = f"Mismatch at step {step} ({commands[step]}{args[step]}): Got {res}, Expected {exp}"
                    break
                        
        except Exception as e:
            test_passed = False
            error_msg = f"{type(e).__name__}: {e}"
            
        if test_passed:
            print(f"Test {i}: PASSED ({len(commands)} operations)")
            passed += 1
        else:
            print(f"Test {i}: FAILED | {error_msg}")
            
    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.\n")


# --- IMPLEMENTATION ---
class StockSpanner:
    def __init__(self):
        self.stack = []         # stack of tuples (price , span)   Mono ..If cur price is bigger ..pop and calculate. store cur span with the price

    def next(self, price: int) -> int:
        span = 1
        
        while self.stack and price >= self.stack[-1][0]:
            _, pspan = self.stack.pop()
            span += pspan
        self.stack .append((price, span))
        return span


# Execute harness without __main__ block
test_harness(StockSpanner, stock_spanner_tests)
