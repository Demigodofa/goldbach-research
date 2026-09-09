"""Phase, cell, normalization and budget guards; not a prime experiment."""
from fractions import Fraction as F
from math import cos, pi, sin
import unittest

from rapid_complementary_phase import (
    cell_derivative_order, rapid_derivative, rapid_model_budget, rapid_phase,
)


class RapidComplementaryTests(unittest.TestCase):
    def test_complementary_phase_is_exact_for_noninteger_frequency(self):
        for k in (3.7,17.25,53.5):
            for a in (0.25,0.37,0.5,0.63,0.75):
                self.assertAlmostEqual(rapid_phase(a,3.01,k)+
                                       rapid_phase(1-a,3.01,k),3.01,places=13)
                self.assertAlmostEqual(rapid_derivative(a,3.01,k,1),
                                       rapid_derivative(1-a,3.01,k,1),places=12)

    def test_each_cell_selects_a_uniform_nonvanishing_derivative(self):
        for cell in range(-12,13):
            order=cell_derivative_order(cell)
            for sample in range(9):
                angle=(cell+sample/8)*pi/4
                selected=sin(angle) if order == 2 else cos(angle)
                self.assertGreaterEqual(abs(selected),2**-0.5-1e-14)

    def test_growth_is_outside_the_common_C3_class(self):
        for k in (10,100,1000):
            self.assertEqual(rapid_derivative(0.5,3,k,1),4)
            self.assertEqual(rapid_derivative(0.5,3,k,2),0)
            self.assertEqual(rapid_derivative(0.5,3,k,3),-k*k)
            self.assertAlmostEqual(rapid_derivative(0.5+pi/(2*k),3,k,2),-k)

    def test_every_new_window_error_is_paid(self):
        b=rapid_model_budget()
        self.assertEqual(b['window_discretization'],F(2,5))
        self.assertEqual(b['window_phase_taylor'],-F(3,10))
        self.assertEqual(b['window_fourier_tail'],-F(3,2))
        self.assertEqual(F(1,2)+b['window_discretization'],b['paired_cross_error'])
        self.assertEqual(b['periodic_averaging_error'],b['paired_cross_error'])

    def test_partition_count_and_euler_error_are_not_dropped(self):
        b=rapid_model_budget()
        self.assertEqual(b['second_derivative_integral'],-F(2,5))
        self.assertEqual(b['third_derivative_integral'],-F(4,15))
        self.assertEqual(b['centered_integral_sum'],F(11,15))
        self.assertGreater(b['centered_euler_sum'],b['centered_integral_sum'])
        self.assertLess(b['normalized_projection'],-F(1,44))

    def test_positive_average_has_an_interior_positive_witness(self):
        a,theta=0.5,pi/2
        velocity=3+cos(theta)
        self.assertAlmostEqual(a*velocity,1.5)
        self.assertAlmostEqual((1-a)*velocity,1.5)
        self.assertEqual(rapid_model_budget()['paired_prefactor'],2*F(1,4)**2)

    def test_periodic_primitive_keeps_the_slow_derivative_correction(self):
        # q(a,theta)=a*cos(theta), R=a*sin(theta), qbar=0.
        # Exact chain rule and endpoint identity for arbitrary noninteger K.
        k=7.3
        for a in (0.3,0.45,0.7):
            angle=k*(a-0.5)
            total_derivative=sin(angle)+a*k*cos(angle)
            self.assertAlmostEqual((total_derivative-sin(angle))/k,a*cos(angle))
        with self.assertRaises(ValueError):
            cell_derivative_order(1.5)


if __name__ == '__main__':
    unittest.main()
