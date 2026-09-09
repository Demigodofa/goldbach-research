"""Normalization and conditional-budget guards, not a phase decomposition."""
from cmath import exp
from fractions import Fraction as F
from math import pi
import unittest

from window_phase_projection import conditional_band_budget, normalized_projection_budget


class WindowPhaseProjectionTests(unittest.TestCase):
    def test_adjoint_jacobian_gives_sqrt_u_divided_by_N(self):
        # Perfect squares make the normalization check exact.
        for root_n,root_N in ((75,100),(6,10),(9,20)):
            n,N = root_n**2,root_N**2
            u = F(n,N)
            self.assertEqual(u/F(root_n*root_N),F(root_n,root_N)/N)
            self.assertNotEqual(u/F(root_n*root_N),u/N)

    def test_fourier_inversion_selects_positive_local_phase_frequency(self):
        samples,mode = 32,5
        transform = [exp(-2j*pi*mode*j/samples) for j in range(samples)]
        positive = sum(transform[j]*exp(2j*pi*mode*j/samples)
                       for j in range(samples))/samples
        negative = sum(transform[j]*exp(-2j*pi*mode*j/samples)
                       for j in range(samples))/samples
        self.assertAlmostEqual(abs(positive-1),0,places=14)
        self.assertAlmostEqual(abs(negative),0,places=14)

    def test_normalized_errors_keep_the_division_by_sqrtN_and_N(self):
        b = normalized_projection_budget()
        self.assertEqual(b['prime'],F(43,44)-1)
        self.assertEqual(b['zero_transfer'],F(1,10)-F(1,2))
        self.assertEqual(b['finite_period'],F(9,10)-1)
        self.assertEqual(b['beta_endpoint'],-F(7,10)-1)
        self.assertLess(b['adjoint'],b['prime'])
        self.assertLess(b['fourier_tail'],b['prime'])

    def test_complex_paired_functional_does_not_insert_a_conjugate(self):
        field = (1+2j,2-1j)
        reflected_weight = (3*field[1],3*field[0])
        actual = sum(a*b for a,b in zip(field,reflected_weight))
        conjugated = sum(a*b.conjugate() for a,b in zip(field,reflected_weight))
        self.assertEqual(actual,6*field[0]*field[1])
        self.assertNotEqual(actual,conjugated)

    def test_concrete_conditional_band_has_a_strict_power_saving(self):
        b = conditional_band_budget(F(1,100),F(1,50))
        self.assertEqual(b['prime_projection'],F(543,550))
        self.assertEqual(b['residual'],F(49,50))
        self.assertEqual(max(b.values()),F(543,550))
        self.assertTrue(all(exponent < 1 for exponent in b.values()))

    def test_endpoint_and_nonvanishing_residual_do_not_certify_cancellation(self):
        for kappa,sigma in ((F(1,44),F(1,50)),(F(0),F(0)),
                            (F(-1,100),F(1,50)),(0.01,F(1,50))):
            with self.assertRaises(ValueError):
                conditional_band_budget(kappa,sigma)


if __name__ == '__main__':
    unittest.main()
