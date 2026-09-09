"""Exact formal factor identities and independently enumerated sieve supports."""
from fractions import Fraction as F
from math import comb, gcd, prod
import unittest

from quintic_partner_weight import (quintic_formal_weight, quintic_support,
                                    semiprime_sieve_indices)
from test_character_partner_weight import trial_factors


def direct_subset_weight(kappa, negative, positive):
    shares = negative+positive
    result = F(0)
    for mask in range(1 << len(shares)):
        argument = sum(v for i, v in enumerate(shares) if not mask & (1 << i))
        sign = (-1)**sum(bool(mask & (1 << i)) for i in range(len(negative)))
        result += sign*(argument-kappa*argument**2*(1-argument)**2*(1-2*argument))
    return result


class QuinticPartnerWeightTests(unittest.TestCase):
    def test_all_support_types_against_independent_divisor_expansion(self):
        seen = set()
        for k, h in ((1, 0), (1, 1), (1, 2), (1, 3), (3, 0), (3, 1),
                     (3, 2), (5, 0), (5, 1), (7, 0), (7, 1)):
            total = (k+h)*(k+h+1)//2
            shares = tuple(F(i, total) for i in range(1, k+h+1))
            negative, positive = shares[:k], shares[k:]
            category = quintic_support(k, h)
            seen.add(category)
            for kappa in (F(0), F(1), F(100), F(7, 3)):
                value = quintic_formal_weight(kappa, negative, positive)
                self.assertEqual(value, direct_subset_weight(kappa, negative, positive))
                self.assertEqual(value, quintic_formal_weight(
                    kappa, tuple(reversed(negative)), tuple(reversed(positive))))
                if category == 'vanishing':
                    self.assertEqual(value, 0)
                if category == 'prime':
                    self.assertEqual(value, 1)
                if k == 5:
                    self.assertEqual(value, 240*kappa*2**h*prod(negative))
        self.assertEqual(seen, {'prime', 'semiprime', 'triple', 'four_factor',
                               'five_factor', 'six_factor', 'multiple_positive', 'vanishing'})

    def test_positive_pure_triples_have_the_small_cofactor(self):
        positives = 0
        for i in range(1, 39):
            for j in range(1, 40-i):
                shares = (F(i, 40), F(j, 40), F(40-i-j, 40))
                x, y, z = shares
                value = quintic_formal_weight(F(100), shares)
                self.assertEqual(value, 400*x*y*z*(1-5*(x*y+x*z+y*z)))
                if value > 0:
                    positives += 1
                    self.assertGreater(sum(v*v for v in shares), F(3, 5))
                    self.assertGreater(max(shares), F(18, 25))
                    self.assertLess(1-max(shares), F(7, 25))
        self.assertGreater(positives, 0)
        self.assertLess(F(18, 25)**2+F(7, 25)**2, F(3, 5))
        self.assertGreater(quintic_formal_weight(
            F(100), (F(73, 100), F(269, 1000), F(1, 1000))), 0)
        self.assertLess(quintic_formal_weight(
            F(100), (F(18, 25), F(279, 1000), F(1, 1000))), 0)
        # Even at the largest allowed epsilon,delta, the cofactor leaves
        # an absolute exponent margin for the auxiliary prime sieve.
        epsilon, delta = F(1, 100), F(1, 300)
        exponent = F(1, 2)-epsilon-3*delta/4-F(7, 25)
        self.assertEqual(exponent, F(83, 400))
        self.assertGreater(exponent, F(1, 5))

    def test_balanced_five_factor_and_large_positive_factor_leaks(self):
        self.assertEqual(quintic_formal_weight(F(100), (F(1, 5),)*5), F(192, 25))
        distinct = (F(1, 10), F(3, 20), F(1, 5), F(1, 4), F(3, 10))
        self.assertEqual(quintic_formal_weight(F(100), distinct), F(27, 5))
        self.assertEqual(quintic_formal_weight(F(100), (F(1, 10),)*5, (F(1, 2),)), F(12, 25))
        self.assertEqual(quintic_formal_weight(F(100), (F(1, 6),)*3, (F(1, 2),)), F(175, 81))
        self.assertGreater(F(1, 2), F(1, 2)-2*F(1, 100))
        # These are formal proportions, including equal shares. They do
        # not assert distinct actual primes of exactly equal logarithms.

    def test_noninjective_semiprime_sieve_indices_and_multiplicity(self):
        for level, cutoff, limit in ((1500, 11, 120), (800, 5, 100)):
            candidates = [m for m in range(1, limit+1)
                          if len(trial_factors(m)) == 2
                          and all(a == 1 for a in trial_factors(m).values())]
            for index in range(1, level+2):
                expected = []
                if index <= level and all(a == 1 for a in trial_factors(index).values()):
                    for m in candidates:
                        if index % m:
                            continue
                        e = index//m
                        if gcd(m, e) == 1 and all(p <= cutoff for p in trial_factors(e)):
                            expected.append((m, e))
                actual = semiprime_sieve_indices(index, level, limit, cutoff)
                self.assertEqual(actual, tuple(expected))
                self.assertLessEqual(len(actual), comb(len(trial_factors(index)), 2))
        self.assertEqual(semiprime_sieve_indices(5005, 6000, 200, 11),
                         ((65, 77), (91, 55), (143, 35)))
        self.assertEqual(semiprime_sieve_indices(385, 1000, 100, 11),
                         ((35, 11), (55, 7), (77, 5)))
        self.assertEqual(semiprime_sieve_indices(25*7, 1000, 100, 11), ())

    def test_strict_domains_and_finite_factor_count_cap(self):
        for k, h in ((True, 0), (0, 1), (2, 0), (1, -1), (1, True), (63, 2)):
            with self.assertRaises(ValueError):
                quintic_support(k, h)
        for kappa in (True, 100, 100.0, F(-1)):
            with self.assertRaises(ValueError):
                quintic_formal_weight(kappa, (F(1),))
        for negative, positive in (([F(1)], ()), ((1,), ()), ((F(0),), (F(1),)),
                                   ((F(1, 2),), ()), ((F(1, 2),), [F(1, 2)]),
                                   ((F(1, 2),), (0.5,)), ((True,), ())):
            with self.assertRaises(ValueError):
                quintic_formal_weight(F(100), negative, positive)
        for args in ((True, 100, 20, 5), (0, 100, 20, 5), (1, 100, 0, 5),
                     (1, 100, 101, 5), (1, 100, 20, 1), (1, 100, 20, 101),
                     (1, 100.0, 20, 5)):
            with self.assertRaises(ValueError):
                semiprime_sieve_indices(*args)


if __name__ == '__main__':
    unittest.main()
