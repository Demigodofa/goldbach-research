import unittest
from fractions import Fraction as F

from mobius_aligned_band_gate import (aligned_parseval_budget,
                                      aligned_phase_receipt)


class MobiusAlignedBandGateTests(unittest.TestCase):
    def test_both_kernel_phases_remove_the_long_index(self):
        for d, m in ((1, 5), (2, 5), (3, 7), (5, 11)):
            for h in range(-4, 5):
                for ell in range(-3, 4):
                    for shift in range(-2, 3):
                        for reflected in (False, True):
                            result = aligned_phase_receipt(
                                d, m, h, ell, shift, target=38,
                                reflected=reflected)
                            self.assertTrue(result["long_index_removed"])
                            self.assertEqual(result["full_numerator"],
                                             result["collapsed_full_numerator"])
                            self.assertEqual(result["low_numerator"],
                                             result["collapsed_low_numerator"])

    def test_parseval_collision_has_the_same_long_block_threshold(self):
        edge = aligned_parseval_budget(F(1499, 2000))
        self.assertEqual(edge["collision_exponent"], F(1499, 1000))
        self.assertTrue(edge["fits_target_by_parseval"])
        above = aligned_parseval_budget(F(3, 4))
        self.assertFalse(above["fits_target_by_parseval"])
        self.assertTrue(above["arithmetic_progression_estimate_needed"])
        self.assertFalse(above["alignment_removes_collision"])


if __name__ == "__main__":
    unittest.main()
