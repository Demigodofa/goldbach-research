"""Exact finite guards; no numerical zero list or prime-correlation claim."""
from fractions import Fraction as F
import unittest

from pointwise_zero_pair_gate import (
    corrected_window_budget, difference_coefficient, quadratic_window,
    sum_coefficient, zero_tail_profile,
)


class PointwiseZeroPairTests(unittest.TestCase):
    def test_sum_and_difference_frequencies_are_not_interchangeable(self):
        coefficients = {1:F(2),2:F(3),3:F(5)}
        self.assertEqual(sum_coefficient(coefficients,4),29)
        self.assertEqual(difference_coefficient(coefficients,4),0)
        self.assertEqual(difference_coefficient(coefficients,0),38)

    def test_exact_square_perturbation_obeys_the_l2_budget(self):
        for shift in range(-3,4):
            source = {j:F(j*j+shift,7) for j in range(1,7)}
            error = {j:F((-1)**j*(j+shift),11) for j in range(0,8)}
            model = {j:source.get(j,F(0))-error.get(j,F(0)) for j in range(0,8)}
            source_norm = sum(v*v for v in source.values())
            error_norm = sum(v*v for v in error.values())
            for target in range(0,15):
                gap = abs(sum_coefficient(source,target)-sum_coefficient(model,target))
                # Equivalent to gap <= 2sqrt(source_norm*error_norm)+error_norm,
                # without rounding a square root or squaring a negative side.
                if gap > error_norm:
                    self.assertLessEqual((gap-error_norm)**2,4*source_norm*error_norm)

    def test_positive_window_normalization_and_unit_resolution(self):
        for h in range(1,10):
            values = {t:quadratic_window(t,h) for t in range(-1,3*h+2)}
            self.assertTrue(all(v>=0 for v in values.values()))
            self.assertEqual(sum(values.values()),1)
            self.assertEqual(sum(t*v for t,v in values.items()),F(3*h,2))
            self.assertEqual(values[0],0)
            self.assertEqual(values[3*h],0)
        self.assertEqual([quadratic_window(t,1) for t in range(4)],
                         [F(0),F(1,2),F(1,2),F(0)])

    def test_unit_window_extracts_two_adjacent_coefficients_not_an_average_claim(self):
        weights = {j:F(j*j%13-4,9) for j in range(1,35)}
        def average(x):
            return sum((w*max(0,x-j)**2/2 for j,w in weights.items()),F(0))
        for n in range(4,30,2):
            x=n+2
            delta=average(x)-3*average(x-1)+3*average(x-2)-average(x-3)
            self.assertEqual(2*delta-weights[n+1],weights[n])
        # A valid size envelope has no automatic derivative saving.
        for x in (10,100,1000):
            e=lambda j: (-1)**j*j*j
            delta=e(x)-3*e(x-1)+3*e(x-2)-e(x-3)
            self.assertEqual(delta,(-1)**x*(8*x*x-24*x+24))
            self.assertGreater(abs(delta),x)

    def test_corrected_source_error_changes_the_window_threshold(self):
        self.assertEqual(corrected_window_budget(F(1,2)),
                         {'relative_x_power':F(1,2),'power_saving':False})
        self.assertEqual(corrected_window_budget(F(2,3)),
                         {'relative_x_power':F(0),'power_saving':False})
        self.assertTrue(corrected_window_budget(F(3,4))['power_saving'])

    def test_zero_height_budget_pays_all_polynomial_and_logarithmic_factors(self):
        for saving in (1,3,10):
            budget=zero_tail_profile(F(saving+5))
            self.assertEqual(budget['n_power'],F(-saving)-F(5,2))
            self.assertEqual(budget['logn_power'],F(5,2))
            self.assertLess(budget['n_power'],-saving)


if __name__ == '__main__':
    unittest.main()
