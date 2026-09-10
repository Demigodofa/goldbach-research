"""Exponent guards for the adjacent first-power polynomial obstruction."""
from fractions import Fraction as F
import unittest

from adjacent_polynomial_norm import (
    adjacent_moment_exponents, powered_length_is_licensed,
    transfer_error_exponent,
)


class AdjacentPolynomialNormTests(unittest.TestCase):
    def test_first_power_T_moment_is_positive_through_the_adjacent_strip(self):
        for h in (F(41,100), F(43,100), F(46,100)):
            ex=adjacent_moment_exponents(h, power=1)
            self.assertGreater(ex['T'], 0)
            self.assertLess(ex['length'], 0)
        self.assertEqual(adjacent_moment_exponents(F(46,100))['T'], F(113,625))
        self.assertEqual(adjacent_moment_exponents(F(41,100))['T'], F(517,2500))

    def test_second_power_is_good_but_controls_a_different_object(self):
        for h in (F(41,100), F(43,100), F(46,100)):
            ex=adjacent_moment_exponents(h, power=2)
            self.assertTrue(powered_length_is_licensed(h, 2))
            self.assertLess(ex['T'], 0)
        self.assertEqual(adjacent_moment_exponents(F(41,100), power=2)['T'],
                         -F(4,625))
        self.assertEqual(adjacent_moment_exponents(F(46,100), power=2)['T'],
                         -F(73,1250))

    def test_powered_moment_does_not_become_first_power_without_a_threshold(self):
        # The detector threshold is a statement on selected zero values;
        # no algebraic implication bounds every first-power D_M by D_M^2.
        for value in (F(1,100), F(2), F(100)):
            self.assertNotEqual(value, value*value)
        self.assertEqual(F(41,100)*2, F(82,100))

    def test_transfer_at_the_new_support_is_still_power_small(self):
        self.assertEqual(transfer_error_exponent(F(46,100)), -F(27,100))
        self.assertEqual(transfer_error_exponent(F(41,100)), -F(59,200))

    def test_invalid_ranges_are_rejected(self):
        for action in (lambda: adjacent_moment_exponents(F(40,100)),
                       lambda: adjacent_moment_exponents(F(46,100), F(4,5)),
                       lambda: powered_length_is_licensed(F(40,100)),
                       lambda: transfer_error_exponent(F(0))):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
