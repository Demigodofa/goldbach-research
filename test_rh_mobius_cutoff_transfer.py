import unittest
from fractions import Fraction as F

from complementary_divisor_correlation import frozen_mobius_log_vector
from major_arc_kernel import _factorization
from rh_mobius_cutoff_transfer import (
    bulk_residual_numerator, cutoff_log_coefficients,
    far_tail_log_squared_cap, harmonic_coefficient,
    prefix_residual_numerator, residual_numerator,
)
from unexceptional_vaughan_gate import _add, _clean


class RhMobiusCutoffTransferTests(unittest.TestCase):
    def test_coefficients_reconstruct_existing_goldbach_cutoff(self):
        for r in (2, 3, 6, 12):
            coeffs = cutoff_log_coefficients(r)
            self.assertNotIn(r, coeffs)
            self.assertNotIn(4, coeffs)
            for m in range(1, 3*r):
                total = {}
                for d, vector in coeffs.items():
                    if m % d == 0:
                        _add(total, vector)
                self.assertEqual(_clean(total),
                                 frozen_mobius_log_vector(m, r, upper=r))

    def test_fractional_and_prefix_identity_across_all_ranges(self):
        for r in (2, 7, 12):
            for y in (F(1, 3), F(1), F(7, 6), F(r),
                      F(2*r+1, 2), F(r*r+1, 3)):
                self.assertEqual(residual_numerator(r, y),
                                 prefix_residual_numerator(r, y))

    def test_bulk_identity_including_proper_prime_powers(self):
        for r in (3, 8, 12):
            for twice_y in range(3, 2*r+1):
                y = F(twice_y, 2)
                self.assertEqual(residual_numerator(r, y),
                                 bulk_residual_numerator(r, y))

    def test_chebyshev_bulk_has_the_prime_power_jump(self):
        r = 10
        difference = {}
        _add(difference, bulk_residual_numerator(r, F(4)))
        _add(difference, bulk_residual_numerator(r, F(7, 2)), -1)
        _add(difference, harmonic_coefficient(r), F(-1, 2))
        self.assertEqual(_clean(difference), ((2, -1),))

    def test_low_range_and_strict_indicator_endpoint(self):
        r = 6
        expected = {}
        _add(expected, harmonic_coefficient(r), F(1, 2))
        self.assertEqual(residual_numerator(r, F(1, 2)), _clean(expected))
        endpoint = {}
        _add(endpoint, harmonic_coefficient(r))
        _add(endpoint, _factorization(r), -1)
        self.assertEqual(residual_numerator(r, 1), _clean(endpoint))
        with self.assertRaises(ValueError):
            bulk_residual_numerator(r, 1)

    def test_tail_bound_retains_normalization(self):
        for r in (2, 5, 12):
            self.assertEqual(far_tail_log_squared_cap(r, r**3), F(4, r))
            self.assertEqual(far_tail_log_squared_cap(r, 2*r**3), F(2, r))

    def test_invalid_inputs_and_ranges(self):
        for r in (True, 1, 2.0):
            with self.assertRaises(ValueError):
                cutoff_log_coefficients(r)
        for y in (True, 0, -1, 1.5):
            with self.assertRaises(ValueError):
                residual_numerator(6, y)
        with self.assertRaises(ValueError):
            bulk_residual_numerator(6, 7)
        with self.assertRaises(ValueError):
            far_tail_log_squared_cap(6, 5)


if __name__ == '__main__':
    unittest.main()
