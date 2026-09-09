"""Finite algebra guards, not numerical evidence for an exceptional zero."""
from fractions import Fraction as F
from math import gcd
import unittest

from rare_divisor_calibration import (
    conductor_coefficients, euler_calibration, lambda_w_identity,
    signed_calibration, weighted_abel_identity,
)


class RareDivisorCalibrationTests(unittest.TestCase):
    def test_four_orientations_retain_logarithmic_sign_and_factor(self):
        witnessed_negative_small_factor = False
        for D, m, sign in ((31, 62, 1), (33, 22, 1), (40, 20, 1),
                           (40, 40, -1), (120, 20, 1)):
            for a, c in ((1, 1), (7, 11), (11, 7), (13, 17)):
                if gcd(a*c, D) != 1:
                    continue
                (A, B, C), direct, predicted = conductor_coefficients(D, m, a, c, two_sign=sign)
                self.assertEqual((B, C), (0, -A))
                self.assertEqual(direct, predicted)
                self.assertEqual(direct[1], -2*direct[0])
                witnessed_negative_small_factor |= direct[0] < 0
        self.assertTrue(witnessed_negative_small_factor)

    def test_unsuppressed_control_does_not_drop_mixed_residues(self):
        mixed_nonzero = False
        for m in (2, 4, 6, 8):
            (A, B, C), direct, predicted = conductor_coefficients(31, m, 7, 11)
            self.assertEqual(direct, predicted)
            self.assertNotEqual(C, -A)
            mixed_nonzero |= B != 0
        self.assertTrue(mixed_nonzero)

    def test_exact_euler_ratio_restores_two_and_three_conductor_factors(self):
        for D, m, sign in ((31, 62, 1), (33, 22, 1), (40, 20, 1),
                           (40, 40, -1), (120, 20, 1)):
            actual, predicted = euler_calibration(D, m, D+20, two_sign=sign)
            self.assertEqual(actual, predicted)
            self.assertGreater(actual, 0)

    def test_weighted_abel_factor_two_and_empty_factor_atom(self):
        for root, cutoff, D in ((20, 3, 31), (30, 7, 33), (25, 11, 31)):
            direct, abel = weighted_abel_identity(root, cutoff, D)
            self.assertEqual(direct, abel)
            self.assertTrue(direct)
        direct, abel = weighted_abel_identity(20, 100, 31)
        self.assertEqual(direct, ((2, F(4)), (5, F(2))))  # exactly 2 log(20)
        self.assertEqual(direct, abel)

    def test_positive_character_log_identity_and_negative_side_guard(self):
        for n in (1, 5, 19, 95, 3*11, 3**2*5):
            sign, lam, twice_w, lam_log = lambda_w_identity(n, 31)
            self.assertEqual(sign, 1)
            self.assertEqual(twice_w, lam_log)
            self.assertGreaterEqual(lam, 0)
        sign, lam, twice_w, lam_log = lambda_w_identity(3, 31)
        self.assertEqual((sign, lam, lam_log), (-1, 0, ()))
        self.assertEqual(twice_w, ((3, F(2)),))

    def test_signed_harmonic_integral_cannot_bound_the_replacement_error(self):
        q0, s0, ratio, residual, bound = signed_calibration(
            (F(1), F(1)), (F(1), F(-1)), (F(5), F(3)),
            F(1, 3), F(1, 2), F(1, 5), F(2))
        self.assertEqual(q0, 0)
        self.assertEqual(ratio, F(4, 5))
        self.assertEqual(s0, F(1, 15))
        self.assertEqual(residual, bound)
        self.assertGreater(residual, 0)

    def test_input_scope_rejects_invalid_exact_normalizations(self):
        for a, c in ((0, 1), (2, 2), (31, 1), (True, 1)):
            with self.assertRaises(ValueError):
                conductor_coefficients(31, 62, a, c)
        for D, m, cutoff in ((31, 62, 31), (31, 63, 50), (31, 0, 50)):
            with self.assertRaises(ValueError):
                euler_calibration(D, m, cutoff)
        with self.assertRaises(ValueError):
            signed_calibration((F(1),), (F(1),), (F(2),), F(1), F(0), F(1), F(1))


if __name__ == '__main__':
    unittest.main()
