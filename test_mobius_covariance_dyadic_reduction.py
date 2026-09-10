import unittest

from mobius_covariance_dyadic_reduction import (
    dyadic_partition,
    dyadic_partition_receipt,
    finite_energy_cauchy_receipt,
)


class MobiusCovarianceDyadicReductionTests(unittest.TestCase):
    def test_all_small_intervals_partition_exactly_with_two_per_scale(self):
        for right in range(1, 100):
            for left in range(right):
                result = dyadic_partition_receipt(left, right)
                covered = []
                for block_left, block_right in result["blocks"]:
                    length = block_right - block_left
                    self.assertEqual(length & (length - 1), 0)
                    self.assertEqual(block_left % length, 0)
                    covered.extend(range(block_left + 1, block_right + 1))
                self.assertEqual(covered, list(range(left + 1, right + 1)))
                self.assertLessEqual(result["block_count"],
                                     result["logarithmic_cap"])
                self.assertTrue(result["at_most_two_per_scale"])

    def test_partition_example_preserves_open_left_closed_right_convention(self):
        self.assertEqual(dyadic_partition(3, 10),
                         ((3, 4), (4, 8), (8, 10)))

    def test_energy_cauchy_is_exactly_the_block_count_loss(self):
        result = finite_energy_cauchy_receipt([
            (1 + 2j, -3j, 2),
            (-2 + 0.5j, 4, 1j),
            (0.25, -1j, 3 - 2j),
        ])
        self.assertEqual(result["block_count"], 3)
        self.assertTrue(result["inequality_holds"])

    def test_aligned_interval_needs_one_block(self):
        self.assertEqual(dyadic_partition(32, 64), ((32, 64),))


if __name__ == "__main__":
    unittest.main()
