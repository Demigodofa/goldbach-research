"""Exact controls for the source coefficient and prime-power removal."""
from fractions import Fraction
from math import lcm
import unittest

from character_suppression import suppression_classes
from exceptional_character_model import character_values
from exceptional_pointwise_bridge import (pointwise_coefficient, proper_power_position_cap,
                                          separated_zero_ranges, density_collapse_target)
from redistribution import trial_prime


class ExceptionalPointwiseBridgeTests(unittest.TestCase):
    def test_density_collapse_target_exact_range_and_character_coefficient(self):
        for d, sign in ((31, 1), (33, 1), (35, 1), (40, 1), (40, -1),
                        (60, 1), (120, 1), (120, -1), (280, -1)):
            target = density_collapse_target(d, two_sign=sign)
            self.assertIsNotNone(target)
            self.assertEqual(target % 2, 0)
            self.assertGreaterEqual(target, d**10)
            self.assertLess(target, d**10+lcm(2, d))
            self.assertLess(target, 2*d**10)
            self.assertLess(target, d**11)  # 10 <= V < 11, without floats.
            self.assertEqual(pointwise_coefficient(d, target, two_sign=sign), 0)
            chi = character_values(d, two_sign=sign)
            r = target % d
            allowed = [a for a in range(d) if chi[a] and chi[(r-a) % d]]
            self.assertEqual(sum(chi[a]*chi[(r-a) % d] for a in allowed),
                             -len(allowed))
            # Independently exhaust the preceding short interval, not D**10.
            for n in range(d**10, target):
                if n % 2 == 0:
                    self.assertNotEqual(pointwise_coefficient(d, n, two_sign=sign), 0)

    def test_density_collapse_even_characters_need_nonmultiple_targets(self):
        for d, residue in ((33, 22), (40, 20)):
            chi = character_values(d)
            self.assertEqual(chi[-1], 1)
            self.assertEqual(pointwise_coefficient(d, 0), 2)
            self.assertEqual(pointwise_coefficient(d, residue), 0)
            target = density_collapse_target(d)
            self.assertNotEqual(target % d, 0)
            self.assertEqual(pointwise_coefficient(d, target), 0)
        self.assertEqual(density_collapse_target(40), 40**10+20)

    def test_density_collapse_empty_family_is_not_a_negative_certificate(self):
        for d in (29, 37, 41, 65, 385):
            self.assertIsNone(density_collapse_target(d))
        self.assertIn("NOT a zero detection", density_collapse_target.__doc__)

    def test_density_collapse_input_semantics(self):
        for d in (True, 24, 25, 27, 30, 32, 36, 40.0, 45):
            with self.assertRaises(ValueError):
                density_collapse_target(d)
        for d, sign in ((31, -1), (40, True), (40, 0)):
            with self.assertRaises(ValueError):
                density_collapse_target(d, two_sign=sign)

    def test_source_product_against_independent_character_periods(self):
        different_from_full_bias = False
        for d, sign in ((29, 1), (31, 1), (33, 1), (35, 1), (40, 1),
                        (40, -1), (60, 1), (65, 1), (120, 1), (120, -1),
                        (280, 1), (280, -1), (385, 1)):
            chi = character_values(d, two_sign=sign)
            for n in range(0, lcm(2, d), 2):
                allowed = [a for a in range(d) if chi[a] and chi[(n-a) % d]]
                a = len(allowed)
                b = sum(chi[x] for x in allowed)
                c = sum(chi[x]*chi[(n-x) % d] for x in allowed)
                coefficient = pointwise_coefficient(d, n, two_sign=sign)
                self.assertEqual(coefficient, 1+Fraction(c, a))
                different_from_full_bias |= coefficient != Fraction(a-2*b+c, a)
        self.assertTrue(different_from_full_bias)
        self.assertEqual(pointwise_coefficient(40, 2), 1)  # 4 does not divide2.
        self.assertEqual(pointwise_coefficient(40, 20), 0)
        self.assertEqual(pointwise_coefficient(40, 20, two_sign=-1), 2)

    def test_exact_excluded_family_empty_family_and_powers_of_two(self):
        checked = 0
        for d in range(25, 241):
            for sign in (1, -1):
                try:
                    q0, period, excluded = suppression_classes(d, two_sign=sign)
                except ValueError:
                    continue
                self.assertEqual(not excluded, d % 12 in (1, 5))
                for n in range(0, period, 2):
                    coefficient = pointwise_coefficient(d, n, two_sign=sign)
                    self.assertEqual(coefficient == 0, n in excluded)
                    if n not in excluded:
                        self.assertGreaterEqual(coefficient, Fraction(2, 3))
                for j in (1, 2, 3, 12, 101):
                    self.assertNotEqual(2**j % q0, 0)
                    self.assertGreaterEqual(pointwise_coefficient(d, 2**j, two_sign=sign),
                                            Fraction(2, 3))
                checked += 1
        self.assertGreater(checked, 70)

    def test_proper_power_removal_including_even_powers_and_center(self):
        for n in (6, 8, 10, 18, 26, 50, 98, 128, 242, 512, 1000):
            powers = set()
            for p in range(2, n):
                if not trial_prime(p):
                    continue
                value = p*p
                while value <= n:
                    powers.add(value)
                    value *= p
            contaminated = {a for a in range(1, n) if a in powers or n-a in powers}
            self.assertLessEqual(len(contaminated), proper_power_position_cap(n))
            self.assertLessEqual(2*len(powers), proper_power_position_cap(n))
            if n in (8, 18, 50, 98, 242):
                self.assertIn(n//2, contaminated)  # Proper-square center counts once.
            if n in (6, 10, 18):
                self.assertIn(2, contaminated)  # A prime2 can pair with a power of2.
        self.assertEqual(proper_power_position_cap(8), 8)

    def test_input_semantics_and_primitive_boundary(self):
        for d in (True, 24, 25, 27, 30, 32, 36, 40.0, 45):
            with self.assertRaises(ValueError):
                pointwise_coefficient(d, 2)
        for n in (True, -2, 1, 2.0):
            with self.assertRaises(ValueError):
                pointwise_coefficient(31, n)
        for d, sign in ((31, -1), (40, True), (40, 0)):
            with self.assertRaises(ValueError):
                pointwise_coefficient(d, 2, two_sign=sign)
        for n in (True, 4, 7, 8.0):
            with self.assertRaises(ValueError):
                proper_power_position_cap(n)
        self.assertIn("not a prime-count certificate", pointwise_coefficient.__doc__)

    def test_zero_range_boundary_and_required_second_zero_strength(self):
        # Synthetic conditional parameters; c=1/100 is NOT asserted to be
        # a valid numerical Landau/Page constant, and no zeros are supplied.
        c, alpha = Fraction(1, 100), Fraction(1, 2)
        self.assertTrue(separated_zero_ranges(c, 100, 100, alpha))
        self.assertFalse(separated_zero_ranges(c, 99, 100, alpha))
        self.assertFalse(separated_zero_ranges(c, 100, 99, alpha))
        self.assertFalse(separated_zero_ranges(c, 100, 100, alpha, log_gap_factor=2))
        self.assertTrue(separated_zero_ranges(c, 400, 100, alpha, log_gap_factor=2))
        self.assertTrue(separated_zero_ranges(c, 1000, 100, Fraction(1, 3)))
        self.assertFalse(separated_zero_ranges(c, 999, 100, Fraction(1, 3)))

    def test_fractional_exponents_and_independent_log_endpoint_comparison(self):
        # alpha=2/3 and eta=(10/3)^3 give eta^alpha=100/9 exactly.
        c, eta = Fraction(9, 1000), Fraction(1000, 27)
        self.assertTrue(separated_zero_ranges(c, eta, Fraction(1000, 9), Fraction(2, 3)))
        self.assertFalse(separated_zero_ranges(c, eta-Fraction(1, 10**30),
                                               Fraction(1000, 9), Fraction(2, 3)))
        # Formal logarithmic coordinates ell_i=log D_i: directly compare
        # interval endpoints; these coordinates do not assert actual zeros.
        for root in (10, 20, 30):
            strength = root*root
            for ell1 in (Fraction(1), Fraction(7, 3)):
                ell2 = Fraction(1, 100)*strength*ell1+Fraction(1, 1000)
                upper1 = root*ell1  # eta^(1-alpha)*ell1 for alpha=1/2.
                lower2 = 10*ell2
                self.assertTrue(separated_zero_ranges(Fraction(1, 100), strength,
                                                       100, Fraction(1, 2)))
                self.assertGreater(lower2, upper1)
                if root >= 20:
                    self.assertGreater(lower2, 2*upper1)

    def test_zero_range_input_semantics(self):
        for args in ((True, 100, 100, Fraction(1, 2)),
                     (0, 100, 100, Fraction(1, 2)),
                     (2, 100, 100, Fraction(1, 2)),
                     (Fraction(1, 100), 9, 100, Fraction(1, 2)),
                     (Fraction(1, 100), 100, 100.0, Fraction(1, 2)),
                     (Fraction(1, 100), 100, 100, 0),
                     (Fraction(1, 100), 100, 100, 1)):
            with self.assertRaises(ValueError):
                separated_zero_ranges(*args)
        for gap in (0, Fraction(1, 2), True, 1.0):
            with self.assertRaises(ValueError):
                separated_zero_ranges(Fraction(1, 100), 100, 100, Fraction(1, 2),
                                      log_gap_factor=gap)
        self.assertIn("False is inconclusive", separated_zero_ranges.__doc__)


if __name__ == "__main__":
    unittest.main()
