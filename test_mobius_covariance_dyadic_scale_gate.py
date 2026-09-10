import unittest
from fractions import Fraction as F

from mobius_covariance_dyadic_scale_gate import (
    dyadic_scale_budget,
    finite_parseval_collision_receipt,
)


class MobiusCovarianceDyadicScaleGateTests(unittest.TestCase):
    def test_exact_scale_threshold(self):
        result = dyadic_scale_budget()
        self.assertEqual(result["divisor_family"], F(599, 1000))
        self.assertEqual(result["target"], F(1499, 1000))
        self.assertEqual(result["paid_length_threshold"], F(1499, 2000))
        self.assertEqual(result["collision_at_threshold"], result["target"])
        self.assertEqual(result["family_at_threshold"], F(2697, 2000))
        self.assertEqual(result["family_margin_at_threshold"], F(301, 2000))
        self.assertTrue(result["long_blocks_require_arithmetic_input"])
        self.assertTrue(result["short_blocks_paid_uniformly_in_location"])

    def test_full_continued_kernel_obeys_collision_bound(self):
        result = finite_parseval_collision_receipt(
            2, 5, 0, 24,
            {1: 2 - 1j, 3: -0.5, 7: 3j, 9: 1.25, 11: -2j,
             13: 0.75, 17: -1 + 0.5j, 19: 2.5, 21: -0.25j, 23: 1},
        )
        self.assertTrue(result["bound_holds"])
        self.assertLessEqual(result["additive_energy"],
                             (result["length"] + result["modulus"])
                             * result["square_mass"] + 1e-9)

    def test_d_equals_one_low_term_is_retained(self):
        result = finite_parseval_collision_receipt(
            1, 7, 10, 22, {11: 1, 12: -2j, 13: 0.5, 15: -1, 20: 3j}
        )
        self.assertGreater(result["low_energy"], 0)
        self.assertTrue(result["bound_holds"])


if __name__ == "__main__":
    unittest.main()
