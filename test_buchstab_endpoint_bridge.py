"""Exact decomposition/support checks; none estimates an infinite prime sum."""
from fractions import Fraction as F
from math import prod
import unittest

from buchstab_endpoint_bridge import (buchstab_split, endpoint_exponents,
                                      endpoint_factors, negative_endpoint_factors)


def trial_factors(n):
    factors = []
    p = 2
    while p*p <= n:
        while n % p == 0:
            factors.append(p)
            n //= p
        p += 1
    if n > 1:
        factors.append(n)
    return factors


class BuchstabEndpointTests(unittest.TestCase):
    def test_identity_against_independent_prime_times_rough_enumeration(self):
        limit = 900
        factors = {n: trial_factors(n) for n in range(2, limit+1)}
        primes = [n for n in factors if factors[n] == [n]]
        weights = [F(0), F(0)]+[F((n*17) % 23-11, n % 7+1)
                                  for n in range(2, limit+1)]
        for z, r in ((2, 2), (2, 7), (5, 19), (13, 29), (29, 47)):
            result = buchstab_split(weights, z, r)
            removed = F(0)
            for q in primes:
                if z < q <= r:
                    removed += weights[q]  # k=1 is real in a generic weight.
                    for k in range(q, limit//q+1):
                        if min(factors[k]) >= q:
                            removed += weights[q*k]
            terminal = sum((weights[n] for n in factors if min(factors[n]) > r), F(0))
            initial = sum((weights[n] for n in factors if min(factors[n]) > z), F(0))
            self.assertEqual((result.initial, result.removed, result.terminal),
                             (initial, removed, terminal))
            self.assertEqual(result.initial-result.removed, result.terminal)

    def test_cutoff_equalities_prime_term_and_repeated_factor_guard(self):
        weights = [0]*126
        weights[5], weights[25], weights[125], weights[35], weights[49] = 2, 3, 5, 7, 11
        result = buchstab_split(weights, 3, 5)
        self.assertEqual(result.removed_by_prime, ((5, F(17)),))
        self.assertEqual(result.terminal, 11)
        # A strict cofactor >q roughness condition would lose both 25 and125.
        self.assertEqual(buchstab_split(weights, 5, 5).initial, 11)
        self.assertEqual(endpoint_factors(49, 125, 5), (7, 7))

    def test_endpoint_partition_exhaustive_small_integers_and_negative_signs(self):
        limit, cutoff = 500, 7  # 8^3>500, although 7^3<500.
        prime_mass = composite_mass = terminal_mass = F(0)
        weights = [0]*(limit+1)
        seen_mixed = seen_prime = False
        for n in range(2, limit+1):
            expected = trial_factors(n)
            if min(expected) <= cutoff:
                continue
            actual = endpoint_factors(n, limit, cutoff)
            self.assertEqual(actual, tuple(expected))
            self.assertIn(len(actual), (1, 2))
            # Independent Legendre symbol modulo31, not the production table.
            residue = pow(n, 15, 31)
            if residue != 30:
                continue
            signs = negative_endpoint_factors(n, limit, cutoff, 31)
            self.assertEqual(prod(sign for _, sign in signs), -1)
            weights[n] = n % 11+1
            terminal_mass += weights[n]
            if len(actual) == 1:
                prime_mass += weights[n]
                seen_prime = True
            else:
                self.assertNotEqual(actual[0], actual[1])
                self.assertEqual(sorted(sign for _, sign in signs), [-1, 1])
                composite_mass += weights[n]
                seen_mixed = True
        self.assertTrue(seen_mixed and seen_prime)
        split = buchstab_split(weights, 2, cutoff)
        self.assertEqual(split.terminal, terminal_mass)
        self.assertEqual(split.terminal, prime_mass+composite_mass)

    def test_actual_reflected_prime_support_without_zero_or_density_claim(self):
        # Finite character/sign check only. Modulo31 is NOT asserted to have
        # an exceptional zero. Integer p*n replaces logarithms for exactness.
        target, limit, cutoff = 2790, 2000, 13
        weights = [0]*(limit+1)
        prime_mass = semiprime_mass = 0
        for n in range(limit//2+1, limit+1):
            p = target-n
            if (limit//2 < p <= limit and trial_factors(p) == [p]
                    and pow(p, 15, 31) == 1 and n % 31):
                weights[n] = p*n
                self.assertEqual(pow(n, 15, 31), 30)
                factors = trial_factors(n)
                if min(factors) > cutoff:
                    if len(factors) == 1:
                        prime_mass += weights[n]
                    else:
                        self.assertEqual(len(factors), 2)
                        self.assertNotEqual(*factors)
                        semiprime_mass += weights[n]
        result = buchstab_split(weights, 5, cutoff)
        self.assertGreater(prime_mass, 0)
        self.assertGreater(semiprime_mass, 0)
        self.assertEqual(result.terminal, prime_mass+semiprime_mass)
        # The source's 1459+11^3 example is removed, with no squarefree step.
        self.assertEqual(weights[1331], 1459*1331)
        self.assertGreater(dict(result.removed_by_prime)[11], 0)

    def test_exponents_and_strict_domains(self):
        for eps in (F(1, 100), F(1, 1000), F(1, 99999)):
            lower, upper, slack = endpoint_exponents(eps)
            self.assertEqual(lower+upper, 1)
            self.assertEqual(upper-lower, 4*eps)
            self.assertGreaterEqual(lower, F(12, 25))
            self.assertLessEqual(upper, F(13, 25))
            self.assertGreater(slack, 0)
        for args in ((343, 512, 7), (49, 500, 7), (7, 500, 7), (True, 500, 7)):
            with self.assertRaises(ValueError):
                endpoint_factors(*args)
        with self.assertRaises(ValueError):
            negative_endpoint_factors(121, 500, 7, 31)
        for eps in (0, 0.01, F(1, 99), True):
            with self.assertRaises(ValueError):
                endpoint_exponents(eps)
        for weights in ([0, 1, 0], [0, 0, 1.0], [0, 0, True], (0, 0, 1)):
            with self.assertRaises(ValueError):
                buchstab_split(weights, 2, 2)
        for cutoffs in ((1, 2), (3, 2), (2, 3), (True, 2)):
            with self.assertRaises(ValueError):
                buchstab_split([0, 0, 1], *cutoffs)


if __name__ == '__main__':
    unittest.main()
