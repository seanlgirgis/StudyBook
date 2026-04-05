"""Reusable test harness for Two Sum.

Pass your implementation function into `run_test_harness`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Sequence, Set, Tuple
import random

TwoSumFn = Callable[[List[int], int], Sequence[int]]


@dataclass(frozen=True)
class TestCase:
    name: str
    nums: List[int]
    target: int
    expected_index_sets: Optional[Set[Tuple[int, int]]] = None


def _normalize_pair(i: int, j: int) -> Tuple[int, int]:
    return (i, j) if i <= j else (j, i)


def _validate_output(fn: TwoSumFn, tc: TestCase) -> None:
    out = fn(tc.nums[:], tc.target)

    if not isinstance(out, (list, tuple)):
        raise AssertionError(f"{tc.name}: output must be a list/tuple of two indices. Got type={type(out).__name__}")

    if len(out) != 2:
        raise AssertionError(f"{tc.name}: output must have length 2. Got {out}")

    i, j = out[0], out[1]
    if not isinstance(i, int) or not isinstance(j, int):
        raise AssertionError(f"{tc.name}: indices must be integers. Got {out}")

    n = len(tc.nums)
    if i < 0 or i >= n or j < 0 or j >= n:
        raise AssertionError(f"{tc.name}: indices out of range for n={n}. Got {out}")

    if i == j:
        raise AssertionError(f"{tc.name}: cannot use same element twice. Got {out}")

    if tc.nums[i] + tc.nums[j] != tc.target:
        raise AssertionError(
            f"{tc.name}: nums[i] + nums[j] must equal target. "
            f"nums[{i}]={tc.nums[i]}, nums[{j}]={tc.nums[j]}, target={tc.target}"
        )

    if tc.expected_index_sets is not None:
        pair = _normalize_pair(i, j)
        if pair not in tc.expected_index_sets:
            raise AssertionError(
                f"{tc.name}: wrong index pair. Got {pair}, expected one of {sorted(tc.expected_index_sets)}"
            )


def _base_test_cases() -> List[TestCase]:
    return [
        TestCase(
            name="example_1",
            nums=[2, 7, 11, 15],
            target=9,
            expected_index_sets={_normalize_pair(0, 1)},
        ),
        TestCase(
            name="example_2",
            nums=[3, 2, 4],
            target=6,
            expected_index_sets={_normalize_pair(1, 2)},
        ),
        TestCase(
            name="example_3_duplicates",
            nums=[3, 3],
            target=6,
            expected_index_sets={_normalize_pair(0, 1)},
        ),
        TestCase(
            name="negative_numbers",
            nums=[-3, 4, 3, 90],
            target=0,
            expected_index_sets={_normalize_pair(0, 2)},
        ),
        TestCase(
            name="zero_pair",
            nums=[0, 4, 3, 0],
            target=0,
            expected_index_sets={_normalize_pair(0, 3)},
        ),
        TestCase(
            name="minimal_length",
            nums=[1, 5],
            target=6,
            expected_index_sets={_normalize_pair(0, 1)},
        ),
        TestCase(
            name="large_values",
            nums=[1_000_000, -999_999, -1, 2],
            target=1,
            expected_index_sets={_normalize_pair(0, 2)},
        ),
        TestCase(
            name="tail_duplicates",
            nums=[1, 2, 3, 4, 4],
            target=8,
            expected_index_sets={_normalize_pair(3, 4)},
        ),
        TestCase(
            name="multiple_valid_pairs_allowed",
            nums=[1, 1, 1, 2, 2],
            target=3,
            expected_index_sets=None,
        ),
    ]


def _random_generated_cases(count: int = 30, seed: int = 42) -> Iterable[TestCase]:
    rng = random.Random(seed)
    for idx in range(count):
        size = rng.randint(6, 30)
        nums = [rng.randint(-500, 500) for _ in range(size)]
        i, j = rng.sample(range(size), 2)
        target = nums[i] + nums[j]
        yield TestCase(name=f"random_{idx+1}", nums=nums, target=target, expected_index_sets=None)


def run_test_harness(two_sum_fn: TwoSumFn, include_random: bool = True) -> dict:
    """Run deterministic (and optional random) tests against a two_sum implementation.

    Args:
        two_sum_fn: function with signature (nums: List[int], target: int) -> Sequence[int]
        include_random: whether to include additional generated tests

    Returns:
        Dict summary with pass/fail counts.
    """
    tests = _base_test_cases()
    if include_random:
        tests.extend(list(_random_generated_cases()))

    passed = 0
    failed = 0
    failures = []

    for tc in tests:
        try:
            _validate_output(two_sum_fn, tc)
            passed += 1
        except Exception as exc:
            failed += 1
            failures.append(f"{tc.name}: {exc}")

    summary = {
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "failures": failures,
    }
    return summary


def print_summary(summary: dict) -> None:
    print("=" * 58)
    print("Two Sum Test Harness Summary")
    print("=" * 58)
    print(f"Total  : {summary['total']}")
    print(f"Passed : {summary['passed']}")
    print(f"Failed : {summary['failed']}")

    if summary["failed"]:
        print("\nFailures:")
        for line in summary["failures"]:
            print(f"- {line}")
    else:
        print("\nAll tests passed.")
