"""Run Two Sum tests against your implementation in solution.py."""

from solution import two_sum
from test_harness import print_summary, run_test_harness


if __name__ == "__main__":
    summary = run_test_harness(two_sum, include_random=True)
    print_summary(summary)
