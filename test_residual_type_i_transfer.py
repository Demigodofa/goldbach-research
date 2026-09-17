"""Exact identities and boundary guards, not tests of asymptotic estimates."""

import unittest
from fractions import Fraction as F
from math import comb, gcd, lcm, prod

from complementary_divisor_correlation import central_interval, frozen_mobius_log_vector
from cutoff_normalized_remainder import cutoff_log_vectors
from major_arc_kernel import _factorization, _mobius_phi
from residual_type_i_transfer import (
    cutoff_progression_density_log_vector as direct_density,
    grouped_cutoff_progression_density_log_vector as grouped_density,
)
from unexceptional_vaughan_gate import (
    _add, _clean, _divisors, large_divisor_log_vector,
    mangoldt_log_vector, vaughan_log_vectors,
)


def product_into(result, left, right, scalar=1):
    for p, a in left:
        for q, b in right:
            key = tuple(sorted((p, q)))
            result[key] = result.get(key, 0) + scalar * a * b


def clean_product(result):
    return {key: value for key, value in result.items() if value}


class ResidualTypeITransferTests(unittest.TestCase):
    def test_density_grouping_for_all_residue_types(self):
        for cutoff in (1, 3, 7, 12, 19):
            for modulus in (1, 2, 6, 9, 12, 25):
                for residue in range(-1, modulus + 1):
                    self.assertEqual(direct_density(cutoff, modulus, residue),
                                     grouped_density(cutoff, modulus, residue))

    def test_density_is_exact_complete_period_mean(self):
        for cutoff in (3, 5, 7):
            for modulus in (1, 4, 6):
                period = lcm(modulus, *range(1, cutoff + 1))
                for residue in range(modulus):
                    vector = {}
                    for n in range(1, period + 1):
                        if n % modulus == residue:
                            _add(vector, frozen_mobius_log_vector(n, cutoff, upper=cutoff),
                                 F(1, period))
                    self.assertEqual(_clean(vector), direct_density(cutoff, modulus, residue))

    def test_nonreduced_main_cancels_including_repeated_factors(self):
        for modulus in (1, 2, 8, 12, 30, 49):
            for residue in range(modulus):
                coefficient = sum(_mobius_phi(h)[0]
                                  for h in _divisors(gcd(modulus, residue)))
                self.assertEqual(coefficient, int(gcd(modulus, residue) == 1))

    def test_noninteger_inner_cutoff_does_not_round_log_weight(self):
        # q=2,r=0 has the h=2 cutoff 7/2, not 3 in its logarithm.
        # d=3 and d=6 cancel log 3; d=5 leaves (log 5-log 7)/10.
        self.assertEqual(grouped_density(7, 2, 0),
                         ((2, F(1, 3)), (5, F(1, 10)), (7, F(-1, 10))))

    def test_reflection_preserves_progressions_and_strict_endpoints(self):
        for target in (30, 32, 60):
            points = list(central_interval(target))
            for d in (1, 3, 7, 12):
                original = [n for n in points if n % d == 0]
                self.assertEqual(sorted(target - n for n in original),
                                 [m for m in points if (m - target) % d == 0])
            self.assertNotIn(F(target, 3), points)
            self.assertNotIn(F(2 * target, 3), points)

    def test_lcm_mask_and_multiplicity_bound(self):
        for q in range(1, 50):
            divisors = _divisors(q)
            pairs = [(d, g) for d in divisors for g in divisors if lcm(d, g) == q]
            self.assertLessEqual(len(pairs), len(divisors) ** 2)
            for d, g in pairs:
                for n in (q, q + 1, 2 * q):
                    self.assertEqual(n % d == 0 and n % g == 0, n % q == 0)

    def test_fixed_divisor_moment_domination(self):
        for n in range(1, 100):
            for exponent in range(5):
                d_k = prod(comb(power + 2 ** exponent - 1, 2 ** exponent - 1)
                           for _, power in _factorization(n))
                self.assertLessEqual(len(_divisors(n)) ** exponent, d_k)

    def test_vaughan_transfer_exact_on_unit_and_nonunit_sets(self):
        for target, cutoff, u, v in ((30, 7, 3, 2), (60, 7, 4, 3), (256, 13, 3, 3)):
            for unit in (False, True):
                actual, expanded, remainder, grouped = {}, {}, {}, {}
                for n in central_interval(target):
                    if (gcd(n, target) == 1) != unit:
                        continue
                    partner = cutoff_log_vectors(target - n, cutoff)[1]
                    product_into(actual, mangoldt_log_vector(n), partner)
                    terms = vaughan_log_vectors(n, u, v)
                    self.assertEqual(terms[0], ())
                    for term in terms:
                        product_into(expanded, term, partner)
                    product_into(remainder, terms[3], partner)
                    for a in _divisors(n):
                        b = n // a
                        if a > v and b > u:
                            product_into(grouped, large_divisor_log_vector(b, u), partner,
                                         _mobius_phi(a)[0])
                self.assertEqual(clean_product(actual), clean_product(expanded))
                self.assertEqual(clean_product(remainder), clean_product(grouped))

    def test_free_convolution_factor_and_no_factor_coprimality_filter(self):
        self.assertEqual(large_divisor_log_vector(15, 3), ((5, 1),))
        self.assertNotEqual(large_divisor_log_vector(15, 3), mangoldt_log_vector(15))
        self.assertNotEqual(large_divisor_log_vector(15, 3), _factorization(15))
        self.assertIn(7 * 15, central_interval(256))
        self.assertEqual(gcd(7 * 15, 256), 1)
        # a=b=5 is allowed on the unit core and contributes a nonzero term.
        self.assertIn(25, central_interval(64))
        self.assertEqual(gcd(25, 64), 1)
        self.assertNotEqual(large_divisor_log_vector(5, 3), ())
        self.assertNotEqual(cutoff_log_vectors(39, 7)[1], ())

    def test_validation_and_residue_periodicity(self):
        for density in (direct_density, grouped_density):
            for args in ((0, 2, 1), (7, 0, 1), (True, 2, 1), (7, 2, 0.5)):
                with self.assertRaises(ValueError):
                    density(*args)
            self.assertEqual(density(7, 12, -1), density(7, 12, 11))


if __name__ == "__main__":
    unittest.main()
