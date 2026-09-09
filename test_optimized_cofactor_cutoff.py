"""Finite guards for real cutoff changes and the paid norm-only route."""
from fractions import Fraction as F
import unittest

from major_arc_kernel import _factorization, _mobius_phi
from optimized_cofactor_cutoff import (
    cofactor_interval_norm, cofactor_weight, cutoff_diagonal_form,
    cutoff_prime_vector, cutoff_quadratic, cutoff_vaughan_vectors,
    optimal_cutoff, ramanujan_mean_square,
)
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector, vaughan_log_vectors


def combine(vectors):
    result = {}
    for vector in vectors:
        for p, coefficient in vector:
            result[p] = result.get(p, F(0))+coefficient
    return tuple((p, c) for p, c in sorted(result.items()) if c)


class OptimizedCofactorCutoffTests(unittest.TestCase):
    def test_generalized_identity_keeps_all_compensating_terms(self):
        for weights in ((0, 1, F(-1, 3), F(1, 2), F(1, 4)), optimal_cutoff(5)[0]):
            for u in (2, 3, 5):
                for n in (1, 2, 4, 6, 14, 20, 25, 30, 49, 72, 105):
                    self.assertEqual(combine(cutoff_vaughan_vectors(n, u, weights)), mangoldt_log_vector(n))

    def test_hard_cutoff_recovers_all_four_original_terms(self):
        for v in (2, 3, 5):
            hard = (0,)+tuple(_mobius_phi(d)[0] for d in range(1, v+1))
            for n in (6, 14, 20, 30, 49, 72, 105):
                self.assertEqual(cutoff_vaughan_vectors(n, 3, hard), vaughan_log_vectors(n, 3, v))

    def test_prime_slot_matches_direct_tuple_sum_without_multiplicity(self):
        weights = optimal_cutoff(3)[0]
        for n in (14, 25, 30, 49, 72, 77, 105):
            direct = []
            for p, _ in _factorization(n):
                if p > 3:
                    direct.append(((p, sum((_mobius_phi(a)[0]-(weights[a] if a < len(weights) else 0)
                                            for a in _divisors(n//p)), F(0))),))
            self.assertEqual(cutoff_prime_vector(n, 3, weights), combine(direct))
        self.assertEqual(cutoff_prime_vector(79, 3, weights), ())
        self.assertEqual(cutoff_prime_vector(49, 3, weights), ((7, -1),))

    def test_optimized_cutoff_has_small_cofactors_and_signed_values(self):
        weights, minimum = optimal_cutoff(3)
        self.assertEqual(weights, (0, 1, F(-4, 5), F(-3, 5)))
        self.assertEqual(minimum, F(2, 5))
        self.assertEqual(cofactor_weight(2, weights), F(1, 5))
        self.assertEqual(cofactor_weight(6, weights), F(-2, 5))
        self.assertEqual(cutoff_prime_vector(14, 3, weights), ((7, F(-1, 5)),))
        self.assertEqual(vaughan_log_vectors(14, 3, 3)[3], ())

    def test_optimizer_minimum_diagonalization_and_coefficient_bounds(self):
        for v in range(1, 13):
            weights, minimum = optimal_cutoff(v)
            self.assertEqual(cutoff_quadratic(weights), minimum)
            self.assertEqual(cutoff_diagonal_form(weights), minimum)
            self.assertTrue(all(abs(a) <= 1 for a in weights))
            self.assertEqual(weights[1], 1)
            for d in range(1, v+1):
                if _mobius_phi(d)[0] == 0:
                    self.assertEqual(weights[d], 0)
            hard = (0,)+tuple(_mobius_phi(d)[0] for d in range(1, v+1))
            self.assertGreaterEqual(cutoff_quadratic(hard), minimum)
        self.assertEqual(optimal_cutoff(2)[1], F(1, 2))

    def test_finite_interval_norm_pays_endpoint_error(self):
        for v in (2, 3, 7):
            weights = optimal_cutoff(v)[0]
            for start in (1, 2, 5, 20, 90):
                direct, floor_form, main, error = cofactor_interval_norm(start, weights)
                self.assertEqual(direct, floor_form)
                self.assertLessEqual(abs(direct-main), error)
        direct, _, main, _ = cofactor_interval_norm(1, optimal_cutoff(3)[0])
        self.assertNotEqual(direct, main)

    def test_full_period_ramanujan_norm_keeps_only_equal_moduli(self):
        for coefficients in ({1: 1, 2: -1, 3: F(-1, 2)}, {2: F(2, 3), 4: F(-1, 3), 6: F(1, 5)}):
            direct, diagonal = ramanujan_mean_square(coefficients)
            self.assertEqual(direct, diagonal)

    def test_invalid_inputs_do_not_silently_change_normalization(self):
        for weights in ((0, 0, 1), (0, 1, 1.0), (0, 1, True), (0, 1, 2)):
            with self.assertRaises(ValueError):
                cutoff_quadratic(weights)
        with self.assertRaises(ValueError):
            optimal_cutoff(True)
        with self.assertRaises(ValueError):
            cofactor_interval_norm(0, (0, 1))


if __name__ == '__main__':
    unittest.main()
