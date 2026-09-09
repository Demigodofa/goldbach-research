"""Exact identity and method-scope guards, without a prime scan."""
from fractions import Fraction as F
import unittest

from free_divisor_correlation import free_correlation_budget
from multifactor_identity_gate import (
    divisor_count, heath_brown_log_vectors, localized_hb_term,
    long_free_type_i, weighted_type_i_budget,
)
from unexceptional_vaughan_gate import mangoldt_log_vector


def add_vectors(vectors):
    result = {}
    for vector in vectors:
        for p, coefficient in vector:
            result[p] = result.get(p, 0)+coefficient
    return tuple((p, c) for p, c in sorted(result.items()) if c)


class MultifactorIdentityGateTests(unittest.TestCase):
    def test_exact_identity_includes_the_residual_outside_its_valid_range(self):
        for order, cutoff in ((1, 2), (2, 2), (3, 2), (3, 3), (4, 2)):
            for n in (1, 2, 4, 9, 12, 18, 25, 30, 54, 81):
                terms, residual = heath_brown_log_vectors(n, order, cutoff)
                self.assertEqual(add_vectors(terms+(residual,)), mangoldt_log_vector(n))
                if n < 2*(cutoff+1)**order:
                    self.assertEqual(residual, ())

    def test_first_possible_residual_is_not_silently_discarded(self):
        terms, residual = heath_brown_log_vectors(18, 2, 2)
        self.assertEqual(residual, ((2, 1),))
        self.assertEqual(add_vectors(terms), ((2, -1),))
        # The endpoint can vanish if the least allowed Mobius value is zero.
        self.assertEqual(heath_brown_log_vectors(32, 2, 3)[1], ())
        self.assertEqual(heath_brown_log_vectors(9, 2, 2)[1], ())

    def test_all_short_free_tuple_is_nonzero_but_full_identity_cancels(self):
        for order, prime in ((2, 5), (3, 5), (4, 3)):
            n, vector = localized_hb_term((prime,)*order, (1,)*(order-1), 2, order, prime)
            self.assertEqual(n, 2*prime**order)
            self.assertEqual(vector, ((2, -1),))
            self.assertLess(F(1, 2), F(n, 3*prime**order))
            self.assertLess(F(n, 3*prime**order), 1)
            terms, residual = heath_brown_log_vectors(n, order, prime)
            self.assertEqual(add_vectors(terms), ())
            self.assertEqual(residual, ())
            self.assertEqual(mangoldt_log_vector(n), ())

    def test_log_one_and_mobius_support_are_real_boundaries(self):
        self.assertEqual(localized_hb_term((5, 5), (1,), 1, 2, 5)[1], ())
        self.assertEqual(localized_hb_term((4, 5), (1,), 2, 2, 5)[1], ())
        with self.assertRaises(ValueError):
            localized_hb_term((5, 7), (1,), 2, 2, 5)
        with self.assertRaises(ValueError):
            localized_hb_term((5, 5), (), 2, 2, 5)

    def test_divisor_moment_dominance_and_harmonic_bounds(self):
        for n in range(1, 81):
            for a, b in ((1, 3), (2, 2), (2, 3), (3, 3)):
                self.assertLessEqual(divisor_count(n, a)*divisor_count(n, b), divisor_count(n, a*b))
            for s in (1, 2, 3):
                self.assertLessEqual(divisor_count(n, s)**2*divisor_count(n, 2), divisor_count(n, 2*s*s))
        # Exact finite H_D replaces the coarser 1+log(D) in these guards.
        d = 20
        harmonic = sum((F(1, n) for n in range(1, d+1)), F(0))
        for order in (1, 2, 3, 4):
            self.assertLessEqual(sum((F(divisor_count(n, order), n) for n in range(1, d+1)), F(0)), harmonic**order)
            self.assertLessEqual(sum(divisor_count(n, order) for n in range(1, d+1)), d*harmonic**(order-1))

    def test_weighted_type_i_pays_the_full_moment_and_outside_logs(self):
        budget = weighted_type_i_budget(3, 10, 2)
        self.assertEqual(budget.moment_log_power, 19)
        self.assertEqual(budget.required_input_log_saving, 43)
        self.assertEqual(F(budget.required_input_log_saving-budget.moment_log_power, 2)-2,
                         budget.resulting_log_saving)

    def test_positive_long_free_criterion_and_failed_short_corner_budget(self):
        gamma = F(49, 100)
        self.assertTrue(long_free_type_i(gamma, F(2, 3)))
        self.assertFalse(long_free_type_i(gamma, F(0)))
        self.assertFalse(long_free_type_i(gamma, F(51, 100)))
        self.assertTrue(long_free_type_i(gamma, F(52, 100)))
        corner = free_correlation_budget(F(1), F(1))
        self.assertEqual((corner.first, corner.second), (F(9, 5), F(15, 8)))

    def test_invalid_exact_inputs_are_rejected(self):
        for args in ((0, 2, 3), (18, True, 2), (18, 2, 0)):
            with self.assertRaises(ValueError):
                heath_brown_log_vectors(*args)
        with self.assertRaises(ValueError):
            divisor_count(4, -1)
        with self.assertRaises(ValueError):
            long_free_type_i(0.49, F(2, 3))


if __name__ == '__main__':
    unittest.main()
