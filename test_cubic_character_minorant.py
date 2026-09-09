"""Exact cubic identities and finite one-sided partition controls."""
from collections import defaultdict
from itertools import product
from math import isqrt
import unittest

from character_partner_weight import negative_log_coefficients
from cubic_character_minorant import negative_cubic_coefficients, negative_semiprime_sign
from exceptional_character_model import character_values
from redistribution import trial_prime
from test_character_partner_weight import trial_factors


def generalized_mangoldt_cube(n):
    """Independent closed coefficients of mu*log^3, by distinct-factor count."""
    factors = sorted(trial_factors(n).items())
    if len(factors) == 1:
        (p, a), = factors
        return {(p, p, p): 3*a*a-3*a+1}
    if len(factors) == 2:
        (p, a), (q, b) = factors
        return {(p, p, q): 3*(2*a-1), (p, q, q): 3*(2*b-1)}
    if len(factors) == 3:
        return {tuple(p for p, _ in factors): 6}
    return {}


def nonnegative_convolution_cube(n, chi):
    """Compute lambda*Lambda_3 independently of the chi*log^3 expansion."""
    result = defaultdict(int)
    for d in range(1, isqrt(n)+1):
        if n % d:
            continue
        for k in ((d,) if d*d == n else (d, n//d)):
            lam = 1
            for p, a in trial_factors(n//k).items():
                sign = chi[p % len(chi)]
                lam *= a+1 if sign == 1 else (1 if sign == 0 else int(a % 2 == 0))
            for monomial, coefficient in generalized_mangoldt_cube(k).items():
                result[monomial] += lam*coefficient
    return {key: value for key, value in result.items() if value}


def log_square_times_linear(n, linear):
    result = defaultdict(int)
    factors = tuple(trial_factors(n).items())
    for prime, coefficient in linear.items():
        for (p, a), (q, b) in product(factors, repeat=2):
            result[tuple(sorted((prime, p, q)))] += coefficient*a*b
    return dict(result)


class CubicCharacterMinorantTests(unittest.TestCase):
    def test_complete_negative_prefix_matches_positive_convolution(self):
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1)):
            chi = character_values(conductor, two_sign=sign)
            for n in range(2, 1201):
                if chi[n % conductor] != -1:
                    continue
                cubic, numerator = map(dict, negative_cubic_coefficients(n, conductor, two_sign=sign))
                self.assertEqual(cubic, nonnegative_convolution_cube(n, chi))
                self.assertTrue(all(value > 0 for value in cubic.values()))
                squared_w = log_square_times_linear(
                    n, dict(negative_log_coefficients(n, conductor, two_sign=sign)))
                expected = {key: 10*squared_w.get(key, 0)-9*cubic.get(key, 0)
                            for key in squared_w.keys() | cubic.keys()}
                self.assertEqual(numerator, {key: value for key, value in expected.items() if value})

    def test_prime_normalization_negative_triples_and_prime_cube(self):
        for p in (11, 17, 43):
            cubic, numerator = negative_cubic_coefficients(p, 31)
            self.assertEqual(cubic, (((p, p, p), 1),))
            self.assertEqual(numerator, cubic)
        cubic, numerator = negative_cubic_coefficients(11*17*43, 31)
        self.assertEqual(cubic, (((11, 17, 43), 6),))
        self.assertEqual(numerator, (((11, 17, 43), -54),))
        self.assertEqual(negative_log_coefficients(11*17*43, 31), ())
        # This particular repeated-factor contribution is exactly zero;
        # the analytic reduction still charges all repeated factors safely.
        cubic, numerator = negative_cubic_coefficients(11**3, 31)
        self.assertEqual(cubic, (((11, 11, 11), 20),))
        self.assertEqual(numerator, ())

    def test_semiprime_factorization_sign_and_formal_boundary(self):
        for r, q, expected_sign in ((11, 19, 1), (43, 5, 1), (11, 131, -1)):
            cubic, numerator = map(dict, negative_cubic_coefficients(r*q, 31))
            self.assertEqual(cubic, {tuple(sorted(key)): coefficient for key, coefficient in
                                    (((r, r, r), 2), ((r, r, q), 3), ((r, q, q), 3))})
            self.assertEqual(numerator, {tuple(sorted(key)): coefficient for key, coefficient in
                                        (((r, r, r), 2), ((r, r, q), 13), ((r, q, q), -7))})
            self.assertEqual(negative_semiprime_sign(r*q, 31), (r, q, expected_sign))
        # Formal positive log variables test both sides and the boundary;
        # y=2x is not claimed to come from two actual distinct primes.
        for x in range(1, 8):
            for y in range(1, 18):
                polynomial = 2*x**3+13*x*x*y-7*x*y*y
                factored = x*(2*x-y)*(x+7*y)
                self.assertEqual(polynomial, factored)
                self.assertEqual((polynomial > 0)-(polynomial < 0), (2*x > y)-(2*x < y))

    def test_finite_pool_partition_preserves_the_one_sided_direction(self):
        chi = character_values(31)
        seen = set()
        # Finite cutoffs test the exact partition only, not an exceptional
        # zero or analytic eligibility; every target is inside the old prefix.
        for upper, target, z, w, w_star in ((400, 558, 4, 10, 12),
                                           (2100, 2790, 10, 50, 100),
                                           (2100, 3038, 10, 50, 100),
                                           (12000, 16430, 10, 50, 100),
                                           (12000, 17918, 10, 10, 100)):
            for p in range(upper//2+1, upper+1):
                n = target-p
                if not upper//2 < n <= upper or not trial_prime(p) or chi[p % 31] != 1:
                    continue
                if chi[n % 31] == 0:
                    continue
                self.assertEqual(chi[n % 31], -1)
                factors = trial_factors(n)
                if any(q <= z or (chi[q % 31] == 1 and q <= w) for q in factors):
                    continue
                cubic, numerator = map(dict, negative_cubic_coefficients(n, 31))
                w_linear = dict(negative_log_coefficients(n, 31))
                if trial_prime(n):
                    seen.add('prime')
                    self.assertEqual(numerator, {(n, n, n): 1})
                    continue
                if any(a > 1 for a in factors.values()):
                    category = 'repeated'
                elif len(factors) == 2:
                    r, q, k_sign = negative_semiprime_sign(n, 31)
                    if q <= w_star:
                        category = 'small'
                    elif k_sign < 0:
                        seen.add('negative_semiprime')
                        self.assertGreater(q, r*r)
                        continue  # Dropping this negative term raises the total.
                    else:
                        seen.add('middle')
                        self.assertLess(q, r*r)
                        self.assertGreater(k_sign, 0)
                        continue  # Keep its exact K contribution as E_mid.
                elif not w_linear:
                    seen.add('zero_w')
                    self.assertTrue(all(value < 0 for value in numerator.values()))
                    continue  # K=-9U/log(n)^2<=0, even though W was zero.
                else:
                    category = 'multiple_positive'
                    self.assertGreaterEqual(sum(chi[q % 31] == 1 for q in factors), 2)
                seen.add(category)
                upper_polynomial = log_square_times_linear(n, {q: 10*c for q, c in w_linear.items()})
                difference = {key: upper_polynomial.get(key, 0)-numerator.get(key, 0)
                              for key in upper_polynomial.keys() | numerator.keys()}
                self.assertEqual({key: value for key, value in difference.items() if value},
                                 {key: 9*value for key, value in cubic.items()})
                self.assertTrue(all(value >= 0 for value in difference.values()))
        self.assertEqual(seen, {'prime', 'repeated', 'small', 'negative_semiprime',
                               'middle', 'zero_w', 'multiple_positive'})

    def test_strict_domain_and_semiprime_requirements(self):
        for function in (negative_cubic_coefficients, negative_semiprime_sign):
            for n, conductor, sign in ((True, 31, 1), (11.0, 31, 1), (1, 31, 1),
                                       (20001, 31, 1), (121, 31, 1), (31, 31, 1),
                                       (11, 25, 1), (11, True, 1), (11, 31, True)):
                with self.assertRaises(ValueError):
                    function(n, conductor, two_sign=sign)
        for n in (11, 11**3, 11*17*43, 11*19**2):
            with self.assertRaises(ValueError):
                negative_semiprime_sign(n, 31)


if __name__ == '__main__':
    unittest.main()
