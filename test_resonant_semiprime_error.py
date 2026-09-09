"""Exact algebra/support guards; no sampled prime-correlation experiment."""
from fractions import Fraction as F
from math import gcd
import unittest

from resonant_semiprime_error import (
    complete_divisor_layer_vectors, conditional_resonance_terms, resonance_power_gaps,
    primitive_progression_pair, resonant_exponents, resonant_rows, resonant_value_pair,
    weighted_progression_energy,
)
from optimized_cofactor_cutoff import cutoff_prime_vector, cutoff_vaughan_vectors
from unexceptional_vaughan_gate import mangoldt_log_vector


def vector_difference(left, right):
    result = dict(left)
    for p, coefficient in right:
        result[p] = result.get(p, F(0))-coefficient
    return tuple((p, coefficient) for p, coefficient in sorted(result.items()) if coefficient)


class ResonantSemiprimeErrorTests(unittest.TestCase):
    def test_full_denominator_equals_the_two_centered_divisor_counts(self):
        for n in (0, 1, 7, 21, 35, 77, 105, 231, 385):
            direct, factored = resonant_value_pair(n, (7, 11), (3, 5))
            self.assertEqual(direct, factored)
        self.assertEqual(resonant_value_pair(21, (7,), (3,))[0], F(4, 7))
        with self.assertRaises(ValueError):
            resonant_value_pair(10, (7,), (7,))

    def test_partial_prime_resonances_cancel_but_full_modulus_resonance_remains(self):
        for step in (1, 3, 7, 14, 21, 42):
            for shift in (0, 1, 3):
                period = 21//gcd(21, step)
                total, mean_total, bound = primitive_progression_pair(7, 3, shift, step, 0, period-1)
                self.assertEqual(total, mean_total)
                if step % 21:
                    self.assertEqual(total, 0)
                self.assertLess(bound, 2)
        total, mean, _ = primitive_progression_pair(7, 3, 0, 21, 0, 4)
        self.assertEqual(total, mean)
        self.assertEqual(total, F(20, 7))

    def test_incomplete_intervals_have_bounded_discrepancy_even_at_shared_primes(self):
        for step in (1, 3, 7, 14):
            for first, last in ((-3, 2), (0, 0), (2, 18), (100, 137)):
                total, mean, bound = primitive_progression_pair(7, 3, 4, step, first, last)
                self.assertEqual(mean, 0)
                self.assertLessEqual(abs(total), bound)

    def test_type_i_and_fourier_savings_coexist_with_a_variance_violation_gap(self):
        ti, fourier, lower, target, gap = resonant_exponents()
        self.assertEqual(ti, F(49507, 50000))
        self.assertEqual(fourier, F(25009, 50000))
        self.assertLess(fourier, 1-F(1, 4096))
        self.assertEqual(lower-target, gap)
        self.assertEqual(gap, F(1, 25000))
        self.assertGreater(gap, 0)
        with self.assertRaises(ValueError):
            resonant_exponents(F(1, 2))

    def test_finite_rows_reinforce_instead_of_canceling(self):
        rows = resonant_rows(200, (7, 11), (3, 5))
        self.assertTrue(all(value > 0 for row in rows.values() for value in row))
        variance = sum((sum(row, F(0))**2 for row in rows.values()), F(0))
        diagonal = sum((value**2 for row in rows.values() for value in row), F(0))
        cross = sum((2*row[i]*row[j] for row in rows.values()
                     for i in range(len(row)) for j in range(i+1, len(row))), F(0))
        self.assertEqual(variance, diagonal+cross)
        self.assertGreater(cross, 0)
        with self.assertRaises(ValueError):
            resonant_rows(201, (7,), (3,))

    def test_weighted_energy_uses_density_weights_and_exact_y_normalization(self):
        coefficients = {21: F(2, 3), 35: F(4, 5)}
        y = 200
        # Equal relative progression errors e_r=1 give equality in Cauchy.
        rows = {r: (F(y, r),) for r in coefficients}
        total, mass, energy, diagonal = weighted_progression_energy(y, coefficients, rows)
        self.assertEqual(total, y*mass)
        self.assertEqual(energy, mass)
        self.assertEqual(energy, diagonal)
        self.assertEqual(total**2, y*y*mass*energy)
        resonant = resonant_rows(y, (7, 11), (3, 5))
        coeffs = {r: F(1, 2) for r in resonant}
        total, mass, energy, diagonal = weighted_progression_energy(y, coeffs, resonant)
        self.assertLessEqual(total**2, y*y*mass*energy)
        self.assertGreater(energy, diagonal)
        with self.assertRaises(ValueError):
            weighted_progression_energy(y, {21: -1}, {21: (1,)})

    def test_complete_layers_match_cutoff_change_including_composite_divisors(self):
        weights = (0, 1, F(-2, 3), F(-1, 2), F(1, 4), F(-1, 5))
        for indices in ((3,), (2, 4), (2, 3, 4, 5)):
            changed = tuple(0 if d in indices else value for d, value in enumerate(weights))
            for n in (7, 14, 21, 28, 63, 105, 147, 231, 300):
                full, prime, compensation = complete_divisor_layer_vectors(n, 5, weights, indices)
                self.assertEqual(full, compensation)
                self.assertEqual(full, vector_difference(cutoff_vaughan_vectors(n, 5, weights)[3],
                                                        cutoff_vaughan_vectors(n, 5, changed)[3]))
                self.assertEqual(prime, vector_difference(cutoff_prime_vector(n, 5, weights),
                                                         cutoff_prime_vector(n, 5, changed)))
        with self.assertRaises(ValueError):
            complete_divisor_layer_vectors(7, 5, weights, (1,))

    def test_full_prime_range_and_internal_proper_powers_cannot_be_silently_dropped(self):
        weights = (0, 1, 0, F(-1, 2))
        full, prime, compensation = complete_divisor_layer_vectors(231, 5, weights, (3,))
        self.assertEqual(full, ((7, F(1, 2)), (11, F(1, 2))))
        self.assertEqual(prime, full)
        self.assertEqual(compensation, full)
        # Keeping only p=7 discards a nonzero piece of the exact layer.
        self.assertNotEqual(((7, F(1, 2)),), compensation)
        full, prime, compensation = complete_divisor_layer_vectors(147, 5, weights, (3,))
        self.assertEqual(full, ((7, 1),))  # internal b=7 and b=49
        self.assertEqual(prime, ((7, F(1, 2)),))
        self.assertEqual(compensation, full)
        self.assertEqual(cutoff_prime_vector(113, 5, (0, 1)), ())

    def test_extra_prime_product_is_present_outside_the_admissible_window(self):
        for n in (21, 105, 231, 1155):
            terms = conditional_resonance_terms(n, 7, 3, (7, 11), (3, 5))
            self.assertEqual(sum(terms, F(0)), resonant_value_pair(n, (7, 11), (3, 5))[0])
            self.assertEqual(terms[3], int(n == 1155))
        left_gap, right_gap, extra_pair, error = resonance_power_gaps()
        for below, above in (left_gap, right_gap):
            self.assertLess(below, 1)
            self.assertGreater(above, 1)
        self.assertGreater(extra_pair, 1)
        self.assertEqual(error, F(5001, 6250))
        self.assertLess(error, 1)

    def test_prime_power_support_uses_power_gaps_not_just_prime_support(self):
        # Y=1000, bases 13 and 7: all listed Lambda witnesses avoid the bands.
        for n in (509, 512, 529, 625, 729, 841, 961, 997):
            self.assertTrue(mangoldt_log_vector(n))
            self.assertEqual(resonant_value_pair(n, (13,), (7,))[0], F(1, 91))
        # A different window admits 3^4=81; constancy must then fail.
        self.assertTrue(mangoldt_log_vector(81))
        self.assertNotEqual(resonant_value_pair(81, (7,), (3,))[0], F(1, 21))


if __name__ == '__main__':
    unittest.main()
