"""Exact complementary-phase guards; no prime or zero computations."""
from cmath import exp
from fractions import Fraction as F
from math import cos, pi
import unittest

from complementary_window_chirp import local_frequency, model_budget, phase


class ComplementaryWindowChirpTests(unittest.TestCase):
    def test_complementary_phase_is_constant_even_when_local_frequency_varies(self):
        for slope in (F(29,10),F(3),F(31,10)):
            for j in range(21):
                a=F(j,20)
                self.assertEqual(phase(a,slope)+phase(1-a,slope),slope)
        self.assertNotEqual(local_frequency(F(2,5),F(3)),local_frequency(F(3,5),F(3)))

    def test_cubic_derivative_survives_every_linear_fourier_modulation(self):
        for a,h,slope in ((F(1,4),F(1,20),F(3)),(F(1,2),F(1,100),F(-17))):
            third=(phase(a+3*h,slope)-3*phase(a+2*h,slope)
                   +3*phase(a+h,slope)-phase(a,slope))
            self.assertEqual(third,6*h**3)

    def test_both_window_frequencies_overlap_the_positive_chi_support(self):
        for a in (F(49,100),F(1,2),F(51,100)):
            self.assertGreater(local_frequency(a,F(3)),F(7,5))
            self.assertLess(local_frequency(a,F(3)),F(8,5))
        self.assertEqual(local_frequency(F(1,2),F(3)),F(3,2))

    def test_positive_cosine_side_has_half_the_modulation_amplitude(self):
        # Finite Fourier fixture guards the angular sign and epsilon/2.
        samples,mode,epsilon=64,7,0.5
        coefficient=sum((1+epsilon*cos(2*pi*mode*j/samples))
                        *exp(-2j*pi*mode*j/samples) for j in range(samples))/samples
        self.assertAlmostEqual(coefficient.real,epsilon/2,places=14)
        self.assertAlmostEqual(coefficient.imag,0,places=14)

    def test_odd_phase_and_beta_weights_give_the_negative_one_eighth_factor(self):
        epsilon=F(1,2)
        # a=9/25 makes both square roots rational.
        prefactor=2*(epsilon/2*F(3,5))*(epsilon/2*F(4,5))/F(12,25)
        self.assertEqual(prefactor,F(1,8))
        for k in (1,3,11,101):
            self.assertAlmostEqual(exp(1j*pi*k).real,-1,places=13)

    def test_every_error_is_below_the_paired_main_and_fourier_bound_saves_a_power(self):
        b=model_budget()
        self.assertEqual(b['sum_to_integral'],F(2,5))
        self.assertEqual(b['local_linearization'],-F(2,5))
        self.assertEqual(b['paired_cross_error'],F(9,10))
        self.assertEqual(b['global_fourier'],F(7,10))
        self.assertEqual(b['slope_replacement'],F(1,10))
        self.assertEqual(b['paired_prefactor'],F(1,8))
        self.assertLess(b['paired_cross_error'],1)


if __name__ == '__main__':
    unittest.main()
