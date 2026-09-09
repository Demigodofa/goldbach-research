"""Exact guards for the epsilon patch, unequal energies and actual error."""
from fractions import Fraction as F
import unittest

from guth_maynard_spectral_cancellation import (
    far_relative_powers, near_density_slack, patch_parameters,
    patched_energy_gaps, preserved_ratio_deletion_power, remainder_majorant,
    stationary_remainder_exponent,
)


class GuthMaynardSpectralTests(unittest.TestCase):
    def test_concrete_fixed_epsilon_is_paid_only_away_from_one(self):
        kappa=F(17,20)
        parameters=patch_parameters(kappa)
        self.assertEqual(parameters['far_gap'],F(1,26))
        self.assertEqual(parameters['epsilon'],F(1,442))
        self.assertEqual(parameters['far_saving'],F(1,520))
        edge=far_relative_powers(kappa,kappa,F(1,10),kappa)
        self.assertEqual(edge,{'row':-F(1,520),'column':-F(1,520)})
        # Illegally extending this fixed epsilon to u~0 would LOSE a power.
        unpaid=-parameters['far_gap']*F(1,100000)+kappa*parameters['epsilon']
        self.assertGreater(unpaid,0)
        with self.assertRaises(ValueError):
            far_relative_powers(kappa,kappa,F(1,100000),kappa)

    def test_both_unequal_energy_bases_keep_the_claimed_gap(self):
        kappa=F(17,20)
        p=patch_parameters(kappa)
        grid=(F(9,20),F(1,2),F(3,4),F(5,6),kappa)
        for g in grid:
            for h in grid:
                if g>h:
                    continue
                far=patched_energy_gaps(g,h)
                near=patched_energy_gaps(g,h,True)
                self.assertEqual(far['row']-far['column'],F(4,13)*(h-g))
                for gap in far.values():
                    self.assertGreaterEqual(gap,p['far_gap'])
                for gap in near.values():
                    self.assertGreaterEqual(gap,p['near_gap'])
                for u in (F(1,10),F(1,4),F(1,2)):
                    for power in far_relative_powers(g,h,u,kappa).values():
                        self.assertLessEqual(power,-p['far_saving'])

    def test_near_one_huxley_slack_is_the_exact_nonnegative_factorization(self):
        for j in range(101):
            u=F(j,1000)
            factor=9*u*(1-10*u)/(17*(2-3*u))
            self.assertEqual(near_density_slack(u),factor)
            self.assertGreaterEqual(factor,0)

    def test_actual_error_envelope_switches_at_five_sixths(self):
        heights=(F(9,20),F(1,2),F(4,5),F(5,6),F(17,20),F(173,200))
        reals=(F(0),F(1,10),F(1,4),F(1,2))
        for h in heights:
            bound=remainder_majorant(h)
            self.assertLessEqual(bound,F(91,100))
            for g in heights:
                if g>h:
                    continue
                for u in reals:
                    for v in reals:
                        self.assertLessEqual(stationary_remainder_exponent(g,h,u,v),bound)
        self.assertEqual(remainder_majorant(F(17,20)),F(17,20))

    def test_gamma_error_absorption_has_a_positive_margin_at_the_new_ceiling(self):
        self.assertGreater(F(9,20)-F(13,15)/2,0)
        self.assertEqual(F(9,20)-F(13,15)/2,F(1,60))

    def test_new_column_mask_preserves_and_strengthens_the_existing_ratio_bound(self):
        self.assertEqual(preserved_ratio_deletion_power(F(17,20)),F(1983,2000))
        self.assertLess(preserved_ratio_deletion_power(F(17,20)),F(124,125))

    def test_the_endpoint_and_growing_kappa_are_not_licensed(self):
        with self.assertRaises(ValueError):
            patch_parameters(F(13,15))
        with self.assertRaises(ValueError):
            patch_parameters(F(9,10))


if __name__ == '__main__':
    unittest.main()
