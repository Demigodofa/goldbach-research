"""Guards for the analytic countermodel, not evidence about actual primes."""
from cmath import exp
from fractions import Fraction as F
from math import cos, pi, sqrt
import unittest

from analytic_complementary_phase import (
    analytic_phase, derivative_order_for_cell, phase_derivative, probe_exponent,
)


class AnalyticComplementaryPhaseTests(unittest.TestCase):
    def test_complementary_phase_and_reflected_derivative_identities(self):
        for slope in (2.1, 3.0, 3.7):
            for j in range(-20, 31):
                a = j/10
                self.assertAlmostEqual(analytic_phase(a,slope)+analytic_phase(1-a,slope),
                                       slope, places=13)
                self.assertAlmostEqual(phase_derivative(a,slope,1),
                                       phase_derivative(1-a,slope,1), places=13)
                self.assertGreater(phase_derivative(a,slope,1), 0)

    def test_linear_correction_preserves_the_required_central_frequency(self):
        self.assertEqual(analytic_phase(0.5,3.0), 1.5)
        self.assertEqual(phase_derivative(0.5,3.0,1), 3.0)
        for a in (0.49, 0.5, 0.51):
            local = a*phase_derivative(a,3.0,1)
            self.assertGreater(local, 1.4)
            self.assertLess(local, 1.6)

    def test_each_quarter_cell_has_a_uniformly_nonzero_selected_derivative(self):
        # Endpoints guard the transitions where a single derivative can vanish.
        for degree in range(1, 13):
            for cell in range(-12, 13):
                order = derivative_order_for_cell(degree,cell)
                self.assertIn(order, (degree+1,degree+2))
                for step in range(9):
                    a = 0.5+(cell+step/8)*pi/4
                    self.assertGreaterEqual(abs(phase_derivative(a,3.0,order)),
                                            1/sqrt(2)-2e-14)
        self.assertEqual(phase_derivative(0.5,3.0,4), 0)
        self.assertEqual(abs(phase_derivative(0.5,3.0,5)), 1)

    def test_probe_exponents_save_a_power_only_with_degree_fixed(self):
        self.assertEqual(probe_exponent(1), F(7,10))
        self.assertEqual(probe_exponent(3), F(41,50))
        previous = F(0)
        for degree in range(1, 101):
            current = probe_exponent(degree)
            self.assertGreater(current, previous)
            self.assertLess(current, 1)
            previous = current
        self.assertLess(1-probe_exponent(100), F(1,100))

    def test_linear_reduction_preserves_lattice_values_and_alias_separation(self):
        for angle in (-17.3, -pi, pi, 24.7):
            reduced = (angle+pi) % (2*pi)-pi
            for n in range(1, 12):
                self.assertAlmostEqual(abs(exp(-1j*angle*n)-exp(-1j*reduced*n)),
                                       0, places=12)
            for k in (-9,-2,-1,1,2,9):
                self.assertGreaterEqual(abs(reduced+2*pi*k), pi*abs(k)-1e-14)

    def test_paired_main_keeps_the_negative_one_eighth_factor(self):
        t_scale, odd = 30, 29
        slope = pi*odd/t_scale
        for a in (0.3,0.5,0.7):
            paired = exp(1j*t_scale*analytic_phase(a,slope))
            paired *= exp(1j*t_scale*analytic_phase(1-a,slope))
            self.assertAlmostEqual(paired.real, -1, places=13)
            self.assertAlmostEqual(paired.imag, 0, places=13)
        self.assertEqual(2*F(1,4)**2, F(1,8))

    def test_invalid_parameters_do_not_claim_uniform_increasing_degree(self):
        for degree in (0,-1,3.0,True):
            with self.assertRaises(ValueError):
                probe_exponent(degree)
            with self.assertRaises(ValueError):
                derivative_order_for_cell(degree,0)
        with self.assertRaises(ValueError):
            phase_derivative(0.5,3.0,0)
        with self.assertRaises(ValueError):
            derivative_order_for_cell(3,0.5)


if __name__ == '__main__':
    unittest.main()
