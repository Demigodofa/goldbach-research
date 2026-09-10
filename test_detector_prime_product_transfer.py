"""Scale, divisor-convolution and retained-mask arithmetic guards."""
from fractions import Fraction as F
from math import prod
import unittest

from major_arc_kernel import _factorization
from unexceptional_vaughan_gate import _divisors
from detector_prime_product_transfer import (
    convolution_log_vector, density_tangent_gap, full_mobius_log_vector,
    middle_mask_budget, moment_time_exponent, transfer_exponents,
    truncated_mobius_coefficient,
)


class DetectorPrimeProductTests(unittest.TestCase):
    def test_density_tangent_controls_every_dilated_scale(self):
        for j in range(101):
            u=F(j,200)
            self.assertEqual(density_tangent_gap(u),(1-2*u)**2/(3*(1+u)))
            self.assertGreaterEqual(density_tangent_gap(u),0)
            for s in (F(59,100),F(4,5),F(1)):
                exponent=F(9,10)*3*u/(1+u)+s*(F(1,2)-u)
                self.assertLessEqual(exponent,F(9,10))
        self.assertEqual(density_tangent_gap(F(1,2)),0)

    def test_full_transfer_and_damping_exponents_are_separate(self):
        self.assertEqual(transfer_exponents(),
            {'dilated_lower':F(59,100),'field_error':F(41,200),
             'normalized_error':-F(59,200),'damping':-F(1,25),
             'damping_transfer':-F(67,200)})
        self.assertLess(2*transfer_exponents()['field_error'],1)
        self.assertLess(transfer_exponents()['damping_transfer'],-F(1,25))

    def test_divisor_log_convolution_includes_prime_powers_and_squares(self):
        for n in range(1,201):
            tau=lambda d:prod(e+1 for p,e in _factorization(d))
            coefficients={d:F(tau(d)) for d in _divisors(n)}
            expected=tuple((p,F(tau(n)*e,2)) for p,e in _factorization(n))
            self.assertEqual(convolution_log_vector(n,coefficients),expected)
        self.assertEqual(convolution_log_vector(8,{1:F(1),2:F(2),4:F(3)}),((2,F(6)),))

    def test_unrestricted_mobius_identity_is_exact(self):
        for cutoff in (1,2,5,11):
            for n in range(1,161):
                coefficients={d:F(truncated_mobius_coefficient(d,cutoff))
                              for d in _divisors(n)}
                self.assertEqual(convolution_log_vector(n,coefficients),
                                 full_mobius_log_vector(n,cutoff))

    def test_bad_length_and_damping_masks_cannot_be_dropped(self):
        # Rational damping is a formal coefficient fixture, not exp(-n/Y).
        # The actual theorem keeps that exponential in its exact identity.
        cutoff=5
        mask={n:F(truncated_mobius_coefficient(n,cutoff),2)
              for n in range(17,33)}
        self.assertEqual(convolution_log_vector(101,mask),())
        self.assertEqual(full_mobius_log_vector(101,cutoff),((101,1),))
        self.assertEqual(convolution_log_vector(31*101,mask),((101,F(1,2)),))
        self.assertEqual(full_mobius_log_vector(31*101,cutoff),((31,1),(101,1)))
        undamped={n:2*v for n,v in mask.items()}
        self.assertEqual(convolution_log_vector(31*101,undamped),((101,F(1)),))
        self.assertNotEqual(convolution_log_vector(31*101,undamped),
                            full_mobius_log_vector(31*101,cutoff))

    def test_crude_weighted_masks_give_positive_upper_budgets_only(self):
        self.assertEqual(middle_mask_budget(-F(4,625)),F(361,1250))
        self.assertEqual(middle_mask_budget(-F(6,125)),F(309,1250))
        self.assertGreater(middle_mask_budget(-F(4,625)),0)

    def test_upper_support_cannot_replace_shorter_actual_product_length(self):
        beta=F(19,25)
        self.assertEqual(moment_time_exponent(beta,F(7,10)),F(7,125))
        self.assertEqual(moment_time_exponent(beta,F(41,50)),-F(4,625))
        self.assertGreater(moment_time_exponent(beta,F(49,150)),0)
        self.assertGreater(moment_time_exponent(beta,F(7,10)),0)
        with self.assertRaises(ValueError):
            density_tangent_gap(F(3,4))


if __name__ == '__main__':
    unittest.main()
