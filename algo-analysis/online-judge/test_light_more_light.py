import time
import unittest
from dataclasses import dataclass

from ligh_more_light import is_bulb_on, is_bulb_on_iterative


@dataclass(frozen=True)
class PerformanceTestCase:
    label: str
    n: int
    expected_state: bool
    isqrt_max_duration_sec: float = 0.0001
    skip_iterative: bool = False


class TestBulbPerformance(unittest.TestCase):
    def setUp(self) -> None:
        max_32_bit = (1 << 32) - 1

        self.table: list[PerformanceTestCase] = [
            PerformanceTestCase("One", 1, True),
            PerformanceTestCase("Small Prime", 13, False),
            PerformanceTestCase("Small Square", 10_000, True),
            PerformanceTestCase("Mid Non-Square", 100_003, False),
            PerformanceTestCase("Mid Square (10^6)", 1_000_000, True),
            PerformanceTestCase("Iterative Limit (~10^7)", 10_000_000, False),
            PerformanceTestCase(
                "Large Non-Square (2^28 - 1)",
                (1 << 28) - 1,
                False,
                skip_iterative=True,
            ),
            PerformanceTestCase(
                "Largest 32-bit Square (65535^2)",
                65535**2,
                True,
                skip_iterative=True,
            ),
            PerformanceTestCase(
                "Max 32-bit Ceiling (2^32 - 1)",
                max_32_bit,
                False,
                skip_iterative=True,
            ),
        ]

    def test_correctness_and_performance(self) -> None:
        header = f"\n{'Label':<32} | {'N':<12} | {'Iterative (s)':<14} | {'isqrt (s)':<12} | {'Speedup':<12}"
        print(header)
        print("-" * len(header))

        for tc in self.table:
            with self.subTest(label=tc.label, n=tc.n):
                # 1. Benchmark O(1) math.isqrt
                t0 = time.perf_counter()
                trials = 5_000 if tc.n < 10_000_000 else 1_000
                for _ in range(trials):
                    fast_res = is_bulb_on(tc.n)
                fast_duration = (time.perf_counter() - t0) / trials

                self.assertEqual(fast_res, tc.expected_state)
                self.assertLessEqual(
                    fast_duration,
                    tc.isqrt_max_duration_sec,
                    f"[{tc.label}] isqrt took {fast_duration * 1e6:.2f}µs",
                )

                # 2. Benchmark iterative if allowed
                if not tc.skip_iterative:
                    t1 = time.perf_counter()
                    iter_res = is_bulb_on_iterative(tc.n)
                    iter_duration = time.perf_counter() - t1

                    self.assertEqual(iter_res, fast_res)
                    iter_str = f"{iter_duration:.6f}"
                    speedup_str = f"{iter_duration / fast_duration:,.0f}x"
                else:
                    iter_str = "SKIPPED"
                    speedup_str = "N/A (>10s)"

                print(
                    f"{tc.label:<32} | {tc.n:<12} | {iter_str:<14} | {fast_duration:.8f}   | {speedup_str:<12}"
                )


if __name__ == "__main__":
    unittest.main()
