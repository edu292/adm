#!/usr/bin/env python
import unittest
from dataclasses import dataclass

from three_n_plus_one import solve_3n1


@dataclass(frozen=True)
class TestCase:
    name: str
    i: int
    j: int
    expected_max: int
    rationale: str


TEST_CASES = [
    TestCase(
        name="Base single element: 1",
        i=1,
        j=1,
        expected_max=1,
        rationale="1 prints '1' and immediately halts. Cycle length is 1.",
    ),
    TestCase(
        name="Base single element: 22",
        i=22,
        j=22,
        expected_max=16,
        rationale="From problem description: 22 takes 16 numbers.",
    ),
    TestCase(
        name="Sample case: 1 to 10",
        i=1,
        j=10,
        expected_max=20,
        rationale="9 has cycle length 20 (9->28->14->7->22->...->1), which is the max in [1, 10].",
    ),
    TestCase(
        name="Sample case: 100 to 200",
        i=100,
        j=200,
        expected_max=125,
        rationale="Peak cycle length in this range is 125.",
    ),
    TestCase(
        name="Sample case: 201 to 210",
        i=201,
        j=210,
        expected_max=89,
        rationale="Peak cycle length in this range is 89.",
    ),
    TestCase(
        name="Sample case: 900 to 1000",
        i=900,
        j=1000,
        expected_max=174,
        rationale="Peak cycle length in this range is 174.",
    ),
    TestCase(
        name="Trap case: reversed order (i > j)",
        i=10,
        j=1,
        expected_max=20,
        rationale="Must search range [1, 10] even though input came in as (10, 1).",
    ),
    TestCase(
        name="Upper boundary check (< 10,000)",
        i=1,
        j=9999,
        expected_max=262,
        rationale="Number 6171 and 9709 have the maximal cycle length of 262 under 10,000.",
    ),
]


class TestCollatzCycle(unittest.TestCase):
    def test_all_cases(self):
        for tc in TEST_CASES:
            with self.subTest(tc.name):
                result = solve_3n1(tc.i, tc.j)
                self.assertEqual(
                    result,
                    tc.expected_max,
                    f"\nFailed: {tc.name}\nRationale: {tc.rationale}\nGot: {result}, Expected: {tc.expected_max}",
                )


if __name__ == "__main__":
    unittest.main()
