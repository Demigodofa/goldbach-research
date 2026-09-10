import math
import unittest

from row_periodic_crt_cancellation import (
    complete_row_period_receipt,
    endpoint_error_fourier_reconstruction,
    same_row_crt_count_error,
    worst_incomplete_row_block,
)


class RowPeriodicCrtCancellationTests(unittest.TestCase):
    def test_exact_crt_count_matches_direct_pairs(self):
        modulus = 71
        for ell in range(5):
            for left, right in ((5, 7), (6, 10), (10, 14)):
                for separation in (-17, -1, 0, 8, 19):
                    receipt = same_row_crt_count_error(
                        modulus, ell, left, right, separation)
                    direct = sum(
                        (modulus * ell + x) % left == 0
                        and (modulus * ell + y) % right == 0
                        for x in range(1, modulus)
                        for y in range(1, modulus)
                        if x - y == separation)
                    self.assertEqual(receipt["count"], direct)

    def test_every_start_has_zero_complete_period_sum(self):
        for left, right, separation in (
                (5, 7, 17), (6, 10, 8), (10, 14, 19)):
            for ell_first in (0, 1, 11, 37):
                receipt = complete_row_period_receipt(
                    71, ell_first, left, right, separation)
                self.assertAlmostEqual(receipt["error_sum"], 0, places=11)
                self.assertTrue(
                    receipt["complete_period_cancellation_proved"])

    def test_fourier_reconstruction_has_zero_constant_term(self):
        receipt = endpoint_error_fourier_reconstruction(71, 5, 7, 17)
        self.assertAlmostEqual(receipt["mean_error"], 0, places=12)
        self.assertLess(receipt["maximum_reconstruction_error"], 1e-12)
        self.assertGreater(
            receipt["largest_nonzero_fourier_coefficient"], 0)

    def test_fourier_helper_rejects_nonpermuting_rotation(self):
        with self.assertRaisesRegex(ValueError, "coprime"):
            endpoint_error_fourier_reconstruction(15, 3, 5, 0)

    def test_resonant_incomplete_block_retains_constant_fraction(self):
        # Here 71 == 1 (mod lcm(5,7)), so the row rotation advances one
        # residue at a time.  Periodicity alone cannot give A^(-delta).
        receipt = worst_incomplete_row_block(71, 5, 7, 17, 8)
        self.assertGreater(receipt["absolute_sum_over_row_count"], .4)
        self.assertFalse(receipt["incomplete_period_power_saving_proved"])

    def test_incompatible_separation_has_zero_error(self):
        receipt = same_row_crt_count_error(71, 3, 6, 10, 7)
        self.assertFalse(receipt["compatible"])
        self.assertEqual(receipt["error"], 0)


if __name__ == "__main__":
    unittest.main()
