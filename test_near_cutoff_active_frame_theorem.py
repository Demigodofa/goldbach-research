import unittest

from near_cutoff_active_frame_theorem import (
    row_near_cutoff_active_frame_bound,
)


class NearCutoffActiveFrameTheoremTests(unittest.TestCase):
    def test_combined_bound_dominates_exact_centered_active_gram(self):
        receipt = row_near_cutoff_active_frame_bound(
            1009, 5, 9, 8, compare_exact=True)
        self.assertLessEqual(
            receipt["exact_active_frame_schur_row_sum"],
            receipt["proved_exact_centered_active_schur_bound"])
        self.assertTrue(receipt["same_complete_row_active_frame_theorem"])
        self.assertTrue(receipt["asymptotic_same_row_active_full_theorem"])
        self.assertFalse(receipt["shifted_rows_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_composite_modulus_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            row_near_cutoff_active_frame_bound(1001, 5, 9, 8)


if __name__ == "__main__":
    unittest.main()
