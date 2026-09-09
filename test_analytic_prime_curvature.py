"""Guards for actual phase budgets and masks, not numerical prime evidence."""
from fractions import Fraction as F
from math import cos, log, sin
import unittest

from analytic_prime_curvature import (
    phase_difference_curvature, sine_curvatures, type_i_budget, type_ii_budget,
)


class AnalyticPrimeCurvatureTests(unittest.TestCase):
    def test_type_i_pays_the_full_product_of_cutoffs(self):
        self.assertEqual(type_i_budget(), (F(17,20),F(11,20)))
        self.assertGreater(type_i_budget()[0], F(1,5)+F(9,20))

    def test_oriented_type_ii_budget_has_the_claimed_worst_exponent(self):
        for j in range(61):
            k = F(1,5)+F(j,200)
            budget = type_ii_budget(k)
            self.assertLessEqual(max(budget.values()), F(39,40))
            self.assertLess(max(budget.values()), F(79,80))
        self.assertEqual(type_ii_budget(F(1,5))['diagonal'], F(9,10))
        self.assertEqual(type_ii_budget(F(1,2))['curvature'], F(39,40))
        self.assertEqual(type_ii_budget(F(1,2))['inverse_curvature'], F(31,40))
        self.assertEqual(F(79,80)-F(39,40), F(1,80))

    def test_both_sine_curvatures_are_needed_and_nonzero_on_the_fixed_interval(self):
        a, b = 0.55, 0.70
        for j in range(31):
            u = a+(b-a)*j/30
            second, dilation = sine_curvatures(u)
            self.assertLessEqual(second, -sin(a-0.5)+1e-14)
            self.assertLessEqual(dilation, -a*a*cos(b-0.5)+1e-14)
        self.assertEqual(sine_curvatures(0.5)[0], 0)
        self.assertNotEqual(sine_curvatures(0.5)[1], 0)

    def test_differenced_curvature_matches_the_exact_dilation_identity(self):
        n_scale, t_scale, k, r = 10000, 200.0, 80, 76
        for m in (74,76,78,80,82,84):
            x, y = m*k/n_scale, m*r/n_scale
            gdiff = -x*x*sin(x-0.5)+y*y*sin(y-0.5)
            direct = phase_difference_curvature(m,k,r,n_scale,t_scale)
            self.assertAlmostEqual(direct, -t_scale*gdiff/(m*m), places=15)
            self.assertGreater(direct, 0)
            self.assertAlmostEqual(direct,
                -phase_difference_curvature(m,r,k,n_scale,t_scale), places=15)
            self.assertEqual(phase_difference_curvature(m,k,k,n_scale,t_scale), 0)

    def test_product_support_requires_the_intersection_for_both_factors(self):
        a,b,n_scale,k,r = F(11,20),F(7,10),10000,80,76
        left = {m for m in range(65,96) if a <= F(m*k,n_scale) <= b}
        right = {m for m in range(65,96) if a <= F(m*r,n_scale) <= b}
        both = left & right
        self.assertEqual(both, set(range(73,88)))
        self.assertNotEqual(both,left)
        self.assertNotEqual(both,right)
        for m in both:
            self.assertGreater(phase_difference_curvature(m,k,r,n_scale,200.0), 0)

    def test_log_phase_is_a_real_degeneracy_of_the_second_condition(self):
        # Nonzero log curvature alone cannot license the Type II step.
        for u in (F(1,2),F(3,5),F(7,10)):
            second = -1/(u*u)
            third = 2/(u*u*u)
            self.assertNotEqual(second,0)
            self.assertEqual(2*u*second+u*u*third,0)
        self.assertNotAlmostEqual(log(0.3)+log(0.7),2*log(0.5))

    def test_invalid_factor_ranges_do_not_silently_reverse_cauchy_orientation(self):
        for k in (F(1,10),F(3,5),0.25,1):
            with self.assertRaises(ValueError):
                type_ii_budget(k)


if __name__ == '__main__':
    unittest.main()
