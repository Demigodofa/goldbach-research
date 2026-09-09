"""Exact guards for the nonstationary endpoint obstruction; no zero list."""
from fractions import Fraction as F
import unittest

from spectral_endpoint_obstruction import (
    phase_derivative, reflected_weight_mass, smooth_interior_mass_budget,
    stationary_numerator,
)


class SpectralEndpointTests(unittest.TestCase):
    def test_coordinate_change_preserves_both_real_and_imaginary_terms(self):
        for n in (3,10,101):
            for t in (F(0),F(1,n),F(1,2),F(3)):
                for b in (F(1,2),F(1),F(3,2)):
                    h=F(52*n)
                    u=n*t
                    self.assertEqual(phase_derivative(n,t,h,b),
                                     n*stationary_numerator(u,h,b)/(1+u*u))

    def test_sum_height_stationary_root_is_not_a_difference_height_root(self):
        gamma,eta=F(7),F(11)
        self.assertEqual(stationary_numerator(gamma+eta,gamma+eta,F(1)),0)
        self.assertNotEqual(stationary_numerator(gamma+eta,eta-gamma,F(1)),0)

    def test_tiny_stationary_point_must_be_paid_separately(self):
        # Toy roots u=1/1000 and u=500 have product1-b=1/2.
        small,large=F(1,1000),F(500)
        h=small+large
        b=F(1,2)
        for u in (small,large):
            self.assertEqual(stationary_numerator(u,h,b),0)
        n=10
        self.assertLess(small/n,F(1,n))
        self.assertGreater(large/n,F(22,7))
        self.assertGreater(phase_derivative(n,F(0),h,b),0)
        self.assertLess(phase_derivative(n,F(1,n),h,b),0)

    def test_bulk_nonstationarity_keeps_the_lower_endpoint_cut(self):
        # 52N lies between16piN and18piN; 22/7 safely exceeds pi.
        for n in (3,10,101):
            for b in (F(1,100),F(1,2),F(1),F(199,100)):
                for t in (F(1,n),F(1,2),F(1),F(3),F(22,7)):
                    self.assertLessEqual(phase_derivative(n,t,F(52*n),b),-7*n)

    def test_reflection_lower_bound_preserves_off_line_zeros_and_multiplicity(self):
        orbits=[(F(1,3),2),(F(5,2),3),(F(7),1)]
        count,weight=reflected_weight_mass(orbits,4)
        self.assertEqual(count,16)
        self.assertGreater(weight,count)
        self.assertEqual(reflected_weight_mass([(1/x,m) for x,m in orbits],4),
                         (count,weight))
        self.assertEqual(reflected_weight_mass([],7),(7,F(7)))
        # Ordered pairs include the diagonal: the weight is the full square.
        individual=[F(1,3),F(3),F(5,2),F(2,5),F(1)]
        self.assertEqual(sum(x*y for x in individual for y in individual),
                         sum(individual)**2)

    def test_smooth_cutoff_budget_pays_all_pairs_and_off_line_gamma_growth(self):
        self.assertEqual(smooth_interior_mass_budget(2),
                         {'n_power':1,'logn_power':2,'all_log_small_on_n_scale':False})
        self.assertEqual(smooth_interior_mass_budget(4),
                         {'n_power':-1,'logn_power':2,'all_log_small_on_n_scale':True})


if __name__ == '__main__':
    unittest.main()
