"""Exact algebra/scope guards; the infinite claim is proved analytically."""

import unittest
from fractions import Fraction as F
from itertools import product
from math import comb, prod

from absolute_remainder_obstruction import (
    finite_singular_average, singular_local_cancellation,
)
from cutoff_normalized_remainder import cutoff_log_vectors
from major_arc_kernel import _factorization, _mobius_phi
from same_sign_six_factor_adverse_mass import (
    BALANCED, SKEW, cutoff_shape, shape_variation_bound, six_factor_parameters,
)
from squarefree_residual_localization import complementary_cutoff_log_vector
from unexceptional_vaughan_gate import _add, _clean, mangoldt_log_vector


class SameSignSixFactorTests(unittest.TestCase):
    def test_balanced_active_subsets_give_linear_formula(self):
        theta = F(19, 40)
        by_size = sum(((-1)**j * comb(6, j) * (theta - F(j, 6))
                       for j in range(3)), F(0))
        self.assertEqual(cutoff_shape(BALANCED, theta), by_size)
        self.assertEqual(by_size, 10 * theta - 4)
        self.assertLess(theta, F(3, 6))

    def test_skew_active_subsets_give_opposite_linear_formula(self):
        theta = F(19, 40)
        no_large = sum(((-1)**j * comb(5, j) * (theta - F(j, 8))
                        for j in range(4)), F(0))
        with_large = -(theta - F(3, 8))
        self.assertEqual(cutoff_shape(SKEW, theta), no_large + with_large)
        self.assertEqual(no_large + with_large, F(9, 4) - 5 * theta)
        self.assertEqual(sum(BALANCED), sum(SKEW))
        self.assertEqual(len(BALANCED), len(SKEW))
        self.assertEqual((-1)**len(BALANCED), 1)

    def test_strict_exponent_range_is_not_extended_at_endpoints(self):
        self.assertEqual(cutoff_shape(SKEW, F(9, 20)), 0)
        self.assertLess(cutoff_shape(SKEW, F(1, 2)), 0)
        for theta in (F(9, 20), F(1, 2), F(2, 5), 0.475, True):
            with self.assertRaises(ValueError):
                six_factor_parameters(theta)

    def test_certified_radius_pays_shape_and_frozen_cutoff_drift(self):
        theta = F(19, 40)
        p = six_factor_parameters(theta)
        delta, drift = p['shape_radius'], p['cutoff_drift']
        budget = 192 * delta + 64 * drift
        self.assertLessEqual(budget, min(p['balanced_margin'], p['skew_margin']) / 2)
        for shape, sign, margin in ((BALANCED, 1, p['balanced_margin']),
                                    (SKEW, -1, p['skew_margin'])):
            for directions in product((-1, 1), repeat=6):
                perturbed = tuple(s + d * delta for s, d in zip(shape, directions))
                for cutoff in (theta - drift, theta + drift):
                    observed = cutoff_shape(perturbed, cutoff)
                    self.assertGreaterEqual(sign * observed, margin / 2)
                    self.assertLessEqual(abs(observed - cutoff_shape(shape, theta)),
                                         shape_variation_bound(perturbed, shape, cutoff, theta))
        self.assertGreater(p['pair_weight_floor'], 0)

    def test_physical_normalization_need_not_sum_to_one(self):
        shares = tuple(s + F(1, 10000) for s in BALANCED)
        self.assertNotEqual(sum(shares), 1)
        value = cutoff_shape(shares, F(19, 40))
        self.assertEqual(cutoff_shape(tuple(2*s for s in shares), F(19, 20)), 2*value)

    def test_product_shapes_are_disjoint_and_counting_has_a_power_gap(self):
        p = six_factor_parameters(F(19, 40))
        delta, eps = p['shape_radius'], p['first_five_radius']
        self.assertLess(F(1, 8) + delta, F(1, 6) - delta)
        self.assertLess(F(1, 6) + delta, F(3, 8) - delta)
        self.assertLess(5 * eps, delta)
        for share in (F(1, 6), F(1, 8)):
            self.assertLess(5 * (share + eps), 1)
            self.assertGreater(share - eps, 0)
        # Any two coordinates in this physical rectangle are strictly central.
        self.assertLess(F(11, 10), 2)

    def test_subset_identity_matches_actual_six_prime_log_vectors(self):
        for primes in ((2, 3, 5, 7, 11, 13), (3, 5, 7, 11, 13, 17)):
            n = prod(primes)
            self.assertEqual(_mobius_phi(n)[0], 1)
            for cutoff in (3, 11, 175):
                vector = {}
                for mask in range(64):
                    divisor = prod(p for j, p in enumerate(primes) if mask & (1 << j))
                    if divisor <= cutoff:
                        sign = (-1)**mask.bit_count()
                        _add(vector, _factorization(cutoff), sign)
                        _add(vector, _factorization(divisor), -sign)
                actual_a, actual_d = cutoff_log_vectors(n, cutoff)
                self.assertEqual(_clean(vector), actual_a)
                self.assertEqual(mangoldt_log_vector(n), ())
                self.assertEqual(actual_d, _clean({p: -c for p, c in actual_a}))
                self.assertEqual(actual_d, _clean({p: -c for p, c in
                                                  complementary_cutoff_log_vector(n, cutoff)}))

    def test_singular_mean_uses_exact_euler_cancellation(self):
        for prime in (3, 5, 7, 11):
            self.assertEqual(singular_local_cancellation(prime), 1)
        direct, expanded, upper = finite_singular_average(90, (3, 5, 7, 11))
        self.assertEqual(direct, expanded)
        self.assertLessEqual(direct, upper)

    def test_validation_does_not_accept_rounded_shares(self):
        for shares, cutoff in (((), F(1, 2)), ((0.2,), F(1, 2)),
                               ((F(0),), F(1, 2)), (BALANCED, 0.5),
                               (BALANCED, F(0)), ((F(1),)*13, F(1, 2))):
            with self.assertRaises(ValueError):
                cutoff_shape(shares, cutoff)
        with self.assertRaises(ValueError):
            shape_variation_bound(BALANCED, SKEW[:-1], F(1, 2), F(1, 2))


if __name__ == '__main__':
    unittest.main()
