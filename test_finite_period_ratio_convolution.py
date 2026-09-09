"""Exact scaling guards plus one finite-interval normalization diagnostic.

Quadrature below checks the identity on ordinary Gamma parameters. It is
not a computation of actual zeros or evidence for an asymptotic theorem.
"""
from cmath import exp
from fractions import Fraction as F
from math import e, pi
import unittest

from finite_period_ratio_convolution import (
    convolution_budget, energy_power, finite_interval_kernel,
)
from linear_height_ratio_cancellation import linear_remainder_exponents


def simpson(function, lower, upper, panels=32768):
    step=(upper-lower)/panels
    total=function(lower)+function(upper)
    for j in range(1,panels):
        total+=(4 if j%2 else 2)*function(lower+j*step)
    return total*step/3


class FinitePeriodRatioConvolutionTests(unittest.TestCase):
    def test_fourier_kernel_keeps_orientation_and_value_at_origin(self):
        self.assertEqual(finite_interval_kernel(0),complex(pi))
        self.assertAlmostEqual(finite_interval_kernel(1).real,0,places=14)
        self.assertAlmostEqual(finite_interval_kernel(1).imag,2,places=14)
        self.assertEqual(finite_interval_kernel(-0.7),finite_interval_kernel(0.7).conjugate())
        with self.assertRaises(ValueError):
            finite_interval_kernel(1,0)

    def test_laplace_convolution_matches_direct_finite_period_integral(self):
        # rho=sigma=1 are a normalization fixture, not zeta zeros.
        # B_x=2x. The x>120 tail is <1e-13 at N=3.
        n=3
        direct=e/pi*simpson(lambda t:exp(1j*n*t)/(1/n+1j*t)**2,0,pi)
        convolved=e/(2*pi)*simpson(
            lambda x:exp(-x/n)*finite_interval_kernel(n-x)*2*x,0,120)
        self.assertLess(abs(direct-convolved),1e-8)
        reversed_argument=e/(2*pi)*simpson(
            lambda x:exp(-x/n)*finite_interval_kernel(x-n)*2*x,0,120)
        self.assertGreater(abs(direct-reversed_argument),0.01)

    def test_energy_maximum_handles_bases_on_either_side_of_height(self):
        a=F(109,1170)
        for y,z in ((F(3,5),F(1)),(F(4,5),F(1,4)),(F(3,5),F(0))):
            layer=max(z+a*y,z+y-z+a*y)
            self.assertEqual(energy_power(y,z,a),layer)
            self.assertGreaterEqual(layer,y)  # total-count baseline is paid.
        self.assertEqual(energy_power(F(3,5),F(-1,5),a),F(4,5))

    def test_two_energy_scales_have_the_claimed_max_identity(self):
        a=F(109,1170)
        g,h=F(1,2),F(9,10)
        for x in (h-g,F(1,2),F(1),F(2)):
            row=energy_power(g,x+g-h,a)
            column=energy_power(h,x,a)
            predicted=max(h,x)+(1+a)*g/2+(a-1)*h/2
            self.assertEqual((row+column)/2,predicted)

    def test_small_base_integral_pays_its_extra_root_of_height_ratio(self):
        a=F(109,1170)
        g,h=F(9,20),F(1)
        direct=-1+(1+a/2)*h+(h-g)/2
        self.assertEqual(direct,F(11,40)+a/2)
        self.assertLess(direct,F(1,2))
        self.assertLess(F(11,40)+F(1,6),F(1,2))

    def test_convolution_logarithm_and_source_loss_are_not_erased(self):
        budget=convolution_budget(F(53,64),F(1,1170))
        self.assertEqual(budget['core_power'],F(25583,25600))
        self.assertEqual(budget['core_log_power'],55)
        self.assertEqual(budget['gamma_log_power'],15)
        self.assertEqual(budget['zero_endpoint_power'],F(53,128))
        self.assertLess(budget['small_base_power'],F(1,2))
        with self.assertRaises(ValueError):
            convolution_budget(F(53,64),F(1,585))

    def test_only_gamma_error_is_needed_and_its_affine_endpoints_are_paid(self):
        for g in (F(9,20),F(3,4),F(53,64)):
            for u in (F(0),F(3,10),F(1,2)):
                for v in (F(0),F(1,5),F(1,2)):
                    for h in (g,F(1)):
                        gamma=linear_remainder_exponents(g,h,u,v)['gamma']
                        self.assertLessEqual(gamma,F(91,100))


if __name__ == '__main__':
    unittest.main()
