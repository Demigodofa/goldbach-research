"""Exact source-envelope, ratio, ceiling and finite-period error guards."""
from fractions import Fraction as F
import unittest

from guth_maynard_ratio_cancellation import (
    affine_density_slack, box_power, linear_remainder_exponents,
    ratio_parameters, selected_density_power, tag_ratio_eligible,
)


class GuthMaynardRatioTests(unittest.TestCase):
    def test_all_three_envelope_slacks_match_their_independent_factorizations(self):
        for j in range(101):
            u=F(j,200)
            if u<=F(1,5):
                factor=(12*(1-5*u)+29*u+390*u*(F(1,5)-u))/(65*(2-3*u))
            elif u<=F(3,10):
                factor=(3-10*u)*(65*u+16)/(65*(8-5*u))
            else:
                factor=(10*u-3)*(13*u-2)/(65*(1+u))
            self.assertEqual(affine_density_slack(u),factor)
            self.assertGreaterEqual(factor,0)
        self.assertEqual(affine_density_slack(F(3,10)),0)

    def test_selected_exponents_join_at_the_correct_real_parts(self):
        self.assertEqual(selected_density_power(F(1,5)),F(3,7))
        self.assertEqual(15*F(1,5)/(8-5*F(1,5)),F(3,7))
        self.assertEqual(selected_density_power(F(3,10)),F(9,13))
        self.assertEqual(3*F(3,10)/(1+F(3,10)),F(9,13))

    def test_fixed_source_loss_is_retained_in_the_concrete_decay(self):
        p=ratio_parameters(F(53,64),F(1,1170))
        self.assertEqual(p['density_excess'],F(109,1170))
        self.assertEqual(p['decay'],F(1,1280))
        self.assertEqual(p['current_core_power'],F(25583,25600))
        for h in (F(3,5),F(17,20),F(1)):
            g=F(53,64)*h
            self.assertEqual(box_power(g,h,F(53,64),F(1,1170)),1-h/1280)

    def test_endpoint_or_excessive_epsilon_is_rejected(self):
        with self.assertRaises(ValueError):
            ratio_parameters(F(59,71),F(1,100000))
        with self.assertRaises(ValueError):
            ratio_parameters(F(53,64),F(1,585))

    def test_both_actual_errors_remain_below_the_retained_envelope(self):
        theta=F(53,64)
        reals=(F(0),F(1,10),F(3,10),F(1,2))
        for g in (F(9,20),F(3,4),theta):
            for h in (g,(g+1)/2,F(1)):
                for u in reals:
                    for v in reals:
                        for power in linear_remainder_exponents(g,h,u,v).values():
                            self.assertLessEqual(power,F(91,100))

    def test_the_new_tag_family_strictly_contains_old_selected_tags(self):
        small=2**53
        large=2**64
        self.assertTrue(tag_ratio_eligible(small,large,F(53,64)))
        self.assertFalse(tag_ratio_eligible(small,large,F(4,5)))

    def test_half_target_ceiling_needs_asymmetry_to_pay_stationary_condition(self):
        # Exact geometry fixture; this is not a numerical onset for actual zeros.
        small=2**53
        large=2**64
        scale=4*large
        maximum_height_sum=2*small+2*large
        self.assertEqual(2*large,scale//2)
        self.assertLess(4*maximum_height_sum,3*scale)  # pi>3 suffices.
        self.assertGreater(4*(2*large+2*large),3*scale)


if __name__ == '__main__':
    unittest.main()
