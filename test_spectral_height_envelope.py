"""Exact envelope guards, not a finite substitute for the analytic proof."""
from fractions import Fraction as F
import unittest

from spectral_height_envelope import (
    critical_line_box_exponent, middle_branch_crossing_polynomial,
    rational_density_slack, thirteen_twentieths_envelope,
)
from spectral_low_axis_bound import density_box_exponent, density_power


class SpectralHeightEnvelopeTests(unittest.TestCase):
    def test_rational_density_majorant_has_a_positive_square_certificate(self):
        for j in range(101):
            u=F(j,200)
            numerator=4000*(u-F(3163,8000))**2+F(187431,16000)
            self.assertEqual(rational_density_slack(u),numerator/(2600*(1+u)))
            self.assertGreater(rational_density_slack(u),0)

    def test_enlarging_smaller_height_retains_a_valid_upper_bound(self):
        for h in (F(1,100),F(1,3),F(1,2),F(13,20)):
            for g in (F(0),h/2,h):
                for u,v in ((F(0),F(1,2)),(F(1,10),F(2,5)),(F(2,5),F(1,10))):
                    direct=density_box_exponent(g,h,u,v)
                    diagonal=density_box_exponent(h,h,u,v)
                    self.assertEqual(diagonal-direct,(h-g)*(F(1,2)-u+density_power(u)))
                    self.assertLessEqual(direct,diagonal)
                    self.assertLessEqual(diagonal,thirteen_twentieths_envelope(h,u,v))

    def test_zero_free_loss_is_retained_at_small_height(self):
        u=F(1,25)
        for h in (F(0),F(1,100),F(1,10)):
            self.assertLessEqual(thirteen_twentieths_envelope(h,u,F(0)),1-u/2)
        self.assertEqual(thirteen_twentieths_envelope(F(0),F(0),F(0)),1)

    def test_middle_branch_crossing_is_strictly_between_065_and_two_thirds(self):
        self.assertLess(middle_branch_crossing_polynomial(F(13,20)),0)
        self.assertGreater(middle_branch_crossing_polynomial(F(2,3)),0)
        # Smaller algebraic root is outside this branch; test a forbidden call.
        with self.assertRaises(ValueError):
            middle_branch_crossing_polynomial(F(1,5))

    def test_critical_line_envelope_itself_reaches_main_scale_at_two_thirds(self):
        self.assertEqual(critical_line_box_exponent(F(2,3)),1)
        self.assertEqual(critical_line_box_exponent(F(13,20)),F(39,40))
        self.assertEqual(critical_line_box_exponent(F(3,4)),F(9,8))


if __name__ == '__main__':
    unittest.main()
