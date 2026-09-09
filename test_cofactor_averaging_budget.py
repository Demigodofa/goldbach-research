"""Exact scaling checks; no prime or oscillatory-sum measurement."""
from fractions import Fraction as F
import unittest

from cofactor_averaging_budget import bc_budget, worst_bc_budget


class CofactorAveragingBudgetTests(unittest.TestCase):
    def test_critical_boxes_norms_and_poisson_normalization(self):
        budget = worst_bc_budget(F(1, 5))
        self.assertEqual((budget.inverse_variable, budget.denominator, budget.frequency),
                         (F(3, 5), F(1, 2), F(1, 10)))
        self.assertEqual((budget.prefactor, budget.norm_product, budget.phase_factor),
                         (-F(1, 10), F(3, 5), 0))
        self.assertEqual((budget.first, budget.second), (F(107, 100), F(83, 80)))
        endpoint = worst_bc_budget(F(13, 25))
        self.assertEqual((endpoint.first, endpoint.second), (F(611, 500), F(479, 400)))

    def test_independent_affine_formulas_and_monotonicity_on_rational_boxes(self):
        checked = 0
        for b in (F(0), F(1, 19), F(1, 8), F(1, 5), F(1, 3), F(13, 25)):
            corner = worst_bc_budget(b)
            self.assertEqual(corner.first, F(39, 40)+F(19, 40)*b)
            self.assertEqual(corner.second, F(15, 16)+b/2)
            for i in range(21):
                x = (1-b)*F(i, 40)
                for j in range(21):
                    y = F(j, 40)
                    if b+x+y < 1:
                        continue
                    v = bc_budget(b, x, y)
                    r, s = b+x, y
                    self.assertEqual(v.first, F(3, 20)+F(7, 10)*(r+s)+max(r, s)/4)
                    self.assertEqual(v.second, F(7, 8)*(r+s)+max(r, s)/8)
                    self.assertEqual(v.phase_factor, 0)
                    self.assertLessEqual(v.first, corner.first)
                    self.assertLessEqual(v.second, corner.second)
                    checked += 1
        self.assertGreater(checked, 40)

    def test_both_source_terms_and_fixed_frequency_variant(self):
        self.assertEqual(worst_bc_budget(F(1, 19)).first, 1)
        self.assertEqual(worst_bc_budget(F(1, 8)).second, 1)
        # Choosing only the smaller source term would give a false window.
        between = worst_bc_budget(F(1, 10))
        self.assertGreater(between.first, 1)
        self.assertLess(between.second, 1)
        for b in (F(1, 5), F(1, 3), F(13, 25)):
            value = worst_bc_budget(b)
            # Independent fixed-frequency substitution: norm sqrt(R*C),
            # numerator length1, and a final count K of individual sums.
            r, s, k = value.inverse_variable, value.denominator, value.frequency
            first = 1-r-s+(r+s)/2+F(7, 20)*(r+s)+max(r, s)/4+k
            second = 1-r-s+(r+s)/2+F(3, 8)*(r+s)+max(r, s)/8+k
            self.assertEqual(value.fixed_frequency_first, first)
            self.assertEqual(value.second, second)
            self.assertGreater(value.fixed_frequency_first, value.first)

    def test_support_and_exact_input_guards(self):
        for bad in (True, 0.2, "1/5"):
            with self.assertRaises(ValueError):
                worst_bc_budget(bad)
        for bad in (-1, F(3, 5)):
            with self.assertRaises(ValueError):
                worst_bc_budget(bad)
        with self.assertRaises(ValueError):
            bc_budget(F(1, 5), F(1, 2), F(1, 2))
        with self.assertRaises(ValueError):
            bc_budget(F(1, 5), F(1, 10), F(1, 10))


if __name__ == "__main__":
    unittest.main()
