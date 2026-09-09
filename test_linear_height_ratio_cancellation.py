"""Exact density, ratio, mask and separate-error guards; no zero evidence."""
from fractions import Fraction as F
import unittest

from linear_height_ratio_cancellation import (
    linear_remainder_exponents, piecewise_density_power, ratio_decay,
    ratio_density_slack, signed_box_relative_exponent, tag_ratio_eligible,
)


class LinearHeightRatioCancellationTests(unittest.TestCase):
    def test_piecewise_density_majorant_has_both_exact_factorizations(self):
        for j in range(101):
            u=F(j,200)
            slack=ratio_density_slack(u)
            if u<=F(1,4):
                factored=(1-4*u)*(15*u+2)/(10*(2-3*u))
            else:
                factored=(5*u-1)*(4*u-1)/(10*(1+u))
            self.assertEqual(slack,factored)
            self.assertGreaterEqual(slack,0)
        self.assertEqual(piecewise_density_power(F(1,4)),F(3,5))
        self.assertEqual(ratio_density_slack(F(1,4)),0)

    def test_height_ratio_pays_energy_growth_and_exposes_its_endpoint(self):
        theta=F(4,5)
        self.assertEqual(ratio_decay(theta),F(1,100))
        for h in (F(3,4),F(4,5),F(1)):
            self.assertEqual(signed_box_relative_exponent(theta*h,h),-ratio_decay(theta)*h)
            self.assertLess(signed_box_relative_exponent(theta*h-F(1,20),h),-ratio_decay(theta)*h)
        self.assertEqual(ratio_decay(F(9,11)),0)
        self.assertLess(ratio_decay(F(9,10)),0)

    def test_each_energy_can_exceed_its_base_without_losing_the_product(self):
        # At the linear ceiling h=1, g=4/5, the two energy powers are
        # 11g/10 and11/10, but the bilinear sum has their mean exponent99/100.
        g,h=F(4,5),F(1)
        row_energy=1+g-h+g/10
        column_energy=1+h/10
        self.assertGreater(row_energy,1+g-h)
        self.assertGreater(column_energy,1)
        self.assertEqual((row_energy+column_energy)/2,F(99,100))
        self.assertEqual((row_energy+column_energy)/2,1+signed_box_relative_exponent(g,h))

    def test_two_actual_error_exponents_are_affine_and_paid(self):
        for g in (F(9,20),F(1,2),F(3,4),F(4,5),F(9,11)):
            for u in (F(0),F(1,1000),F(1,4),F(1,2)):
                for v in (F(0),F(1,4),F(1,2)):
                    left=linear_remainder_exponents(g,g,u,v)
                    right=linear_remainder_exponents(g,F(1),u,v)
                    mid=linear_remainder_exponents(g,(g+1)/2,u,v)
                    for key in ('integral','gamma'):
                        self.assertEqual(mid[key],(left[key]+right[key])/2)
                        self.assertLessEqual(left[key],F(91,100))
                        self.assertLessEqual(right[key],F(91,100))

    def test_gamma_error_cannot_always_be_absorbed_in_the_integral_error(self):
        errors=linear_remainder_exponents(F(9,20),F(1),F(1,2),F(1,2))
        self.assertGreater(errors['gamma'],errors['integral'])
        self.assertEqual(errors['gamma'],F(1,2))

    def test_dyadic_boundary_is_an_exact_tag_condition_not_a_curved_mask(self):
        self.assertTrue(tag_ratio_eligible(2**16,2**20))
        self.assertFalse(tag_ratio_eligible(2**17,2**20))
        self.assertLess(2*2**16,F(2**20,2))
        # Eligibility at tiny tags does not alone prove eventual separation.
        self.assertTrue(tag_ratio_eligible(1,1))
        self.assertGreater(2*1,F(1,2))
        with self.assertRaises(ValueError):
            tag_ratio_eligible(3,8)

    def test_full_family_and_actual_core_exponents_are_distinct(self):
        delta=ratio_decay(F(4,5))
        self.assertEqual(1-F(9,20)*delta,F(1991,2000))
        self.assertEqual(1-F(4,5)*delta,F(124,125))
        self.assertGreater(F(124,125),F(91,100))


if __name__ == '__main__':
    unittest.main()
