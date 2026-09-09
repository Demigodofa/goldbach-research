"""Exact scale and density guards; no numerical zero or prime evidence."""
from fractions import Fraction as F
import unittest

from unequal_spectral_cancellation import (
    energy_base_powers, remainder_density_slack, residual_mixed_derivative,
    stationary_remainder_exponent, stationary_remainder_majorant,
    unequal_energy_gaps, unequal_scale_powers,
)


class UnequalSpectralCancellationTests(unittest.TestCase):
    def test_mixed_curvature_survives_the_zero_ratio_limit(self):
        for r in (F(0),F(1,1000000),F(1,2),F(1)):
            for x in (F(1,2),F(1),F(3)):
                for y in (F(1,2),F(1),F(3)):
                    curvature=-residual_mixed_derivative(r,x,y)
                    self.assertGreaterEqual(curvature,F(1,6))
                    self.assertLessEqual(curvature,2)
                    if r==0:
                        self.assertEqual(curvature,1/y)

    def test_both_energies_retain_the_four_fifths_gap(self):
        for g,h in ((F(9,20),F(4,5)),(F(1,2),F(2,3)),
                    (F(3,4),F(4,5)),(F(4,5),F(4,5))):
            gaps=unequal_energy_gaps(g,h)
            self.assertGreaterEqual(gaps['column'],F(2,25))
            self.assertGreaterEqual(gaps['row'],gaps['column'])
            self.assertEqual(gaps['row']-gaps['column'],F(2,5)*(h-g))
        edge=unequal_energy_gaps(F(5,6),F(5,6))
        self.assertEqual(edge,{'row':F(0),'column':F(0)})
        self.assertLess(unequal_energy_gaps(F(9,10),F(9,10))['column'],0)

    def test_different_energy_bases_keep_the_same_relative_baseline(self):
        g,h=F(9,20),F(4,5)
        powers=energy_base_powers(g,h)
        self.assertEqual(powers['row_base'],1+g-h)
        self.assertEqual(g-powers['row_base'],powers['row_relative_baseline'])
        self.assertEqual(powers['row_relative_baseline'],powers['column_relative_baseline'])
        self.assertEqual(powers['product_root'],(1+powers['row_base'])/2)
        self.assertLess(powers['product_root'],1)

    def test_remainder_density_slack_has_the_exact_factorization(self):
        for j in range(101):
            u=F(j,200)
            slack=remainder_density_slack(u)
            self.assertEqual(slack,(1-2*u)*(2-3*u)/(5*(1+u)))
            self.assertGreaterEqual(slack,0)

    def test_unequal_remainder_exponent_is_paid_uniformly(self):
        for g,h in ((F(9,20),F(9,20)),(F(9,20),F(5,6)),
                    (F(2,3),F(4,5)),(F(5,6),F(5,6))):
            for u in (F(0),F(1,1000),F(1,4),F(1,2)):
                for v in (F(0),F(1,1000),F(1,4),F(1,2)):
                    exponent=stationary_remainder_exponent(g,h,u,v)
                    diagonal=stationary_remainder_exponent(h,h,u,v)
                    majorant=stationary_remainder_majorant(h,u,v)
                    self.assertLessEqual(exponent,diagonal)
                    self.assertLessEqual(diagonal,majorant)
                    self.assertLessEqual(majorant,F(91,100))

    def test_physical_scales_and_gamma_error_are_not_suppressed_for_free(self):
        for g,h in ((F(9,20),F(5,6)),(F(4,5),F(4,5))):
            powers=unequal_scale_powers(g,h)
            self.assertEqual(powers['continuous']+powers['stationary_amplitude'],0)
            self.assertEqual(powers['projection_remainder']-powers['continuous'],-F(7,2)*g)
            self.assertLessEqual(powers['gamma_relative_error'],powers['integral_relative_error'])
        outside=unequal_scale_powers(F(1,10),F(4,5))
        self.assertGreater(outside['gamma_relative_error'],outside['integral_relative_error'])


if __name__ == '__main__':
    unittest.main()
