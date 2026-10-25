import time
import unittest
from dataclasses import dataclass

from primary_arithmetic import get_carry_count


@dataclass(frozen=True)
class CarryTestCase:
    name: str
    nums: list[str]
    expected: int
    max_duration_sec: float = 0.05


class TestGetCarryCount(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cases: list[CarryTestCase] = [
            # Edge Cases
            CarryTestCase(name="empty_list", nums=[], expected=0),
            CarryTestCase(name="single_number_no_carry", nums=["123"], expected=0),
            CarryTestCase(name="all_zeros", nums=["0", "0"], expected=0),
            CarryTestCase(name="multi_zeros", nums=["0", "0", "0", "0"], expected=0),
            # Simple Operations
            CarryTestCase(name="two_numbers_no_carry", nums=["123", "456"], expected=0),
            CarryTestCase(name="two_numbers_single_carry", nums=["5", "5"], expected=1),
            CarryTestCase(
                name="two_numbers_unequal_length", nums=["99", "1"], expected=2
            ),
            # Cascading / Chained Carries
            CarryTestCase(
                name="cascading_carries_ripple", nums=["999", "1"], expected=3
            ),
            CarryTestCase(name="intermittent_carries", nums=["555", "555"], expected=3),
            # Multi-Number Additions (list length > 2)
            CarryTestCase(
                name="three_numbers_no_carry", nums=["11", "22", "33"], expected=0
            ),
            CarryTestCase(
                name="three_numbers_single_carry", nums=["15", "15", "15"], expected=1
            ),
            CarryTestCase(
                name="multi_carry_greater_than_one",
                nums=["9", "9", "9", "9", "9"],  # sum = 45 -> carry = 4
                expected=1,
            ),
            CarryTestCase(
                name="varied_lengths_cascading",
                nums=["9999", "1", "99", "901"],
                expected=4,
            ),
            # Performance / Scale
            CarryTestCase(
                name="large_digit_strings",
                nums=["9" * 1000, "1"],
                expected=1000,
                max_duration_sec=0.1,
            ),
            CarryTestCase(
                name="many_inputs",
                nums=["9" for _ in range(100)],
                expected=2,
                max_duration_sec=0.1,
            ),
        ]

    def test_get_carry_count_table_driven(self) -> None:
        for tc in self.test_cases:
            with self.subTest(msg=tc.name):
                start = time.perf_counter()
                actual = get_carry_count(tc.nums)
                duration = time.perf_counter() - start

                self.assertEqual(
                    actual,
                    tc.expected,
                    f"[{tc.name}] Expected {tc.expected}, got {actual}",
                )
                self.assertLessEqual(
                    duration,
                    tc.max_duration_sec,
                    f"[{tc.name}] Exceeded time limit: {duration:.4f}s > {tc.max_duration_sec}s",
                )


if __name__ == "__main__":
    unittest.main()
