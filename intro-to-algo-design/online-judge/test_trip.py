#!/bin/env python
import time
import unittest
from dataclasses import dataclass

from trip import solve_trip


@dataclass(frozen=True)
class TestCase:
    name: str
    expenses_cents: list[int]
    expected_cents: int
    rationale: str
    max_duration_sec: float = 0.001


TEST_CASES = [
    TestCase(
        name="Sample 1: Even split",
        expenses_cents=[1000, 2000, 3000],
        expected_cents=1000,
        rationale="Total 6000 / 3 = exactly 2000 each.",
    ),
    TestCase(
        name="Sample 2: Uneven remainder",
        expenses_cents=[1500, 1501, 300, 301],
        expected_cents=1199,
        rationale="3602 cents splits into two 901s and two 900s.",
    ),
    TestCase(
        name="Single traveler",
        expenses_cents=[1000],
        expected_cents=0,
        rationale="No one else to exchange money with.",
    ),
    TestCase(
        name="Already equal costs",
        expenses_cents=[555, 555, 555],
        expected_cents=0,
        rationale="Zero net transfers required.",
    ),
    TestCase(
        name="All zero expenses",
        expenses_cents=[0, 0, 0],
        expected_cents=0,
        rationale="Nobody spent anything.",
    ),
    TestCase(
        name="Remainder smaller than group (no transfer needed)",
        expenses_cents=[1, 0, 0],
        expected_cents=0,
        rationale="1 cent splits into targets [1, 0, 0]. Already balanced within 1c.",
    ),
    TestCase(
        name="Remainder requires single-cent transfer",
        expenses_cents=[0, 0, 2],
        expected_cents=1,
        rationale="2 cents splits into targets [1, 1, 0]. One student pays 1 cent.",
    ),
    TestCase(
        name="Upper boundary limits",
        expenses_cents=[0] * 500 + [1_000_000] * 500,
        expected_cents=250_000_000,
        rationale="1000 people, 500_000 target each.",
    ),
]


class TestTheTrip(unittest.TestCase):
    def test_functional_and_unit_latency(self):
        for tc in TEST_CASES:
            with self.subTest(tc.name):
                data = list(tc.expenses_cents)

                start = time.perf_counter()
                result = solve_trip(data)
                elapsed = time.perf_counter() - start

                self.assertEqual(result, tc.expected_cents, tc.rationale)
                self.assertLessEqual(
                    elapsed,
                    tc.max_duration_sec,
                    f"Too slow: {elapsed * 1000:.3f}ms (budget: {tc.max_duration_sec * 1000:.1f}ms)",
                )

    def test_stress_throughput(self):
        sample_trip = [1234] * 500 + [5678] * 500
        max_duration_sec = 0.050

        start = time.perf_counter()
        for _ in range(100):
            solve_trip(list(sample_trip))
        elapsed = time.perf_counter() - start

        self.assertLessEqual(
            elapsed,
            max_duration_sec,
            f"100 calls took {elapsed * 1000:.2f}ms (budget: {max_duration_sec * 1000:.1f}ms)",
        )


if __name__ == "__main__":
    unittest.main()
