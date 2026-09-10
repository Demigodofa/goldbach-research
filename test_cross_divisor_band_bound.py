import unittest

from cross_divisor_band_bound import row_cross_divisor_band_bound


class CrossDivisorBandBoundTests(unittest.TestCase):
    def test_rectangular_bound_dominates_exact_cross_operator(self):
        receipt = row_cross_divisor_band_bound(
            1009, 5, 9, 12, 8, 16, compare_exact=True)
        self.assertLessEqual(
            receipt["exact_cross_band_operator_norm"],
            receipt["proved_cross_band_active_frame_operator_bound"])
        self.assertTrue(receipt["cross_band_active_frame_bound_proved"])
        self.assertFalse(receipt["all_lower_bands_assembled"])

    def test_bound_is_invariant_under_transpose(self):
        forward = row_cross_divisor_band_bound(1009, 5, 9, 12, 8, 16)
        reverse = row_cross_divisor_band_bound(1009, 5, 12, 9, 16, 8)
        self.assertAlmostEqual(
            forward["proved_cross_band_active_frame_operator_bound"],
            reverse["proved_cross_band_active_frame_operator_bound"],
            places=10)

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            row_cross_divisor_band_bound(1001, 5, 9, 12, 8, 16)


if __name__ == "__main__":
    unittest.main()
