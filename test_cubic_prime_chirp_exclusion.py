"""Arithmetic and normalization guards; no substitute for the source proof."""
from cmath import exp
from fractions import Fraction as F
from math import cos, pi
import unittest

from cubic_prime_chirp_exclusion import cubic_bound_budget, reciprocal_approximant


class CubicPrimeChirpExclusionTests(unittest.TestCase):
    def test_reciprocal_rounding_gives_a_reduced_admissible_fraction(self):
        # Both rounding directions, ties, near-one and large denominators.
        for value in (F(101, 100), F(149, 100), F(3, 2), F(151, 100),
                      F(201, 100), F(2000001, 2), F(100000099, 100)):
            q = reciprocal_approximant(value)
            self.assertLessEqual(abs(q-value), F(1, 2))
            self.assertLess(abs(-1/value+F(1, q)), F(1, q*q))
            self.assertEqual(F(-1, q).denominator, q)

    def test_prime_bound_keeps_the_one_half_term_and_outer_sixteenth(self):
        b = cubic_bound_budget()
        self.assertEqual(b['denominator'], F(21, 10))
        self.assertEqual(b['bracket'], -F(1, 2))
        self.assertEqual(b['harman_power'], F(1, 16))
        self.assertEqual(b['prime_total'], F(63, 64))
        self.assertLess(b['proper_power'], b['prime_total'])
        self.assertLess(b['prime_total'], 1)

    def test_epsilon_cannot_be_absorbed_without_a_strict_margin(self):
        self.assertEqual(cubic_bound_budget(epsilon=F(1, 32))['prime_total'], 1)
        self.assertGreater(cubic_bound_budget(epsilon=F(1, 16))['prime_total'], 1)
        self.assertEqual(cubic_bound_budget(t=F(1, 4))['bracket'], -F(1, 4))
        self.assertEqual(cubic_bound_budget(t=F(11, 4))['bracket'], -F(1, 4))

    def test_angular_to_e_notation_preserves_the_mixed_cubic(self):
        n_scale, t_scale, slope = 100, 17.0, 3.03
        for n in (2, 27, 50, 71, 99):
            a = n/n_scale
            angular = -t_scale*(slope*a+(a-0.5)**3)
            polynomial = (-t_scale/(2*pi*n_scale**3)*n**3
                          +3*t_scale/(4*pi*n_scale**2)*n**2
                          -t_scale*(slope+0.75)/(2*pi*n_scale)*n
                          +t_scale/(16*pi))
            self.assertAlmostEqual(abs(exp(1j*angular)-exp(2j*pi*polynomial)), 0, places=13)

    def test_model_own_phase_has_one_quarter_constant_coefficient(self):
        for phase in (0.0, 0.3, 1.2, 3.8):
            actual = (1+0.5*cos(phase))*exp(-1j*phase)
            expanded = exp(-1j*phase)+0.25+0.25*exp(-2j*phase)
            self.assertAlmostEqual(abs(actual-expanded), 0, places=14)
        self.assertEqual(cubic_bound_budget()['model_coefficient'], F(1, 4))

    def test_invalid_exact_parameters_do_not_create_a_certificate(self):
        for value in (1, F(1), F(-2), 2.5):
            with self.assertRaises(ValueError):
                reciprocal_approximant(value)
        for t, eps in ((F(0),F(1,64)), (F(3),F(1,64)), (F(9,10),F(0)),
                       (0.9,F(1,64))):
            with self.assertRaises(ValueError):
                cubic_bound_budget(t,eps)


if __name__ == '__main__':
    unittest.main()
