import unittest
from fractions import Fraction as F

from shift_bandpass_target import (additive_frequency_exponent,
                                   angular_band_excludes_zero,
                                   square_root_shift_budget,
                                   target_receipt)


class ShiftBandpassTargetTests(unittest.TestCase):
    def test_actual_top_frequency_scale(self):
        self.assertEqual(additive_frequency_exponent(), F(499, 1000))

    def test_conditional_square_root_gain_would_barely_close(self):
        self.assertEqual(square_root_shift_budget(), F(-1, 1000))

    def test_zero_frequency_is_excluded_by_actual_cutoff_support(self):
        self.assertTrue(angular_band_excludes_zero())
        with self.assertRaises(ValueError):
            angular_band_excludes_zero(F(0), F(2))

    def test_receipt_does_not_promote_conditional_gain(self):
        result = target_receipt()
        self.assertFalse(result["saving_proved"])
        self.assertFalse(result["hard_truncation_leakage_paid"])
        self.assertIn("arbitrary discrepancy", result["generic_obstruction"])


if __name__ == "__main__":
    unittest.main()
