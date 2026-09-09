"""Exact controls for rare-sign residues and partner conditions only."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from character_suppression import suppression_classes
from exceptional_character_model import character_values
from major_arc_kernel import _factorization, _mobius_phi
from rare_prime_sieve import rare_sieve_density, rough_factor_limit, suppressed_residue_split
from redistribution import trial_prime


class RarePrimeSieveTests(unittest.TestCase):
    def test_suppressed_classes_have_opposite_signs_and_half_or_full_units(self):
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1), (105, 1), (120, 1)):
            _, period, residues = suppression_classes(conductor, two_sign=sign)
            self.assertTrue(residues)
            chi = character_values(conductor, two_sign=sign)
            for residue in residues:
                proportion, positive, negative = suppressed_residue_split(conductor, residue,
                                                                          two_sign=sign)
                self.assertIn(proportion, (F(1), F(1, 2)))
                self.assertEqual(len(positive), len(negative))
                self.assertTrue(all(chi[(residue-a) % conductor] == -1 for a in positive))
                self.assertTrue(all(chi[(residue-a) % conductor] == 1 for a in negative))
                self.assertEqual({(residue-a) % conductor for a in positive}, set(negative))
                self.assertEqual(suppressed_residue_split(conductor, residue+period,
                                                         two_sign=sign)[0], proportion)
        self.assertEqual(suppressed_residue_split(33, 22)[0], F(1, 2))
        self.assertEqual(suppressed_residue_split(31, 62)[0], 1)

    def test_sieve_densities_by_independent_complete_crt_counts(self):
        for conductor, target, sign in ((31, 62, 1), (33, 22, 1),
                                        (40, 20, 1), (40, 40, -1), (120, 20, 1)):
            chi = character_values(conductor, two_sign=sign)
            _, positive, _ = suppressed_residue_split(conductor, target, two_sign=sign)
            phi_d = sum(bool(value) for value in chi)
            base_density = F(len(positive), phi_d)
            for divisor in range(1, 16):
                if _mobius_phi(divisor)[0] == 0:
                    continue
                period = lcm(conductor, divisor)
                units = [a for a in range(period) if gcd(a, period) == 1]
                count = sum(chi[a % conductor] == 1 and gcd(target-a, conductor) == 1
                            and (target-a) % divisor == 0 for a in units)
                direct = F(count, len(units))/base_density
                self.assertEqual(rare_sieve_density(conductor, target, divisor, two_sign=sign),
                                 direct)
        self.assertEqual(rare_sieve_density(31, 62, 31), 0)
        self.assertEqual(rare_sieve_density(31, 62, 2), 0)
        self.assertEqual(rare_sieve_density(31, 62, 3), F(1, 2))

    def test_actual_small_prime_pairs_are_twice_the_positive_first_part(self):
        representations = 0
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1)):
            _, period, residues = suppression_classes(conductor, two_sign=sign)
            chi = character_values(conductor, two_sign=sign)
            for residue in residues:
                target = residue+6*period
                upper = (2*target+2)//3
                interval = [n for n in range(upper//2+1, upper+1)
                            if upper//2 < target-n <= upper]
                self.assertTrue(all(n > conductor and target-n > conductor for n in interval))
                actual = [n for n in interval if trial_prime(n) and trial_prime(target-n)]
                positive = [n for n in actual if chi[n % conductor] == 1]
                self.assertEqual(len(actual), 2*len(positive))
                self.assertTrue(all(chi[n % conductor]*chi[(target-n) % conductor] == -1
                                    for n in actual))
                self.assertNotIn(target//2, actual)
                representations += len(actual)
        self.assertGreater(representations, 0)

    def test_composite_partner_guard_and_repeated_factor_bounds(self):
        chi = character_values(31)
        for prime, partner, cutoff in ((1459, 1331, 10), (281, 215, 4)):
            self.assertTrue(trial_prime(prime))
            self.assertFalse(trial_prime(partner))
            self.assertEqual(chi[prime % 31], 1)
            self.assertEqual(chi[partner % 31], -1)
            self.assertEqual((prime+partner) % 62, 0)
            factors = _factorization(partner)
            self.assertTrue(all(p > cutoff for p, _ in factors))
            self.assertLessEqual(sum(exponent for _, exponent in factors),
                                 rough_factor_limit(partner, cutoff))
        self.assertEqual(_factorization(1331), ((11, 3),))
        self.assertEqual(chi[11], -1)
        self.assertEqual((chi[5], chi[43 % 31]), (1, -1))
        self.assertEqual([rough_factor_limit(n, 10) for n in (120, 121, 1330, 1331)],
                         [1, 2, 2, 3])

    def test_scope_and_exact_input_boundaries(self):
        for conductor, target, sign in ((24, 0, 1), (25, 0, 1), (31, 2, 1),
                                        (37, 74, 1), (33, 11, 1), (40, 20, True)):
            with self.assertRaises(ValueError):
                suppressed_residue_split(conductor, target, two_sign=sign)
        for divisor in (0, True, 1.0, 4, 9):
            with self.assertRaises(ValueError):
                rare_sieve_density(31, 62, divisor)
        for upper, cutoff in ((0, 2), (100, 1), (True, 2), (100, 2.0)):
            with self.assertRaises(ValueError):
                rough_factor_limit(upper, cutoff)
        self.assertIn("not an actual count", rare_sieve_density.__doc__)


if __name__ == "__main__":
    unittest.main()
