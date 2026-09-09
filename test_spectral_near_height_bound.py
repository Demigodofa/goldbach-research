"""Finite exact guards for the near-strip proof, not numerical zero evidence."""
from fractions import Fraction as F
import unittest

from spectral_near_height_bound import (
    finite_near_height_model, height_comparison_ratio_squared, retained_decay,
)


class SpectralNearHeightTests(unittest.TestCase):
    def test_unequal_low_heights_need_the_width_cost(self):
        for gamma,eta in ((F(10000),F(1,100)),(F(3),F(8)),(F(8),F(3)),(F(7),F(7))):
            ratio=height_comparison_ratio_squared(gamma,eta)
            self.assertLessEqual(ratio,1+abs(gamma-eta))
        self.assertGreater(height_comparison_ratio_squared(F(10000),F(1,100)),F(9000))

    def test_sqrtlog_width_retains_decay_but_an_overlarge_rate_does_not(self):
        for alpha in (F(1),F(1,2),F(1,100)):
            self.assertEqual(retained_decay(alpha,alpha/30),alpha/20)
            self.assertEqual(retained_decay(alpha,alpha/15),0)
            self.assertLess(retained_decay(alpha,alpha/10),0)

    def test_equal_heights_include_all_product_multiplicities(self):
        rows=[(2,F(1),3),(2,F(2),2),(3,F(3),1)]
        model=finite_near_height_model(rows,F(0))
        self.assertEqual(model['pair_copies'],26)  # (3+2)^2+1^2, not3^2+2^2+1
        self.assertEqual(model['pair_sum'],F(55,2))  # (3*1+2*2)^2/2+3^2/3
        self.assertEqual(model['max_degree'],5)

    def test_amgm_neighbor_bound_on_full_copy_expansion(self):
        rows=[(2,F(1,3),3),(2,F(7,2),2),(3,F(2),1),(4,F(1,5),4),(6,F(5),1)]
        copies=[(r,x) for r,x,m in rows for _ in range(m)]
        for width in (F(0),F(5),F(8),F(12),F(100)):
            model=finite_near_height_model(rows,width)
            expanded=sum((x*y/min(r,s) for r,x in copies for s,y in copies
                          if abs(r*r-s*s)<=width),F(0))
            self.assertEqual(model['pair_sum'],expanded)
            self.assertLessEqual(expanded**2,(1+width)*model['max_degree']**2*model['first_moment']**2)

    def test_neighbor_windows_keep_the_boundary_and_distant_exclusion(self):
        rows=[(2,F(1),1),(3,F(1),1),(4,F(1),1)]
        self.assertEqual(finite_near_height_model(rows,F(5))['pair_copies'],5)
        self.assertEqual(finite_near_height_model(rows,F(7))['pair_copies'],7)
        self.assertEqual(finite_near_height_model(rows,F(12))['pair_copies'],9)


if __name__ == '__main__':
    unittest.main()
