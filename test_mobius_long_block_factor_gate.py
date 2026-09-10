import unittest
from fractions import Fraction as F

from mobius_long_block_factor_gate import long_block_factor_budget


class MobiusLongBlockFactorGateTests(unittest.TestCase):
    def test_all_three_regimes_keep_the_fatal_collision(self):
        y = F(3, 4)
        lower = long_block_factor_budget(y, F(1, 5))
        balanced = long_block_factor_budget(y, F(1, 2))
        upper = long_block_factor_budget(y, F(9, 10))
        self.assertEqual(lower["regime"], "lower")
        self.assertEqual(balanced["regime"], "balanced")
        self.assertEqual(upper["regime"], "upper")
        for result in (lower, balanced, upper):
            self.assertEqual(result["collision_exponent"], F(3, 2))
            self.assertTrue(result["shorter_factor_below_block_length"])
            self.assertFalse(result["collision_fits"])
            self.assertFalse(result["factor_by_factor_route_proves_block"])

    def test_extreme_upper_factor_pays_family_but_not_collision(self):
        result = long_block_factor_budget(F(4, 5), F(9, 10))
        self.assertEqual(result["shorter_factor"], F(1, 10))
        self.assertEqual(result["short_factor_cap"], F(1, 10))
        self.assertEqual(result["best_family_exponent"], result["target"])
        self.assertTrue(result["best_family_fits"])
        self.assertFalse(result["collision_fits"])

    def test_balanced_box_misses_both_terms(self):
        result = long_block_factor_budget(F(4, 5), F(1, 2))
        self.assertEqual(result["best_family_exponent"], F(1899, 1000))
        self.assertFalse(result["best_family_fits"])
        self.assertFalse(result["factor_by_factor_route_proves_block"])

    def test_threshold_cap_is_just_above_tail_cutoff(self):
        result = long_block_factor_budget(F(3, 4), F(17, 20))
        self.assertEqual(result["short_factor_cap"], F(3, 20))
        self.assertEqual(result["shorter_factor"], F(3, 20))
        self.assertTrue(result["best_family_fits"])
        self.assertFalse(result["collision_fits"])


if __name__ == "__main__":
    unittest.main()
