import cmath
import unittest
from fractions import Fraction as F
from math import gcd, pi

from prime_band_vaughan_type_i import (
    band_type_i_budgets,
    continued_active_kernel_parseval_energy,
    mobius_tail_log_vector,
    twisted_vaughan_log_vectors,
    unit_residue_deviations,
)


class PrimeBandVaughanTypeITests(unittest.TestCase):
    def test_full_family_type_i_exponents_fit_the_absolute_benchmark(self):
        result = band_type_i_budgets()
        self.assertEqual(result["linear_type_i"], F(337, 250))
        self.assertEqual(result["grouped_type_i"], F(749, 500))
        self.assertEqual(result["absolute_band_benchmark"], F(1499, 1000))
        self.assertEqual(result["grouped_margin"], F(1, 1000))
        self.assertEqual(result["proper_powers"], result["absolute_band_benchmark"])
        self.assertEqual(result["mobius_split_mobius_cutoff"], F(3, 20))
        self.assertEqual(result["mobius_split_type_i"], F(749, 500))
        self.assertTrue(result["mobius_split_grouped_term_zero"])
        self.assertFalse(result["type_ii_energy_proved"])
        self.assertFalse(result["relative_band_conjecture_proved"])

    def test_constant_progressions_have_unit_residue_spread_at_most_one(self):
        for modulus in (5, 10, 21, 35):
            deviations = dict(unit_residue_deviations(modulus, 37, 311))
            values = tuple(deviations.values())
            self.assertEqual(sum(values, F(0)), 0)
            self.assertLessEqual(max(values) - min(values), 1)

    def test_continued_active_kernel_parseval_matches_direct_fourier_sum(self):
        d, m, c = 6, 5, 7
        deviations = unit_residue_deviations(d * m, 19, 173)
        exact = continued_active_kernel_parseval_energy(d, m, c, deviations)
        values = dict(deviations)
        inverse_m = pow(m, -1, d)
        direct = 0.0
        for h in range(d * m):
            transform = sum(
                float(value)
                * (cmath.exp(-2j * pi * h * c * residue / (d * m))
                   + cmath.exp(-2j * pi * h * inverse_m * c * residue / d) / (m - 1))
                for residue, value in values.items()
            )
            direct += abs(transform) ** 2
        self.assertAlmostEqual(direct, float(exact), places=8)

    def test_low_term_does_not_break_continued_kernel_energy_bound(self):
        for d, m, c in ((1, 5, 2), (2, 5, 3), (3, 5, 2), (6, 5, 7)):
            q = d * m
            deviations = unit_residue_deviations(q, 17, 197)
            exact = continued_active_kernel_parseval_energy(d, m, c, deviations)
            square_mass = sum((value * value for _, value in deviations), F(0))
            self.assertLessEqual(exact, 4 * q * square_mass)

    def test_coprimality_twist_keeps_or_annihilates_all_four_terms(self):
        for n in range(2, 80):
            terms = twisted_vaughan_log_vectors(n, 5, 7, 30)
            if gcd(n, 30) != 1:
                self.assertEqual(terms, ((), (), (), ()))
            else:
                combined = {}
                for term in terms:
                    for prime, coefficient in term:
                        combined[prime] = combined.get(prime, 0) + coefficient
                combined = tuple((p, c) for p, c in sorted(combined.items()) if c)
                expected = twisted_vaughan_log_vectors(n, n, n, 1)[0]
                self.assertEqual(combined, expected)

    def test_u_one_split_is_exact_mobius_inversion_with_no_grouped_term(self):
        for cutoff in (2, 5, 10):
            for n in range(2, 100):
                low, linear, subtracted, tail = twisted_vaughan_log_vectors(
                    n, 1, cutoff, 1
                )
                self.assertEqual(low, ())
                self.assertEqual(subtracted, ())
                self.assertEqual(tail, mobius_tail_log_vector(n, cutoff))
                combined = {}
                for term in (linear, tail):
                    for prime, coefficient in term:
                        combined[prime] = combined.get(prime, 0) + coefficient
                combined = tuple((p, c) for p, c in sorted(combined.items()) if c)
                expected = twisted_vaughan_log_vectors(n, n, n, 1)[0]
                self.assertEqual(combined, expected)


if __name__ == "__main__":
    unittest.main()
