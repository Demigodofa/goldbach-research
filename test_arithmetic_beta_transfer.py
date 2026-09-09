"""Exact beta normalization, stationary separation and tail-budget guards."""
from fractions import Fraction as F
from math import comb
import unittest

from arithmetic_beta_transfer import (
    integer_beta_integral, left_phase_numerator,
    transfer_error_powers, upper_tail_imaginary_coefficient,
)


class ArithmeticBetaTransferTests(unittest.TestCase):
    def test_beta_identity_matches_independent_polynomial_integration(self):
        for p in range(1,8):
            for q in range(1,8):
                direct=sum((F((-1)**j*comb(q-1,j),p+j) for j in range(q)),F(0))
                self.assertEqual(integer_beta_integral(p,q),direct)

    def test_factor_two_and_target_scale_match_the_physical_integral(self):
        for n,p,q in ((3,1,1),(5,2,3),(7,3,2)):
            physical=2*sum((F((-1)**j*comb(q-1,j)*n**(q-1-j)*n**(p+j),p+j)
                            for j in range(q)),F(0))
            quotient=2*n**(p+q-1)*integer_beta_integral(p,q)
            self.assertEqual(physical,quotient)
        self.assertEqual(2*3*integer_beta_integral(1,1),6)

    def test_fixed_cutoff_gap_excludes_the_entire_stationary_ratio_range(self):
        c=F(1,100)
        for s in (c,2*c):
            for t in (c,2*c):
                for a in (F(0),F(1,4),F(3,10)):
                    self.assertGreaterEqual(left_phase_numerator(s,t,a),c/10)
                stationary=s/(s+t)
                self.assertEqual(left_phase_numerator(s,t,stationary),0)
                self.assertGreaterEqual(stationary,F(1,3))
                self.assertLessEqual(stationary,F(2,3))

    def test_upper_tail_has_positive_imaginary_sign_from_damped_integral(self):
        # Integral_0^infty exp[(-eps+iN)t]dt =1/(eps-iN).
        n=F(10)
        eps=F(1,100)
        damped_imag=n/(eps**2+n**2)
        expected=upper_tail_imaginary_coefficient(F(0),F(3))/n
        self.assertGreater(damped_imag,0)
        self.assertLess(abs(damped_imag-expected),F(1,1000000))
        with self.assertRaises(ValueError):
            upper_tail_imaginary_coefficient(F(3),F(3))

    def test_first_moment_improvement_pays_both_remainders(self):
        actual=transfer_error_powers()
        self.assertEqual(actual['upper_tail_remainder'],0)
        self.assertEqual(actual['beta_endpoint_remainder'],-1)
        old=transfer_error_powers(F(3,2))
        self.assertEqual(old['upper_tail_remainder'],1)
        self.assertEqual(old['beta_endpoint_remainder'],0)


if __name__ == '__main__':
    unittest.main()
