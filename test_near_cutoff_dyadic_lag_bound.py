import unittest

from near_cutoff_dyadic_lag_bound import dyadic_lag_band_receipt


class NearCutoffDyadicLagBoundTests(unittest.TestCase):
    def test_pairwise_bounds_sum_without_lag_count_loss(self):
        receipt = dyadic_lag_band_receipt(457, 2, 9, 4, 1, 3)
        self.assertLessEqual(
            abs(receipt["exact_signed_active_over_budget"]),
            receipt["proved_absolute_active_over_budget"])
        self.assertTrue(receipt["dyadic_lag_bookkeeping_proved"])
        self.assertFalse(receipt["cross_divisor_bands_proved"])
        self.assertFalse(receipt["d_greater_than_one_proved"])

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            dyadic_lag_band_receipt(451, 2, 9, 4, 1, 3)


if __name__ == "__main__":
    unittest.main()
