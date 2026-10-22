#!/usr/bin/env python
import time
import unittest
from dataclasses import dataclass

from australian_voting import solve_voting


@dataclass(frozen=True)
class TestCase:
    name: str
    candidates: list[str]
    ballots: list[list[int]]
    expected_winners: list[str]
    rationale: str
    max_duration_sec: float = 0.010


TEST_CASES = [
    TestCase(
        name="Problem Sample: Multi-round transfer",
        candidates=["John Doe", "Jane Smith", "Jane Austen"],
        ballots=[
            [1, 2, 3],
            [2, 1, 3],
            [2, 3, 1],
            [1, 2, 3],
            [3, 1, 2],
        ],
        expected_winners=["John Doe"],
        rationale=(
            "Round 1: John=2, Jane S.=2, Jane A.=1. Jane A. eliminated. "
            "Her ballot transfers to John Doe, giving him 3/5 votes (> 50%)."
        ),
    ),
    TestCase(
        name="Immediate majority (first round)",
        candidates=["Alice", "Bob", "Charlie"],
        ballots=[
            [1, 2, 3],
            [1, 3, 2],
            [1, 2, 3],
            [2, 1, 3],
        ],
        expected_winners=["Alice"],
        rationale="Alice receives 3/4 (75%) first-choice votes directly.",
    ),
    TestCase(
        name="Exact 50% does not win",
        candidates=["Alice", "Bob"],
        ballots=[
            [1, 2],
            [2, 1],
        ],
        expected_winners=["Alice", "Bob"],
        rationale="Strictly > 50% is required. Equal split means a tie.",
    ),
    TestCase(
        name="Simultaneous lowest elimination triggers tie",
        candidates=["Alice", "Bob", "Charlie"],
        ballots=[
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2],
        ],
        expected_winners=["Alice", "Bob", "Charlie"],
        rationale="All have 1 vote each (min == max). All tie simultaneously.",
    ),
    TestCase(
        name="Multiple candidates tied for lowest eliminated together",
        candidates=["Alice", "Bob", "Charlie", "David"],
        ballots=[
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [2, 1, 3, 4],
            [3, 1, 2, 4],
            [4, 1, 2, 3],
        ],
        expected_winners=["Alice"],
        rationale=(
            "Round 1: Alice=2, Bob=1, Charlie=1, David=1. "
            "Bob, Charlie, and David all share min votes (1). All are eliminated; Alice wins."
        ),
    ),
    TestCase(
        name="Single candidate",
        candidates=["Solo Candidate"],
        ballots=[
            [1],
            [1],
            [1],
        ],
        expected_winners=["Solo Candidate"],
        rationale="Only candidate immediately has 100% of votes.",
    ),
    TestCase(
        name="Deep preference cascading",
        candidates=["A", "B", "C", "D"],
        ballots=[
            [4, 3, 2, 1],
            [4, 3, 2, 1],
            [3, 2, 1, 4],
            [2, 1, 3, 4],
            [1, 2, 3, 4],
        ],
        expected_winners=["D"],
        rationale="Rounds eliminate bottom candidates sequentially until D secures > 50%.",
    ),
    TestCase(
        name="Max constraints boundary (20 candidates, 1000 voters)",
        candidates=[f"Candidate {i}" for i in range(1, 21)],
        # 501 voters prefer Candidate 1, 499 prefer Candidate 2
        ballots=[[1] + list(range(2, 21)) for _ in range(501)]
        + [[2, 1] + list(range(3, 21)) for _ in range(499)],
        expected_winners=["Candidate 1"],
        rationale="Candidate 1 has 501/1000 votes (> 50%) at max input dimensions.",
    ),
]


class TestAustralianVoting(unittest.TestCase):
    def test_functional_and_unit_latency(self):
        for tc in TEST_CASES:
            with self.subTest(tc.name):
                ballots_copy = [list(b) for b in tc.ballots]

                start = time.perf_counter()
                winners = solve_voting(tc.candidates, ballots_copy)
                elapsed = time.perf_counter() - start

                self.assertEqual(
                    sorted(winners),
                    sorted(tc.expected_winners),
                    msg=f"\nFailed: {tc.name}\nRationale: {tc.rationale}\nGot: {winners}, Expected: {tc.expected_winners}",
                )
                self.assertLessEqual(
                    elapsed,
                    tc.max_duration_sec,
                    f"Execution exceeded budget: {elapsed * 1000:.2f}ms > {tc.max_duration_sec * 1000:.1f}ms",
                )

    def test_stress_throughput(self):
        candidates = [f"C{i}" for i in range(1, 21)]
        ballot_template = list(range(1, 21))
        large_ballots = [
            ballot_template[i % 20 :] + ballot_template[: i % 20] for i in range(1000)
        ]

        max_batch_time = 0.150

        start = time.perf_counter()
        for _ in range(50):
            solve_voting(candidates, [list(b) for b in large_ballots])
        elapsed = time.perf_counter() - start

        self.assertLessEqual(
            elapsed,
            max_batch_time,
            f"50 large elections took {elapsed * 1000:.2f}ms (budget: {max_batch_time * 1000:.1f}ms)",
        )


if __name__ == "__main__":
    unittest.main()
