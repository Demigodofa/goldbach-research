"""Exact source-normalization and local-transfer guards, not prime estimates."""
from fractions import Fraction as F
import unittest

from prime_producing_comparison_gate import (
    band_normalization, common_scaling_interval, constant_band_error,
    normalized_ray_interval, prime_partner_local_density,
)


class PrimeProducingComparisonTests(unittest.TestCase):
    def test_local_density_is_independent_of_the_large_factor_multiplier(self):
        for target in (60, 202, 330):
            for modulus in (2, 3, 5, 7):
                for multiplier in (11*13, 11*11, 17*19*23):
                    actual, predicted = prime_partner_local_density(target, multiplier, modulus)
                    self.assertEqual(actual, predicted)
        self.assertEqual(prime_partner_local_density(60, 143, 3), (1, 1))
        self.assertEqual(prime_partner_local_density(202, 143, 3), (F(1, 2), F(1, 2)))
        with self.assertRaises(ValueError):
            prime_partner_local_density(60, 15, 3)

    def test_normalized_factor_region_reduces_to_one_interval(self):
        # v=(2,3,t)/(5+t), with v1<=1/4, v3>=1/2, v2>=1/5.
        halfspaces = (((1, 0, 0), F(1, 4)), ((0, 0, -1), F(-1, 2)),
                      ((0, -1, 0), F(-1, 5)))
        interval = normalized_ray_interval((2, 3), (1, 20), halfspaces)
        self.assertEqual(interval, (F(5), F(10)))
        for t in (F(1), F(9, 2), F(5), F(15, 2), F(10), F(21, 2), F(20)):
            vector = (F(2, 5+t), F(3, 5+t), t/(5+t))
            direct = all(sum(c*v for c, v in zip(coefficients, vector)) <= bound
                         for coefficients, bound in halfspaces)
            self.assertEqual(direct, interval[0] <= t <= interval[1])
        self.assertIsNone(normalized_ray_interval((2, 3), (1, 20), (((1, 1, 1), F(1, 2)),)))
        self.assertEqual(normalized_ray_interval((2, 3), (1, 20), (((1, 1, 1), 1),)), (1, 20))

    def test_pointwise_band_normalization_varies_across_the_physical_interval(self):
        a, b = F(2, 5), F(9, 20)
        endpoint, derivative = band_normalization(a, b)
        interior, _ = band_normalization(a, b, F(9, 10))
        self.assertEqual(endpoint, F(27, 22))
        self.assertEqual(derivative, F(-5, 33))
        self.assertGreater(interior, endpoint)
        low, high = constant_band_error(a, b)
        self.assertGreater(low, 0)
        self.assertLessEqual(low, high)
        self.assertLess(high-low, F(1, 10**10))

    def test_logarithmic_rescaling_cannot_satisfy_both_bounded_requirements(self):
        # Algebraic asymptotic-scale fixture, not measured prime counts.
        lower, upper = common_scaling_interval(100, 10, 1, 2)
        self.assertEqual(lower, F(1, 2))
        self.assertEqual(upper, F(2, 45))
        self.assertGreater(lower, upper)
        dividing_by_log = F(1, 100)
        self.assertLessEqual(dividing_by_log, upper)
        self.assertLess(dividing_by_log, lower)

    def test_safe_counterexample_geometry_has_no_allowed_type_two_divisor(self):
        gamma, theta, width = F(49, 100), F(1, 100), F(1, 3)-F(2, 100)
        a, b = F(491, 1000), F(499, 1000)
        self.assertLess(theta+width, gamma)
        self.assertTrue(gamma < a < b < F(1, 2))
        for alpha in (a, (a+b)/2, b):
            # Supported semiprime exponents alpha,1-alpha at total scale1.
            self.assertTrue(all(not theta <= d <= theta+width for d in (alpha, 1-alpha)))
            self.assertTrue(all(d > gamma for d in (alpha, 1-alpha)))
        with self.assertRaises(ValueError):
            band_normalization(F(2, 5), F(1, 2))
        with self.assertRaises(ValueError):
            common_scaling_interval(1, 2, 1, 2)


if __name__ == '__main__':
    unittest.main()
