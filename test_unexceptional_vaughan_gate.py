"""Finite identities and method-budget controls, never a prime-correlation test."""
from fractions import Fraction as F
import unittest

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import (
    chirp_difference_counts, covariance_matrix, diagonal_margin, generic_completion_budget,
    large_divisor_log_vector, mangoldt_log_vector, vaughan_log_vectors,
)


def add_vectors(vectors):
    result = {}
    for vector in vectors:
        for p, coefficient in vector:
            result[p] = result.get(p, 0)+coefficient
    return tuple((p, c) for p, c in sorted(result.items()) if c)


class UnexceptionalVaughanGateTests(unittest.TestCase):
    def test_vaughan_identity_retains_all_four_signed_terms(self):
        for u, v in ((1, 1), (2, 3), (5, 2), (7, 11)):
            for n in range(1, 101):
                self.assertEqual(add_vectors(vaughan_log_vectors(n, u, v)),
                                 mangoldt_log_vector(n))
        # The low term cannot be dropped in an identity for arbitrary n.
        self.assertEqual(vaughan_log_vectors(4, 4, 2)[0], ((2, 1),))

    def test_missing_free_convolution_factor_has_a_nonzero_counterfixture(self):
        self.assertEqual(large_divisor_log_vector(10, 2), ((5, 1),))
        self.assertEqual(mangoldt_log_vector(10), ())
        n = 30
        correct = vaughan_log_vectors(n, 2, 2)[3]
        omitted_free_factor = []
        for a in range(3, n+1):
            if n % a == 0 and n//a > 2:
                omitted_free_factor.append(tuple((p, _mobius_phi(a)[0]*c)
                                                 for p, c in mangoldt_log_vector(n//a)))
        self.assertEqual(correct, ())
        self.assertEqual(add_vectors(omitted_free_factor), ((3, 1), (5, 1)))

    def test_type_ii_weight_is_signed_and_divisor_weight_is_not_log(self):
        self.assertEqual(vaughan_log_vectors(25, 2, 2)[3], ((5, -1),))
        self.assertEqual(large_divisor_log_vector(30, 2), ((3, 1), (5, 1)))
        self.assertNotEqual(large_divisor_log_vector(30, 2), _factorization(30))
        self.assertEqual(large_divisor_log_vector(12, 4), ())
        self.assertEqual(large_divisor_log_vector(16, 4), ((2, 2),))

    def test_type_i_grouped_coefficient_has_the_exact_log_bound(self):
        for d in range(1, 81):
            parts = []
            for a in range(1, min(d, 7)+1):
                if d % a == 0 and d//a <= 5:
                    parts.append(tuple((p, _mobius_phi(a)[0]*c)
                                       for p, c in mangoldt_log_vector(d//a)))
            coefficients = dict(add_vectors(parts))
            full_log = dict(_factorization(d))
            self.assertTrue(all(abs(c) <= full_log[p] for p, c in coefficients.items()))
            if d > 35:
                self.assertEqual(coefficients, {})

    def test_covariance_keeps_intersection_masks_and_is_a_gram_matrix(self):
        errors = {n: F((3*n) % 7-3, 5) for n in range(1, 41)}
        a_values, b_values = (2, 3, 4), (3, 5, 7)
        rows, gram = covariance_matrix(40, a_values, b_values, errors, 10, 23)
        self.assertEqual(rows[0][:2], (F(0), F(0)))
        self.assertEqual(rows[2][2], 0)
        alpha, beta = (F(1), F(-1), F(0)), (F(2, 3), F(-1), F(1, 2))
        row_sums = [sum((b*z for b, z in zip(beta, row)), F(0)) for row in rows]
        direct_energy = sum((s*s for s in row_sums), F(0))
        expanded_energy = sum((beta[i]*beta[j]*gram[i][j]
                               for i in range(3) for j in range(3)), F(0))
        self.assertEqual(direct_energy, expanded_energy)
        total = sum((a*s for a, s in zip(alpha, row_sums)), F(0))
        self.assertLessEqual(total*total, sum(a*a for a in alpha)*expanded_energy)
        self.assertGreater(expanded_energy, 0)
        for a in a_values:
            for b1 in b_values:
                for b2 in b_values:
                    p1, p2 = 40-a*b1, 40-a*b2
                    self.assertEqual(b2*p1-b1*p2, (b2-b1)*40)

    def test_chirp_completion_loss_is_sharp_for_bounded_sequences(self):
        for p in (3, 5, 7, 11, 17):
            self.assertEqual(chirp_difference_counts(p, 0), (p,)+(0,)*(p-1))
            for shift in range(1, p):
                self.assertEqual(chirp_difference_counts(p, shift), (1,)*p)
        with self.assertRaises(ValueError):
            chirp_difference_counts(2, 1)

    def test_completion_budget_cannot_absorb_long_arithmetic_coefficients(self):
        self.assertEqual(generic_completion_budget(F(1, 4)), F(4607, 4096))
        self.assertEqual(generic_completion_budget(F(1, 2048)), 1)
        self.assertLess(generic_completion_budget(F(1, 4096)), 1)
        self.assertGreater(generic_completion_budget(F(5, 24)), 1)

    def test_invalid_exact_inputs_are_rejected(self):
        for args in ((0, 2, 2), (12, True, 2), (12, 2, 0)):
            with self.assertRaises(ValueError):
                vaughan_log_vectors(*args)
        with self.assertRaises(ValueError):
            covariance_matrix(10, (1, 1), (2,), {}, 0, 9)
        with self.assertRaises(ValueError):
            generic_completion_budget(0.25)

    def test_covariance_diagonal_has_a_uniform_fixed_power_margin(self):
        for delta, eps in ((F(1, 4800), F(1, 13)), (F(1, 9600), F(1, 100))):
            self.assertGreater(diagonal_margin(delta, eps), F(5, 24)-F(1, 1200))
        for delta, eps in ((F(1, 100), F(1, 13)), (F(1, 4800), F(1, 12))):
            with self.assertRaises(ValueError):
                diagonal_margin(delta, eps)


if __name__ == '__main__':
    unittest.main()
