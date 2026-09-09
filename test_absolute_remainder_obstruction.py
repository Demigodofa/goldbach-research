"""Finite normalization and support guards for the absolute-mass obstruction."""
from fractions import Fraction as F
import unittest

from absolute_remainder_obstruction import (
    absolute_mass_constants, finite_singular_average, prime_model_pair,
    prime_partner_budget, prime_triple_geometry, singular_local_cancellation,
)
from major_arc_kernel import sampled_kernel
from optimized_cofactor_cutoff import cofactor_weight, cutoff_prime_vector, cutoff_vaughan_vectors, optimal_cutoff
from unexceptional_vaughan_gate import vaughan_log_vectors


class AbsoluteRemainderObstructionTests(unittest.TestCase):
    def test_prime_model_value_is_constant_but_composite_values_need_not_be(self):
        samples = (0, 1, 1, F(1, 2), F(1, 3), F(1, 4))
        for q in (7, 11, 769, 773):
            direct, constant = prime_model_pair(q, samples)
            self.assertEqual(direct, constant)
            self.assertEqual(constant, F(37, 16))
        self.assertEqual(sampled_kernel(6, 1, samples), F(-7, 16))

    def test_explicit_delta_and_scale_conditions_pay_the_prime_error(self):
        for bound, delta, inverse_log in ((F(1), F(1, 4800), F(1, 40)),
                                          (F(100), F(1, 8000), F(1, 4000))):
            upper, lower = prime_partner_budget(bound, delta, inverse_log)
            self.assertLessEqual(upper, F(1, 4))
            self.assertGreaterEqual(lower, F(1, 2))
        with self.assertRaises(ValueError):
            prime_partner_budget(F(100), F(1, 4800), F(1, 4000))
        with self.assertRaises(ValueError):
            prime_partner_budget(F(1), F(1, 4800), F(1, 39))

    def test_actual_rough_semiprime_coefficient_survives_every_sampled_cutoff(self):
        for weights in ((0, 1, -1, -1, 0, -1), optimal_cutoff(5)[0],
                        (0, 1, F(1, 2), F(-1, 3), F(1, 4), 0)):
            for c in (13, 59):
                self.assertEqual(cofactor_weight(c, weights), 1)
            expected = ((13, -1), (59, -1))
            self.assertEqual(cutoff_vaughan_vectors(767, 5, weights)[3], expected)
            self.assertEqual(cutoff_prime_vector(767, 5, weights), expected)
        self.assertEqual(vaughan_log_vectors(767, 5, 5)[3], ((13, -1), (59, -1)))

    def test_prime_triple_maps_into_the_central_even_target_without_factor_ambiguity(self):
        n, target, first, second = prime_triple_geometry(1000, 13, 59, 769, 5)
        self.assertEqual((n, target), (767, 1536))
        self.assertEqual((first, second), (F(767, 1000), F(769, 1000)))
        self.assertEqual(target % 2, 0)
        self.assertNotEqual(target % 13, 0)
        self.assertNotEqual(target % 59, 0)
        # W=5 also fits gamma=49/100 with exact integer-power comparisons.
        self.assertLessEqual(5**200, 1000**49)
        self.assertLess(1000**49, 6**200)
        with self.assertRaises(ValueError):
            prime_triple_geometry(1000, 59, 13, 769, 5)

    def test_singular_series_average_has_exact_euler_normalization(self):
        for p in (3, 5, 7, 11, 17):
            self.assertEqual(singular_local_cancellation(p), 1)
        for y in (1, 7, 30, 100):
            for primes in ((), (3,), (3, 5, 7, 11)):
                direct, expanded, bound = finite_singular_average(y, primes)
                self.assertEqual(direct, expanded)
                self.assertLessEqual(direct, bound)
        with self.assertRaises(ValueError):
            finite_singular_average(10, (2, 3))

    def test_average_and_target_constants_do_not_drop_a_prime_log_or_factor_two(self):
        self.assertEqual(absolute_mass_constants(), (F(1, 16000), F(1, 32000)))
        with self.assertRaises(ValueError):
            prime_model_pair(5, (0, 1, 1, 1, 1, 1))


if __name__ == '__main__':
    unittest.main()
