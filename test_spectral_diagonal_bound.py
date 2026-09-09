"""Exact phase, density-budget and multiplicity guards; no numerical zeros."""
from fractions import Fraction as F
import unittest

from spectral_diagonal_bound import (
    density_integrand_powers, identical_location_pair_counts,
    low_height_relative_exponent, normalized_phase_data,
)


class SpectralDiagonalTests(unittest.TestCase):
    def test_small_rescaled_interval_has_the_required_monotonicities(self):
        for h in (F(8),F(32),F(128)):
            for b in (F(1,100),F(1,2),F(1),F(199,100)):
                for u in (F(1),(1+h/4)/2,h/4):
                    data=normalized_phase_data(h,b,u)
                    self.assertLess(data['phase_first'],0)
                    self.assertGreaterEqual(data['phase_second'],0)
                    self.assertGreater(data['log_amplitude_first'],0)
        self.assertGreater(normalized_phase_data(F(8),F(1,2),F(0))['phase_first'],0)

    def test_stationary_region_curvature_and_far_tail_are_uniform(self):
        for h in (F(8),F(32),F(128)):
            for b in (F(1,100),F(1,2),F(1),F(199,100)):
                for u in (h/4,h/2,h,2*h,4*h):
                    second=normalized_phase_data(h,b,u)['phase_second']
                    self.assertGreaterEqual(second,F(3,100)/h)
                    self.assertLessEqual(second,20/h)
                for u in (4*h,8*h,100*h):
                    self.assertGreater(normalized_phase_data(h,b,u)['phase_first'],F(2,3))

    def test_three_density_regions_keep_the_direction_of_the_height_inequality(self):
        for numerator in range(501):
            u=F(numerator,1000)
            powers=density_integrand_powers(u)
            if u<=F(1,10):
                self.assertLessEqual(powers['h_power'],-F(5,22))
            if F(1,10)<=u<=F(1,5):
                self.assertLessEqual(powers['h_power'],0)
                self.assertLessEqual(powers['n_power'],-F(1,5))
            if u>=F(1,5):
                self.assertGreaterEqual(powers['h_power'],0)
                self.assertLessEqual(powers['n_power']+powers['h_power'],-F(1,4))

    def test_location_diagonal_uses_multiplicity_squared(self):
        multiplicities={(F(1,3),F(7)):3,(F(2,3),F(7)):2,(F(1,2),F(11)):1}
        self.assertEqual(identical_location_pair_counts(multiplicities),
                         {'copies':6,'identical_pairs':14,'distinct_location_pairs':22})
        # The two locations at height7 contribute12 distinct ordered pairs.
        self.assertEqual(2*multiplicities[(F(1,3),F(7))]*multiplicities[(F(2,3),F(7))],12)

    def test_low_height_cutoff_must_be_tied_to_the_zero_free_constant(self):
        for alpha,c in ((F(1,5),F(1,25)),(F(1,2),F(1,4)),(F(1),F(2))):
            self.assertLessEqual(low_height_relative_exponent(alpha,c),-alpha/2)
        self.assertGreater(low_height_relative_exponent(F(1),F(1,25)),0)

    def test_increasing_low_height_weight_needs_zero_free_decay(self):
        for u in (F(0),F(1,20),F(1,10)):
            powers=density_integrand_powers(u)
            self.assertLess(powers['h_power'],0)
        # At u=0 a fixed height alone supplies no decay as N increases.
        self.assertEqual(density_integrand_powers(F(0))['n_power'],0)


if __name__ == '__main__':
    unittest.main()
