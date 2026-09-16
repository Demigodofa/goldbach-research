"""Exact periodic/window distinctions; no asymptotic inference from tests."""

import unittest
from fractions import Fraction as F
from math import gcd, lcm

from complementary_divisor_correlation import (
    central_interval, complementary_expansion, divisor_value,
)
from cutoff_normalized_remainder import (
    cutoff_log_vectors, ramanujan_density_channels, selberg_coordinates,
)
from major_arc_kernel import _factorization, _mobius_phi, ramanujan


class ResidualPeriodicKernelTests(unittest.TestCase):
    def test_ramanujan_divisor_indicator_including_prime_powers(self):
        for d in (1, 2, 4, 6, 9, 12, 15):
            for n in (0, 1, 6, 12, 25, 34):
                self.assertEqual(sum(ramanujan(q, n) for q in range(1, d + 1)
                                     if d % q == 0), d if n % d == 0 else 0)

    def test_reflected_orthogonality_over_complete_common_period(self):
        target = 34
        for q, r in ((1, 1), (6, 6), (15, 15), (4, 4), (4, 9), (6, 10)):
            period = lcm(q, r)
            actual = F(sum(ramanujan(q, n) * ramanujan(r, target - n)
                           for n in range(1, period + 1)), period)
            self.assertEqual(actual, ramanujan(q, target) if q == r else 0)

    def test_signed_spectrum_matches_crt_density_with_nonsquarefree_support(self):
        coefficients = {1: 2, 2: -1, 4: F(3, 2), 6: -2, 9: F(1, 3)}
        for target in (30, 34, 50):
            channels = ramanujan_density_channels(target, coefficients)
            self.assertEqual(sum(channels.values(), F(0)),
                             complementary_expansion(target, coefficients).density)
            self.assertLessEqual(abs(sum(channels.values(), F(0))),
                                 sum(map(abs, channels.values()), F(0)))
        self.assertTrue(any(v < 0 for v in ramanujan_density_channels(34, coefficients).values()))

    def test_full_long_divisor_expansion_matches_actual_residual(self):
        # Linear log-prime substitution checks exact algebra, not real log bounds.
        def log_value(n):
            return sum(p * exponent for p, exponent in _factorization(n))

        target, cutoff = 50, 7
        interval = central_interval(target)
        upper = interval.stop - 1
        coefficients = {d: _mobius_phi(d)[0] * (log_value(cutoff) - log_value(d))
                        for d in range(cutoff + 1, upper + 1)}
        coordinates = selberg_coordinates(coefficients)
        self.assertTrue(all(_mobius_phi(q)[0] != 0 for q in coordinates))
        for n in interval:
            expected = sum(p * power for p, power in cutoff_log_vectors(n, cutoff)[1])
            self.assertEqual(divisor_value(n, coefficients), expected)
            self.assertEqual(sum(value * ramanujan(q, n)
                                 for q, value in coordinates.items()), expected)

    def test_crt_and_incomplete_ramanujan_discrepancies_are_identical(self):
        target = 34
        coefficients = {1: 2, 3: -3, 5: -5, 15: 15}
        coordinates = selberg_coordinates(coefficients)
        expansion = complementary_expansion(target, coefficients)
        interval = central_interval(target)
        spectral_error = F(0)
        for q, left in coordinates.items():
            for r, right in coordinates.items():
                raw = sum(ramanujan(q, n) * ramanujan(r, target - n)
                          for n in interval)
                average = F(target, 3) * ramanujan(q, target) if q == r else F(0)
                spectral_error += left * right * (raw - average)
        self.assertEqual(spectral_error, expansion.discrepancy)
        self.assertEqual(expansion.correlation,
                         F(target, 3) * expansion.density + spectral_error)

    def test_positive_periodic_density_does_not_transfer_to_finite_window(self):
        # This is c_15(n), not the actual Goldbach residual D(n).
        coefficients = {1: 1, 3: -3, 5: -5, 15: 15}
        target = 34
        self.assertEqual(selberg_coordinates(coefficients), {15: F(1)})
        self.assertEqual(ramanujan_density_channels(target, coefficients), {15: F(1)})
        expansion = complementary_expansion(target, coefficients)
        self.assertEqual(expansion.correlation, -3)
        self.assertEqual(expansion.discrepancy, F(-43, 3))
        self.assertEqual(sum(ramanujan(15, n) * ramanujan(15, target - n)
                             for n in central_interval(target)), -3)

    def test_gcd_tail_grouping_keeps_divisors_larger_than_split(self):
        target, split, limit = 60, 7, 120
        direct = sum((F(gcd(q, target), q * q)
                      for q in range(split + 1, limit + 1)), F(0))
        grouped = sum((F(_mobius_phi(g)[1], g * g)
                       * sum((F(1, h * h)
                              for h in range(split // g + 1, limit // g + 1)), F(0))
                       for g in range(1, target + 1) if target % g == 0), F(0))
        self.assertEqual(direct, grouped)
        tau = sum(target % g == 0 for g in range(1, target + 1))
        self.assertLessEqual(direct, F(2 * tau, split))

    def test_validation_and_zero_coordinates(self):
        self.assertEqual(ramanujan_density_channels(34, {}), {})
        with self.assertRaises(ValueError):
            ramanujan_density_channels(33, {1: 1})
        with self.assertRaises(ValueError):
            ramanujan_density_channels(34, {0: 1})
        with self.assertRaises(ValueError):
            ramanujan_density_channels(34, {1: 0.5})


if __name__ == "__main__":
    unittest.main()
