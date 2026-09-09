"""Exact local/normalization checks, not evidence of exceptional prime density."""
from fractions import Fraction as F
from math import gcd
import unittest

from rare_affine_small_cofactor import (affine_orientation_densities,
                                       affine_residue_factor,
                                       aggregate_weil_exponents)


def chi31(n):
    value = pow(n, 15, 31)
    return -1 if value == 30 else value


class RareAffineSmallCofactorTests(unittest.TestCase):
    def test_four_orientation_mean_against_independent_affine_character_formula(self):
        saw_cancellation = False
        for m in (31, 42, 62, 93):
            for multiplier in (1, 3, 7, 9, 11):
                k = F(4*sum(chi31(a) == chi31(m-multiplier*a) == 1
                            for a in range(31)), 31)
                for a, c in ((1, 1), (2, 5), (3, 7), (7, 2), (9, 11)):
                    if gcd(multiplier*a, c) != 1:
                        continue
                    terms = affine_orientation_densities(31, multiplier, m, a, c)
                    self.assertEqual(sum(terms), F(chi31(a)*chi31(c), a*c)*k)
                    saw_cancellation |= sum(map(abs, terms)) > abs(sum(terms))
        self.assertTrue(saw_cancellation)

    def test_conductor_unit_density_is_preserved_under_multiplier_permutation(self):
        for conductor in (4, 8, 12, 24, 31, 35, 40):
            for m in (2, 6, conductor, 2*conductor):
                unit_count = sum(gcd(a, conductor) == gcd(m-a, conductor) == 1
                                 for a in range(conductor))
                for multiplier in (1, 3, 7, 11, 13):
                    if gcd(multiplier, conductor) != 1:
                        continue
                    k, density = affine_residue_factor(conductor, multiplier, m)
                    self.assertEqual(density, F(unit_count, conductor))
                    self.assertGreaterEqual(k, 0)
                    self.assertLessEqual(k, 4*density)
        # For chi31(-1)=-1 and m=62, negative M synchronizes rare signs;
        # positive M instead forces them to be opposite. Finite residues only.
        self.assertEqual(affine_residue_factor(31, 3, 62)[0], F(60, 31))
        self.assertEqual(affine_residue_factor(31, 7, 62)[0], 0)

    def test_jacobian_and_prime_power_multiplier_are_retained(self):
        # A missing 1/a would multiply the density by7. M=27 is a prime
        # power, allowed by the theorem's cofactor family (at suitable scale).
        multiplier, m, a, c = 27, 62, 7, 2
        k, _ = affine_residue_factor(31, multiplier, m)
        value = sum(affine_orientation_densities(31, multiplier, m, a, c))
        self.assertNotEqual(k, 0)
        self.assertEqual(value, F(chi31(a)*chi31(c), a*c)*k)
        self.assertNotEqual(value, F(chi31(a)*chi31(c), c)*k)

    def test_method_budgets_and_strict_input_domains(self):
        self.assertEqual(aggregate_weil_exponents(F(1, 5)),
                         (F(19, 20), F(9, 10), F(44, 45)))
        self.assertEqual(aggregate_weil_exponents(F(1, 4))[0], 1)
        self.assertEqual(aggregate_weil_exponents(F(1, 3))[1], 1)
        self.assertEqual(aggregate_weil_exponents(F(13, 25))[1], F(57, 50))
        for bad in (True, -1, F(3, 2), 0.2):
            with self.assertRaises(ValueError):
                aggregate_weil_exponents(bad)
        with self.assertRaises(ValueError):
            affine_residue_factor(31, 31, 62)
        with self.assertRaises(ValueError):
            affine_orientation_densities(31, 3, 62, 2, 6)
        with self.assertRaises(ValueError):
            affine_orientation_densities(31, 3, 62, 31, 2)


if __name__ == "__main__":
    unittest.main()
