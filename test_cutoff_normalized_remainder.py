"""Check exact algebra; the external estimates are not finite-test claims."""

import unittest
from fractions import Fraction as F
from math import gcd, isqrt, log

from complementary_divisor_correlation import (
    central_interval, complementary_expansion, frozen_mobius_log_vector,
)
from cutoff_normalized_remainder import (
    common_divisor_density_blocks, cutoff_log_vectors,
    singular_divisor_blocks, singular_multiplier,
)
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import mangoldt_log_vector


def combine(*weighted_vectors):
    result = {}
    for coefficient, vector in weighted_vectors:
        for p, power in vector:
            result[p] = result.get(p, 0) + coefficient * power
    return tuple(sorted((p, power) for p, power in result.items() if power))


class CutoffNormalizedTests(unittest.TestCase):
    def test_singular_divisor_collapse_including_repeated_primes(self):
        for n in (1, 3, 15, 2, 4, 8, 12, 18, 30, 210, 360):
            self.assertEqual(sum(singular_divisor_blocks(n).values(), F(0)),
                             singular_multiplier(n))
        self.assertEqual(singular_divisor_blocks(8),
                         {1: F(0), 2: F(1), 4: F(0), 8: F(0)})
        self.assertEqual(singular_multiplier(30), F(8, 3))

    def test_small_and_large_common_divisor_main_split(self):
        n, cutoff = 210, 16
        blocks = singular_divisor_blocks(n)
        small = sum((v for g, v in blocks.items() if g <= isqrt(cutoff)), F(0))
        tail = sum((v for g, v in blocks.items() if g > isqrt(cutoff)), F(0))
        self.assertGreater(tail, 0)
        self.assertEqual(small + tail, singular_multiplier(n))
        tau = sum(n % g == 0 for g in range(1, n + 1))
        self.assertLessEqual(tail, F(2 * tau ** 3, isqrt(cutoff)))

    def test_gcd_grouping_matches_ungrouped_density(self):
        coefficients = {1: F(7, 3), 2: -2, 3: -1, 5: F(-3, 7), 6: F(5, 4), 10: 1}
        for n in (12, 30, 50, 210):
            blocks = common_divisor_density_blocks(n, coefficients)
            self.assertEqual(sum(blocks.values(), F(0)),
                             complementary_expansion(n, coefficients).density)
            self.assertTrue(all(n % g == 0 for g in blocks))

    def test_common_divisor_tail_is_not_silently_dropped(self):
        coefficients = {1: 2, 2: -3, 3: -1, 6: 2}
        blocks = common_divisor_density_blocks(30, coefficients)
        threshold = isqrt(max(coefficients))
        tail = sum((v for g, v in blocks.items() if g > threshold), F(0))
        self.assertNotEqual(tail, 0)
        small = sum((v for g, v in blocks.items() if g <= threshold), F(0))
        self.assertEqual(small + tail, complementary_expansion(30, coefficients).density)

    def test_squarefree_support_is_required_for_pairwise_coprimality(self):
        with self.assertRaises(ValueError):
            common_divisor_density_blocks(12, {4: 1})
        self.assertEqual(common_divisor_density_blocks(12, {4: 0}), {})

    def test_cutoff_gauge_recovers_lambda_including_n_below_cutoff(self):
        for n, cutoff in ((2, 7), (4, 7), (7, 7), (30, 7), (31, 7), (72, 11), (25, 1)):
            short, residual = cutoff_log_vectors(n, cutoff)
            self.assertEqual(combine((1, short), (1, residual)), mangoldt_log_vector(n))

    def test_scale_change_transfers_exactly_between_short_and_long(self):
        scale, cutoff = 100, 7
        shift = combine((1, _factorization(scale)), (-1, _factorization(cutoff)))
        for n in (25, 30, 31, 49, 60):
            short, residual = cutoff_log_vectors(n, cutoff)
            old_short = frozen_mobius_log_vector(n, scale, upper=cutoff)
            old_residual = frozen_mobius_log_vector(n, scale, lower=cutoff, upper=n)
            mobius_sum = sum(_mobius_phi(d)[0] for d in range(1, cutoff + 1) if n % d == 0)
            self.assertEqual(old_short, combine((1, short), (mobius_sum, shift)))
            self.assertEqual(old_residual, combine((1, residual), (-mobius_sum, shift)))

    def test_exact_residual_correlation_identity_with_prime_powers(self):
        # An additive rational log-prime assignment checks this algebra exactly.
        def value(vector):
            return sum(p * power for p, power in vector)

        n, cutoff = 50, 7
        interval = central_interval(n)
        short = {x: value(cutoff_log_vectors(x, cutoff)[0]) for x in interval}
        residual = {x: value(cutoff_log_vectors(x, cutoff)[1]) for x in interval}
        lam = {x: value(mangoldt_log_vector(x)) for x in interval}
        prime = {x: x if _factorization(x) == ((x, 1),) else 0 for x in interval}
        def correlation(left, right):
            return sum(left[x] * right[n - x] for x in interval)
        aa, al = correlation(short, short), correlation(short, lam)
        dd = correlation(residual, residual)
        total = correlation(prime, prime)
        powers = correlation(lam, lam) - total
        self.assertGreater(powers, 0)
        self.assertEqual(total, 2 * al - aa + dd - powers)
        self.assertEqual(correlation(short, residual), al - aa)

    def test_nonreduced_mixed_prime_support_is_empty_above_cutoff(self):
        n, cutoff = 210, 13
        for d in range(1, cutoff + 1):
            if gcd(d, n) == 1:
                continue
            for m in central_interval(n):
                if m % d == n % d and _factorization(m) == ((m, 1),):
                    self.fail("a nonreduced class cannot contain a prime above d")

    def test_logarithmic_coefficient_l1_bound_smoke(self):
        for cutoff in (1, 2, 3, 7, 16, 50):
            self.assertLessEqual(sum(log(cutoff / d) for d in range(1, cutoff + 1)),
                                 cutoff - 1 + 1e-12)

    def test_validation(self):
        for n in (0, -2, 2.0, True):
            with self.assertRaises(ValueError):
                singular_multiplier(n)
        with self.assertRaises(ValueError):
            cutoff_log_vectors(1, 7)
        with self.assertRaises(ValueError):
            cutoff_log_vectors(10, 0)


if __name__ == "__main__":
    unittest.main()
