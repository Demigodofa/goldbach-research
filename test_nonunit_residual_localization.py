"""Exact cutoff, Euler, overlap and support checks; not asymptotic evidence."""

import unittest
from fractions import Fraction as F
from math import comb, gcd, lcm

from complementary_divisor_correlation import central_interval, frozen_mobius_log_vector
from cutoff_normalized_remainder import cutoff_log_vectors, singular_multiplier
from major_arc_kernel import _factorization, _mobius_phi
from nonunit_residual_localization import (
    excluded_cutoff_log_vector, excluded_singular_blocks,
    multiple_argument_log_vector, nonunit_mobius_weight,
)
from unexceptional_vaughan_gate import mangoldt_log_vector


def value(vector):
    # Rational log-prime substitution preserves identities, not log bounds.
    return sum(p * exponent for p, exponent in vector)


def interval_any_parity(target):
    return range(target // 3 + 1, (2 * target - 1) // 3 + 1)


class NonunitResidualLocalizationTests(unittest.TestCase):
    def test_multiple_argument_identity_including_shared_prime_powers(self):
        for common in (1, 2, 6, 12, 15, 30):
            for n in (1, 2, 3, 6, 10, 15):
                for cutoff in (3, 7, 12):
                    self.assertEqual(multiple_argument_log_vector(n, cutoff, common),
                                     frozen_mobius_log_vector(common * n, cutoff, upper=cutoff))

    def test_fractional_cutoff_and_empty_support_are_exact(self):
        self.assertEqual(excluded_cutoff_log_vector(15, 7, 2, 3), ((3, -1), (7, 1)))
        self.assertEqual(excluded_cutoff_log_vector(15, 7, 2, 8), ())
        self.assertEqual(excluded_cutoff_log_vector(12, 7, 6), ((7, 1),))

    def test_alternating_main_coefficient_vanishes_only_for_nontrivial_common(self):
        for common in (1, 2, 6, 15, 30):
            coefficient = sum(_mobius_phi(h)[0] for h in range(1, common + 1)
                              if common % h == 0)
            self.assertEqual(coefficient ** 2, int(common == 1))

    def test_excluded_euler_main_including_odd_reduced_target(self):
        for target in (6, 10, 12, 18, 30, 60, 90, 210):
            for common in range(1, target + 1):
                if target % common:
                    continue
                blocks = excluded_singular_blocks(target, common)
                expected = F(common, _mobius_phi(common)[1]) * singular_multiplier(target)
                self.assertEqual(sum(blocks.values(), F(0)), expected)
        self.assertEqual(sum(excluded_singular_blocks(6, 2).values()), F(4))

    def test_nonunit_inclusion_exclusion_and_overlap_correction(self):
        for target in (6, 12, 30, 60, 210):
            for n in range(1, target + 1):
                self.assertEqual(nonunit_mobius_weight(n, target), int(gcd(n, target) > 1))
        self.assertEqual(sum(6 % p == 0 for p, _ in _factorization(30)), 2)
        self.assertEqual(nonunit_mobius_weight(6, 30), 1)

    def test_signed_nonunit_sum_matches_divisor_inclusion_exclusion(self):
        target = 60
        weights = {n: F((-1) ** n * n, 7) for n in central_interval(target)}
        direct = sum(w for n, w in weights.items() if gcd(n, target) > 1)
        expanded = -sum(_mobius_phi(g)[0] * sum(w for n, w in weights.items() if n % g == 0)
                        for g in range(2, target + 1) if target % g == 0)
        self.assertEqual(direct, expanded)

    def test_reflected_cutoff_expansion_respects_scaled_strict_endpoints(self):
        for target, common in ((6, 2), (30, 2), (30, 3), (60, 6), (90, 15)):
            reduced, cutoff = target // common, 7
            reduced_points = interval_any_parity(reduced)
            self.assertEqual([common * m for m in reduced_points],
                             [n for n in central_interval(target) if n % common == 0])
            direct = sum(value(cutoff_log_vectors(common * m, cutoff)[0])
                         * value(cutoff_log_vectors(target - common * m, cutoff)[0])
                         for m in reduced_points)
            divisors = [h for h in range(1, common + 1) if common % h == 0]
            expanded = sum(_mobius_phi(h)[0] * _mobius_phi(k)[0] * sum(
                value(excluded_cutoff_log_vector(m, cutoff, common, h))
                * value(excluded_cutoff_log_vector(reduced - m, cutoff, common, k))
                for m in reduced_points) for h in divisors for k in divisors)
            self.assertEqual(direct, expanded)

    def test_excluded_crt_density_for_odd_reduced_target(self):
        reduced, excluded, cutoff = 15, 2, 7
        coefficients = {
            d: _mobius_phi(d)[0] * (value(((7, 1),)) - value(_factorization(d)))
            for d in range(1, cutoff + 1) if gcd(d, excluded) == 1
        }
        period = lcm(*coefficients)
        observed = F(sum(sum(c for d, c in coefficients.items() if n % d == 0)
                         * sum(c for d, c in coefficients.items() if (reduced - n) % d == 0)
                         for n in range(period)), period)
        density = sum((F(c * b, lcm(d, e)) for d, c in coefficients.items()
                       for e, b in coefficients.items() if reduced % gcd(d, e) == 0), F(0))
        self.assertEqual(observed, density)

    def test_residual_identity_on_nonunit_set_is_not_pointwise_zero(self):
        target, cutoff = 60, 7
        points = [n for n in central_interval(target) if gcd(n, target) > 1]
        short = {n: value(cutoff_log_vectors(n, cutoff)[0]) for n in points}
        residual = {n: value(cutoff_log_vectors(n, cutoff)[1]) for n in points}
        actual = {n: value(mangoldt_log_vector(n)) for n in points}
        def corr(left, right):
            return sum(left[n] * right[target - n] for n in points)
        self.assertEqual(corr(residual, residual), corr(short, short)
                         - 2 * corr(short, actual) + corr(actual, actual))
        self.assertEqual(cutoff_log_vectors(30, 7)[1], ((5, -1), (7, 1)))
        self.assertNotEqual(residual[30] ** 2, 0)

    def test_squarefree_multiplicity_uses_fourfold_divisor_weight(self):
        for g in range(1, 100):
            if _mobius_phi(g)[0]:
                factors = _factorization(g)
                tau = 1
                d4 = 1
                for _, exponent in factors:
                    tau *= exponent + 1
                    d4 *= comb(exponent + 3, 3)
                self.assertEqual(tau * tau, d4)

    def test_validation(self):
        for args in ((0, 7, 2), (12, 0, 2), (12, 7, False), (12, 7, 2, 0)):
            with self.assertRaises(ValueError):
                excluded_cutoff_log_vector(*args)
        with self.assertRaises(ValueError):
            excluded_singular_blocks(30, 7)
        with self.assertRaises(ValueError):
            nonunit_mobius_weight(0, 30)


if __name__ == "__main__":
    unittest.main()
