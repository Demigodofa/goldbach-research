"""Exact mechanism guards for the mock spectrum, not numerical zeta evidence."""
from fractions import Fraction as F
import unittest

from spectral_count_resonance_model import (
    endpoint_alias_argument_upper, floor_increment_selection,
    lattice_carrier_turns, summed_pair_remainder_power,
    thinning_error_powers, transverse_curvature,
)


class SpectralCountResonanceModelTests(unittest.TestCase):
    def test_quarter_shift_makes_every_pair_carrier_negative(self):
        for k in (-2,0,1,19):
            for j in (-1,0,6,101):
                turns=lattice_carrier_turns(k,j)
                self.assertEqual(turns-(turns.numerator//turns.denominator),F(1,2))
                unshifted=lattice_carrier_turns(k,j,F(0))
                self.assertEqual(unshifted.denominator,1)
        # A half-cell shift on each coordinate would give a positive carrier.
        self.assertEqual(lattice_carrier_turns(0,0,F(1,2)),1)

    def test_transverse_gaussian_has_the_required_curvature(self):
        for h in (F(1),F(2),F(100)):
            self.assertEqual(transverse_curvature(h,F(0)),1/h)
            self.assertEqual(transverse_curvature(h,h/2),F(4,3)/h)
            self.assertGreater(transverse_curvature(h,h/2),transverse_curvature(h,F(0)))

    def test_floor_increment_rule_is_binary_and_telescopes(self):
        profiles=([F(2,7)+F(7*j,10) for j in range(41)],
                  [F(-3,4)+F(11*j,12) for j in range(31)],
                  [F(0),F(0),F(1,2),F(1),F(1),F(19,10)])
        for profile in profiles:
            chosen=floor_increment_selection(profile)
            self.assertTrue(all(x in (0,1) for x in chosen))
            for n in range(len(chosen)+1):
                discrepancy=F(sum(chosen[:n]))-(profile[n]-profile[0])
                self.assertLess(abs(discrepancy),1)
            self.assertEqual(sum(chosen),profile[-1].numerator//profile[-1].denominator
                             -profile[0].numerator//profile[0].denominator)

    def test_large_count_steps_are_not_silently_rounded_to_one_point(self):
        with self.assertRaises(ValueError):
            floor_increment_selection([F(0),F(3,2)])
        with self.assertRaises(ValueError):
            floor_increment_selection([F(1),F(1,2)])

    def test_thinning_saves_a_half_log_only_with_the_proved_removed_count(self):
        powers=thinning_error_powers()
        self.assertEqual(powers['stationary_N'],1)
        self.assertEqual(powers['stationary_log'],F(3,2))
        self.assertEqual(powers['endpoint_N'],1)
        self.assertEqual(powers['endpoint_log'],1)
        too_many=thinning_error_powers(F(1),F(1))
        self.assertEqual(too_many['stationary_log'],2)

    def test_coarse_pairwise_error_would_not_prove_the_model(self):
        self.assertEqual(summed_pair_remainder_power(-F(1)),1)
        self.assertEqual(summed_pair_remainder_power(-F(3,2)),F(1,2))

    def test_close_endpoint_alias_is_uniformly_nonstationary(self):
        for j in range(11):
            x=F(1,100)+F(j,1000)
            bound=endpoint_alias_argument_upper(x)
            self.assertGreater(bound,0)
            self.assertLessEqual(bound,F(1,75))
            self.assertLess(bound,1)


if __name__ == '__main__':
    unittest.main()
