"""Exact guards for axis density exponents; no actual zero or prime data."""
from fractions import Fraction as F
import unittest

from spectral_low_axis_bound import (
    density_box_exponent, density_power, diagonal_endpoint_envelope,
    fixed_log_width_relative_power, unequal_kernel_powers,
)


class SpectralLowAxisTests(unittest.TestCase):
    def test_unequal_gamma_power_keeps_the_missing_half(self):
        self.assertEqual(unequal_kernel_powers(F(1,2),F(1,2)),
                         {'N':F(0),'G':F(0),'H':-F(1,2)})
        self.assertEqual(unequal_kernel_powers(F(1),F(1)),
                         {'N':F(1),'G':F(1,2),'H':-F(1)})
        for b,d in ((F(2,3),F(3,4)),(F(1,5),F(4,5))):
            # Gamma at eta and the partial integral supply these two H powers.
            independently_combined=d-F(1,2)+F(1,2)-b-d
            self.assertEqual(unequal_kernel_powers(b,d)['H'],independently_combined)

    def test_density_inequalities_have_exact_nonnegative_slacks(self):
        for j in range(101):
            u=F(j,200)
            slack1=2*u+F(1,8)-density_power(u)
            self.assertEqual(slack1,(16*(u-F(7,32))**2+F(15,64))/(8*(1+u)))
            self.assertGreater(slack1,0)
            slack2=F(1,2)-density_power(u)+u
            self.assertEqual(slack2,(F(1,2)-u)*(1-u)/(1+u))
            self.assertGreaterEqual(slack2,0)

    def test_both_height_endpoints_control_the_intervening_boxes(self):
        for gi in range(11):
            g=F(gi,20)
            for ui in range(6):
                for vi in range(6):
                    u,v=F(ui,10),F(vi,10)
                    left=density_box_exponent(g,g,u,v)
                    right=density_box_exponent(g,F(1),u,v)
                    self.assertLessEqual(left,diagonal_endpoint_envelope(g,u,v))
                    self.assertLessEqual(right,F(1,2)+g)
                    for t in (F(1,4),F(1,2),F(3,4)):
                        h=(1-t)*g+t
                        actual=density_box_exponent(g,h,u,v)
                        self.assertEqual(actual,(1-t)*left+t*right)
                        self.assertLessEqual(actual,max(left,right))

    def test_zero_free_loss_is_needed_at_fixed_small_height(self):
        self.assertEqual(density_box_exponent(F(0),F(0),F(0),F(0)),1)
        self.assertEqual(diagonal_endpoint_envelope(F(0),F(1,20),F(0)),F(19,20))
        for g in (F(0),F(1,20),F(1,4)):
            u=F(1,30)
            self.assertLessEqual(diagonal_endpoint_envelope(g,u,F(0)),1-u/2)

    def test_square_root_axis_endpoint_has_no_saving_in_this_budget(self):
        self.assertEqual(density_box_exponent(F(1,2),F(1),F(1,2),F(1,2)),1)
        self.assertEqual(density_box_exponent(F(2,5),F(1),F(1,2),F(1,2)),F(9,10))
        self.assertEqual(fixed_log_width_relative_power(F(14)),0)
        self.assertEqual(fixed_log_width_relative_power(F(25)),-11)


if __name__ == '__main__':
    unittest.main()
