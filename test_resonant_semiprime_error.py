"""Exact algebra/support guards; no sampled prime-correlation experiment."""
from fractions import Fraction as F
from math import gcd
import unittest

from resonant_semiprime_error import (
    primitive_progression_pair, resonant_exponents, resonant_rows, resonant_value_pair,
    weighted_progression_energy,
)


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


if __name__ == '__main__':
    unittest.main()
