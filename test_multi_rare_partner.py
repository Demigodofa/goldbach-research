"""Finite algebra controls for the uniform-cofactor reduction, not asymptotics."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from math import prod
import unittest

from exceptional_character_model import character_values
from multi_rare_partner import affine_local_factor, rare_product_tail, split_squarefree_partner
from redistribution import trial_prime


def trial_factors(n):
    result = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            result[d] = result.get(d, 0)+1
            n //= d
        d += 1
    if n > 1:
        result[n] = result.get(n, 0)+1
    return result


class MultiRarePartnerTests(unittest.TestCase):
    def test_local_factors_by_complete_residue_counts(self):
        for cofactor, target, cutoff in ((1, 62, 5), (77, 62, 5),
                                          (143, 122, 5), (779, 17918, 10)):
            for prime in (2, 3, 5, 7, 11, 13, 19, 31, 41):
                roots, divisor, combined = affine_local_factor(prime, cofactor, target, cutoff)
                direct_roots = sum(v*(target-cofactor*v) % prime == 0 for v in range(prime))
                self.assertEqual(roots, direct_roots)
                # Nonzero exact-valuation tuples partition this union, not the
                # sum of the two individual divisibility events.
                modulus = prime**2
                union = sum(v % prime == 0 or (target-cofactor*v) % prime == 0
                            for v in range(modulus))
                direct_divisor = F(1) if prime <= cutoff else 1+F(union, modulus)
                self.assertEqual(divisor, direct_divisor)
                self.assertEqual(combined, (1-F(direct_roots, prime))*direct_divisor)
                self.assertLessEqual(combined, 1)
        self.assertEqual(affine_local_factor(7, 77, 62, 5), (1, F(8, 7), F(48, 49)))
        self.assertEqual(affine_local_factor(31, 77, 62, 5), (1, F(32, 31), F(960, 961)))
        self.assertEqual(affine_local_factor(5, 77, 62, 5), (2, F(1), F(3, 5)))

    def test_finite_euler_tail_and_rational_quadratic_bound(self):
        for primes in ((), (19,), (19, 41), (19, 41, 47, 59, 61), (2, 3, 5)):
            harmonic, tail = rare_product_tail(primes)
            direct = sum((F(2**size, prod(subset))
                          for size in range(2, len(primes)+1)
                          for subset in combinations(primes, size)), F(0))
            self.assertEqual(harmonic, sum((F(1, q) for q in primes), F(0)))
            self.assertEqual(tail, direct)
            self.assertGreaterEqual(tail, 0)
            if 2*harmonic < 1:
                self.assertLessEqual(tail, 2*harmonic**2/(1-2*harmonic))
        self.assertEqual(rare_product_tail((19, 41))[1], F(4, 19*41))

    def test_prime_semiprime_multifactor_and_zero_weight_partition(self):
        expected = {11: (11, 1, 0, 1), 209: (11, 19, 1, 2),
                    11*19*41: (11, 19*41, 2, 4),
                    11*19*41*47: (11, 19*41*47, 3, 8), 11*17*43: None}
        for n, split in expected.items():
            self.assertEqual(split_squarefree_partner(n, 31, 10, 10), split)
            if split is not None:
                r, cofactor, h, weight = split
                self.assertEqual(r*cofactor, n)
                self.assertEqual(weight, 2**h)
                self.assertEqual(len(trial_factors(cofactor)), h)
        with self.assertRaises(ValueError):
            split_squarefree_partner(209, 31, 10, 19)

    def test_actual_finite_multifactor_term_matches_fixed_cofactor_count(self):
        # This target is below the already certified 20,000 prefix. It is an
        # algebra control, with no exceptional-zero or new coverage assertion.
        upper, target, cutoff, bound = 11000, 17918, 10, 10
        chi = character_values(31)
        direct = defaultdict(int)
        for p in range(upper//2+1, upper+1):
            n = target-p
            if not upper//2 < n <= upper or not trial_prime(p) or chi[p % 31] != 1:
                continue
            factors = trial_factors(n)
            if any(a != 1 or q <= cutoff for q, a in factors.items()) or chi[n % 31] != -1:
                continue
            positive = [q for q in factors if chi[q % 31] == 1]
            negative = [q for q in factors if chi[q % 31] == -1]
            if len(negative) != 1 or len(positive) < 2 or any(q <= bound for q in positive):
                continue
            split = split_squarefree_partner(n, 31, cutoff, bound)
            self.assertEqual(split, (negative[0], prod(positive), len(positive), 2**len(positive)))
            direct[tuple(sorted((p, negative[0])))] += 2**len(positive)

        max_cofactor = upper//(cutoff+1)
        positive_primes = [q for q in range(bound+1, max_cofactor//(bound+1)+1)
                           if trial_prime(q) and chi[q % 31] == 1]
        switched = defaultdict(int)
        for h in range(2, len(positive_primes)+1):
            for subset in combinations(positive_primes, h):
                cofactor = prod(subset)
                if cofactor > max_cofactor:
                    continue
                for r in range(upper//(2*cofactor)+1, upper//cofactor+1):
                    p = target-cofactor*r
                    if (r > cutoff and trial_prime(r) and chi[r % 31] == -1
                            and upper//2 < p <= upper and trial_prime(p) and chi[p % 31] == 1):
                        switched[tuple(sorted((p, r)))] += 2**h
        self.assertEqual(dict(direct), dict(switched))
        self.assertEqual(direct[(11, 9349)], 4)

    def test_invalid_domains(self):
        for args in ((4, 77, 62, 5), (True, 77, 62, 5), (7, 77, 77, 5),
                     (7, 77, 154, 5), (7, 77, 62, 7), (7, 77.0, 62, 5),
                     (7, 0, 62, 5), (7, 77, 0, 5), (7, 77, 62, 1)):
            with self.assertRaises(ValueError):
                affine_local_factor(*args)
        for primes in ([19, 41], (19, 19), (True,), (19.0,), (1,), (21,)):
            with self.assertRaises(ValueError):
                rare_product_tail(primes)
        for args in ((True, 31, 10, 10), (11.0, 31, 10, 10), (1331, 31, 10, 10),
                     (121, 31, 10, 10), (31, 31, 10, 10), (11, 25, 10, 10),
                     (209, 31, 11, 11), (209, 31, 10, 9), (209, 31, 10.0, 10)):
            with self.assertRaises(ValueError):
                split_squarefree_partner(*args)


if __name__ == "__main__":
    unittest.main()
