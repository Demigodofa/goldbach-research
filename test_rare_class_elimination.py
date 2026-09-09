"""Exact coverage and remaining-gap guards; no finite zero or density claim."""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, prod
import unittest

from rare_class_elimination import affine_range_certificate, factor_share_kernel
from character_partner_weight import negative_hyperbola_terms, negative_log_coefficients
from exceptional_character_model import character_values
from quintic_partner_weight import quintic_formal_weight
from rare_prime_sieve import suppressed_residue_split
from redistribution import trial_prime


class RareClassEliminationTests(unittest.TestCase):
    def test_actual_finite_even_classes_meet_every_algebraic_support_condition(self):
        # Three frozen fixtures, not a prime-coverage scan or actual-zero data.
        cases = (
            (2304, 1823, 2021, 47, (43,)),
            (262144, 215051, 215787, 503, (3, 11, 13)),
            (5*2**32, 16774402709, 16774403217, 100003, (3, 11, 13, 17, 23)),
        )
        chi = character_values(31)
        for Y, p, n, q, negatives in cases:
            with self.subTest(factor_count=len(negatives)+1):
                self.assertTrue(all(trial_prime(r) for r in (p, q, *negatives)))
                self.assertEqual(len(set((q, *negatives))), len(negatives)+1)
                self.assertEqual((chi[p % 31], chi[q % 31], chi[n % 31]), (1, 1, -1))
                self.assertTrue(all(chi[r % 31] == -1 for r in negatives))
                m = p+n
                _, positive_classes, negative_classes = suppressed_residue_split(31, m)
                self.assertIn(p % 31, positive_classes)
                self.assertIn(n % 31, negative_classes)
                M = affine_range_certificate(Y, p, n, q, F(1, 100))
                self.assertEqual(M, prod(negatives))
                self.assertEqual(gcd(M, 31*m), 1)
                self.assertEqual(chi[M % 31], -1)
                self.assertTrue(all(r > 2 for r in negatives))
                self.assertLess(Y, 2*M*q)
                self.assertLessEqual(M*q, Y)
                self.assertLess(M**25, Y**13)

    def test_floor_endpoint_cannot_be_replaced_by_the_wrong_reciprocal_chain(self):
        Y = 2**25
        R = 2**12  # Exactly Y^(12/25).
        q = R+1
        M = Y//q
        n = M*q
        self.assertEqual(affine_range_certificate(Y, 3*Y//4, n, q, F(1, 100)), M)
        self.assertLess(M, 2**13)
        # At the excluded equality q=R the claimed STRICT cofactor bound fails.
        with self.assertRaises(ValueError):
            affine_range_certificate(Y, 3*Y//4, Y, R, F(1, 100))
        nonintegral_Y = Y+1
        self.assertLess(R**25, nonintegral_Y**12)
        self.assertLess(nonintegral_Y**12, (R+1)**25)
        self.assertGreater(F(nonintegral_Y, R)**25, nonintegral_Y**13)

    def test_prime_atom_and_wrong_first_interval_are_not_composite_transfers(self):
        with self.assertRaises(ValueError):
            affine_range_certificate(2304, 1823, 2021, 2021, F(1, 100))
        with self.assertRaises(ValueError):
            affine_range_certificate(2304, 1152, 2021, 47, F(1, 100))
        with self.assertRaises(ValueError):
            affine_range_certificate(2304, 1823, 2021, 43, F(1, 10))

    def test_general_finite_difference_reproduces_remaining_quintic_classes(self):
        kappa = F(7, 3)
        coefficients = (0, 1, -kappa, 4*kappa, -5*kappa, 2*kappa)
        for negative_count, positive_count in ((1, 0), (1, 1), (3, 0), (3, 1),
                                                (5, 0), (5, 1), (7, 0), (7, 1)):
            count = negative_count+positive_count
            shares = tuple(F(i, count*(count+1)//2) for i in range(1, count+1))
            negative, positive = shares[:negative_count], shares[negative_count:]
            result = factor_share_kernel(coefficients, negative, positive)
            self.assertEqual(result, quintic_formal_weight(kappa, negative, positive))
            if negative_count > 5:
                self.assertEqual(result, 0)
        self.assertLess(factor_share_kernel(coefficients, (F(1, 3),)*3), 0)
        self.assertGreater(factor_share_kernel(coefficients, (F(9, 10), F(1, 25), F(3, 50))), 0)
        self.assertGreater(factor_share_kernel(coefficients, (F(1, 5),)*5), 0)

    def test_every_normalized_quadratic_has_the_same_squarefree_W_kernel(self):
        for quadratic in (F(-100), F(0), F(1, 3), F(100)):
            coefficients = (0, 1-quadratic, quadratic)
            for k, h in ((1, 0), (1, 1), (1, 4), (3, 0), (3, 2), (5, 0)):
                shares = tuple(F(i, (k+h)*(k+h+1)//2) for i in range(1, k+h+1))
                result = factor_share_kernel(coefficients, shares[:k], shares[k:])
                self.assertEqual(result, 2**h*shares[0] if k == 1 else 0)
        for n in (3*11*13, 3*11*13*17*23):
            self.assertEqual(negative_log_coefficients(n, 31), ())

    def test_new_negligible_error_does_not_turn_truncation_into_a_lower_bound(self):
        n, R = 3*11*29, 26
        self.assertLessEqual(R**25, n**12)
        self.assertLess(n**12, (R+1)**25)
        low, boundary = defaultdict(int), defaultdict(int)
        for d, sign in negative_hyperbola_terms(n, 31):
            result = low if d <= R else boundary
            for prime in (3, 11, 29):
                result[prime] += sign*(1-2*int(d % prime == 0))
        self.assertEqual(dict(low), {3: 1, 11: 1, 29: -1})
        self.assertEqual(dict(boundary), {3: -1, 11: -1, 29: 1})
        self.assertEqual(negative_log_coefficients(n, 31), ())
        self.assertGreater(F(3*11, 29), 1)  # T_low=log(33/29)>W(n)=0.

    def test_terminal_semiprime_error_maps_with_both_strict_rough_cutoffs(self):
        Y, p, n, q, r = 2304, 1823, 2021, 47, 43
        R = 41
        self.assertLessEqual(R**25, Y**12)
        self.assertLess(Y**12, (R+1)**25)
        self.assertGreater((R+1)**3, Y)
        self.assertGreater(min(q, r), R)
        self.assertEqual(n, q*r)
        self.assertEqual(affine_range_certificate(Y, p, n, q, F(1, 100)), r)
        self.assertLess(n**12, q**25)  # Exact log(n)/log(q)<25/12.


if __name__ == '__main__':
    unittest.main()
