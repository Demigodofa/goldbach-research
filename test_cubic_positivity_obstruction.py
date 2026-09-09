"""Independent finite algebra, support and rational tail-margin controls."""
from collections import defaultdict
from fractions import Fraction as F
from math import factorial, isqrt
import unittest

from cubic_positivity_obstruction import (dickman_main_enclosure,
                                        paired_hyperbola_split,
                                        paired_kernel_coefficients,
                                        rough_smooth_index_split)
from character_partner_weight import negative_hyperbola_terms, negative_log_coefficients
from exceptional_character_model import character_values
from test_character_partner_weight import trial_factors
from test_cubic_character_minorant import (log_square_times_linear,
                                         nonnegative_convolution_cube)


def add_polynomials(*items):
    result = defaultdict(F)
    for item in items:
        for key, value in item:
            result[key] += value
    return {key: value for key, value in result.items() if value}


class CubicPositivityObstructionTests(unittest.TestCase):
    def test_complete_prefix_hyperbola_matches_independent_convolution(self):
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1)):
            chi = character_values(conductor, two_sign=sign)
            for n in range(2, 601):
                if chi[n % conductor] != -1:
                    continue
                u = nonnegative_convolution_cube(n, chi)
                w = log_square_times_linear(n, dict(negative_log_coefficients(
                    n, conductor, two_sign=sign)))
                for kappa in (F(0), F(9), F(100), F(1, 3)):
                    expected = {key: (1+kappa)*w.get(key, 0)-kappa*u.get(key, 0)
                                for key in w.keys() | u.keys()}
                    expected = {key: value for key, value in expected.items() if value}
                    for cutoff in (0, max(1, isqrt(n)//2), isqrt(n)):
                        low, boundary = paired_hyperbola_split(
                            n, conductor, kappa, cutoff, two_sign=sign)
                        self.assertEqual(add_polynomials(low, boundary), expected)
                        if cutoff == 0:
                            self.assertEqual(low, ())
                        if cutoff == isqrt(n):
                            self.assertEqual(boundary, ())

    def test_boundary_can_have_either_sign_and_negative_triple_is_retained(self):
        # Each has exactly one nontrivial smaller divisor. Since h(x)>0
        # for 0<x<1/2 and kappa>=0, that divisor's character is its sign.
        self.assertEqual(negative_hyperbola_terms(215, 31), ((1, 1), (5, 1)))
        self.assertEqual(negative_hyperbola_terms(1331, 31), ((1, 1), (11, -1)))
        for kappa in (F(0), F(9), F(100)):
            low, boundary = paired_hyperbola_split(1331, 31, kappa, 1)
            self.assertEqual(low, (((11, 11, 11), F(27)),))
            self.assertEqual(boundary, (((11, 11, 11), -9-2*kappa),))
            low, boundary = paired_hyperbola_split(11*17*43, 31, kappa, 11)
            self.assertEqual(add_polynomials(low, boundary),
                             {} if kappa == 0 else {(11, 17, 43): -6*kappa})
            for i in range(1, 50):
                x = F(i, 100)
                value = sum(c*x**j for j, c in enumerate(paired_kernel_coefficients(kappa)))
                self.assertEqual(value, (1-2*x)*(1+kappa*x*(1-x)))
                self.assertGreater(value, 0)

    def test_complete_rough_smooth_support_and_injectivity(self):
        for level, cutoff, limit in ((1000, 5, 100), (600, 3, 50)):
            expected = {}
            for d in range(1, limit+1):
                if any(p <= cutoff or exponent != 1
                       for p, exponent in trial_factors(d).items()):
                    continue
                for e in range(1, level//d+1):
                    if any(p > cutoff or exponent != 1
                           for p, exponent in trial_factors(e).items()):
                        continue
                    self.assertNotIn(d*e, expected)
                    expected[d*e] = (d, e)
            for index in range(1, level+2):
                self.assertEqual(rough_smooth_index_split(index, cutoff, level, limit),
                                 expected.get(index))
        self.assertEqual(rough_smooth_index_split(462, 5, 1000, 100), (77, 6))
        self.assertEqual(rough_smooth_index_split(30, 5, 1000, 100), (1, 30))
        self.assertIsNone(rough_smooth_index_split(308, 5, 1000, 100))
        self.assertIsNone(rough_smooth_index_split(462, 5, 1000, 76))

    def test_rational_dickman_enclosures_and_independent_tail_majorants(self):
        for m in (2, 3, 10, 48):
            for j in (0, 1, 2):
                partial = sum(F((v+1)**j, factorial(v)) for v in range(m, m+40))
                self.assertLess(partial, F(3*(m+1)**j, factorial(m)))
                for v in range(m, m+20):
                    ratio = F((v+2)**j, (v+1)**(j+1))
                    self.assertLessEqual(ratio, F(16, 27))
        # These certify the limiting divisor integral, not a finite prime
        # count or a numerical onset for the full analytic theorem.
        for kappa, theta, a in ((F(100), F(1, 1000), F(12, 25)),
                                 (F(200), F(1, 2000), F(49, 100)),
                                 (F(100), F(1, 100), F(12, 25))):
            lower, upper = dickman_main_enclosure(kappa, theta, a)
            c = paired_kernel_coefficients(kappa)
            # Independent differentiation and normalized Dickman moments.
            moments = (F(1), F(1), F(3, 2))
            center = -sum((j+1)*c[j+1]*theta**j*moments[j] for j in range(3))
            self.assertEqual((lower+upper)/2, center)
            self.assertLess(upper, -kappa/2)
            self.assertGreater(lower, -kappa)
        for kappa in (F(0), F(1), F(2)):
            lower, _ = dickman_main_enclosure(kappa, F(1, 100), F(12, 25))
            self.assertGreater(lower, 0)

    def test_strict_domains_and_finite_verifier_caps(self):
        for kappa in (True, 9, 9.0, F(-1)):
            with self.assertRaises(ValueError):
                paired_kernel_coefficients(kappa)
        for n, cutoff in ((True, 1), (1, 1), (20001, 1), (11, True),
                          (11, -1), (11, 20001), (11, 1.0), (19, 1)):
            with self.assertRaises(ValueError):
                paired_hyperbola_split(n, 31, F(9), cutoff)
        for args in ((True, 5, 100, 10), (0, 5, 100, 10), (1, 1, 100, 10),
                     (1, 5, 100, 5), (1, 5, 100, 101), (1, 5.0, 100, 10)):
            with self.assertRaises(ValueError):
                rough_smooth_index_split(*args)
        for theta, endpoint in ((0.01, F(1, 2)), (F(0), F(1, 2)),
                                 (F(1, 3), F(1, 2)), (F(1, 100), F(3, 4)),
                                 (F(1, 30000), F(1, 2)), (F(1, 100), True)):
            with self.assertRaises(ValueError):
                dickman_main_enclosure(F(9), theta, endpoint)


if __name__ == '__main__':
    unittest.main()
