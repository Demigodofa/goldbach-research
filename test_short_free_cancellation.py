"""Finite combined-coefficient and actual-prime-slot guards."""
from fractions import Fraction as F
import unittest

from major_arc_kernel import _factorization, _mobius_phi
from multifactor_identity_gate import divisor_count, heath_brown_log_vectors
from short_free_cancellation import (
    cofactor_sieve_sum, combined_short_vector, cutoff_inverse, cutoff_log_vector,
    internal_power_margin, inverse_depth, prime_slot_log_vector, short_hb_vectors,
)
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector, vaughan_log_vectors


def add_vectors(vectors):
    result = {}
    for vector in vectors:
        for p, coefficient in vector:
            result[p] = result.get(p, 0)+coefficient
    return tuple((p, c) for p, c in sorted(result.items()) if c)


class ShortFreeCancellationTests(unittest.TestCase):
    def test_combined_binomial_factorization_matches_direct_short_convolutions(self):
        for order, z, t in ((2, 3, 2), (3, 5, 2), (3, 3, 4)):
            for n in (1, 2, 4, 12, 16, 18, 30, 54, 81, 108):
                self.assertEqual(add_vectors(short_hb_vectors(n, order, z, t)),
                                 combined_short_vector(n, order, z, t))

    def test_whole_short_sector_is_nonzero_while_full_identity_cancels(self):
        for order, prime in ((2, 5), (3, 5), (4, 3)):
            n = 2*prime**order
            terms = short_hb_vectors(n, order, prime, 2)
            self.assertEqual(terms[:-1], ((),)*(order-1))
            self.assertEqual(terms[-1], ((2, -1),))
            self.assertEqual(combined_short_vector(n, order, prime, 2), ((2, -1),))
            full, residual = heath_brown_log_vectors(n, order, prime)
            self.assertEqual(add_vectors(full), ())
            self.assertEqual(residual, ())

    def test_lower_orders_vanish_by_product_support_and_large_primes_are_absent(self):
        for n in (37, 54, 72, 108, 162):
            terms = short_hb_vectors(n, 3, 3, 2)
            self.assertGreater(n, (3*2)**2)
            self.assertEqual(terms[:2], ((), ()))
        for n in (35, 70, 105):
            self.assertEqual(add_vectors(short_hb_vectors(n, 3, 5, 2)), ())

    def test_truncated_log_derivative_is_not_the_prime_weight(self):
        self.assertEqual(cutoff_log_vector(4, 2), ((2, -1),))
        self.assertEqual(mangoldt_log_vector(4), ((2, 1),))
        self.assertEqual(cutoff_log_vector(8, 2), ((2, 1),))
        for n in (3, 6, 12, 15):
            self.assertEqual(cutoff_log_vector(n, 2), ())

    def test_inverse_is_exact_and_has_a_fixed_depth_divisor_majorant(self):
        for t in (2, 3, 5):
            for n in range(1, 61):
                self.assertEqual(sum(cutoff_inverse(n//d, t) for d in _divisors(n) if d <= t), int(n == 1))
                depth = inverse_depth(n, t)
                self.assertLessEqual(abs(cutoff_inverse(n, t)), (depth+1)*divisor_count(n, 2*depth+1))
        self.assertEqual(inverse_depth(26, 2), 2)
        self.assertEqual(inverse_depth(27, 2), 3)

    def test_prime_slot_matches_direct_large_mobius_prime_tuples(self):
        for n in (20, 25, 30, 49, 72, 77, 100, 105, 210):
            for w in (2, 3, 5):
                direct = []
                for p, _ in _factorization(n):
                    if p > w:
                        direct.append(((p, sum(_mobius_phi(a)[0] for a in _divisors(n//p) if a > w)),))
                self.assertEqual(prime_slot_log_vector(n, w), add_vectors(direct))
        self.assertEqual(prime_slot_log_vector(77, 3), ((7, -1), (11, -1)))
        self.assertEqual(prime_slot_log_vector(49, 3), ((7, -1),))
        self.assertEqual(prime_slot_log_vector(79, 3), ())

    def test_internal_prime_powers_and_signed_cofactor_weight_are_not_dropped_exactly(self):
        self.assertEqual(vaughan_log_vectors(72, 3, 3)[3], ((2, 1),))
        self.assertEqual(prime_slot_log_vector(72, 3), ())
        self.assertEqual(vaughan_log_vectors(20, 3, 3)[3], ((2, -1),))
        self.assertEqual(prime_slot_log_vector(20, 3), ())
        self.assertEqual(cofactor_sieve_sum(1, 3), 1)
        for n in (2, 3):
            self.assertEqual(cofactor_sieve_sum(n, 3), 0)
        self.assertEqual(cofactor_sieve_sum(6, 3), -1)
        self.assertEqual(cofactor_sieve_sum(5, 3), 1)
        self.assertGreater(internal_power_margin(F(49, 100), F(1, 4800)), 0)

    def test_invalid_exact_inputs_are_rejected(self):
        for args in ((0, 2, 3, 2), (18, True, 3, 2), (18, 2, 3, 0)):
            with self.assertRaises(ValueError):
                short_hb_vectors(*args)
        with self.assertRaises(ValueError):
            internal_power_margin(F(1, 2), F(1, 4800))


if __name__ == '__main__':
    unittest.main()
